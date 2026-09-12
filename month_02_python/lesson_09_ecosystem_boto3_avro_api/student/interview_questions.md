# Interview questions: Lekcja 09

1. Jak działa Boto3 i skąd wie gdzie jest AWS?
2. Kiedy użyjesz Avro, a kiedy Parquet?
3. Jak obsługujesz paginację w REST API?
4. Dlaczego klient S3 przekazujesz jako parametr zamiast tworzyć w funkcji?
5. Jak testujesz kod który robi upload na S3 bez prawdziwego AWS?
6. Czym różni się PySpark od Polars?

---

## Pytania — Python concurrency (bardzo często na rekrutacji)

7. Co to GIL i co z tego wynika praktycznie?

   GIL (Global Interpreter Lock) = tylko jeden wątek CPython wykonuje bytecode naraz.
   Wynika z tego:
   - **threading** pomaga przy IO-bound (czekanie na sieć, dysk) — wątek zwalnia GIL podczas IO
   - **threading** NIE przyspiesza CPU-bound (liczenie, transformacje) — jeden wątek blokuje resztę
   - **multiprocessing** omija GIL — każdy proces ma osobny interpreter i osobny GIL

8. Kiedy threading, kiedy multiprocessing, kiedy asyncio?

```text
threading:
   IO-bound + kilka wątków + prosty kod
   Przykład: 10 requestów HTTP równolegle, wczytywanie wielu plików

multiprocessing:
   CPU-bound: transformacje danych, kompresja, parsowanie dużych plików
   Przykład: przetwarzanie 8 partycji Parquet na 8 rdzeniach

asyncio:
   IO-bound + dużo równoległych operacji (setki/tysiące)
   Przykład: 500 requestów HTTP naraz, obsługa wielu połączeń WebSocket
   httpx, aiohttp — async-native libraries
```

9. Jak zrównoleglisz 100 requestów HTTP w Pythonie?

```python
# threading — prosty, dobry do kilkunastu requestów
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_order, order_ids))

# asyncio — lepszy do setek requestów
import asyncio
import httpx

async def fetch_all(ids):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(f"/orders/{id}") for id in ids]
        return await asyncio.gather(*tasks)
```

10. Jak zrównoleglisz CPU-bound transformacje (np. 8 partycji Parquet)?

```python
from concurrent.futures import ProcessPoolExecutor

def process_partition(path):
    import polars as pl
    return pl.read_parquet(path).filter(...).collect()

with ProcessPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(process_partition, partition_paths))
```

    Uwaga: Polars sam w sobie jest wielowątkowy (Rust backend) —
    ProcessPoolExecutor ma sens gdy masz wiele niezależnych plików do przetworzenia.

11. Dlaczego Polars jest szybszy od Pandas?

```text
Pandas:  Python + NumPy, single-threaded domyślnie, eager evaluation
Polars:  Rust backend, wielowątkowy z automatu, lazy evaluation (query planner)
```

    Na typowym DE workloadzie (100MB-10GB) Polars jest 5-20x szybszy od Pandas.
    Na danych >100GB rozważ PySpark (klaster) lub DuckDB (SQL on files).

Dobra odpowiedź: GIL → IO vs CPU-bound → właściwe narzędzie → przykład z kodu.
