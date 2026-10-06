# Praca domowa: Lekcja 13b - Spark na Databricks

## Cel

Masz pokazac, ze rozumiesz, jak lokalna logika Spark przechodzi do workflow Databricks.
Nie chodzi o klikanie w UI na pamiec.
Chodzi o umiejetnosc nazwania warstw i decyzji operacyjnych.

## Co i gdzie robisz

```text
student/lab/
  databricks_spark_flow.md
  spark_databricks_local_sim.py

homework/lesson_13b/
  01_workflow_map.md
  02_notebook_to_job.md
  03_delta_checkpoint_notes.md
  04_tutorial_walkthrough.md
  05_interview_answers.md
```

## Krok 0: przejdz lab albo tutorial

Sciezka A: masz Databricks workspace

1. Przejdz oficjalny tutorial ETL quick start.
2. Zapisz, jak tworzysz compute.
3. Zapisz, gdzie pojawia sie notebook, Delta table i job.

Sciezka B: nie masz workspace

1. Przejdz [lab/databricks_spark_flow.md](lab/databricks_spark_flow.md).
2. Uruchom lokalna symulacje.
3. Odpowiedz na te same pytania koncepcyjne.

## Krok 1: `01_workflow_map.md`

Narysuj i opisz flow:

```text
workspace -> notebook -> compute -> Delta table -> job
```

Dla kazdego elementu dopisz:

```text
Co to jest?
Po co jest?
Co by sie stalo bez tego?
```

## Krok 2: `02_notebook_to_job.md`

Opisz roznice:

1. development notebook,
2. scheduled job,
3. all-purpose compute,
4. job compute albo serverless.

Dopisz praktyczne pytanie:

```text
Kiedy notebook przestaje byc tylko eksperymentem?
```

## Krok 3: `03_delta_checkpoint_notes.md`

Wyjasnij:

1. czym jest Delta output,
2. czym jest checkpoint,
3. dlaczego checkpoint jest potrzebny przy incremental ingest,
4. co moze pojsc zle bez checkpointu.

## Krok 4: `04_tutorial_walkthrough.md`

Na podstawie tutoriala opisz krok po kroku:

1. create compute,
2. create notebook,
3. ingest data,
4. write Delta table,
5. schedule job.

Jesli nie masz workspace, napisz jak wygladalby ten sam flow i jakie decyzje musialbys podjac w prawdziwym srodowisku.

## Krok 5: `05_interview_answers.md`

Odpowiedz na pytania:

1. Jak wyglada podstawowy workflow Spark w Databricks?
2. Co daje job ponad reczny run notebooka?
3. Po co jest checkpoint?
4. Jaka jest roznica miedzy compute a notebookiem?
5. Co sprawia, ze ETL w Databricks staje sie powtarzalny?

## Definition of done

Praca jest gotowa, gdy umiesz pokazac:

1. caly workflow od notebooka do joba,
2. role compute,
3. role Delta output,
4. role checkpointu,
5. jedna roznice miedzy lokalnym Spark a Databricks runem.
