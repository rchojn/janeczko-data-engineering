# Pytania na lekcji: Lekcja 13b - Spark na Databricks

Ten plik sluzy do rozmowy na zywo.
Mentor nie musi przejsc przez wszystkie pytania.

## Pytania startowe

1. Co nowego dodaje Databricks do lokalnego Spark workflow?
   Odpowiedz: compute lifecycle, notebook workflow, Delta tables jako zarzadzany output i jobs jako repeatable execution.

2. Dlaczego ta lekcja jest osobna od Databricks Platform?
   Odpowiedz: Bo tutaj uczymy sie podstawowego runu Spark na Databricks. Governance i Unity Catalog sa nastepnym poziomem.

## Workflow

1. Co jest pierwszym krokiem: notebook czy compute?
   Odpowiedz: compute, bo bez zasobu wykonawczego notebook nie uruchomi kodu.

2. Co odroznia DataFrame pokazany w notebooku od Delta table?
   Odpowiedz: DataFrame to obiekt w runtime, a Delta table to trwaly output pipeline.

3. Po co job, skoro notebook juz dziala?
   Odpowiedz: job daje repeatability, harmonogram, retries i monitoring.

## Incremental ingest

1. Po co jest checkpoint?
   Odpowiedz: zeby pipeline wiedzial, co juz przetworzyl.

2. Co moze pojsc zle bez checkpointu?
   Odpowiedz: duplicate processing albo brak wznowienia po awarii.

## Closing check

1. Jak jednym zdaniem opiszesz workflow tej lekcji?
   Odpowiedz: Databricks zamienia lokalny Spark kod w kontrolowany workflow: compute, notebook, Delta output i job.
