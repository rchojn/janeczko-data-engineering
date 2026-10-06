# Lab: Airflow W Praktyce

Pracuj w:

```text
lab/airflow_project/
```

## Task 1: Uruchom Airflow

W katalogu `airflow_project` uruchom Airflow:

```bash
docker compose up -d
```

Ta komenda uruchamia `postgres`, jednorazowy krok `airflow-init`, `airflow-webserver` i `airflow-scheduler`.

Sprawdz status:

```bash
docker compose ps
```

Oczekiwane:

- `postgres` dziala,
- `airflow-webserver` dziala,
- `airflow-scheduler` dziala.

`airflow-init` moze miec status zakonczony albo nie byc widoczny jako dzialajacy kontener. To jest poprawne, bo ten kontener tylko inicjalizuje baze Airflow.

Wejdz w przegladarce:

```text
http://localhost:8080
```

Login:

```text
airflow
```

Haslo:

```text
airflow
```

## Task 2: Znajdz DAG

W Airflow UI znajdz DAG:

```text
ecommerce_modern_stack_pipeline
```

Sprawdz:

- czy DAG jest widoczny,
- czy nie ma import error,
- jakie ma tagi,
- jaki ma schedule,
- czy `catchup` jest wylaczony.

## Task 3: Uruchom DAG Manualnie

Uruchom DAG przyciskiem trigger.

Wejdz w:

- Grid View,
- Graph View,
- logs dla wybranego taska.

Odpowiedz:

1. Ktory task wystartowal pierwszy?
2. Ktore taski byly w Task Group?
3. Ile instancji dynamicznego taska powstalo dla zrodel?
4. Gdzie widac status `success`?

## Task 4: Dodaj Nowe Zrodlo Do Dynamicznych Taskow

Cel tego zadania: zobaczyc, ze Airflow moze utworzyc wiecej instancji tego samego taska na podstawie konfiguracji, bez kopiowania kodu DAG-a.

W poprzednim runie dynamiczne taski byly tworzone dla trzech zrodel:

```text
orders
order_items
customers
```

Teraz dodasz czwarte zrodlo.

Otworz plik:

```text
include/pipeline_config.py
```

Znajdz liste:

```python
DATA_SOURCES = [
    "orders",
    "order_items",
    "customers",
]
```

Dodaj do niej nowe zrodlo:

```python
"payments"
```

Po zmianie fragment listy powinien wygladac podobnie:

```python
DATA_SOURCES = [
    "orders",
    "order_items",
    "customers",
    "payments",
]
```

Poczekaj, az scheduler odswiezy DAG, albo odswiez UI. Jesli po ok. minucie nie widzisz zmiany, zrestartuj scheduler:

```bash
docker compose restart airflow-scheduler
```

Uruchom DAG ponownie.

Sprawdz:

- czy w dynamicznych taskach pojawilo sie zrodlo `payments`,
- czy liczba mapped task instances wzrosla z 3 do 4,
- czy log taska `extract_source` dla `payments` pokazuje `source=payments`,
- czy nie trzeba bylo kopiowac funkcji `extract_source` ani `validate_source`.

Odpowiedz jednym zdaniem:

```text
Dlaczego dodanie elementu do configu wystarczylo, zeby Airflow uruchomil dodatkowa instancje taska?
```

## Task 5: Symulacja Bledu i Retry

W pliku:

```text
include/pipeline_config.py
```

ustaw:

```python
SIMULATE_FAILURE_FOR = "customers"
```

Uruchom DAG.

Sprawdz:

- ktory task failuje,
- jak wyglada log bledu,
- czy Airflow probuje retry,
- jaki status widac dla taskow downstream.

Potem ustaw:

```python
SIMULATE_FAILURE_FOR = None
```

Uruchom DAG ponownie.

## Task 6: Custom Operator

Otworz:

```text
dags/ecommerce_modern_stack_pipeline.py
```

Znajdz klase:

```python
CloudJobTriggerOperator
```

Odpowiedz:

1. Jakie parametry przyjmuje operator?
2. Co zapisuje w logach?
3. Dlaczego w labie tylko symulujemy cloud job?
4. Co trzeba byloby dodac w produkcji?

## Task 7: Dodaj Cloud Task

W Task Group `transform_and_quality` dodaj nowy task:

```text
refresh_bi_dataset
```

Uzyj `CloudJobTriggerOperator`.

Wymagania:

- task ma uruchomic sie po `run_dbt_tests`,
- `job_name`: `refresh_power_bi_dataset`,
- payload ma zawierac `dataset: sales_daily`,
- po zmianie DAG ma dalej przechodzic poprawnie.

Po edycji DAG-a poczekaj, az Airflow odswiezy plik. Jesli nowy task nie pojawia sie w UI po ok. minucie, zrestartuj scheduler:

```bash
docker compose restart airflow-scheduler
```

## Task 8: Kontekst Produkcyjny

Odpowiedz:

1. Ktory task w prawdziwym projekcie moglby odpalac `dbt run`?
2. Ktory task moglby odpalac Databricks Job?
3. Gdzie powinny byc przechowywane tokeny i hasla?
4. Co powinno byc idempotentne?

## Expected Results

Po poprawnym uruchomieniu:

- DAG jest widoczny w Airflow UI,
- run konczy sie statusem `success`,
- widzisz Task Group `extract_and_validate`,
- widzisz Task Group `transform_and_quality`,
- dynamiczne taski powstaja dla kazdego zrodla z configu,
- po ustawieniu bledu widzisz `failed` i retry,
- po naprawie configu DAG znowu przechodzi.

## Sprzatanie

Po lekcji mozesz zatrzymac kontenery:

```bash
docker compose down
```

Jesli chcesz usunac lokalna baze i logi:

```bash
docker compose down --volumes --remove-orphans
```

Pelne czyszczenie usuwa lokalna baze metadanych Airflow. Po takim czyszczeniu kolejny start ponownie utworzy uzytkownika `airflow / airflow`.
