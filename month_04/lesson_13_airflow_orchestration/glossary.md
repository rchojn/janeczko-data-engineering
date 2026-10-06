# Glossary

## Apache Airflow

Narzędzie do orkiestracji workflow. Definiuje, kiedy i w jakiej kolejnosci uruchamiac taski.

## Orchestrator

Warstwa zarzadzajaca procesem. Orchestrator nie musi wykonywac ciezkich obliczen, tylko koordynuje narzedzia.

## DAG

Directed Acyclic Graph. Graf taskow i zaleznosci bez cykli.

## Task

Pojedynczy krok w DAG-u.

## Operator

Szablon wykonania taska, np. Python task, Bash task albo custom operator.

## Custom Operator

Operator napisany pod potrzeby projektu lub organizacji.

## Dependency

Zaleznosc miedzy taskami, np. `extract >> validate`.

## Schedule

Harmonogram uruchamiania DAG-a.

## Catchup

Mechanizm nadrabiania zaleglych uruchomien dla poprzednich dat.

## Retry

Ponowienie taska po bledzie.

## Task State

Status taska w Airflow, np. `success`, `failed`, `running`, `queued`.

## Task Group

Logiczne grupowanie taskow w DAG-u.

## Dynamic Task Mapping

Mechanizm tworzenia wielu instancji taska na podstawie listy danych.

## Dynamic DAG Generation

Generowanie struktury DAG-a na podstawie konfiguracji podczas parsowania pliku DAG.

## Metadata Database

Baza, w ktorej Airflow trzyma informacje o DAG-ach, runach, taskach i statusach.

## Scheduler

Proces Airflow, ktory decyduje, ktore taski powinny zostac uruchomione.

## Webserver

Proces udostepniajacy Airflow UI.
