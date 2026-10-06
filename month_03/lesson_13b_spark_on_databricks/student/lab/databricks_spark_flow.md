# Lab: Spark na Databricks - workflow walkthrough

## Cel

Masz przejsc flow:

```text
compute -> notebook -> ingest -> Delta -> job
```

Nie chodzi o pamiec klikniec.
Chodzi o nazwanie warstw i decyzji.

## Sciezka A: masz Databricks workspace

Przejdz tutorial:

https://docs.databricks.com/aws/en/getting-started/etl-quick-start

Podczas pracy zapisz:

1. Jaki compute tworzysz?
2. Co jest inputem?
3. Gdzie zapisujesz Delta table?
4. Gdzie jest checkpoint?
5. Jak zamieniasz notebook w job?

## Sciezka B: nie masz Databricks workspace

Przejdz przez ten sam flow koncepcyjnie:

1. compute = klaster / serverless resource,
2. notebook = miejsce developmentu,
3. ingest = wczytanie danych,
4. Delta = trwaly output,
5. job = scheduler i run history.

## Checkpointy

Po kazdym kroku odpowiedz:

```text
Co tu zyje tylko w runtime?
Co tu zostaje po runie?
Co jest konfiguracja platformy, a co logika danych?
```
