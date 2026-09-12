# Teoria: Lekcja 07 - Data contracts, schema drift i reject policy

## Cel materialu

W lekcji 06 zbudowales maly pipeline. W lekcji 07 dokladasz warstwe odpowiedzialna za wiarygodnosc danych.

Najkrotsza wersja celu:

```text
Nie wystarczy, ze pipeline "dziala".
Pipeline ma dzialac poprawnie nawet wtedy, gdy producer zmienia payload.
```

Po tej lekcji uczestnik powinien umiec:

```text
zdefiniowac data contract dla payloadu,
wdrozyc walidacje na granicy pipeline'u,
rozroznic dataclass i Pydantic w praktyce,
zaprojektowac accepted/rejected flow,
zrozumiec i testowac schema drift,
wytlumaczyc contract versioning i reject policy,
powiazac contracty z metrykami data quality.
```

## Kontekst ekosystemu

> Czytaj to pierwsze.

W realnych systemach danych najwieksze awarie czesto nie wynikaja z kodu transformacji, tylko z cichych zmian na wejsciu.

Typowe sytuacje:

```text
API zwraca nowe pole i usuwa stare bez uprzedzenia,
kolumna numeric staje sie stringiem z waluta,
status dostaje nowa wartosc, ktorej raport nie rozumie,
null-e zaczynaja pojawiac sie w polu, ktore bylo "zawsze wypelnione".
```

Jesli pipeline nie ma twardego kontraktu, takie zmiany trafiaja do metryk i dashboardow jako "poprawne" dane. Efekt: liczby sa ladne, ale nieprawdziwe.

## ELI5

Data contract to umowa miedzy producerem i consumerem danych:

```text
Tak powinien wygladac rekord.
Jesli rekord tak nie wyglada, nie licz go do metryki.
```

Pipeline z kontraktem dziala tak:

```text
raw payload -> validate contract -> accepted / rejected -> transform accepted only
```

Najwazniejsze: bledny rekord nie znika. Zostaje zapisany z powodem odrzucenia.

## First Principles

Kazdy pipeline odpowiada na dwa odrebne pytania:

```text
1) Czy rekord ma prawo wejsc do logiki biznesowej?
2) Co policzyc na rekordach, ktore przeszly?
```

Pytanie (1) to data contract. Pytanie (2) to transformacja.

Jesli zmieszasz te odpowiedzialnosci w jednej funkcji, tracisz:

```text
przejrzystosc,
mozliwosc testowania,
wiarygodnosc metryk,
latwe debugowanie incydentow jakosci danych.
```

Dlatego profesjonalny podzial wyglada tak:

```text
Boundary layer: walidacja payloadu (Pydantic)
Domain layer: jawny rekord biznesowy (dataclass)
Business layer: metryki i agregacje na accepted records
```

## Definicje kluczowe

### Data contract

Formalny opis, jakie dane sa akceptowane:

```text
required fields,
types,
allowed values,
range constraints,
nullability,
reject policy.
```

### Schema drift

Zmiana ksztaltu danych po stronie producenta.

Podstawowe klasy driftu:

```text
non-breaking: nowa opcjonalna kolumna,
potentially breaking: zmiana typu,
breaking: usuniecie wymaganego pola lub zmiana semantyki.
```

### Reject policy

Jasna decyzja, co robimy z rekordem, ktory nie spelnia kontraktu.

Minimalna polityka:

```text
reject + reason + metadata + monitoring.
```

## dict vs Pydantic vs dataclass

To nie sa zamienniki. To trzy etapy dojrzalosci rekordu.

| Reprezentacja | Gdzie | Po co | Czego nie robi |
|---|---|---|---|
| `dict` | tuz po odczycie CSV/JSON/API | przechowuje raw payload | nie gwarantuje kontraktu |
| Pydantic `BaseModel` | granica pipeline'u | waliduje shape, typy, reguly | nie jest lekkim modelem domenowym do wszystkich transformacji |
| `dataclass` | po walidacji | daje czytelny rekord biznesowy | sam z siebie nie waliduje mocno danych z zewnatrz |

Wzorzec produkcyjny:

```text
raw dict -> Pydantic -> dataclass -> transform
```

## Kontrakt przykładowy: zamowienie

```python
from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator


ALLOWED_STATUSES: set[str] = {"completed", "cancelled", "pending", "refunded"}


class OrderPayload(BaseModel):
  order_id: str = Field(min_length=1)
  status: str
  total_amount: float = Field(ge=0)
  source: str = "unknown"

  @field_validator("status")
  @classmethod
  def normalize_and_validate_status(cls, value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in ALLOWED_STATUSES:
      allowed = ", ".join(sorted(ALLOWED_STATUSES))
      raise ValueError(f"status must be one of: {allowed}")
    return normalized


@dataclass(frozen=True)
class Order:
  order_id: str
  status: str
  total_amount: float
  source: str
```

Co ten kontrakt egzekwuje:

```text
order_id musi istniec i nie moze byc pusty,
status jest normalizowany i sprawdzany w enum,
total_amount ma byc liczba >= 0,
source dostaje default unknown.
```

## Accepted / rejected flow

Walidacja to nie tylko "True/False". To decyzja operacyjna.

Minimalny model rejected rekordu:

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RejectedRecord:
  raw_record: dict[str, Any]
  reason: str
  validation_stage: str
  contract_version: str
```

Minimalny output pipeline'u powinien odpowiadac na pytania:

```text
ile rekordow przyjeto?
ile odrzucono?
dlaczego odrzucono?
czy problem dotyczy konkretnego source?
```

## Contract versioning

Kontrakt bez wersji utrudnia utrzymanie.

Prosty model:

```text
v1: order_id, status, total_amount, source
v2: +currency (required), status enum rozszerzony o disputed
```

Przy zmianie kontraktu aktualizujesz jednoczesnie:

```text
model Pydantic,
testy walidacji,
notatke changelog,
dashboard z reject reasons.
```

## Kompatybilnosc zmian

Praktyczna klasyfikacja zmian:

| Typ zmiany | Przykład | Dzialanie pipeline'u |
|---|---|---|
| backward-compatible | nowa opcjonalna kolumna | akceptuj, loguj, rozważ update modelu |
| soft-breaking | nowa wartosc enum, ale logika moze ja pominac | tymczasowo reject + alert + uzgodnienie ze zrodlem |
| hard-breaking | brak pola wymaganego, zmiana typu | fail fast na walidacji i zapis do rejected |

## Data quality KPI

Samo posiadanie pliku rejected to za malo. Potrzebujesz metryk.

Minimalny zestaw:

```text
accepted_count,
rejected_count,
reject_rate,
top_reject_reasons,
reject_rate_by_source,
contract_version_distribution.
```

Praktyczna zasada:

```text
Gdy reject_rate skacze po deployu producera, traktuj to jak incydent danych.
```

## Test strategy dla kontraktow

Testy powinny obejmowac nie tylko happy path.

Obowiazkowy zestaw:

```text
missing required field,
wrong type,
invalid enum value,
boundary values (0, negative, empty string),
schema drift simulation,
normalization behavior (" Completed " -> "completed"),
accepted/rejected counters.
```

Przyklad testu driftu:

```python
def test_missing_order_id_is_rejected() -> None:
  payload = {"status": "completed", "total_amount": "100.00"}
  result = validate_payloads([payload])

  assert result.accepted_count == 0
  assert result.rejected_count == 1
  assert "order_id" in result.rejected_records[0].reason
```

## Typowe anti-patterny

| Anti-pattern | Objaw | Lepszy wzorzec |
|---|---|---|
| Walidacja tylko w dokumentacji | kod "dziala" do pierwszej zmiany payloadu | walidacja w runtime przez Pydantic |
| Silent cast wszystkiego do str | metryki sa formalnie policzone, ale semantycznie bledne | jawna walidacja typow i zakresow |
| Mieszanie extract/validate/transform | trudny debugging i trudne testy | separacja krokow pipeline'u |
| Brak rejected storage | brak wiedzy, co i dlaczego odpadlo | rejected_records z reason i metadata |
| Retry na validation error | wielokrotne powtarzanie tego samego bledu | retry tylko dla bledow przejsciowych |

## Socratic questions

**Czy moge zostac przy samym `dict`, skoro jest szybciej napisac kod?**

Mozesz w prototypie. Ale im dluzej zyje pipeline, tym drozszy jest brak jawnego kontraktu. `dict` nie komunikuje required fields, enumow i zasad walidacji.

**Czy Pydantic zastapi testy?**

Nie. Pydantic odpowiada na pytanie: "czy pojedynczy rekord jest zgodny z kontraktem?". Testy odpowiadaja na pytanie: "czy caly workflow pipeline'u zachowuje sie poprawnie?".

**Czy dataclass i Pydantic to dublowanie pracy?**

Nie. Pydantic broni granicy wejscia. Dataclass porzadkuje model domeny po walidacji. To dwa rozne etapy cyklu zycia rekordu.

**Czy kazdy schema drift oznacza od razu migracje kontraktu?**

Nie. Najpierw klasyfikujesz drift: kompatybilny czy lamacy. Dopiero potem decydujesz: akceptacja, tymczasowy reject, albo update kontraktu.

## STALY PATTERN - zapamietaj to

```text
DATA CONTRACT + SCHEMA DRIFT HANDLING - staly pattern

=== Extract raw payload ===
raw_records: list[dict[str, object]] = read_from_source(...)
# Extract tylko pobiera dane. Nie robi logiki biznesowej.

=== Validate at boundary ===
payload = OrderPayload.model_validate(raw_record)
# Pydantic sprawdza required fields, typy, enum i zakresy.

=== Convert to domain ===
order = Order(
  order_id=payload.order_id,
  status=payload.status,
  total_amount=payload.total_amount,
  source=payload.source,
)
# Dataclass to jawny rekord dla transformacji.

=== Route accepted / rejected ===
accepted.append(order)
rejected.append(RejectedRecord(...))
# Rejected ma reason i metadata, nie znika po cichu.

=== Transform accepted only ===
metrics = calculate_metrics(accepted)
# Metryki sa liczone tylko na rekordach zgodnych z kontraktem.

=== Persist output + quality summary ===
write_accepted_jsonl(accepted)
write_rejected_jsonl(rejected)
write_quality_report(accepted_count, rejected_count, reject_reasons)
# Output zawiera nie tylko KPI biznesowe, ale tez KPI jakosci danych.

=== Evolve contract safely ===
contract_version = "v1"
# Przy zmianie kontraktu aktualizujesz model, testy i monitoring.

CHECKLIST:
[ ] Czy kontrakt jest wymuszony w kodzie, nie tylko w README?
[ ] Czy required fields i typy sa jawne?
[ ] Czy enumy i range constraints sa walidowane?
[ ] Czy accepted i rejected sa rozdzielone?
[ ] Czy rejected records maja reason + metadata?
[ ] Czy metryki biznesowe licza tylko accepted records?
[ ] Czy masz testy driftu i wartosci granicznych?
[ ] Czy zmiana kontraktu ma wersje i changelog?
```

## Minimalny standard oddania

Implementacja lekcji 07 powinna spelniac ponizsze wymagania:

```text
model Pydantic opisuje kontrakt inputu,
dataclass opisuje rekord domenowy po walidacji,
validation route rozdziela accepted i rejected,
rejected records zawieraja co najmniej raw_record i reason,
testy pokrywaja brak pola, zly typ i invalid status,
material zawiera krotkie notatki o schema drift i decyzji reakcji,
odpowiedz interview tlumaczy granice odpowiedzialnosci kontraktu.
```

## Typowy Python w praktyce DE: multithreading, multiprocessing, asyncio

To jest rozszerzenie "jak robic to szybciej", ale bez psucia semantyki kontraktu.

Zasada nadrzedna:

```text
Poprawnosc danych > szybkosc.
Concurrency nie moze zmienic accepted/rejected decision.
```

---

### Model mentalny: restauracja hamburgerowa

Zanim zobaczysz kod, wyobraz sobie restauracje. Ta analogia wyjasnla WSZYSTKO.

#### Kelnerzy = watki (threading)

```text
Restauracja ma 8 kelnerow.

Kelner podchodzi do stolika -> zapisuje zamowienie -> idzie do kuchni -> czeka na jedzenie -> wraca.
Kiedy czeka na kuchnie, NIE STOI BEZCZYNNIE.
Idzie do innego stolika, przynosi napoje, zbiera brudne talerze.

Kelner NIE gotuje. Kelner CZEKA i PRZYLACZA rzeczy.
```

To jest multithreading:

```text
wiele watkow dziala "rownoczesnie",
kazdy watek czeka na I/O (dysk, siec, API),
kiedy jeden czeka, inny moze sie wykonac,
zadne prawdziwe gotowanie sie nie dzieje — tylko obsluga i czekanie.
```

Kelnerzy wspoldzielaja jedna kuchnie (jeden proces Pythona, jeden GIL).
Szef sali (GIL) mowi: "w tej chwili tylko jeden kelner wydaje jedzenie z kuchni".
Ale podczas czekania — kelnerzy moga dzialac rownolegle.

**Kiedy threading w DE:**

```text
wczytujesz 50 plikow z dysku
pobierasz dane z 20 endpointow API
czytasz z bazy danych przez ORM
uploadujesz pliki na S3
```

---

#### Kucharze = procesy (multiprocessing)

```text
Restauracja otwiera 4 oddzielne kuchnie (oddzielne procesy).

Kazda kuchnia ma swojego szefa, swoj sprzet, swoje skladniki.
Kuchnie nie wiedza o sobie nawzajem — pracuja niezaleznie.
Moga smazy 4 zestawy hamburgerow JEDNOCZESNIE, naprawde rownolegle.

Ale: jesli kelner chce przekazac notatke do innej kuchni,
musi wyjsc, przejsc korytarzem i wejsc do tamtej kuchni.
Komunikacja miedzy kuchniami kosztuje.
```

To jest multiprocessing:

```text
kazdy proces ma osobny interpreter Pythona i osobny GIL,
prawdziwa rownolegle obliczenia CPU,
brak wspoldzielonej pamieci — dane sa kopiowane miedzy procesami (IPC),
koszt uruchamiania procesu jest wyzszy niz watku.
```

**Kiedy multiprocessing w DE:**

```text
parsowanie duzych plikow JSON / XML
obliczenia hash, szyfrowanie, kompresja
ciezkie transformacje Pandas / NumPy bez Spark
przetwarzanie partycji Parquet na wielu rdzeniach
```

---

#### Super-kelner = asyncio

```text
Jedna restauracja, jeden kelner, 200 stolikow.

Kelner NIGDY nie czeka bezczynnie.
Podszedl do stolika 1 -> zapisal zamowienie -> poszedl do stolika 2.
Stolik 1 czeka na kuchnie? Kelner juz jest przy stolikach 3, 4, 5.
Jak kuchnia zadzwoni ze jedzenie gotowe -> kelner "reaguje" i zanosi.

Ten kelner nie spi, nie czeka, non-stop przetwarza zdarzenia.
```

To jest asyncio (event loop):

```text
jeden watek, jeden event loop,
await oddaje sterowanie event loopowi kiedy czekamy na I/O,
event loop przeskakuje do nastepnego coroutine,
bardzo malo overheadu — tysiace rownoleglosci w jednym watku.
```

Wymaga: cala biblioteka musi byc async-native (httpx, aiofiles, asyncpg).
Nie mozna mieszac sync kodu blokujacego z async — to blokuje calego kelnera.

**Kiedy asyncio w DE:**

```text
serwis API z setkami rownolegych requestow
websocket / streaming data
async-native bazy danych (asyncpg, motor)
```

---

### GIL — dlaczego kelnerzy nie moga gotowac

GIL (Global Interpreter Lock) to zamek w CPythonie, ktory mowi:

```text
"W kazdej chwili tylko jeden watek moze wykonywac bytecode Pythona."
```

W analogii restauracyjnej:

```text
GIL = szef sali z kluczem do kasy.
Tylko jeden kelner naraz moze brac kase.
Ale kazdy kelner moze rownoczesnie isc do stolika i zapisywac zamowienie
(I/O — bo to nie wymaga kasy).
```

Konsekwencje praktyczne:

| Operacja | threading pomaga? | dlaczego |
|---|---|---|
| czytanie pliku | TAK | watek zwalnia GIL podczas syscall I/O |
| HTTP request | TAK | watek czeka na siec, GIL zwolniony |
| obliczenia Python (for loop) | NIE | watek trzyma GIL caly czas |
| NumPy / Pandas (C extension) | CZESTO TAK | C kod zwalnia GIL |
| hashowanie / regex w Pythonie | NIE | czysty Python bytecode, GIL nie zwalnia |

Multiprocessing omija GIL calkowicie — kazda kuchnia ma swoj zamek.

---

### I/O-bound vs CPU-bound — diagram decyzyjny

```text
Gdzie znika czas w Twoim kodzie?
         |
         v
    czekasz na dysk / siec / API ?
         |                    |
        TAK                  NIE
         |                    |
    threading            CPU-bound?
    lub asyncio               |
                             TAK
                              |
                      multiprocessing
                      (albo Spark dla duzych danych)
```

W DE czesto:

```text
extract wielu plikow -> I/O-bound -> threading
pobieranie z wielu API -> I/O-bound -> threading lub asyncio
parsowanie ciezkich JSON -> CPU-bound -> multiprocessing
walidacja Pydantic (maly rekord) -> lekko CPU, czesto mieszane -> threading wystarczy
```

---

### Kod: threading dla I/O-bound extract

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def read_single_file(path: Path) -> list[dict]:
    import json
    return json.loads(path.read_text())


def extract_parallel(paths: list[Path], max_workers: int = 8) -> list[dict]:
    """I/O-bound: czytanie wielu plikow rownoczeznie."""
    all_records: list[dict] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(read_single_file, paths))
    for records in results:
        all_records.extend(records)
    return all_records
```

Dlaczego max_workers=8 a nie 100?

```text
zbyt duzo watkow = overhead przelaczania kontekstu,
dla dysku lokalnego: 4-8 wystarczy (I/O bottleneck bedzie dysk, nie ilosc watkow),
dla API: mozna wiecej (20-50), ale uwazaj na rate limits.
```

---

### Kod: multiprocessing dla CPU-bound transform

```python
from concurrent.futures import ProcessPoolExecutor
from typing import Any
import hashlib
import json


def heavy_hash_record(record: dict[str, Any]) -> dict[str, Any]:
    """CPU-bound: obliczanie hasha i normalizacja duzego rekordu."""
    raw = json.dumps(record, sort_keys=True).encode()
    record["_checksum"] = hashlib.sha256(raw).hexdigest()
    return record


def transform_parallel(
    records: list[dict[str, Any]],
    max_workers: int = 4,
) -> list[dict[str, Any]]:
    """CPU-bound: przetwarzamy partie rekordow na wielu rdzeniach."""
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(heavy_hash_record, records))
```

Uwaga na serializacje:

```text
ProcessPoolExecutor kopiuje argumenty przez pickle do innego procesu.
Jezeli rekord jest duzy albo niepicklable (np. otwarty plik, polaczenie DB),
multiprocessing nie bedzie dzialac poprawnie.
Testuj zawsze na realnych danych, nie tylko na malym przykladzie.
```

---

### Kod: asyncio dla wielu rownolegych HTTP requestow

```python
import asyncio
import httpx
from typing import Any


async def fetch_one(client: httpx.AsyncClient, url: str) -> dict[str, Any]:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()


async def fetch_all_async(urls: list[str]) -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [fetch_one(client, url) for url in urls]
        return await asyncio.gather(*tasks)


# Wywolanie z sync kodu:
results = asyncio.run(fetch_all_async(urls))
```

Kiedy asyncio ma sens a threading nie:

```text
500+ rownolegych requestow HTTP -> asyncio (mniej overheadu niz 500 watkow)
20 requestow HTTP -> threading wystarczy, prostszy kod
baza danych sync (psycopg2) -> threading (nie mozesz uzyc asyncio)
baza danych async (asyncpg) -> asyncio
```

---

### Jak to polaczyc z data contract

Bezpieczny workflow z concurrency:

```text
1) Rownolegly extract (threading/async)
         |
         v
2) Walidacja kontraktu (deterministyczna, single-threaded lub rownolegla)
         |
         v
3) Jawny routing accepted/rejected (ostroz na shared list — patrz nizej)
         |
         v
4) Stabilizacja kolejnosci (sort przed zapisem outputu)
```

Walidacja Pydantic jest thread-safe (nie modyfikuje shared state).
Ale lista `accepted` i `rejected` jest shared — trzeba uwazac.

Bezpieczny wzorzec z ThreadPoolExecutor:

```python
from concurrent.futures import ThreadPoolExecutor


def validate_and_route(
    raw_records: list[dict],
) -> tuple[list[Order], list[RejectedRecord]]:
    """Walidacja rownolegla — kazdy watek zwraca wynik, brak shared state."""

    def validate_one(record: dict) -> Order | RejectedRecord:
        try:
            payload = OrderPayload.model_validate(record)
            return Order(
                order_id=payload.order_id,
                status=payload.status,
                total_amount=payload.total_amount,
                source=payload.source,
            )
        except Exception as exc:
            return RejectedRecord(
                raw_record=record,
                reason=str(exc),
                validation_stage="contract",
                contract_version="v1",
            )

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(validate_one, raw_records))

    accepted = [r for r in results if isinstance(r, Order)]
    rejected = [r for r in results if isinstance(r, RejectedRecord)]
    return accepted, rejected
```

Klucz: kazdy watek zwraca nowy obiekt, nie pisze do wspoldzielonej listy.
Agregacja (extend/filter) odbywa sie w watku glownym po zakonczeniu pool.

---

### Anty-patterny concurrency w pipeline

| Anti-pattern | Problem | Fix |
|---|---|---|
| `accepted.append(...)` wewnatrz ThreadPool | race condition: dwie operacje append naraz | kazdy watek zwraca wynik, main thread agreguje |
| brak limitu max_workers | 1000 watkow dla 1000 plikow | ustaw sensowny limit (8-20) |
| ProcessPoolExecutor dla malych rekordow | overhead IPC > zysk | uzyj tylko gdy rekord jest naprawde CPU-heavy |
| asyncio.run() wewnatrz ThreadPoolExecutor | event loop nie moze byc uruchomiony dwa razy | uzyj `asyncio.run_coroutine_threadsafe` lub oddzielny watek |
| porownanie "jest szybciej" bez baseline | moze byc wolniej dla malych danych | zawsze mierz: sekwencyjny vs 4 workers vs 8 workers |

---

### Rule of thumb

```text
I/O-bound (pliki, API, DB)  -> threading lub asyncio
CPU-bound (obliczenia)      -> multiprocessing
malo danych (< 1000 rek.)   -> sequential — overhead concurrency > zysk
nie wiesz                   -> zmierz, nie zgaduj
```

