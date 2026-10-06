# Lekcja 13: Apache Airflow i Orkiestracja

## Rola Airflow W Pipeline Danych

Airflow sluzy do orkiestracji procesow danych. Orkiestracja oznacza zarzadzanie tym:

- co ma sie uruchomic,
- w jakiej kolejnosci,
- kiedy ma sie uruchomic,
- co zrobic po bledzie,
- gdzie sprawdzic logi,
- jaki jest status calego procesu.

Airflow nie jest silnikiem obliczeniowym. Nie zastapi Spark, Databricks, dbt ani warehouse. Airflow mowi innym narzedziom, kiedy maja wykonac prace.

Przyklad:

```text
Airflow uruchamia pipeline
dbt buduje modele SQL
Databricks/Spark wykonuje ciezkie przetwarzanie
Storage trzyma dane
BI korzysta z martow
```

W praktyce Airflow jest przydatny wtedy, gdy pipeline sklada sie z wielu krokow i potrzebujesz widziec:

- ktory krok sie udal,
- ktory krok sie nie udal,
- czy task byl ponawiany,
- gdzie sa logi,
- czy downstream powinien poczekac na upstream,
- czy proces uruchamia sie zgodnie z harmonogramem.

## Airflow Vs Databricks Workflows

Airflow i Databricks Workflows moga sluzyc do orkiestracji, ale zwykle pasuja do troche innych sytuacji.

Databricks Workflows to natywna orkiestracja w Databricks. Jest bardzo wygodna, gdy pipeline dzieje sie glownie w Databricks:

- uruchamiasz notebooki,
- uruchamiasz Spark jobs,
- korzystasz z Databricks SQL,
- pracujesz na Delta Lake,
- caly proces ma zostac blisko Databricks workspace.

Airflow jest bardziej ogolnym orchestrator. Lepiej pasuje, gdy pipeline laczy wiele roznych narzedzi i systemow:

- API zewnetrzne,
- storage,
- dbt,
- Databricks Job,
- warehouse,
- narzedzie BI,
- notyfikacje,
- kilka zespolow albo kilka platform.

Praktyczna zasada:

```text
Pipeline glownie w Databricks -> Databricks Workflows moze byc prostszy.
Pipeline laczy wiele systemow -> Airflow daje wieksza elastycznosc.
```

To nie jest wybor "lepsze/gorsze". W realnych projektach mozna spotkac oba podejscia. Airflow moze nawet uruchamiac Databricks Job jako jeden z krokow wiekszego procesu.

## Airflow Vs dbt Vs Databricks

Te narzedzia moga pracowac razem, ale maja inne role.

```text
Airflow = orchestrator procesu
dbt = projekt transformacji SQL
Databricks/Spark = compute i przetwarzanie danych
Warehouse/lakehouse = miejsce przechowywania i wykonywania zapytan
```

Airflow moze uruchomic:

- `dbt run`,
- `dbt test`,
- Databricks Job,
- zapytanie SQL,
- request do API,
- notyfikacje po sukcesie albo bledzie.

Najwazniejsze: Airflow koordynuje, ale nie powinien byc miejscem na ciezka transformacje danych.

## DAG

DAG to Directed Acyclic Graph, czyli skierowany graf zaleznosci bez cykli.

W praktyce:

```text
extract_orders -> validate_orders -> run_dbt_models -> publish_data
```

Airflow uzywa DAG-a, zeby wiedziec, ktore taski moga wystartowac, a ktore musza poczekac na upstream.

Dlaczego DAG nie moze miec cyklu?

```text
A czeka na B
B czeka na A
```

Taki proces nie ma jednoznacznego konca ani poprawnej kolejnosci wykonania.

## Task

Task to pojedynczy krok w pipeline.

Dobry task powinien miec jasna odpowiedzialnosc, np.:

- pobierz plik,
- sprawdz czy tabela istnieje,
- zwaliduj dane wejsciowe,
- uruchom dbt run,
- uruchom Databricks Job,
- wyslij notyfikacje.

Antywzorzec:

```text
run_everything()
```

Jesli caly pipeline jest jednym taskiem, Airflow nie pomaga w diagnostyce. W UI widzisz tylko jeden duzy krok i jeden duzy log.

## Dependency

Dependency okresla kolejnosc taskow.

```python
extract >> validate >> transform
```

To znaczy:

- `validate` czeka na `extract`,
- `transform` czeka na `validate`,
- jesli upstream failuje, downstream zwykle nie powinien startowac.

Dependency to nie tylko zapis techniczny. To decyzja procesowa: nie publikujemy danych, jesli testy jakosci nie przeszly.

## Schedule I Catchup

Schedule mowi, kiedy DAG ma byc uruchamiany, np. codziennie, co godzine albo tylko manualnie.

Przyklad:

```python
schedule="@daily"
```

W produkcji schedule powinien wynikac z potrzeb biznesowych i dostepnosci danych upstream. Jesli pliki z systemu zrodlowego pojawiaja sie o 02:00, pipeline uruchamiany o 01:00 bedzie generowal falszywe awarie.

Catchup oznacza nadrabianie historycznych uruchomien od `start_date`.

W labie zwykle chcemy:

```python
catchup=False
```

Dzieki temu lokalny Airflow nie probuje uruchamiac wielu zaleglych runow po starcie.

## Retries I Idempotency

Retry to ponowienie taska po bledzie.

Retries pomagaja przy chwilowych problemach:

- timeout API,
- chwilowy blad sieci,
- opoznienie pliku w storage,
- temporary warehouse issue.

Retry nie naprawia bledow logicznych w kodzie.

Przyklad:

```text
API timeout -> retry moze pomoc
zla nazwa kolumny w SQL -> retry raczej nie pomoze
```

Retry ma sens tylko wtedy, gdy task jest bezpieczny do ponownego uruchomienia. To nazywamy idempotency.

Task idempotentny mozna uruchomic kilka razy bez podwojenia efektu albo uszkodzenia danych.

Przyklad:

```text
overwrite partition date=2026-08-14 -> zwykle bezpieczniejsze
append tych samych rekordow bez kontroli -> ryzyko duplikatow
```

## Task State

W Airflow UI task moze miec status, np.:

- `success`,
- `failed`,
- `queued`,
- `running`,
- `skipped`,
- `upstream_failed`.

Status pomaga szybko zobaczyc, gdzie pipeline sie zatrzymal.

Przyklad:

```text
validate_orders = failed
run_dbt_models = upstream_failed
```

To oznacza, ze transformacje nie ruszyly, bo walidacja upstream nie przeszla.

## Logs

Logi taska to pierwsze miejsce diagnostyki.

W logach szukasz:

- parametrow uruchomienia,
- komunikatu bledu,
- stack trace,
- informacji, czy task wykonal oczekiwany krok,
- identyfikatora zewnetrznego joba, np. Databricks run id albo cloud run id.

W realnej pracy samo stwierdzenie "DAG failuje" nie wystarcza. Trzeba umiec powiedziec, ktory task failuje i dlaczego.

## Grid View I Graph View

Grid View pomaga analizowac runy w czasie:

- ktory run sie udal,
- ktory run failowal,
- ile trwal task,
- czy problem powtarza sie codziennie.

Graph View pomaga zrozumiec zaleznosci:

- co jest upstream,
- co jest downstream,
- ktore taski sa w Task Group,
- gdzie zatrzymal sie przeplyw.

Na zajeciach uzywamy obu widokow, bo Data Engineer musi umiec diagnozowac pipeline z UI, a nie tylko pisac kod DAG-a.

## Task Group

Task Group grupuje logicznie powiazane taski w UI.

Przyklad:

```text
extract_and_validate
├── extract_source[orders]
├── extract_source[customers]
└── validate_source[...]
```

Task Group nie jest osobnym procesem. To sposob organizacji grafu, zeby DAG byl czytelny.

Task Group jest szczegolnie przydatny, gdy DAG ma wiele taskow i bez grupowania UI zaczyna byc trudne do czytania.

## Dynamiczne DAGi I Dynamiczne Taski

W praktyce czesto chcesz uniknac kopiowania prawie takiego samego taska dla wielu zrodel.

Przyklad:

```text
orders
order_items
customers
```

Zamiast pisac trzy prawie identyczne taski, mozna wygenerowac taski z listy konfiguracji.

Wazna roznica:

- dynamic DAG generation: struktura DAG-a powstaje z konfiguracji podczas parsowania pliku,
- dynamic task mapping: Airflow tworzy wiele instancji taska dla listy danych.

Przyklad dynamic task mapping:

```python
extract_source.expand(source_name=sorted(DATA_SOURCES))
```

Wazna praktyka: kolejnosc generowania taskow powinna byc stabilna. Dlatego czesto uzywamy `sorted(...)`.

## Custom Operator

Operator opisuje, jaki typ pracy wykonuje task.

Custom Operator tworzymy, gdy w projekcie powtarza sie specyficzna akcja, np.:

- uruchomienie firmowego API,
- odpalenie Databricks Job,
- publikacja danych do narzedzia BI,
- sprawdzenie kontraktu danych.

Dobry Custom Operator ukrywa techniczne detale integracji, ale nie powinien ukrywac calej logiki biznesowej.

Przyklad:

```text
TriggerDatabricksJobOperator
```

Taki operator moglby:

- zbudowac request do API,
- uzyc Airflow Connection,
- przekazac parametry,
- poczekac na status,
- zapisac run id w logach.

## Integracja Z Chmura

Airflow czesto integruje sie z chmura przez:

- provider packages,
- API,
- credentials/secrets,
- operators dla konkretnych uslug,
- taski uruchamiajace dbt, Databricks Jobs albo cloud functions.

W tej lekcji uzywamy mock operatora, ktory symuluje cloud job. Chodzi o wzorzec, nie o prawdziwe sekrety.

W realnym projekcie Azure/Databricks proces moglby wygladac tak:

```text
Airflow DAG
-> check files in ADLS
-> trigger Databricks Job
-> run dbt models
-> run data quality checks
-> refresh BI dataset
-> send notification
```

Sekrety nie powinny byc wpisane w kod DAG-a. Produkcyjnie uzywa sie np. Airflow Connections, secrets backend albo Azure Key Vault.

## Co Zapamietac

- Airflow koordynuje proces, ale nie jest compute engine.
- Databricks Workflows jest wygodne, gdy pipeline zyje glownie w Databricks.
- Airflow jest mocny, gdy proces laczy wiele systemow.
- DAG opisuje taski i zaleznosci bez cykli.
- Dobry task ma jedna odpowiedzialnosc.
- Retry wymaga myslenia o idempotency.
- Grid View, Graph View i logs sa podstawowymi narzedziami diagnostyki.
- Task Group poprawia czytelnosc DAG-a.
- Dynamic task mapping pomaga unikac kopiowania podobnych taskow.
- Custom Operator ma sens dla powtarzalnych integracji.
- Sekrety powinny byc poza kodem DAG-a.
