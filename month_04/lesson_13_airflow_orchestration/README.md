# Lekcja 13: Apache Airflow i Orkiestracja

W tej lekcji zobaczysz Airflow w praktyce. Celem nie jest poznanie calego Airflow, tylko zrozumienie, jak Data Engineer uklada proces danych jako DAG: z taskami, zaleznosciami, harmonogramem, logami i retry.

## Po Lekcji Potrafisz

- wyjasnic, czym Airflow rozni sie od Spark, Databricks i dbt,
- opisac DAG, task, dependency, schedule, retry i task state,
- uruchomic DAG w Airflow UI,
- wejsc w Graph/Grid View i logi taska,
- rozpoznac Task Group,
- wyjasnic, czym sa dynamiczne taski,
- opisac, po co tworzy sie Custom Operator,
- powiedziec, jak Airflow integruje sie z chmura, dbt albo Databricks.

## Praca Na Zajeciach

1. Wykonaj `lab/airflow_warmup.md`.
2. Uruchom lokalny projekt z `lab/airflow_project/`.
3. Przejdz przez `lab/airflow_live_coding.md`.
4. Zobacz DAG w Airflow UI.
5. Uruchom pipeline, sprawdz task states i logi.
6. Zmien konfiguracje pipeline'u i zobacz, jak zmienia sie liczba dynamicznych taskow.

## Setup Przed Lekcja

Do czesci praktycznej potrzebujesz Docker Desktop i Docker Compose. Pelny opis przygotowania srodowiska jest tutaj:

```text
setup.md
```

## Wazne

Do praktyki uzywamy Docker Compose, bo Airflow sklada sie z kilku procesow: webservera, schedulera i metadata database. Docker nie jest tematem lekcji, tylko sposobem na stabilne lokalne srodowisko.

Ten setup jest edukacyjny. Produkcyjny Airflow wymaga osobnej konfiguracji security, deploymentu, monitoringu i zarzadzania sekretami.
