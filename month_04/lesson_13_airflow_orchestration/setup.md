# Setup: Airflow i Docker Compose

Ten plik pomaga przygotowac lokalne srodowisko do lekcji 13.

Po setupie powinienes umiec:

- uruchomic lokalne Airflow przez Docker Compose,
- zalogowac sie do Airflow UI,
- znalezc DAG z lekcji,
- uruchomic DAG manualnie,
- sprawdzic task states, Graph View, Grid View i logi,
- zatrzymac kontenery po lekcji.

Do tej lekcji nie potrzebujesz Azure ani Databricks. Airflow uruchamiamy lokalnie w kontenerach.

## 1. Dlaczego Docker

Airflow sklada sie z kilku elementow:

- webservera,
- schedulera,
- metadata database,
- katalogu z DAG-ami,
- logow taskow.

W tej lekcji uzywamy Docker Compose, zeby uruchomic te elementy jako gotowe lokalne srodowisko. Dzieki temu mozesz skupic sie na Airflow UI, DAG-ach, taskach i logach.

## 2. Zainstaluj Docker Desktop

Pobierz Docker Desktop:

```text
https://www.docker.com/products/docker-desktop/
```

Po instalacji uruchom Docker Desktop i poczekaj, az bedzie gotowy.

Sprawdz w terminalu:

```bash
docker --version
docker compose version
```

Oczekiwany rezultat:

- widzisz wersje Docker,
- widzisz wersje Docker Compose,
- komendy nie zwracaja bledu.

## 3. Otworz Katalog Lekcji

Otworz terminal w katalogu lekcji, czyli tam, gdzie widzisz:

```text
README.md
student_notes.md
setup.md
lab/
```

Nie zakladamy jednej konkretnej sciezki na komputerze, bo materialy moga byc pobrane do dowolnego katalogu.

Jesli nie wiesz, gdzie jestes, sprawdz:

macOS / Linux:

```bash
pwd
ls
```

Windows PowerShell:

```powershell
pwd
dir
```

Jesli widzisz `README.md`, `student_notes.md`, `setup.md` oraz katalog `lab`, jestes w dobrym miejscu.

## 4. Uruchom Airflow

Przejdz do projektu Airflow:

```bash
cd lab/airflow_project
```

W dobrym katalogu powinienes widziec:

```text
docker-compose.yml
dags/
include/
```

Uruchom Airflow:

```bash
docker compose up -d
```

Ta komenda uruchamia wszystkie potrzebne elementy:

- `postgres` jako metadata database,
- `airflow-init` jako jednorazowy krok inicjalizacji,
- `airflow-webserver` jako UI,
- `airflow-scheduler` jako proces planujacy taski.

`airflow-init` przygotowuje baze metadanych i uzytkownika `airflow / airflow`. To kontener pomocniczy. Po zakonczeniu moze miec status `Exited (0)` albo nie byc widoczny jako dzialajacy kontener. To jest poprawne.

Jesli uruchamiasz srodowisko kolejny raz i w logach widzisz komunikat podobny do:

```text
Airflow admin user already exists - continuing
```

to nie jest blad. Oznacza tylko, ze lokalna baza Airflow juz ma utworzonego uzytkownika.

Sprawdz status:

```bash
docker compose ps
```

Oczekiwany rezultat:

- `postgres` dziala,
- `airflow-webserver` dziala,
- `airflow-scheduler` dziala.

Pierwsze uruchomienie moze potrwac kilka minut, bo Docker pobiera obrazy.

## 5. Zaloguj Sie Do Airflow UI

Otworz:

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

Znajdz DAG:

```text
ecommerce_modern_stack_pipeline
```

Oczekiwany rezultat:

- DAG jest widoczny,
- nie ma import error,
- widzisz tagi DAG-a,
- mozesz wejsc w Grid View i Graph View.

## 6. Uruchom Testowy DAG

W Airflow UI:

1. Otworz DAG `ecommerce_modern_stack_pipeline`.
2. Kliknij trigger/manual run.
3. Wejdz w `Grid View`.
4. Poczekaj, az taski sie wykonaja.
5. Wejdz w log wybranego taska.

Oczekiwany rezultat:

- DAG run konczy sie statusem `success`,
- widzisz Task Group `extract_and_validate`,
- widzisz Task Group `transform_and_quality`,
- taski maja status `success`,
- logi pokazuja komunikaty z symulowanych krokow pipeline'u.

## 7. Jesli Port 8080 Jest Zajety

Port `8080` moze byc zajety przez inne narzedzie, np. dbt docs albo lokalna aplikacje.

Jesli masz uruchomione `dbt docs serve`, zatrzymaj je:

```text
Ctrl + C
```

Jesli problem nadal wystepuje, w pliku:

```text
lab/airflow_project/docker-compose.yml
```

zmien mapowanie portu:

```yaml
- "8080:8080"
```

na:

```yaml
- "8081:8080"
```

Uruchom ponownie:

```bash
docker compose up -d
```

Otworz:

```text
http://localhost:8081
```

## 8. Przydatne Komendy

Status kontenerow:

```bash
docker compose ps
```

Logi webservera:

```bash
docker compose logs airflow-webserver
```

Logi schedulera:

```bash
docker compose logs airflow-scheduler
```

Zatrzymanie kontenerow:

```bash
docker compose down
```

Pelne czyszczenie kontenerow, wolumenow i osieroconych zasobow:

```bash
docker compose down --volumes --remove-orphans
```

Pelne czyszczenie przydaje sie, gdy Airflow pamieta stare DAG runy albo chcesz zaczac od zera.

## 9. Readiness Check

Przed lekcja sprawdz:

- [ ] Docker Desktop jest zainstalowany i uruchomiony.
- [ ] `docker --version` dziala.
- [ ] `docker compose version` dziala.
- [ ] `docker compose up -d` uruchamia Airflow.
- [ ] Airflow UI otwiera sie w przegladarce.
- [ ] Potrafie zalogowac sie jako `airflow / airflow`.
- [ ] Widze DAG `ecommerce_modern_stack_pipeline`.
- [ ] DAG nie ma import error.

## 10. Typowe Problemy

### `docker compose` Nie Dziala

Sprawdz:

- czy Docker Desktop jest uruchomiony,
- czy komenda `docker --version` dziala,
- czy system nie wymaga restartu po instalacji Docker Desktop.

### Airflow UI Nie Otwiera Sie

Sprawdz:

```bash
docker compose ps
docker compose logs airflow-init
docker compose logs airflow-webserver
docker compose logs airflow-scheduler
```

Jesli port `8080` jest zajety, zmien mapowanie na `8081:8080`.

### `airflow-init` Pokazuje, Ze Uzytkownik Juz Istnieje

Komunikat podobny do:

```text
Airflow admin user already exists - continuing
```

jest poprawny przy ponownym uruchomieniu srodowiska. Airflow uzywa lokalnej metadata database. Jesli baza nie zostala usunieta przez `docker compose down --volumes --remove-orphans`, uzytkownik `airflow` moze juz istniec.

Wazne jest to, czy po starcie dzialaja:

```bash
docker compose ps
```

Oczekuj:

- `postgres` dziala,
- `airflow-webserver` dziala,
- `airflow-scheduler` dziala.

`airflow-init` nie musi dzialac caly czas. To jednorazowy krok inicjalizacji.

### Airflow Pokazuje Import Error

Sprawdz:

- czy plik DAG znajduje sie w katalogu `dags/`,
- czy plik `include/pipeline_config.py` istnieje,
- czy w kodzie Python nie ma literowki,
- logi schedulera:

```bash
docker compose logs airflow-scheduler
```

## 11. Co Wyslac Mentorowi

Wystarczy krotka wiadomosc:

```text
Lesson 13 setup: ukonczony
Docker Compose: OK
Airflow UI: dziala
DAG ecommerce_modern_stack_pipeline: widoczny
Problemy: brak / opis problemu
```

Nie wysylaj hasel, tokenow, pelnych logow z prywatnymi danymi ani screenshotow zawierajacych wrazliwe informacje.
