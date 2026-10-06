---
title: Lekcja 14 - Databricks Platform i Unity Catalog
author: Data Engineering Course
date: 2026-09-10
---

# Lekcja 14

Databricks Platform i Unity Catalog

```text
Spark liczy dane.
Databricks organizuje srodowisko, governance i operacje.
```

<!-- end_slide -->

# Cel lekcji

Po tej lekcji masz umiec powiedziec:

- co daje Databricks ponad "samego Sparka",
- czym sa workspace, cluster, jobs i SQL warehouse,
- czym jest Unity Catalog i po co jest `catalog.schema.object`,
- jak myslec o dev/test/prod, sekretach, ownerach i access control,
- gdzie koncza sie notebooki, a zaczyna platform engineering.

<!-- end_slide -->

# Problem bez platformy

Masz kod, ktory dziala lokalnie.
W produkcji pojawiaja sie inne pytania:

```text
Kto ma dostep do tabel?
Gdzie trzymamy sekrety?
Jak odpalamy job codziennie o 6:00?
Jak oddzielamy dev od prod?
Jak sprawdzamy lineage i ownership?
```

To nie jest problem samego SQL ani samego Spark API.

<!-- end_slide -->

# First principle

```text
Spark engine != data platform
```

Engine:
- wykonuje obliczenia,
- robi shuffle, join, write.

Platforma:
- zarzadza srodowiskiem,
- kontroluje dostep,
- daje governance,
- planuje uruchomienia,
- daje audit i operacje.

<!-- end_slide -->

# Mental model

```text
Kod        -> notebook / job / query
Compute    -> cluster / warehouse
Data       -> Delta tables / volumes
Governance -> Unity Catalog
Ops        -> jobs, alerts, lineage, owners
```

Jesli umiesz nazwac te 5 warstw, nie myslisz juz o Databricks jak o "notebooku w chmurze".

<!-- end_slide -->

# Architektura od zrodla do raportu

```text
source systems
    |
    v
bronze tables
    |
    v
silver models
    |
    v
gold marts
    |
    +--> BI / dashboards
    +--> ML / features
    +--> operational consumers

Databricks platform otacza caly ten flow:
workspace + jobs + catalog + permissions + monitoring
```

<!-- end_slide -->

# Workspace, cluster, warehouse, jobs

```text
workspace    = miejsce pracy zespolu
cluster      = compute do notebookow i spark jobs
sql warehouse = compute do SQL / BI
jobs         = planowanie i wykonywanie pipeline
```

Typowy blad:

```text
workspace = platforma
```

Nie. Workspace to tylko jeden element calej platformy.

<!-- end_slide -->

# Control plane vs data plane

```text
control plane
  - UI
  - jobs definitions
  - permissions metadata
  - catalog metadata

data plane
  - compute
  - storage
  - spark execution
  - delta files
```

Pytanie kontrolne:

```text
Gdzie leza moje dane, a gdzie tylko metadata i sterowanie?
```

<!-- end_slide -->

# Co daje Unity Catalog

Unity Catalog to nie jest tylko katalog nazw.
To jest governance layer.

Daje:

- centralny namespace,
- permissions,
- lineage,
- discovery,
- audit,
- obsluge managed i external assets.

<!-- end_slide -->

# Namespace, ktory porzadkuje firme

```text
catalog.schema.object
```

Przyklady:

```text
prod.finance.orders
prod.marketing.campaign_spend
dev.ml.customer_features
```

To rozwiazuje chaos typu:

```text
orders_final_v2_really_final
marketing_copy_new_fixed
```

<!-- end_slide -->

# Object model Unity Catalog

```text
metastore
  -> catalog
      -> schema
          -> table / view / volume / function / model
```

Wazne:

```text
Nie wszystko jest tylko tabela.
Governance obejmuje tez inne securable objects.
```

<!-- end_slide -->

# Managed vs external

```text
managed table
  - Databricks zarzadza governance i lifecycle storage

external table
  - Databricks zarzadza governance,
  - storage lifecycle jest poza nim
```

Pytanie praktyczne:

```text
Czy chcemy oddac platformie tez lifecycle storage,
czy tylko warstwe dostepu i katalogu?
```

<!-- end_slide -->

# Dev, test, prod

To nie jest kosmetyka. To jest bezpieczenstwo.

```text
dev  -> eksperyment
qa   -> walidacja
prod -> oficjalne dane i SLA
```

Roznice moga dotyczyc:

- katalogow,
- cluster policies,
- secrets,
- ownerow,
- schedule jobow,
- kosztow compute.

<!-- end_slide -->

# Typowy release flow

```text
notebook / code change
    -> review
    -> test run na dev
    -> publish job / asset
    -> validation na test
    -> prod schedule
    -> monitoring po deployu
```

To jest produkcyjna roznica miedzy "mam notebook" a "mam system".

<!-- end_slide -->

# Cluster policies i koszty

Bez zasad compute latwo przepalic budzet.

```text
policy ogranicza:
- typy maszyn
- autoscaling
- max workers
- runtime version
- access mode
```

Data engineer musi umiec powiedziec:

```text
Czy ten job potrzebuje duzego klastra,
czy tylko malego, stabilnego runtime?
```

<!-- end_slide -->

# Secrets i credentials

Anti-pattern:

```text
token albo haslo w notebooku
```

Lepszy wzorzec:

```text
secret scope / key vault / role-based access
```

Pytanie kontrolne:

```text
Czy osoba z dostepem do notebooka widzi tez raw credentials?
```

<!-- end_slide -->

# Lineage i ownership

W prawdziwej pracy chcesz odpowiedziec:

```text
Skad wziela sie ta tabela?
Kto jest jej ownerem?
Jakie dashboardy i joby od niej zaleza?
```

Unity Catalog i platform metadata sa po to, zeby to nie bylo zgadywanie.

<!-- end_slide -->

# Small files problem

W Delta Lake czeste appendy moga tworzyc wiele malych plikow.

```text
100 batchy -> 100+ malych plikow
read       -> duzy overhead metadata i open/close
```

Problem nie jest logiczny.
Problem jest operacyjny i wydajnosciowy.

<!-- end_slide -->

# OPTIMIZE, ZORDER, VACUUM

```text
OPTIMIZE = kompaktacja malych plikow
ZORDER   = lepszy layout pod czeste filtry
VACUUM   = usuwanie starych nieuzywanych plikow
```

To nie sa magiczne przyciski.
Kazda z tych operacji ma koszt i ryzyko.

<!-- end_slide -->

# Kiedy uzywasz tych operacji

```text
OPTIMIZE
  po wielu appendach albo regularnie na duzych tabelach

ZORDER
  gdy te same kolumny sa stale w WHERE / JOIN

VACUUM
  gdy chcesz kontrolowac storage,
  ale retention nie moze rozwalic time travel
```

<!-- end_slide -->

# Najgrozniejszy blad z VACUUM

```text
Retention za krotki -> tracisz stare pliki
-> ograniczasz time travel
-> utrudniasz debug i rollback
```

To jest typowe pytanie operacyjne:

```text
Czy oszczednosc storage jest warta utraty historii?
```

<!-- end_slide -->

# SQL warehouse vs cluster

Nie wszystko odpalasz na tym samym compute.

```text
cluster
  - ETL
  - data engineering
  - notebooks

SQL warehouse
  - BI queries
  - dashboards
  - ad hoc analytics
```

To rozdziela workload i koszt.

<!-- end_slide -->

# Jobs zamiast recznego Run All

W produkcji chcesz:

- harmonogram,
- retries,
- timeout,
- parametry,
- alerty,
- logs.

Czyli:

```text
job > reczne klikanie notebooka
```

<!-- end_slide -->

# Mini case

Masz tabele:

```text
prod.finance.card_payments
```

Kolumny:

```text
payment_id, customer_id, amount, status, card_number
```

Pytania:

1. Kto widzi `card_number`?
2. Czy BI powinno czytac z tej tabeli bezposrednio?
3. Czy to ma byc managed czy external?
4. Jaki owner odpowiada za jakość i access?

<!-- end_slide -->

# Recipe myslenia o platformie

Zawsze przejdz te pytania:

```text
1. Gdzie ten kod sie uruchamia?
2. Kto ma dostep do danych?
3. Jak rozdzielamy dev/test/prod?
4. Jaki jest owner tabeli i joba?
5. Jak kontrolujemy koszt?
6. Jak diagnozujemy problem po deployu?
```

<!-- end_slide -->

# Najczestsze anti-patterny

- wszystko w jednym notebooku,
- prod i dev w tym samym katalogu,
- brak ownera tabeli,
- sekrety w kodzie,
- brak cluster policy,
- reczne odpalanie krytycznych pipeline.

<!-- end_slide -->

# Tutoriale po lekcji

Oficjalne i sensowne starty:

1. Databricks Getting Started Tutorials
   https://docs.databricks.com/en/getting-started/index.html

2. Build an ETL pipeline using Apache Spark
   https://docs.databricks.com/aws/en/getting-started/etl-quick-start

3. Unity Catalog get started
   https://docs.databricks.com/aws/en/data-governance/unity-catalog/get-started

<!-- end_slide -->

# Co oddajesz po lekcji

```text
homework/lesson_14/
  01_platform_map.md
  02_unity_catalog_design.md
  03_delta_ops_notes.md
  04_security_governance_scenario.md
  05_interview_answers.md
```

Masz umiec nie tylko nazwac pojecia,
ale obronic decyzje jak w prawdziwym projekcie.

<!-- end_slide -->

# Closing check

Powiedz na glos:

```text
Databricks to nie tylko Spark runtime.
To platforma, ktora laczy compute, governance,
job orchestration, lineage i access control.
```

Jesli umiesz to wyjasnic na prostym case,
lekcja jest zaliczona.
