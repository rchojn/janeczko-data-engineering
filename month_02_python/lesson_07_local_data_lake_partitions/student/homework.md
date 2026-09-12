# Praca domowa: Lekcja 07

## Cel

Masz zbudowac warstwe kontraktu danych dla pipeline produkcyjnego.

Kontekst: partner API zaczal wysylac rekordy o niestabilnym ksztalcie.
Twoim zadaniem jest zbudowac mechanizm, ktory przepuszcza poprawne rekordy,
odrzuca bledne z precyzyjnym powodem i daje raport jakosci danych po runie.

Ta praca jest podzielona na 2 czesci:

```text
CZESC I  -> data contract, routing accepted/rejected, quality summary
CZESC II -> multithreading/multiprocessing/asyncio jako rozszerzenie
```

## Co i gdzie robisz

Tworzysz osobny pakiet w katalogu pracy domowej:

```text
homework/lesson_07/
    order_contract.py      <- modele domenowe (dataclass)
    validate_orders.py     <- walidacja kontraktu (Pydantic) i routing
    test_order_contract.py <- testy
    notes.md               <- analiza i odpowiedzi
    interview_answer.md    <- odpowiedz na pytanie rekrutacyjne
```

Plik `student/lab/data_contracts_demo.py` to inspiracja i material do cwiczen.
Nie kopiujesz go do homework — piszesz samodzielnie.

## Krok 0: przygotuj katalog

```bash
mkdir -p homework/lesson_07
cd homework/lesson_07
touch order_contract.py validate_orders.py test_order_contract.py notes.md interview_answer.md
```

## Krok 1: model domenowy

W `order_contract.py` napisz dwa frozen dataclassy:

- `Order` — reprezentuje poprawny rekord po walidacji: `order_id`, `status`, `total_amount`, `source`.
- `RejectedRecord` — reprezentuje odrzucony rekord: `raw_record`, `reason`, `validation_stage`, `contract_version`.

Wskazowka: frozen dataclass nie pozwala modyfikowac pol po utworzeniu obiektu.
To dobra wlasciwosc dla rekordu danych — raz zawalidowany, nie powinien sie zmieniac.

## Krok 2: kontrakt Pydantic

W `validate_orders.py` napisz `OrderPayload` — model Pydantic opisujacy wejscie pipeline.

Wymagania kontraktu:

```text
order_id    -> wymagany, nie moze byc pusty string
status      -> wymagany, normalizowany do lowercase, tylko: completed, cancelled, pending, refunded
total_amount -> wymagany, liczba >= 0
source      -> opcjonalne, domyslnie "unknown"
```

Wskazowka: `status` z realnego API moze przyjsc jako `" Completed "`, `"COMPLETED"` lub `"completed"`.
Walidator musi obsluzyc wszystkie warianty przed sprawdzeniem listy dozwolonych wartosci.

Jesli utkniesz na `field_validator`: przejrzyj `student/patterns.md` — wzorzec jest w sekcji 1.

## Krok 3: routing accepted/rejected

Zaimplementuj funkcje `validate_payloads` ktora przyjmuje liste raw records i zwraca `ValidationResult`.

`ValidationResult` musi trzymac: `accepted` (lista `Order`), `rejected` (lista `RejectedRecord`),
`accepted_count`, `rejected_count`.

Wskazowka: dla kazdego rekordu probuj walidowac przez Pydantic i konwertowac na `Order`.
Jesli sie nie uda — dodaj do rejected z powodem bledu jako reason.

Jak o tym myslec:

```text
Kontrakt to bramka.
Przeszedl -> Order.
Nie przeszedl -> RejectedRecord z powodem.
Nic nie znika po cichu.
```

## Krok 4: persist wynikow

Dodaj funkcje, ktore zapisuja wyniki do plikow:

- Funkcja zapisujaca `accepted` records do JSONL.
- Funkcja zapisujaca `rejected` records do JSONL.
- Funkcja zapisujaca `quality_summary.json` z polami: `accepted_count`, `rejected_count`, `reject_rate`, `top_reject_reasons`, `contract_version`.

Wskazowka: JSONL (JSON Lines) to format gdzie kazda linia to osobny JSON object.
Latwiejszy do debugowania niz jeden duzy JSON array.

## Krok 5: obsluzone przypadki

Upewnij sie, ze Twoj kontrakt obsługuje i testuje wszystkie te scenariusze:

```text
missing order_id              -> reject z "missing required field"
invalid status enum           -> reject z czytelnym reason
negative total_amount         -> reject z czytelnym reason
wrong type (total_amount="abc") -> reject
status z whitespace i caps (" Completed ") -> normalizacja do "completed" i accept
```

## Krok 6: testy

W `test_order_contract.py` napisz minimum osiem testow:

1. Poprawny rekord przechodzi i zamienia sie na `Order`.
2. Brak `order_id` trafia do rejects z czytelnym reason.
3. Ujemny `total_amount` trafia do rejects.
4. Nieznany status trafia do rejects.
5. `" Completed "` jest normalizowane do `"completed"` i przyjmowane.
6. `accepted_count + rejected_count` jest rowne liczbie wejsciowych rekordow.
7. `quality_summary.json` ma poprawny `reject_rate`.
8. Rejected record ma `validation_stage` i `contract_version`.

Jesli utkniesz na testach: zacznij od testu 1 (happy path). Potem dodawaj po jednym blednym przypadku.

## Krok 7: notes.md

W `notes.md` odpowiedz na 5 pytan:

```text
1. Gdzie konczy sie walidacja boundary, a zaczyna domena?
2. Dlaczego sama dataclass nie wystarcza na wejsciu?
3. Co jest breaking vs non-breaking schema drift?
4. Co robisz, gdy reject_rate rosnie z 1% do 15%?
5. Dlaczego retry nie rozwiazuje validation errors?
```

Kazda odpowiedz: 3-5 zdan, na przykladzie z Twojego kodu.

## Krok 8: interview answer

W `interview_answer.md` napisz 8-12 zdan na pytanie:

```text
How do you enforce data contracts in Python pipelines?
```

W odpowiedzi musza pasc slowa: boundary validation, accepted/rejected routing, schema drift, quality metrics.

## CZESC II: concurrency (rozszerzenie lekcji)

W tej czesci pokazujesz, ze rozumiesz kiedy i jak wejsc w:

```text
multithreading
multiprocessing
asyncio
```

To dalej ma byc ten sam pipeline i ta sama semantyka kontraktu.

## Bonus: concurrency

Jesli masz czas po zrobieniu krokow 1-8, dodaj do `validate_orders.py` rownolegly wariant:

- `validate_payloads_parallel(records, workers)` z `ThreadPoolExecutor`.
- Wymaganie: ten sam output shape i te same wyniki accepted/rejected co wersja sekwencyjna.
- Dodaj test porowawczy potwierdzajacy rownowartosc wynikow.

Wskazowka: kazdy watek zwraca wynik (nie dopisuje do shared listy), main thread agreguje.
Patrz slajdy: "Bezpieczny wzorzec dla kontraktu".

## Jak uruchomic

```bash
cd homework/lesson_07
pytest test_order_contract.py -v
```

## Jak oddac prace przez GitHub

```bash
git checkout -b lesson-07-homework
git add homework/lesson_07
git commit -m "Add lesson 07 homework"
git push -u origin lesson-07-homework
```

W opisie PR napisz krotko:

```text
Co zrobilem:
Co bylo trudne:
Czego nie jestem pewien:
```

## Co oddac

```text
homework/lesson_07/
├── order_contract.py
├── validate_orders.py
├── test_order_contract.py
├── accepted_orders.jsonl
├── rejected_orders.jsonl
├── quality_summary.json
├── notes.md
└── interview_answer.md
```

## Wersja ambitna

Tylko po zrobieniu minimum:

1. Dodaj `reject_rate_by_source` do `quality_summary.json`.
2. Napisz test dla schema drift — rekord z nieznanym dodatkowym polem.
3. Dodaj `contract_version` jako parametr do `validate_payloads` zamiast hardcodowac.

## Checklista przed oddaniem

- [ ] Kontrakt jest wymuszany w kodzie przez Pydantic, nie tylko w README.
- [ ] Accepted i rejected sa jawnie rozdzielone.
- [ ] Kazdy rejected record ma `reason`, `validation_stage` i `contract_version`.
- [ ] `accepted_count + rejected_count` = liczba rekordow wejsciowych.
- [ ] Istnieje `quality_summary.json` z `reject_rate`.
- [ ] Testy przechodza przez `pytest`.
- [ ] `notes.md` odpowiada na wszystkie 5 pytan konkretnie.
- [ ] `interview_answer.md` ma 8-12 zdan z wymaganymi slowami.
