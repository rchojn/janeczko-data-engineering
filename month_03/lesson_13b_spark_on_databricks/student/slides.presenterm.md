---
title: Lekcja 13b - Spark na Databricks
author: Data Engineering Course
date: 2026-09-10
---

# Lekcja 13b

Spark na Databricks

```text
To jest most miedzy lokalnym PySpark a platformowym runem w Databricks.
```

<!-- end_slide -->

# Po co osobna lekcja

Masz juz:

- Spark foundations,
- Delta basics,
- Spark internals.

Teraz potrzebujesz zobaczyc:

```text
jak ten sam Spark code zyje w Databricks workflow
```

<!-- end_slide -->

# Najprostszy flow

```text
workspace
  -> compute
  -> notebook
  -> read / transform
  -> Delta table
  -> job
```

Zapamietaj ten lancuch.

<!-- end_slide -->

# Problem bez tej lekcji

Bez tego latwo pomieszac:

- kod,
- compute,
- storage,
- checkpoint,
- scheduler.

I wtedy myslec, ze Databricks to tylko "notebook w chmurze".

<!-- end_slide -->

# Compute first

Pierwsze pytanie nie brzmi:

```text
Jakie query napisze?
```

Pierwsze pytanie brzmi:

```text
Na czym ten kod sie wykona?
```

<!-- end_slide -->

# Notebook role

Notebook sluzy do:

- developmentu,
- exploracji,
- pierwszego ETL walkthrough,
- debugowania.

Notebook sam z siebie nie jest jeszcze operacyjnym pipeline.

<!-- end_slide -->

# Delta output

Outputem nie jest tylko DataFrame na ekranie.
Outputem jest tabela Delta.

To znaczy:

```text
wynik zyje po zakonczeniu notebooka
```

<!-- end_slide -->

# Auto Loader i checkpoint

Tutorial Databricks pokazuje:

```text
new files -> Auto Loader -> checkpoint -> Delta
```

Checkpoint odpowiada na pytanie:

```text
Co juz przetworzylem?
```

<!-- end_slide -->

# Job

Job daje:

- schedule,
- retries,
- monitoring,
- history runow,
- ownership.

Czyli:

```text
job > manual Run notebook
```

<!-- end_slide -->

# Development vs production

```text
manual notebook run = development
scheduled notebook task = operacyjny pipeline
```

To jest granica, ktora musisz umiec nazwac.

<!-- end_slide -->

# Co jest developerskie, a co platformowe

Developerskie:

- Spark transformations,
- schema,
- data logic.

Platformowe:

- compute,
- access,
- storage binding,
- jobs,
- monitoring.

<!-- end_slide -->

# Tutorial anchor

Glowny tutorial:

1. Databricks tutorial: Build an ETL pipeline with Apache Spark on the Databricks platform
   https://docs.databricks.com/aws/en/getting-started/etl-quick-start

<!-- end_slide -->

# Co oddajesz po lekcji

```text
homework/lesson_13b/
  01_workflow_map.md
  02_notebook_to_job.md
  03_delta_checkpoint_notes.md
  04_tutorial_walkthrough.md
  05_interview_answers.md
```

<!-- end_slide -->

# Closing check

Powiedz na glos:

```text
Spark w Databricks to workflow:
compute, notebook, Delta output, checkpoint i job.
```
