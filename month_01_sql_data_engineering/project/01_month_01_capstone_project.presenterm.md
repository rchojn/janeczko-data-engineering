---
title: Month 01 Capstone - NYC Taxi Data Product
author: Data Engineering Course
date: 2026-08-17
---

# Month 01 Capstone

NYC Taxi Data Product

```text
Real data -> reliable SQL model -> validated metrics -> business report
```

Cel projektu: pokazac, ze potrafisz zbudowac maly, odtwarzalny produkt danych, a nie tylko napisac pojedyncze zapytania SQL.

<!-- end_slide -->

# Executive summary

Budujesz lokalny produkt analityczny na publicznych danych NYC TLC Yellow Taxi.

Projekt ma pokazac cztery kompetencje:

```text
1. Rozumiesz odbiorce i pytania biznesowe.
2. Umiesz zamienic surowe pliki w model raw / silver / gold.
3. Umiesz zdefiniowac grain, metryki i walidacje.
4. Umiesz opisac jak projekt odtworzyc, utrzymac i debugowac.
```

Szczegolowe komendy i wymagane pliki sa w briefie:

```text
02_month_01_capstone_project_instructions.md
```

<!-- end_slide -->

# Business context

Odbiorca: zespol city operations / mobility analytics.

Pytania, na ktore produkt ma odpowiedziec:

```text
Ktore strefy generuja najwiekszy popyt i revenue?
W ktorych godzinach wystepuja szczyty popytu?
Jak zachowuja sie przejazdy z lotnisk?
Czy wyniki sa odtwarzalne i wystarczajaco zaufane?
```

To jest projekt o decyzjach biznesowych, nie o samym uruchomieniu DuckDB.

<!-- end_slide -->

# Product outcome

Finalny output ma byc czytelny dla dwoch osob.

```text
Data consumer:
  czyta reports/01_business_summary.md i rozumie najwazniejsze wnioski

Data engineer / reviewer:
  czyta sql/, docs/ i README.md i potrafi odtworzyc pipeline
```

Profesjonalny projekt danych laczy wynik biznesowy z techniczna odtwarzalnoscia.

<!-- end_slide -->

# Scope

W zakresie:

```text
DuckDB
SQL
Parquet + CSV
raw / silver / gold
fact + dimension
data quality checks
EXPLAIN / performance note
backfill plan
incident runbook
business summary
```

Poza zakresem:

```text
Airflow, dbt, Spark, cloud, Python ingestion, dashboard BI
```

Month 01 sprawdza fundamenty SQL Data Engineering.

<!-- end_slide -->

# Dataset

Uzywasz realnych danych NYC TLC.

```text
yellow_tripdata_2024-01.parquet
yellow_tripdata_2024-02.parquet
yellow_tripdata_2024-03.parquet
yellow_tripdata_2024-04.parquet
yellow_tripdata_2024-05.parquet
yellow_tripdata_2024-06.parquet
taxi_zone_lookup.csv
```

Zrodlo:

```text
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
```

Pliki 2024-01 do 2024-06 oraz lookup CSV zostaly zweryfikowane 2026-08-16.

<!-- end_slide -->

# Volume decision

Docelowo pracujesz na 6 miesiacach danych.

```text
Dlaczego 6 miesiecy:
  widac zmiany miesiac do miesiaca
  performance zaczyna miec znaczenie
  backfill ma realny sens
  walidacje row count nie sa tylko formalnoscia
```

Minimalny zakres akceptowalny: 3 miesiace.

Jesli ograniczasz zakres, opisujesz powod w README jako znane ograniczenie.

<!-- end_slide -->

# Architecture overview

```text
NYC TLC Parquet / CSV
        |
        v
raw views
        |
        v
silver_taxi_trips + rejected_taxi_trips
        |
        v
dim_taxi_zone + fact_taxi_trips
        |
        v
gold_daily_zone_metrics
gold_hourly_demand
gold_airport_metrics
        |
        v
validation checks + business report
```

Ta architektura pokazuje przeplyw danych, odpowiedzialnosc warstw i miejsce kontroli jakosci.

<!-- end_slide -->

# Why DuckDB

DuckDB jest dobrym narzedziem do lokalnego capstone, bo pozwala pracowac bez platformy chmurowej.

```text
Czyta Parquet bez recznego importu.
Dziala lokalnie na laptopie.
Pozwala uczyc sie SQL, modelowania i performance.
Nie ukrywa logiki za frameworkiem.
```

Kluczowy wzorzec:

```sql
SELECT *
FROM read_parquet('data/raw/tlc/yellow/year=2024/month=*/yellow_tripdata_2024-*.parquet');
```

<!-- end_slide -->

# Layer responsibilities

```text
raw:
  faithful read of source files; no business cleanup

silver:
  typed, filtered, explainable accepted trips

rejected:
  records not used in metrics, with reason

fact:
  accepted trip-level event table

dimension:
  zone metadata used for business-readable metrics

gold:
  aggregated tables answering concrete business questions
```

Kazda warstwa ma miec jasny powod istnienia.

<!-- end_slide -->

# Data model

Minimalny model koncowy:

```text
dim_taxi_zone
  one row = one NYC taxi zone

fact_taxi_trips
  one row = one accepted Yellow Taxi trip

gold_daily_zone_metrics
  one row = one day + pickup borough + pickup zone

gold_hourly_demand
  one row = one day + pickup hour

gold_airport_metrics
  one row = one day + airport pickup zone
```

Bez grain nie wiadomo, co oznacza COUNT, SUM ani unikalnosc wyniku.

<!-- end_slide -->

# Quality policy

Nie filtrujesz danych po cichu.

Akceptowany rekord musi spelnic minimum:

```text
pickup_at is not null
dropoff_at is not null
pickup_at < dropoff_at
trip_distance > 0
total_amount >= 0
```

Odrzucone rekordy trafiaja do rejected_taxi_trips z reject_reason.

To jest roznica miedzy czyszczeniem danych a kontrolowanym procesem jakosci.

<!-- end_slide -->

# Gold tables

Gold layer ma odpowiadac na pytania odbiorcy.

```text
gold_daily_zone_metrics:
  gdzie jest revenue i popyt dzien po dniu?

gold_hourly_demand:
  ktore godziny maja najwyzszy popyt?

gold_airport_metrics:
  jak lotniska roznia sie od reszty miasta?
```

Kazda tabela gold musi miec opisany grain, metryki i znane ograniczenia interpretacji.

<!-- end_slide -->

# Required SQL capabilities

Projekt ma naturalnie pokazac fundamenty Month 01.

```text
SELECT / WHERE / GROUP BY
JOIN fact -> dimension
CTE for readable transformations
CASE WHEN for reject reasons or categories
window function for ranking or month-over-month comparison
CREATE OR REPLACE for idempotency
EXPLAIN for performance review
```

Nie chodzi o uzycie syntaxu dla checkboxa. Kazdy element ma wynikac z problemu.

<!-- end_slide -->

# Validation strategy

Walidacje odpowiadaja na pytanie: czy mozemy pokazac metryki odbiorcy?

Minimum:

```text
silver has rows
rejected records have reject_reason
silver has no negative total_amount
silver has no non-positive trip_distance
gold_daily_zone_metrics has unique grain
fact_taxi_trips joins to dim_taxi_zone as expected
smoke test confirms main tables exist and contain rows
```

Dobre walidacje sa konkretne i maja opisany oczekiwany wynik.

<!-- end_slide -->

# Operational thinking

Ten projekt nie ma schedulera, ale ma pokazac, ze rozumiesz jak pipeline dziala operacyjnie.

Dokumentujesz:

```text
run metadata design:
  co zapisalbys o kazdym uruchomieniu

backfill plan:
  jak przeliczysz poprawiony miesiac danych

incident runbook:
  jak zbadasz nagly revenue spike
```

To odroznia projekt Data Engineering od folderu z query.

<!-- end_slide -->

# Performance review

Nie musisz byc ekspertem od optymalizacji.

Masz pokazac, ze umiesz zadac dobre pytania:

```text
Ktore query czyta najwiecej danych?
Czy filtrujesz dane przed agregacja gold?
Czy wybierasz tylko potrzebne kolumny?
Czy gold tables ograniczaja ponowne liczenie wszystkiego od zera?
Co zmienilbys, gdyby danych bylo 100x wiecej?
```

Uzyj EXPLAIN i opisz obserwacje prostym jezykiem.

<!-- end_slide -->

# Deliverable structure

Oddajesz uporzadkowany katalog projektu.

```text
homework/month_01_capstone/
├── sql/       raw, silver, fact, dim, gold, checks, smoke test
├── docs/      grain, metrics, contract, runs, backfill, runbook
├── reports/   business summary dla odbiorcy
├── README.md  reproducible project guide
└── .gitignore
```

Nie commitujesz duzych Parquetow, lokalnej bazy DuckDB ani cache.

<!-- end_slide -->

# SQL package

Oczekiwany zestaw SQL:

```text
00_bootstrap.sql
01_raw_sources.sql
02_raw_profiling.sql
03_silver_trips.sql
04_dimensions.sql
05_fact_trips.sql
06_gold_daily_zone_metrics.sql
07_gold_hourly_demand.sql
08_gold_airport_metrics.sql
09_validation_checks.sql
10_performance_review.sql
11_smoke_test.sql
```

To jest pipeline podzielony na odpowiedzialnosci, nie jeden plik all_queries.sql.

<!-- end_slide -->

# Documentation package

Oczekiwane dokumenty:

```text
01_problem_statement.md
02_data_sources.md
03_grain_and_model.md
04_metric_definitions.md
05_data_quality_contract.md
06_pipeline_runs_design.md
07_backfill_plan.md
08_incident_runbook.md
09_query_review.md
10_interview_answer.md
```

Dokumentacja nie jest dodatkiem po projekcie. To czesc produktu danych.

<!-- end_slide -->

# Business report

reports/01_business_summary.md ma byc napisany dla odbiorcy, nie tylko dla reviewera technicznego.

Powinien zawierac 5-8 insightow, na przyklad:

```text
top pickup zones by revenue
top pickup zones by trip count
strongest demand hours
airport revenue share
highest revenue month
data quality observation
metric interpretation risk
```

SQL tworzy wynik. Raport tlumaczy, co z niego wynika.

<!-- end_slide -->

# Review rubric

Reviewer bedzie ocenial trzy obszary.

```text
Reproducibility:
  czy da sie uruchomic projekt od zera z README

Engineering quality:
  czy model, walidacje i SQL sa spojne

Product quality:
  czy wynik odpowiada na realne pytania i jest czytelny
```

Dobry projekt broni sie jako calosc: kod, dane, dokumentacja i raport.

<!-- end_slide -->

# Levels of completion

```text
Level 1 - works end-to-end:
  raw -> silver -> fact/dim -> gold -> basic checks

Level 2 - professional capstone:
  6 months, rejects, validation, EXPLAIN, backfill, runbook, contract

Level 3 - portfolio-ready:
  strong README, clear insights, month-over-month analysis, polished docs
```

Minimalny cel kursu: Level 2.

Ambitny cel portfolio: Level 3.

<!-- end_slide -->

# Recommended execution plan

```text
Day 1: data download, raw views, profiling
Day 2: silver table, rejects, grain documentation
Day 3: dimension, fact table, daily zone metrics
Day 4: hourly demand, airport metrics, month-over-month view
Day 5: validation checks, smoke test, EXPLAIN review
Day 6: metric definitions, quality contract, README
Day 7: backfill plan, incident runbook, business summary, interview answer
```

Aktualizuj dokumenty w trakcie budowy. Nie odtwarzaj decyzji z pamieci na koncu.

<!-- end_slide -->

# Common weak submissions

```text
Jeden plik all_queries.sql bez struktury.
Brak grain dla tabel gold.
Metryki policzone, ale niezdefiniowane.
Odrzucone rekordy znikaja bez rejected table.
README nie pozwala odtworzyc projektu.
Raport biznesowy tylko mowi, ze query dziala.
Brak walidacji unikalnosci i join quality.
```

Te problemy wygladaja jak lab. Capstone ma wygladac jak projekt.

<!-- end_slide -->

# Strong final narrative

Na koniec masz umiec powiedziec:

```text
Zbudowalem lokalny produkt danych na realnych plikach NYC Taxi.
DuckDB czyta Parquet i CSV w warstwie raw.
Silver oddziela poprawne przejazdy od rejected records.
Fact i dimension definiuja model analityczny.
Gold tables odpowiadaja na pytania o revenue, demand i airport trips.
Walidacje, smoke test i EXPLAIN zwiekszaja zaufanie do wynikow.
README, backfill plan i runbook pokazuja, jak projekt utrzymac.
```

To jest praktyczny sens Month 01 SQL Data Engineering.

<!-- end_slide -->

# Next step

Otworz brief projektu i przejdz po nim jak po specyfikacji wykonawczej.

```text
02_month_01_capstone_project_instructions.md
```

Prezentacja daje kontekst i standard jakosci.

Brief daje konkretne pliki, komendy, SQL outputy i acceptance criteria.
