# Dla uczestnika: Lekcja 07 - Data contracts: dataclass, Pydantic i schema drift

## Otworz i zrob to

1. Otwórz [slides.presenterm.md](slides.presenterm.md).
2. Przeczytaj [teoria.md](teoria.md) do sekcji `STALY PATTERN`.
3. Uruchom lab [lab/data_contracts_demo.py](lab/data_contracts_demo.py).
4. Po lekcji zrób [homework.md](homework.md).
5. Przećwicz odpowiedzi z [interview_questions.md](interview_questions.md).

Najkrótsza zasada folderów:

```text
student/lab/              = demo kontraktu danych i schema drift
homework/lesson_07/       = finalny kontrakt + accepted/rejected output do review
```

Nie kopiuj katalogu `student/lab/` do `homework/`. Laby służą do ćwiczenia logiki, a finalny output trafia do osobnego katalogu homework.

## Cel lekcji

Po lekcji 06 masz pipeline. Teraz dodajesz kontrakt danych, zeby pipeline nie ufal slepo raw payloadom.

Flow lekcji:

```text
raw payload -> Pydantic validation -> dataclass/domain object -> accepted/rejected records
```

Ta lekcja odpowiada na pytanie:

```text
Jak zatrzymac zly rekord zanim popsuje KPI?
```

## Co umiesz po lekcji

- opisac rekord przez `dataclass`,
- sprawdzic payload przez Pydantic,
- rozpoznac schema drift,
- zapisac rejected records z powodem,
- odroznic bledy kontraktu od bledow IO,
- zbudowac quality summary (reject_rate, reasons),
- wytlumaczyc roznice `dict` vs `dataclass` vs Pydantic,
- odpowiedziec na interview pytanie o data contracts.

## Glowny artefakt

```text
homework/lesson_07/
├── order_contract.py
├── validate_orders.py
├── quality_summary.json
├── accepted_orders.jsonl
├── rejected_orders.jsonl
├── test_order_contract.py
├── notes.md
└── interview_answer.md
```

## Granice lekcji (zeby nie mieszac tematow)

```text
Lekcja 07: kontrakt danych i reject policy.
Lekcja 09: retry/backoff dla integracji API/S3.
```

W tej lekcji nie retryujesz validation errors.

## Instalacja Pydantic

Jesli uzywasz Poetry:

```bash
poetry add pydantic
```

Jesli robisz szybki sandbox:

```bash
uv pip install pydantic
```
