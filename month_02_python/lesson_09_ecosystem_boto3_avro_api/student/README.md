# Dla uczestnika: Lekcja 09 - Ecosystem: boto3, Avro i ingest API

## Otworz i zrob to

1. Przeczytaj [teoria.md](teoria.md).
2. Ustal, jaki jest flow ingestu: `fetch -> serialize -> upload`.
3. Uruchom lab [lab/ecosystem_demo.py](lab/ecosystem_demo.py).
4. Po lekcji zrób [homework.md](homework.md).
5. Przećwicz odpowiedzi z [interview_questions.md](interview_questions.md).

Najkrótsza zasada folderów:

```text
student/lab/              = lokalne demo integracji i serializacji
homework/lesson_09/       = finalny moduł ingest + testy + opis do review
```

Nie kopiuj katalogu `student/lab/` do `homework/`. Laby są do eksperymentu, a finalny moduł trafia do homework.

## Cel lekcji

Po lekcjach 06-08 masz już fundamenty pipeline'u, walidacji i modularizacji. Teraz uczysz się, jak wygląda integracja z ekosystemem narzędzi real-world Data Engineering:

- pobieranie danych z API z paginacją,
- serializacja do Avro,
- zapis i upload do object storage,
- bezpieczne retry dla transient errors,
- testowanie integracji bez podpinania realnego AWS.

Najważniejszy flow tej lekcji:

```text
API page -> fetch_all -> retryable http -> Avro bytes -> storage upload
```

To jest ważny krok od "skryptu w Pythonie" do wzorca produkcyjnego ingest: dane wchodzą z zewnątrz, są serializowane, a potem zapisane jako binarny artefakt do dalszego przetwarzania.

## Co umiesz po lekcji

- rozumieć paginację `cursor-based`,
- odróżniać transient errors od permanent errors,
- serializować rekordy do Avro,
- używać `boto3` jako klienta z parametru,
- pisać testy mockująco bez realnego AWS,
- pisać prosty i czytelny integracyjny moduł `ingestion`.

## Główny artefakt

```text
student/
├── homework.md
├── interview_questions.md
├── teoria.md
├── lab/
│   └── ecosystem_demo.py
└── README.md
```

## Minimalna zasada projektowa

W tej lekcji nie projektujesz jednego monolitu. Projektujesz mały moduł z wyraźnymi odpowiedzialnościami:

```text
api.py        -> pobieranie i retry
serialize.py  -> Avro encode/decode
storage.py    -> upload do S3/mock storage
```

To jest dokładnie ten sam wzorzec, który widzisz w prawdziwych systemach danych: separacja wejścia, serializacji i eksportu.

## Jak uruchomić lab

```bash
python student/lab/ecosystem_demo.py
```

Jeśli potrzebujesz osobnej konfiguracji środowiska dla pracy domowej, użyj projektu `homework/lesson_09/` i instrukcji z [homework.md](homework.md).
