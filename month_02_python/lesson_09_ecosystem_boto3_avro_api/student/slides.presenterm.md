---
title: "Lekcja 09 - Ecosystem: boto3, Avro i API"
author: Data Engineering Course
date: 2026-08-21
---

# Lekcja 09

Ekosystem: boto3, Avro i API

```text
pobranie -> serializacja -> zapis -> walidacja -> magazyn
```

Do tej pory pracowaliśmy głównie lokalnie. Teraz Python robi to, do czego jest dobrze przygotowany: łączy zewnętrzne źródła danych z narzędziami magazynowania i kontrolą jakości.

<!-- end_slide -->

# TL;DR

Realny pipeline danych wygląda zwykle tak:

```text
API / eksport / event -> Python -> walidacja -> serializacja -> magazyn
```

Najważniejsza umiejętność to nie „umieć zrobić request”. To umieć rozpoznać:

```text
co jest błędem przejściowym,
co jest problemem kontraktu,
co trzeba zapisać jako artefakt,
co jest gotowe do dalszej analityki.
```

<!-- end_slide -->

# Gdzie dane przychodzą w realnym świecie

W data engineering dane zwykle przychodzą z:

```text
API partnerów
S3 / object storage
streaming events
eksportów z systemów operacyjnych
```

Python jest warstwą łączącą: zbiera, waliduje, serializuje i przenosi dane do odpowiedniego magazynu.

<!-- end_slide -->

# Dlaczego to jest złożone

Sama odpowiedź z API to nie jest pipeline. To tylko wejście.

```text
- API ma limity szybkości
- odpowiedź ma paginację
- dane mogą mieć różne typy i nulls
- serializacja musi być stabilna
- zapis do storage ma własne reguły błędów
```

Dlatego zajęcia z ekosystemem są momentem przejścia od „czytam JSON” do „obsługuję realny ingest”.

<!-- end_slide -->

# Wzorzec integracji

Każdy zewnętrzny system ma podobny przepływ:

```text
klient -> wywołanie -> obsługa odpowiedzi -> retry przy błędzie przejściowym -> zapis lub upload
```

Najważniejsze: nie retryujesz wszystkiego. Retry jest zarezerwowany tylko dla błędów przejściowych, a nie dla problemów jakości danych.

<!-- end_slide -->

# HTTP API z paginacją

```python
while True:
    response = client.get(url, params=params)
    response.raise_for_status()
    payload = response.json()
    records.extend(payload["results"])

    if not payload.get("next"):
        break
    params["cursor"] = payload["next"]
```

W praktyce API zwykle nie zwraca wszystkiego naraz. Musisz obsłużyć `next`, `cursor` albo `page` i iterować po serii odpowiedzi.

<!-- end_slide -->

# Typowe błędy przy API

```text
- 429 limit szybkości
- 500 / 502 / 503 timeout
- 400 niepoprawne zapytanie
- 401/403 problem z autoryzacją
- brak tokena paginacji
- częściowa odpowiedź ze zmienionym schematem
```

Nie wszystkie błędy są takie same. To wpływa na to, czy robimy retry, czy natychmiast zgłaszamy błąd kontraktu.

<!-- end_slide -->

# Boto3 — klient S3

```python
import boto3

s3 = boto3.client("s3", region_name="eu-west-1")

s3.upload_file("output/orders.parquet", "my-bucket", "orders/orders.parquet")
s3.put_object(Bucket="my-bucket", Key="orders/data.avro", Body=avro_bytes)
```

W praktyce klient bucketa tworzy się raz, a potem używa wielokrotnie. To jest prosty, ale realny wzorzec pracy z magazynem w chmurze.

<!-- end_slide -->

# Boto3 — błędy i kody odpowiedzi

```python
from botocore.exceptions import ClientError

try:
    s3.download_file(bucket, key, local_path)
except ClientError as exc:
    code = exc.response["Error"]["Code"]
    if code == "NoSuchKey":
        raise FileNotFoundError(f"Missing: s3://{bucket}/{key}") from exc
    raise
```

Nie ma jednego „ogólnego błędu”. Dla S3 ważne są szczegóły odpowiedzi, bo różne kody oznaczają różne decyzje operacyjne.

<!-- end_slide -->

# Avro kontra Parquet

```text
Avro: row-based, dobre do strumieni i payloady eventów
Parquet: columnar, dobre do analityki i zapytań w data lake
```

W tej lekcji najczęściej pracujemy z Avro jako formatem serializacji między etapami ingest. Parquet z kolei zwykle pojawi się w projekcie praktycznym.

<!-- end_slide -->

# Avro — prosty przykład

```python
import fastavro
from io import BytesIO

schema = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "status", "type": "string"},
        {"name": "total_amount", "type": "double"},
    ],
}

records = [{"order_id": "1001", "status": "completed", "total_amount": 120.5}]
buf = BytesIO()
fastavro.writer(buf, fastavro.parse_schema(schema), records)
```

Schema robi za nas kontrakt danych na poziomie serializacji. To ważne, bo format pliku ma znaczenie dla downstream.

<!-- end_slide -->

# Różnica: pobieranie / serializacja / zapis

```text
pobieranie: pobierz dane z API
serializacja: zamień na Avro / JSON / bytes
zapis: zapisz do S3 / lokalnie / do kolejnego systemu
```

To jest podstawowy wzorzec pipeline ingest. Jeśli zrobisz tylko pobieranie, nie zrobisz jeszcze gotowego przepływu danych.

<!-- end_slide -->

# Kiedy retry ma sens

Retry tylko dla błędów przejściowych:

```text
429 (limit szybkości)
408 (timeout)
5xx (przejściowa awaria serwera)
```

Nie retry dla błędów stałych:

```text
400 (złe zapytanie)
401/403 (brak autoryzacji)
404 (zły endpoint)
```

Dobrą regułą jest: retry tylko tam, gdzie problem jest czasowy i ma sens go powtórzyć.

<!-- end_slide -->

# Backoff i jitter

Nie spamujesz API co 100 ms. Zamiast tego używasz rosnących opóźnień:

```text
próba 1 -> 0.5s
próba 2 -> 1.0s
próba 3 -> 2.0s
próba 4 -> 4.0s
```

Jitter rozprasza równoległe retry, więc wiele workerów nie wraca do tego samego endpointu w tej samej chwili.

<!-- end_slide -->

# Co jest „wystarczająco dobrym” pipeline

```text
- czyta zewnętrzne źródło
- obsługuje paginację
- waliduje dane po wejściu
- serializuje do stabilnego formatu
- zapisuje do magazynu
- ma logi i politykę retry
```

To jest minimum, które odróżnia realny ingest od prostego „request + print”.

<!-- end_slide -->

# Definition of Done

```text
[ ] payload API jest pobierany i paginowany
[ ] dane są serializowane do Avro lub innego formatu
[ ] wynik trafia do magazynu
[ ] błędy są rozpoznawane po kodach i typach
[ ] retry jest tylko dla błędów przejściowych
[ ] projekt ma jasno opisany przepływ i kontrakt danych
```

To jest minimum, które odróżnia realny ingest od prostego „request + print”.

<!-- end_slide -->

# Odpowiedź na pytanie rekrutacyjne

Pytanie:

```text
Jak zbudować pipeline ingest w Pythonie dla danych zewnętrznych?
```

Odpowiedź:

```text
Pobieram dane z API z paginacją, waliduję surowe rekordy i serializuję je do stabilnego formatu, na przykład Avro.
Następnie zapisuję artefakt do magazynu obiektowego przez boto3.
Trzymam retry tylko dla błędów przejściowych i traktuję trwałe problemy ze schematem jako problemy kontraktu.
```

<!-- end_slide -->

# Checklist do powtórki

```text
[ ] Czy potrafisz opisać różnicę między pobieraniem, serializacją i zapisem?
[ ] Czy rozumiesz, kiedy retry ma sens, a kiedy nie?
[ ] Czy wiesz, po co używamy Avro / Parquet?
[ ] Czy potrafisz powiedzieć, czym jest paginacja w API?
[ ] Czy rozumiesz, że Python w data engineering jest warstwą łączącą, nie tylko językiem skryptowym?
```

<!-- end_slide -->

W DE to kluczowe, bo duplikaty psuja metryki.

<!-- end_slide -->

# Mocking w testach

Zewnetrzne systemy (S3, API) nie powinny byc wywolywane w testach.

```python
from unittest.mock import MagicMock

def test_upload_calls_put_object() -> None:
    mock_s3 = MagicMock()
    upload_to_s3(b"data", bucket="my-bucket", key="k", client=mock_s3)
    mock_s3.put_object.assert_called_once_with(
        Bucket="my-bucket", Key="k", Body=b"data"
    )
```

Klient jako parametr = testowalnosc bez prawdziwego AWS.

Klient w srodku funkcji = nie da sie przetestowac bez moto/localstack.

<!-- end_slide -->

# Interview answer

Pytanie:

```text
How do you handle external integrations in a Python DE pipeline?
```

Odpowiedz:

```text
I treat each external system as a boundary.
The client is created once per session, not per operation.
IO functions accept the client as a parameter — this makes them testable.
In tests I replace real clients with MagicMock and verify the call arguments.
For S3 I use boto3 with ClientError handling.
For REST APIs I use httpx with cursor-based pagination and bounded retries.
Retry is only for transient errors with exponential backoff and jitter.
```

<!-- end_slide -->

# Homework

Oddajesz:

```text
src/ingestion/
    api.py      ← fetch z paginacja + retry/backoff
    serialize.py ← Avro roundtrip
    storage.py  ← upload z klientem jako parametr
tests/
    test_api.py
    test_serialize.py
    test_storage.py
```

Najwazniejsze:

```text
testy nie robia prawdziwych HTTP ani S3 calls
retry dziala tylko dla transient statusow
mypy src/ — czysto
```
