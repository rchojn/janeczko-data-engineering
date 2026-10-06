# Homework

## Cel

Rozbuduj DAG z lekcji tak, jakby byl czescia realnego pipeline'u danych. Chodzi o czytelnosc procesu, dobra strukture taskow i umiejetnosc wyjasnienia decyzji.

## Minimum

### 1. Dodaj Nowe Zrodlo

W pliku:

```text
lab/airflow_project/include/pipeline_config.py
```

dodaj nowe zrodlo, ktore nie bylo dodawane na zajeciach:

```text
shipments
```

Sprawdz w Airflow UI, czy przy kolejnym runie pojawia sie dodatkowa instancja dynamicznego taska.

### 2. Dodaj Task Publikacji

W DAG-u dodaj task lub operator, ktory symuluje publikacje wyniku:

```text
publish_sales_mart
```

Task powinien uruchomic sie po testach danych.

### 3. Dodaj Logi Diagnostyczne

W nowym tasku zaloguj:

- nazwe publikowanego modelu,
- docelowe srodowisko,
- `run_id` z Airflow context.

### 4. Opisz Decyzje

Dodaj krotka notatke:

```text
homework_notes.md
```

Odpowiedz:

- dlaczego `shipments` jest osobnym zrodlem,
- dlaczego publikacja jest osobnym taskiem,
- co powinno byc idempotentne w tym pipeline,
- gdzie w produkcji bylyby sekrety,
- czym sa `Airflow Connections` i `Airflow Variables` oraz gdzie uzyto by ich w tym pipeline.

## Rozszerzenie

Dodaj Task Group:

```text
quality_gate
```

W srodku umiesc:

- task sprawdzajacy wynik `dbt test`,
- task decydujacy, czy mozna publikowac dane.

Nie musi to byc prawdziwe polaczenie z dbt. Wystarczy sensowna symulacja i czytelne logi.

## Kryteria Oddania

Oddaj:

- zmodyfikowany DAG,
- zmieniony config z nowym zrodlem,
- screenshot albo opis z Airflow UI,
- notatke `homework_notes.md`,
- krotka odpowiedz: czym Airflow rozni sie od narzedzia transformacyjnego.

Rozwiazanie jest poprawne, jesli DAG uruchamia sie bez bledow, nowe zrodlo tworzy dodatkowa dynamiczna instancje taska, publikacja jest osobnym krokiem, a opis pokazuje myslenie o utrzymywalnym pipeline i bezpiecznym zarzadzaniu konfiguracja.
