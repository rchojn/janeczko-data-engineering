# Teoria: Lekcja 13b - Spark na Databricks

Ten plik ma zrobic most miedzy lokalnym PySpark a uruchomieniem w Databricks.
Nie chodzi o zapamietanie przyciskow w UI.
Chodzi o zrozumienie, jak Spark code staje sie produkcyjnym runem w workspace.

Minimum tej lekcji:

```text
1. Rozumiem compute resource.
2. Rozumiem notebook jako miejsce developmentu.
3. Rozumiem Delta table jako output ETL.
4. Rozumiem job jako sposob uruchamiania pipeline.
5. Rozumiem gdzie pojawia sie Auto Loader i checkpoint.
```

## 1. ELI5

Lokalnie uruchamiasz `python script.py`.
W Databricks zwykle pracujesz inaczej:

```text
workspace -> notebook -> compute -> table -> job
```

To jest ta sama logika danych, ale inny model operacyjny.

## 2. Najprostszy mental model

```text
Notebook = miejsce pisania i testowania logiki
Compute  = gdzie kod sie wykonuje
Delta    = gdzie wynik zyje jako tabela
Job      = jak odpalasz to regularnie
```

To rozdziela development od execution.

## 3. Compute resource

Pierwszy krok w Databricks to nie kod.
Pierwszy krok to compute.

Pytanie praktyczne:

```text
Na czym notebook ma sie wykonac?
```

Mozliwe odpowiedzi:

- all-purpose compute do developmentu,
- serverless compute, jesli workspace to wspiera,
- job compute do runow produkcyjnych.

## 4. Notebook workflow

Notebook jest dobry do:

- exploracji,
- developmentu,
- pierwszego ETL walkthrough,
- szybkiego debugowania.

Notebook nie powinien byc koncowym miejscem calej wiedzy o pipeline.
Docelowo chcesz:

```text
czytelna logika,
powtarzalny run,
wersjonowanie,
job schedule.
```

## 5. Delta jako output

W tej lekcji outputem nie jest tylko DataFrame pokazany na ekranie.
Outputem jest tabela Delta.

To jest wazne, bo produkcyjny pipeline odpowiada za:

- trwały zapis,
- czytelny format,
- ponowne odczytanie,
- dalsze wykorzystanie przez inne joby.

## 6. Auto Loader i ingest

Oficjalny tutorial pokazuje Auto Loader.
To jest mechanizm incremental ingestion dla nowych plikow.

Wzorzec mentalny:

```text
new files -> stream-like ingest -> checkpoint -> Delta table
```

Masz zapamietac nie tylko komende, ale role checkpointu:

```text
checkpoint = pamięć postępu pipeline
```

## 7. Checkpoint

Checkpoint odpowiada na pytanie:

```text
Co juz przetworzylem?
```

Bez checkpointu incremental ingest moze:

- przetwarzac te same dane drugi raz,
- nie wiedziec od czego wznowic run,
- dawac niestabilny wynik po awarii.

## 8. Job zamiast manualnego Run

Notebook uruchamiany recznie to development.
Job to poczatek produkcji.

Job dodaje:

- schedule,
- retry,
- status runu,
- historii uruchomien,
- ownera i monitoring.

## 9. Co jest developerskie, a co platformowe

Developerskie:

- transformacje Spark,
- select/filter/join/write,
- schema i logika danych.

Platformowe:

- compute,
- permissions,
- job schedule,
- access do storage,
- secret management.

To wazne rozroznienie. W przeciwnym razie myslisz, ze wszystko jest "po prostu notebookiem".

## 10. Typowy production flow

```text
1. tworzysz compute
2. piszesz notebook
3. czytasz dane
4. zapisujesz Delta table
5. sprawdzasz wynik
6. zamieniasz notebook w job
7. monitorujesz runy
```

## 11. Najczestsze bledy

1. Mieszanie exploratory notebooka z docelowym pipeline.
2. Brak rozroznienia compute dev vs job.
3. Traktowanie checkpointu jak opcjonalnego dodatku.
4. Brak odpowiedzi, gdzie żyje output: DataFrame czy Delta table.
5. Myslenie, ze klikniecie Run oznacza "mam produkcje".

## 12. Closing check

Powiedz na glos:

```text
Spark w Databricks to nie tylko kod.
To workflow: compute, notebook, Delta table, checkpoint i job.
```

Jesli umiesz pokazac ten przeplyw na prostym ETL, lekcja jest zaliczona.
