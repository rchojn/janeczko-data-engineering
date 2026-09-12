# Teoria: czym jest Data Engineering

<!-- end_slide -->

## Jak szeroko masz to rozumiec teraz?

Lekcja 00 jest mapa swiata przed nauka SQL. Masz poznac nazwy i intuicje, ale nie masz jeszcze projektowac calej platformy danych.

Na tym etapie wystarczy:

```text
source system -> ingestion -> lake / warehouse / lakehouse -> marts / metrics -> consumer
```

Nie ucz sie definicji na pamiec. Ucz sie pytan:

- skad dane przyszly?
- czy to jest system transakcyjny, czy analityczny?
- czy dane sa surowe, oczyszczone, czy gotowe dla odbiorcy?
- kto podejmuje decyzje na podstawie wyniku?
- jak sprawdzimy, ze wynik jest godny zaufania?

Szczegoly typu table formats, partitioning, Spark, Iceberg i orchestration wracaja pozniej. Teraz budujemy slownik, zeby SQL w lekcji 01 mial sens.

<!-- end_slide -->

## Fundamenty

Firma podejmuje decyzje na podstawie danych.

Zeby decyzja byla dobra, dane musza byc:

- poprawne,
- aktualne,
- zrozumiale,
- powtarzalne,
- dostepne dla odpowiednich ludzi i systemow.

Data Engineering to praca nad tym, zeby dane przeszly droge od systemow zrodlowych do zaufanych produktow danych.

<!-- end_slide -->

## Przyklad e-commerce

Aplikacja sklepu zapisuje:

- klientow,
- zamowienia,
- pozycje zamowien,
- platnosci,
- klikniecia,
- wyszukiwania,
- eventy marketingowe.

Backend pyta:

```text
Czy zamowienie zostalo zapisane poprawnie teraz?
```

Data Engineer pyta:

```text
Czy za tydzien nadal bedziemy umieli policzyc revenue poprawnie, powtarzalnie i z ta sama definicja?
```

<!-- end_slide -->

## OLTP vs OLAP

OLTP to system transakcyjny. Optymalizuje szybkie zapisy i odczyty pojedynczych rekordow.

Przyklady:

- aplikacyjna baza zamowien,
- user profile database,
- payment records,
- inventory updates.

OLAP to system analityczny. Optymalizuje agregacje, skanowanie wielu rekordow i raportowanie.

Przyklady:

- warehouse,
- data mart,
- OLAP cube,
- DuckDB local analytical lab,
- lakehouse tables.

Postgres moze byc swietnym OLTP source system. Nie robimy z niego glownego celu OLAP w tym kursie.

<!-- end_slide -->

## Data flow

Typowy przeplyw:

```text
Application
  -> production database / event stream
  -> ingestion
  -> Bronze raw data
  -> Silver cleaned data
  -> Gold marts / metrics
  -> dashboard / ML / business decision
```

<!-- end_slide -->

## ETL vs ELT: dlaczego ELT wyparl ETL

ETL (Extract → Transform → Load) powstawalo, gdy storage i compute byly drogie.
Transformowales dane ZANIM je zaladowalem, bo nie mogles pozwolic sobie na przechowywanie surowych danych.

ELT (Extract → Load → Transform) dominuje dzisiaj z trzech powodow:

```text
1. Storage jest tani: S3/GCS/Azure Blob kosztuje grosze za GB.
   Mozesz ladownac surowe dane i trzymac je wiecznie (Bronze).

2. Compute jest w warehouse: BigQuery, Snowflake, Redshift, DuckDB
   maja masywna moc obliczeniowa. Transformacje SQL/dbt uruchamiasz
   bezposrednio tam, gdzie dane juz sa. Nie przenosisz danych do
   zewnetrznego narzedzia transformacji.

3. Reprocessing bez paniki: skoro masz surowe dane (Bronze),
   mozesz przeliczyc Silver i Gold od nowa, gdy logika biznesowa
   sie zmieni. W starym ETL, jesli zmieniles transformacje,
   czesto traciles historyczne dane surowe.
```

Przyklad praktyczny:

```text
ETL (stary sposob):
  Baza aplikacji
    -> Python/Spark transformuje dane na serwerze ETL
    -> Laduje gotowe rekordy do DW
  Problem: co jesli transformacja byla zla? Surowych danych juz nie ma.

ELT (dzisiejszy sposob):
  Baza aplikacji
    -> Ladujemy surowe dane do Bronze (S3/lake)
    -> dbt/SQL transformuje dane wewnatrz warehouse
    -> Silver i Gold sa efektem transformacji na surowych danych
  Zaleta: Bronze zawsze istnieje. Mozesz przeliczyc od nowa.
```

Dlatego w kursie uczymy ELT:
SQLite (Bronze) -> SQL transformacje -> wynik (Silver/Gold).
dbt w miesiacu 4 jest implementacja ELT w skali produkcyjnej.

<!-- end_slide -->

## Bronze, Silver, Gold

Bronze:

- dane prawie takie jak przyszly ze zrodla,
- minimalne zmiany,
- przydatne do audytu i reprocessingu.

Silver:

- dane oczyszczone,
- ujednolicone typy,
- usuniete oczywiste bledy,
- przygotowane do modelowania.

Gold:

- dane pod konkretne uzycie,
- metryki,
- data marts,
- tabele dla dashboardow.

<!-- end_slide -->

## Batch vs stream

Batch:

```text
Co godzine / codziennie bierzemy porcje danych i przetwarzamy.
```

Stream:

```text
Przetwarzamy eventy prawie na zywo, gdy sie pojawiaja.
```

Na starcie kursu batch jest prostszy. Streaming wraca pozniej jako osobny temat.

<!-- end_slide -->

## Pojecia, ktore wystarczy rozpoznawac

Data lake:

- miejsce na duzo danych w plikach,
- czesto trzyma dane blisko formy zrodlowej,
- dobre do historii, reprocessingu i roznych typow danych.

Warehouse:

- system analityczny pod raportowanie i metryki,
- zwykle ma mocniejsze kontrakty tabel i danych dla biznesu,
- dobry do SQL, agregacji i dashboardow.

Lakehouse:

- proba polaczenia lake i warehouse,
- dane sa w plikach, ale z dodatkowymi zasadami jak tabele, schema, transakcje i wersjonowanie,
- szczegoly poznasz pozniej przy Parquet/table formats.

Data mart:

- waski produkt danych dla konkretnego obszaru,
- przyklad: sales mart, marketing mart, finance mart.

Metric layer / metrics:

- miejsce, gdzie definicje metryk maja byc jednoznaczne,
- przyklad: `revenue = paid order_items quantity * unit_price`, bez cancelled orders.

OLAP cube:

- struktura do szybkiej analizy metryk po wymiarach,
- przyklad: revenue po kraju, dniu, produkcie i kanale.

Na tym etapie nie musisz znac implementacji. Masz umiec powiedziec, ktory element jest zrodlem, ktory jest miejscem analityki, a ktory jest produktem dla odbiorcy.

<!-- end_slide -->

## Mapa narzedzi

SQLite:

- pierwsza rozgrzewka SQL,
- maly dataset,
- zero serwera.

DuckDB:

- lokalna analityka,
- CSV/Parquet,
- dobry most do OLAP myslenia.

Parquet:

- kolumnowy format plikow,
- standard w data lake/lakehouse.

dbt:

- transformacje SQL jako projekt,
- modele, testy, dokumentacja.

Airflow:

- orkiestracja: kiedy i w jakiej kolejnosci odpalac kroki.

Postgres:

- dobry przyklad bazy aplikacyjnej / OLTP source,
- nie glowny cel analityczny tej sciezki.

<!-- end_slide -->

## Pytania sprawdzajace zrozumienie

1. Co by sie stalo, gdyby dashboard czytal prosto z production DB?
2. Czy jeden system moze byc jednoczesnie OLTP i OLAP? Jaki jest koszt?
3. Dlaczego raw data nie znaczy trusted data?
4. Dlaczego metryka bez definicji jest ryzykowna?
5. Dlaczego pipeline musi byc powtarzalny?
6. Czy Data Engineer jest blizej backendu, analityka czy platformy?
7. Co musi byc prawda, zebys zaufal tabeli `gold_daily_revenue`?

<!-- end_slide -->

## Otworz i zrob to

To jest opcjonalna diagnostyka. Odpowiedz krotko tylko na te pytania, ktore pomagaja Ci zobaczyc, czego jeszcze nie rozumiesz. Nie szukaj perfekcyjnych definicji.

<!-- end_slide -->

## Minimalny prereq przed prezentacja

Przed slajdami masz umiec powiedziec wlasnymi slowami, nawet bardzo prosto:

1. Gdzie aplikacja zapisuje dane produkcyjne?
2. Dlaczego raport analityczny moze przeszkadzac bazie produkcyjnej?
3. Co oznacza, ze dane sa raw/surowe?
4. Co oznacza, ze dane sa gotowe dla biznesu?
5. Czego jeszcze nie rozumiesz w slowach: lake, warehouse, lakehouse, ETL, ELT, Bronze, Silver, Gold?

<!-- end_slide -->

## Musisz umiec odpowiedziec przed lekcja

1. Co robi aplikacja, gdy uzytkownik sklada zamowienie?
2. Gdzie aplikacja zapisuje dane?
3. Dlaczego dashboard zwykle nie powinien czytac bezposrednio z production DB?
4. Czym intuicyjnie rozni sie data lake od warehouse?
5. Co oznacza Bronze, Silver i Gold w jednym zdaniu?

<!-- end_slide -->

## Czesc 1: doswiadczenie software

1. Co robi typowa aplikacja webowa, gdy uzytkownik sklada zamowienie?
2. Gdzie aplikacja zapisuje dane?
3. Dlaczego baza produkcyjna musi byc szybka dla pojedynczych transakcji?
4. Co moze sie stac, jesli analityk odpali bardzo ciezki raport na bazie produkcyjnej?
5. Czym rozni sie request w aplikacji od batch joba?

<!-- end_slide -->

## Czesc 2: intuicja data flow

1. Skad firma wie, ile zarobila wczoraj?
2. Czy dashboard powinien czytac bezposrednio z bazy aplikacji? Dlaczego tak/nie?
3. Co to znaczy, ze dane sa "surowe"?
4. Co to znaczy, ze dane sa "oczyszczone"?
5. Co to znaczy, ze dane sa "gotowe dla biznesu"?

<!-- end_slide -->

## Czesc 3: OLTP vs OLAP

1. Co Twoim zdaniem znaczy OLTP?
2. Co Twoim zdaniem znaczy OLAP?
3. Czy Postgres moze byc baza aplikacyjna? Dlaczego?
4. Czy Postgres jest automatycznie najlepszym miejscem do duzych raportow analitycznych? Dlaczego niekoniecznie?
5. Dlaczego DuckDB moze byc dobry do lokalnej analityki plikow?

<!-- end_slide -->

## Czesc 4: slownik Data Engineering

To sa pojecia, ktore potem pojawia sie w wzorce w dalszej czesci tego pliku. Najpierw naucz sie je rozpoznawac, potem dopiero uzywaj wzorcow.

Napisz po jednym zdaniu, nawet jesli nie jestes pewny:

1. system zrodlowy / source system - miejsce, gdzie dane powstaja, np. aplikacja albo jej baza,
2. ingestion - pobranie danych ze zrodla do miejsca analitycznego,
3. batch - przetwarzanie paczki danych, np. raz dziennie,
4. stream - przetwarzanie danych na biezaco albo prawie na biezaco,
5. data lake - miejsce na pliki z danymi, czesto w roznych formatach i warstwach,
6. warehouse - baza analityczna zoptymalizowana pod raporty i zapytania,
7. data mart - mniejszy obszar danych dla konkretnego zespolu albo tematu,
8. metryka / metric - liczba z definicja biznesowa, np. przychod z oplaconych zamowien,
9. jakosc danych / data quality - zestaw oczekiwan, ktore dane musza spelniac,
10. pipeline - powtarzalny przeplyw danych od zrodla do wyniku.

<!-- end_slide -->

## Czesc 5: data flow w stylu DataExpert/Zach

Popatrz na schemat ze slajdu: aplikacja -> production DB / Kafka -> data lake -> master data -> OLAP cubes -> metrics.

Odpowiedz:

1. Ktore dane wygladaja jak transakcje?
2. Ktore dane wygladaja jak eventy?
3. Dlaczego eventy moga isc przez Kafka?
4. Dlaczego snapshots z production DB moga isc do data lake?
5. Gdzie powstaje metryka biznesowa?

<!-- end_slide -->

## Czesc 6: Twoje pytania

Zapisz 5 pytan, ktore chcesz pozniej wyjasnic.

Przyklad dobrego pytania:

```text
Nie rozumiem, czemu data lake i warehouse to nie to samo. Czy data lake to po prostu folder z plikami?
```

<!-- end_slide -->

## Jak korzystac z tego pliku

To nie jest regulamin. To mapa bledow myslenia, ktore najczesciej prowadza do zlych danych.

Ucz sie tego przez schemat:

```text
Sytuacja -> ryzyko -> lepsze pytanie -> lepszy wzorzec
```

Twoje zadanie: gdy widzisz sytuacje z danymi, rozpoznaj ryzyko i nazwij lepszy sposob myslenia.

<!-- end_slide -->

## Wzorzec 1: zrodlo danych to jeszcze nie produkt danych

Antywzorzec:

```text
Mamy tabele w bazie, wiec mamy gotowe dane dla biznesu.
```

Dlaczego szkodzi:

- baza aplikacji jest projektowana pod dzialanie produktu, nie pod raportowanie,
- nazwy kolumn nie zawsze tlumacza sens biznesowy,
- dane moga miec duplikaty, braki, anulowane rekordy albo zmienione statusy,
- dashboard moze policzyc metryke inaczej niz inny dashboard.

Lepszy wzorzec:

```text
Tabela zrodlowa -> tabela zrozumiana -> zaufany produkt danych
```

Pytanie kontrolne:

```text
Kto uzywa tej tabeli i jaka decyzje podejmuje?
```

<!-- end_slide -->

## Wzorzec 2: zrodlo OLTP to nie cel OLAP

Antywzorzec:

```text
Znam Postgresa, wiec Postgres bedzie naszym warehouse'em.
```

Dlaczego szkodzi:

- Postgres moze byc swietna baza aplikacyjna,
- mala analityka na Postgresie jest mozliwa,
- ale ciezkie raporty, historia, duze skany i pliki analityczne to inny typ problemu.

Lepszy wzorzec:

```text
Postgres / baza aplikacji = kontekst zrodla OLTP
DuckDB / warehouse / lakehouse = kontekst przetwarzania analitycznego
```

Pytanie kontrolne:

```text
Czy ten system obsluguje transakcje aplikacji, czy analityczne pytania po historii?
```

<!-- end_slide -->

## Wzorzec 3: surowe dane nie sa jeszcze zaufane

Antywzorzec:

```text
Skoro dane trafily do lake, to sa juz dobre.
```

Dlaczego szkodzi:

- surowe dane moga miec zle typy,
- moga zawierac duplikaty,
- moga miec null keys,
- moga przyjsc za pozno,
- moga miec inna definicje statusu niz raport.

Lepszy wzorzec:

```text
Bronze = to, co przyszlo
Silver = to, co oczyscilismy i ujednolicilismy
Gold = to, czego odbiorca moze uzyc
```

Pytanie kontrolne:

```text
Jakie checki musza przejsc dane, zanim ktos podejmie na ich podstawie decyzje?
```

<!-- end_slide -->

## Wzorzec 4: narzedzie wynika z problemu

Antywzorzec:

```text
Najpierw wybierzmy Spark/Kafka/dbt, potem wymyslimy problem.
```

Dlaczego szkodzi:

- narzedzie moze ukryc brak rozumienia danych,
- latwo nauczyc sie nazw bez umiejetnosci projektowania flow,
- za duzo narzedzi naraz zwieksza chaos poznawczy.

Lepszy wzorzec:

```text
Problem -> ksztalt danych -> skala -> wymagania niezawodnosci -> narzedzie
```

Przyklad:

```text
Maly SQL model -> SQLite
Lokalna analityka CSV/Parquet -> DuckDB
Transformacje SQL jako projekt -> dbt
Harmonogram i retry -> Airflow
Duzy distributed processing -> Spark
```

Pytanie kontrolne:

```text
Jaki problem to narzedzie rozwiazuje w tym konkretnym flow?
```

<!-- end_slide -->

## Wzorzec 5: metryka potrzebuje definicji

Antywzorzec:

```text
Revenue to po prostu SUM(amount).
```

Dlaczego szkodzi:

- nie wiadomo, czy liczymy anulowane zamowienia,
- nie wiadomo, czy liczymy brutto/netto,
- nie wiadomo, czy duplikaty sa usuniete,
- nie wiadomo, na jakim grain liczymy wynik.

Lepszy wzorzec:

```text
Metryka = definicja biznesowa + grain + filtry + walidacja
```

Pytanie kontrolne:

```text
Czy dwie osoby policzylyby te metryke tak samo po przeczytaniu naszej definicji?
```

<!-- end_slide -->

## Wzorzec 6: pipeline musi przezyc rzeczywistosc

Antywzorzec:

```text
Pipeline zadzialal raz, wiec jest gotowy.
```

Dlaczego szkodzi:

- pipeline moze odpalic sie drugi raz,
- source moze zmienic schema,
- dane moga przyjsc za pozno,
- retry moze zduplikowac rekordy,
- dashboard moze pokazac stary wynik.

Lepszy wzorzec:

```text
Dziala raz -> jest powtarzalny -> jest zwalidowany -> jest obserwowalny -> jest opisany
```

Pytanie kontrolne:

```text
Co sie stanie, jesli ten sam krok odpali sie dwa razy z tym samym inputem?
```

<!-- end_slide -->

## Mini-checklist przed SQL

Zanim przejdziesz do lekcji 01 SQL, umiej odpowiedziec:

- Skad dane sa tworzone?
- Co pipeline z nimi robi?
- Kiedy dane staja sie produktem danych?
- Czym rozni sie OLTP source od OLAP target?
- Dlaczego DuckDB/Parquet sa bardziej analityczne niz Postgres jako app DB?
- Jakie checki daja zaufanie do wyniku?
