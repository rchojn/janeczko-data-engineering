# Interview Questions

## Podstawowe

### 1. Czym jest Airflow?

Airflow to orchestrator workflow. Pozwala definiowac DAG-i, taski, zaleznosci, schedule, retries i monitorowac wykonanie pipeline'u.

### 2. Czy Airflow przetwarza dane?

Nie powinien byc glownym silnikiem przetwarzania. Airflow koordynuje prace wykonywana przez inne narzedzia, np. Spark, Databricks, dbt, API albo warehouse.

### 3. Czym jest DAG?

DAG to graf taskow i zaleznosci bez cykli. Pokazuje, co ma sie wykonac i w jakiej kolejnosci.

### 4. Czym jest task?

Task to pojedynczy krok workflow, np. walidacja wejscia, uruchomienie dbt, odpalenie joba w Databricks albo wyslanie notyfikacji.

### 5. Po co sa retries?

Retries pomagaja obsluzyc chwilowe problemy, np. timeout API albo chwilowo niedostepny serwis.

### 6. Czym jest Task Group?

Task Group grupuje logicznie powiazane taski w UI, zeby DAG byl czytelniejszy.

## Poglebiajace

### 7. Czym rozni sie Airflow od Databricks Workflows?

Databricks Workflows jest natywna orkiestracja wewnatrz Databricks. Airflow jest bardziej ogolnym orchestrator, ktory moze laczyc wiele systemow: dbt, Databricks, storage, API, warehouse i notyfikacje.

### 8. Czym rozni sie dynamic DAG generation od dynamic task mapping?

Dynamic DAG generation tworzy strukture DAG-a podczas parsowania pliku, zwykle z konfiguracji. Dynamic task mapping tworzy wiele instancji taska dla danych przekazanych do taska.

### 9. Kiedy warto napisac Custom Operator?

Gdy ta sama integracja lub akcja powtarza sie w wielu DAG-ach i chcemy miec jeden dobrze przetestowany, czytelny komponent.

### 10. Dlaczego nie warto wrzucac calej transformacji do jednego taska Python?

Bo tracimy widocznosc, retry na poziomie krokow, czytelny lineage procesu i latwosc diagnozy. Lepiej rozbic proces na logiczne taski.

### 11. Co oznacza idempotency w pipeline?

Task idempotentny mozna uruchomic ponownie bez podwojenia efektow albo uszkodzenia danych.

### 12. Jak Airflow moze integrowac sie z chmura?

Przez provider packages, API, sekrety, operatory albo taski uruchamiajace zewnetrzne joby, np. dbt Cloud, Databricks Job, Azure Function albo proces w storage.
