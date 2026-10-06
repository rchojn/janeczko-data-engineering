# Airflow Project Lab

Minimalny lokalny Airflow do lekcji 13.

## Wymagania

- Docker Desktop,
- Docker Compose v2,
- wolny port `8080`,
- minimum ok. 4 GB RAM dostepne dla Docker Desktop, wygodniej 8 GB.

## Start

```bash
docker compose up -d
```

`airflow-init` uruchamia sie jako jednorazowy krok inicjalizacji. Jesli widzisz, ze ten kontener zakonczyl prace, to jest poprawne.

UI:

```text
http://localhost:8080
```

Login i haslo:

```text
airflow / airflow
```

## Pliki

```text
dags/ecommerce_modern_stack_pipeline.py
include/pipeline_config.py
docker-compose.yml
```

## Najwazniejsze Komendy

```bash
docker compose ps
docker compose logs airflow-init
docker compose logs airflow-scheduler
docker compose logs airflow-webserver
docker compose down
docker compose down --volumes --remove-orphans
```

## Typowe Problemy

Jesli UI nie otwiera sie na `http://localhost:8080`, sprawdz:

```bash
docker compose ps
docker compose logs airflow-init
docker compose logs airflow-webserver
docker compose logs airflow-scheduler
```

Jesli port `8080` jest zajety, zmien mapowanie w `docker-compose.yml`, np.:

```yaml
ports:
  - "8081:8080"
```

Wtedy UI bedzie dostepne pod:

```text
http://localhost:8081
```

## Uwaga

To jest setup edukacyjny. Nie jest przeznaczony do produkcji.
