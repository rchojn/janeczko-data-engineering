# Dla uczestnika: Lekcja 13b - Spark na Databricks

## Otworz i zrob to

1. Przejdz [slides.presenterm.md](slides.presenterm.md) jako glowny deck tej lekcji.
2. Przeczytaj [teoria.md](teoria.md), zeby zrozumiec mapowanie: notebook -> compute -> Delta -> job.
3. Zrob lab z [lab/databricks_spark_flow.md](lab/databricks_spark_flow.md).
4. Jesli masz workspace Databricks, przejdz oficjalny tutorial.
5. Finalna prace zapisz wedlug [homework.md](homework.md).

Najkrotsza zasada folderow:

```text
student/lab/        = przejscie przez flow notebook -> table -> job
homework/lesson_13b/ = finalne artefakty do review
```

Ta lekcja siedzi pomiedzy Spark Internals a Databricks Platform.
Najpierw rozumiesz koszt wykonania Spark joba.
Potem uczysz sie, jak ten job uruchamia sie w Databricks.
Dopiero potem wchodzisz glebiej w governance i platforme.

## Cel lekcji

Po tej lekcji masz umiec powiedziec:

- jak wyglada podstawowy workflow Spark w Databricks,
- czym rozni sie lokalny PySpark script od notebook + compute + job,
- jak dziala tabela Delta jako output ETL,
- jak przejsc od interaktywnego notebooka do zaplanowanego joba,
- jakie decyzje sa developerskie, a jakie platformowe.

## Dwa tryby pracy

Jesli masz Databricks workspace:

1. Idz oficjalnym tutorialem Databricks ETL quick start.
2. Zrob notebook, table i job.
3. Zapisz obserwacje do homeworku.

Jesli nie masz workspace:

1. Przejdz lokalna symulacje i flow w [lab/](lab/).
2. Narysuj architekture uruchomienia.
3. Odpowiedz na pytania operacyjne w homeworkie.

## Jak uruchomic

Najpierw zrozum flow logiczne, a dopiero potem platformowe:

```bash
# lokalna symulacja flow
python student/lab/spark_databricks_local_sim.py
```

W praktyce chcesz zobaczyć trzy warstwy:

```text
notebook / code     -> compute / cluster -> output table / job
```

Jeśli masz Databricks workspace, włącz ten sam wzorzec na platformie: notebook, job, Delta table i monitorowanie wyniku.

<!-- end_slide -->

## Dataset

Pracujesz na prostym, spójnym przypadku biznesowym:

- `orders` / `order_items`
- `customers` / `products`
- output w formacie `Delta` / `Parquet`
- finalny result w tabeli z jobem, nie w pojedynczym notebooku

Celem jest nie „napisać dobry notebook”, tylko pokazać, jak ten sam job przechodzi od eksperymentu do produkcyjnego uruchomienia na platformie.

<!-- end_slide -->

## Co oddajesz po lekcji

Oddajesz finalny katalog `homework/lesson_13b/`.

Typowy output:

```text
homework/lesson_13b/
├── databricks_flow_notes.md
├── architecture_diagram.md
├── notebook_summary.md
└── README.md
```

W praktyce ma pojawic sie:
- opis flow notebook -> job -> Delta table,
- lista decyzji platformowych,
- diagnoza, co jest compute, a co storage,
- minimalny answer na pytanie: „jak ten pipeline wygląda w Databricks”.

<!-- end_slide -->

## Oficjalny tutorial

Glowny tutorial tej lekcji:

1. Databricks tutorial: Build an ETL pipeline with Apache Spark on the Databricks platform
   https://docs.databricks.com/aws/en/getting-started/etl-quick-start

Dodatkowy kontekst:

2. Databricks getting started tutorials
   https://docs.databricks.com/en/getting-started/index.html

## Najwazniejszy kontrakt tej lekcji

Przy kazdym kroku odpowiedz:

```text
Co tu jest compute?
Co tu jest storage?
Co tu jest notebook logic?
Co tu jest job orchestration?
```

Jesli te warstwy sie mieszaja, nie rozumiesz jeszcze Databricks workflow.
