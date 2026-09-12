---
title: Data Engineering Course - roadmapa i narzedzia
author: Course intro
date: 2026-07-12

---

# Programmer -> Data Engineer

## Roadmapa, sposob pracy i narzedzia

Cel pierwszego spotkania: zobaczyc cala mape, zanim zaczniemy pisac SQL.

<!-- end_slide -->

# Zanim zobaczysz mape

Nie musisz znac tych pojec perfekcyjnie. Masz miec intuicje, zeby slajdy nie byly lista obcych slow.

```text
Production DB = baza aplikacji, np. zamowienia i platnosci
Data lake = tanie miejsce na pliki i surowe dane
Warehouse = miejsce pod szybkie SQL, raporty i analityke
Lakehouse = data lake + tabele + transakcje + SQL
ETL = czyscimy dane przed zaladowaniem
ELT = ladujemy dane najpierw, czyscimy pozniej w warehouse/lakehouse
Bronze = dane blisko zrodla
Silver = dane wyczyszczone
Gold = dane gotowe pod metryke, dashboard albo raport
```

Jesli nie rozumiesz slowa, zatrzymaj slajd i dopisz pytanie.

<!-- end_slide -->

# Po co ten kurs?

Nie uczymy listy narzedzi.

Uczymy sie budowac zaufany przeplyw danych:

- skad dane przychodza,
- co oznacza jeden rekord,
- jak dane sa czyszczone,
- kto ich uzywa,
- jak sprawdzamy, ze wynik jest poprawny,
- co robimy, gdy pipeline padnie.

<!-- end_slide -->

# Nowoczesny Data Engineer

Co robi DE na co dzien:

```text
BUILD    projektuje i buduje pipeline: source -> Bronze -> Silver -> Gold
TRUST    sprawdza ze dane sa kompletne, poprawne i na czas
FIX      debuguje co padlo, szuka pierwotnej przyczyny, naprawia
SHIP     wersjonuje, testuje, dokumentuje jak software engineer
EXPLAIN  tlumniczy analitykowi i biznesowi co w danych i czemu
```

Co musi umiec:

- SQL: CTE, window functions, EXPLAIN, grain, kardynalnosc
- Python: ekstrakcja, walidacja, orchestracja (Airflow DAG)
- model danych: relacje, klucze, typy, NULL semantics
- pisac idempotentne pipeline — run N razy = ten sam wynik
- data quality checks — blad widoczny natychmiast, nie ukryty w raporcie
- git + PR + code review jak software engineer
- czytac logi i debugowac bez paniki o 3 w nocy
- tlumaczyc trade-off: batch vs stream, lake vs warehouse, cost vs latency

<!-- end_slide -->

# Docelowa umiejetnosc

Po kursie umiesz zbudowac, wyslac i wyjasnic produkcyjny pipeline od zera.

**SQL**
- pisac zapytania z JOINami, CTE, funkcjami okienkowymi
- definiowac grain i udowodnic, ze go nie lamiesz
- debugowac duplikaty i NULL-e bez podpowiedzi
- czytac `EXPLAIN` i powiedziec, gdzie jest bottleneck

**Pipeline i architektura**
- zaprojektowac Medallion: Bronze → Silver → Gold z uzasadnieniem
- napisac idempotentny krok ETL (uruchom dwa razy, wynik ten sam)
- dodac data quality check, ktory zatrzyma pipeline przy zlych danych
- zaplanowac zadanie w Airflow (DAG, task, dependency, retry)

<!-- end_slide -->

# Docelowa umiejetnosc: praktyka

**Modelowanie**
- opisac model wymiaru i model faktow (star schema)
- dobrac typ join i uzasadnic decyzje
- przetransformowac surowy flat-file w analytical mart

**Narzedzia**
- pisac kod SQL w SQLite, DuckDB, Postgres (te same wzorce)
- korzystac z dbt: model, test, dokumentacja
- wersjonowac pipeline w git (branch, PR, review)
- czytac logi i naprawic failing task samodzielnie

**Komunikacja i interview**
- wyjasnic swoj pipeline niedevcowi w 2 minuty
- napisac README i runbook dla on-call
- opowiedziec o kompromisie technicznym (np. batch vs stream)
- odpowiedziec na pytanie: "co by sie stalo, gdyby to zadanie padlo o 3 w nocy?"

<!-- end_slide -->

# Najwazniejsza zmiana mindsetu

```text
Backend:
  request -> service -> database -> response

Data Engineering:
  source -> ingestion -> transform -> model -> validate -> serve
```

Backend pyta: czy request dziala teraz?

Data Engineer pyta: czy wynik jest poprawny, powtarzalny i zrozumialy jutro?

<!-- end_slide -->

# Dwie sciezki danych

```text
BATCH / transakcje
App -> Production DB -> snapshot / CDC -> Bronze -> Silver -> Gold

STREAM / eventy
App -> Kafka / PubSub -> consumer -> Bronze -> Silver -> Gold

Gold -> Dashboards / ML / Alerts
```

Event = fakt ze cos sie stalo: order_created, payment_failed, page_view.
Obie sciezki laduja do tych samych warstw Medallion.

<!-- end_slide -->

# Wizualnie: trusted data flow

```text
Source DB / API / Files / Kafka
  |
  v
[ ingestion / extraction ]
  |
  v
BRONZE  raw data, blisko zrodla
  |
  v
SILVER  clean data, typy, dedup, joiny
  |
  v
GOLD    marts, metryki, raporty
  |
  v
Dashboards / ML / Reports
```

Ten slajd jest mapa rozmowy: source, ingestion, Bronze, Silver, Gold, quality i odbiorcy.

<!-- end_slide -->

# Pelniejsza mapa architektury

```text
SOURCE LAYER
  App DB / SaaS API / CSV / Events
        |
        v
ORCHESTRATION
  Airflow: schedule, retry, alert
        |
        v
DATA LAKE / WAREHOUSE
  Bronze -> Silver -> Gold
        |
        v
QUALITY
  dbt tests / Great Expectations
        |
        v
SERVING
  BI / Notebooks / ML / API / Alerts
```

<!-- end_slide -->

# Ten sam flow jako model mentalny

Diagram warto umiec przerysowac prosto:

```text
Application
  | writes transactions
  v
Production DB  -- daily snapshots / CDC -->  Data Lake / Bronze
Application
  | emits events
  v
Kafka / PubSub --------------------------->  Data Lake / Bronze
Data Lake / Bronze
  -> Silver / master data
  -> Gold marts / OLAP cubes
  -> Metrics / dashboards / decisions
```

Najwazniejsze:
- aplikacja tworzy dane,
- metryka powstaje po czyszczeniu i modelowaniu.

<!-- end_slide -->

# ETL vs ELT

Roznica jest w miejscu transformacji:

```text
ETL:
Extract -> Transform -> Load
dane czyscimy/przeksztalcamy przed zaladowaniem do docelowej warstwy

ELT:
Extract -> Load -> Transform
dane najpierw ladujemy do lake/warehouse, potem transformujemy SQL/dbt/Spark
```

Dlaczego ELT wygrywa w nowoczesnym DE:

- surowe dane zostaja w lake — mozesz przetransformowac ponownie bez powrotu do zrodla,
- warehouse/lakehouse jest wystarczajaco mocny, zeby robic transformacje SQL na skali,
- zmiana logiki biznesowej = tylko re-run transformacji, nie dotykasz extraction,
- dbt robi "T" deklaratywnie: testowalny, wersjonowany, z lineage.

<!-- end_slide -->

# Architektura 1: Data Warehouse

**Jednym zdaniem:** osobny system/baza do analityki — nie baza aplikacji.

Najprosciej:

```text
Production DB  = baza aplikacji: szybkie zapisy pojedynczych zamowien
Data Warehouse = baza analityczna: szybkie SQL po wielu rekordach naraz
```

To nie jest "skupisko baz danych".
To zwykle jeden docelowy system analityczny.
Kopiujemy i porzadkujemy w nim dane z wielu zrodel.

Analogia: biblioteka z katalogiem.
Zanim cos wlozysz, musisz to opisac i skatalogowac.

Kiedy: ustrukturyzowane dane, duzo zapytan BI, stabilny schemat, szybkie agregaty.

Ryzyko: drogi na surowe dane, zmiana schematu bolesna, nie nadaje sie na logi i pliki binarne.

<!-- end_slide -->

# Architektura 2: Data Lake

**Jednym zdaniem:** tanie miejsce na pliki — surowe, nieprzetworzone, w kazdym formacie.

Analogia: tani magazyn.
Wrzucasz wszystko celowo, zeby przetworzyc pozniej.
Bez organizacji nikt nie wie, co tam jest.

Technologie: S3 + Parquet + Spark (AWS), GCS + BigQuery External, ADLS + Databricks

Kiedy: ogromne wolumeny, surowe dane do ML, logi, historia, tanie przechowywanie.

Ryzyko: bez governance lake zamienia sie w data swamp.
Nikt nie wie, co jest w srodku, kto jest wlascicielem i czy dane sa swieze.

> Lake ma surowe logi z 3 lat.
> Jak znajdziesz event `order_created`, jesli nie ma schematu ani wlasciciela?

<!-- end_slide -->

# Architektura 3: Lakehouse

**Jednym zdaniem:** data lake z gwarancjami SQL.

Dodaje ACID, schemat i time travel na plikach Parquet.

```text
Problem lake:
  tani storage, ale malo gwarancji tabeli

Table formats dodaja:
  ACID, schema evolution, time travel, upserts
```

Technologie:
- Databricks + Delta Lake,
- Apache Iceberg + Trino/Spark.

Kiedy: chcesz taniego storage lake + SQL jak warehouse + dostep dla ML.

Ryzyko: bardziej zlozony setup i operacje niz czysty warehouse.

<!-- end_slide -->

# Architektura 4: Batch vs Streaming

**Jednym zdaniem:**

Batch = przetwarzaj dane paczkami w oknach czasu.
Streaming = przetwarzaj zdarzenia od razu, gdy przychodza.

```text
BATCH                                 STREAMING
-----                                 ---------
co wiemy po oknie czasu?              co dzieje sie teraz?
daily/hourly job                      sub-sekunda latency
Airflow + Spark + SQL                 Kafka + Flink / Spark Streaming
latwiejszy debug i replay             trudniejszy debug (kolejnosc, late data)
wiekszosc DE pracy dzisiaj            alerting, fraud detection, real-time ML
```

Dlaczego batch najpierw:
- latwiej kontrolowac grain, joiny, walidacje i retry,
- streaming dodaje late data, ordering i exactly-once.

<!-- end_slide -->

# Batch vs Streaming: pytanie

> Klient chce real-time dashboard z revenue.
> Czy potrzebuje streaming, czy wystarczy batch co 5 minut?

<!-- end_slide -->

# Dlaczego produkcyjna baza nie wystarczy?

Production DB jest dla aplikacji:

- szybki zapis jednego zamowienia,
- aktualny stan systemu,
- relacje pod transakcje,
- minimalna duplikacja.

Analytics potrzebuje czego innego:

- historia,
- agregaty,
- stabilne metryki,
- tanie skany wielu rekordow,
- dane z wielu systemow.

<!-- end_slide -->

# Slownik na start

| Pojecie | Najprosciej |
|---|---|
| OLTP | baza aplikacji, szybkie transakcje |
| OLAP | analityka, agregaty, raporty |
| Data lake | tanie miejsce na pliki i surowe dane |
| Warehouse | miejsce do szybkiego SQL/analityki |
| Lakehouse | lake + transakcje + metadata + SQL |
| Medallion | Bronze/Silver/Gold jako warstwy jakosci |

<!-- end_slide -->

# Medallion bez magii

```text
Bronze
  dane blisko zrodla, mozna odtworzyc pipeline

Silver
  dane wyczyszczone, ujednolicone, z jasnym grain

Gold
  dane pod konkretny use case: dashboard, metryka, raport
```

Bronze trzyma surowe dane blisko zrodla.
Mozesz odtworzyc pipeline, jesli cos sie zepsuje.

Gold musi miec grain, definicje metryki i checki.
Odbiorca nie powinien zgadywac, co oznacza jeden rekord.

<!-- end_slide -->

# Co to znaczy grain?

Grain = odpowiedz na pytanie:

```text
Co oznacza jeden rekord w tej tabeli?
```

Przyklad:

- `customers`: jeden rekord = jeden klient,
- `orders`: jeden rekord = jedno zamowienie,
- `order_items`: jeden rekord = jedna pozycja zamowienia,
- `daily_sales`: jeden rekord = jeden dzien sprzedazy.

<!-- end_slide -->

# Czego uzywamy na zajeciach?

Minimalny toolchain:

- Git + GitHub/GitLab style PR thinking,
- VS Code,
- terminal Linux albo WSL Ubuntu,
- SQL client,
- SQLite na pierwsze SQL basics,
- DuckDB po fundamentach SQL,
- Python 3.11+,
- pytest,
- Docker,
- dbt,
- Airflow lokalnie,
- Markdown docs.

<!-- end_slide -->

# Dlaczego SQLite teraz, DuckDB potem?

SQLite:

- dobry do absolutnych podstaw SQL,
- zero server setup,
- idealny na maly kontrolowany schema/seed,
- pomaga skupic sie na grain, joinach, agregacji i walidacji.

DuckDB:

- wchodzi po fundamentach,
- szybki lokalny OLAP,
- czyta CSV/Parquet bez serwera,
- pasuje do labow data engineering bez ciezkiej infrastruktury.

Najpierw rozumiemy maly model danych.
Potem bierzemy wieksze pliki i DuckDB.

<!-- end_slide -->

# Czego NIE robi Postgres w tej sciezce?

Postgres nie jest finalnym OLAP celem kursu.

Jest dobry jako:

- baza aplikacyjna,
- system zrodlowy OLTP,
- przyklad snapshot/CDC source,
- kontekst integracji w pozniejszych modulach.

Analityczny lokalny tor: DuckDB + CSV/Parquet.

<!-- end_slide -->

# Jak pracujemy co tydzien?

```text
1. First principles: jaki problem rozwiazujemy?
2. Minimalny przyklad.
3. Live lab.
4. Artefakt w repo.
5. Review checklist.
6. Krotka odpowiedz interview.
```

Kazda lekcja zostawia slad w repo.

<!-- end_slide -->

# Artefakt per lesson

Materialy lekcji maja taki uklad:

```text
lesson_XX/
└── student/
    ├── README.md               <- startuj tutaj, otwierasz jako pierwsze
    ├── teoria.md               <- teoria, wzorce, pytania sprawdzajace
    ├── slides.presenterm.md    <- slajdy z zajec (do obejrzenia po)
    └── lab/
        └── ...                 <- aktywne cwiczenia do utrwalenia
```

Lekcja 00 ma dodatkowo `setup.md` i lab `data_flow_workshop.md`.

Od Lesson 01 dochodzi osobny homework SQL.

> **Check:** przed kazdymi zajecia otwierasz `student/README.md` jako pierwsze.

<!-- end_slide -->

# Miesiac 1

## SQL i modelowanie danych

- Praca z terminalem i Git: lokalne repo, commit, branch, push, PR thinking
- SQL od podstaw do zaawansowanego: grain, JOIN, agregacje, CTE, window functions
- Modelowanie danych: Medallion, Kimball, OBT, data contracts
- Pierwsze artefakty: query z walidacja, grain map, data product brief, PR do review

Cel: umiesz napisac i wyjasnic zapytanie SQL od grain po metryke oraz obronic model danych.

<!-- end_slide -->

# Miesiac 2

## Programowanie i ekosystem analityczny

- Programowanie od podstaw: typy, funkcje, petle, wyjatki, czysty kod
- Python i wizualizacja: pandas, polars, podstawowe wykresy jako narzedzie diagnostyki danych
- Srodowisko developera: Linux, Docker, repozytoria, virtualenv, debugger
- Projekt: maly ETL jako projekt inzynierski — extract, transform, validate, load, testy, CLI

Cel: umiesz napisac ETL jak projekt, nie jednorazowy skrypt.
Twoj kod jest czytelny, testowalny i uruchamialny w powtarzalnym srodowisku.

<!-- end_slide -->

# Miesiac 3

## Big Data i chmura

- Przetwarzanie rozproszone: Spark/PySpark foundations, partycje, shuffle, plan wykonania
- Chmura: podstawy GCP/Azure, storage, compute, uprawnienia, koszty
- Platforma danych w stylu lakehouse: Delta/Iceberg, table formats, schemat, time travel
- Projekt: lokalny pipeline skaluje sie do chmury

Cel: rozumiesz jak lokalny ETL staje sie pipeline produkcyjnym na duzych danych.

<!-- end_slide -->

# Miesiac 4

## Produkcyjne systemy danych

- Orkiestracja: Airflow — DAG, task, dependency, retry, alert, idempotency
- Warstwa transformacji i jakosci: dbt modele, testy, dokumentacja, lineage
- Streaming i architektura zdarzeniowa: Kafka basics, consumer/producer, late data, event schema
- Data quality i observability: Great Expectations, alerty, SLA

Cel: twoj pipeline jest zaplanowany, obserwowalny i ma runbook na wypadek bledu o 3 w nocy.

<!-- end_slide -->

# Miesiac 5

## Projekt koncowy i portfolio

- End-to-end system danych zbliżony do produkcyjnego: od zrodla przez transformacje po monitoring
- Infrastruktura jako kod: podstawy IaC, reproducible setup
- Obrona projektu: tłumaczysz decyzje techniczne, trade-offy, co by sie stalo przy N=10x danych
- Przygotowanie portfolio: README, architektura, runbook, mock interview

```text
source -> Bronze -> Silver -> Gold -> dbt -> Airflow -> monitoring -> README
```

Cel: masz projekt ktory mozesz pokazac na rozmowie i bronic kazdej decyzji.

<!-- end_slide -->

# Czego nie robimy na start?

Nie wchodzimy gleboko w:

- Spark internals,
- administracje Kafka,
- Terraform,
- Unity Catalog,
- pelny Iceberg lab,
- Data Vault jako osobny blok.

Te tematy maja sens dopiero, gdy rozumiemy data flow, grain i reliable batch.

<!-- end_slide -->

# Dzisiaj ma zostac w glowie

```text
Data Engineer nie buduje tylko tabel.

Buduje przeplyw danych, ktoremu mozna zaufac.
```

Jesli nie wiesz, co oznacza jeden rekord, nie wiesz jeszcze, co liczysz.

<!-- end_slide -->

# Mini-zadanie przed zamknieciem laptopa

Narysuj diagram data flow w Excalidraw:

```text
https://excalidraw.com
```

Na diagramie umies wszystkie etapy:

```text
Application  ->  Production DB  ->  Bronze  ->  Silver  ->  Gold  ->  Metrics
```

Dla kazdego etapu dodaj notke:

- kto zapisuje dane,
- kto czyta dane,
- co moze pojsc zle,
- jak sprawdzisz poprawnosc.

Wpisz odpowiedzi w `student/lab/data_flow_workshop.md`.
Jesli robisz diagram w Excalidraw, dodaj link albo screenshot obok odpowiedzi.