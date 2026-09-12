# Dla uczestnika: Lekcja 06 - Python w Data Engineeringu

## Otworz i zrob to

1. Otworz [slides.presenterm.md](slides.presenterm.md).
2. Przeczytaj [teoria.md](teoria.md) do sekcji `STALY PATTERN`.
3. Uruchom lab [lab/de_pipeline_workflow.py](lab/de_pipeline_workflow.py).
4. Po lekcji zrob [homework.md](homework.md).
5. Przećwicz odpowiedzi z [interview_questions.md](interview_questions.md).

## Cel lekcji

Po lekcji 05 umiesz funkcje, `list`, `dict`, `for`, CSV i testy. Teraz uczysz sie, jak z tego robi sie prosty pipeline Data Engineering z kontraktem rekordu.

Najwazniejszy flow:

```text
extract -> validate with Pydantic -> dataclass records -> transform -> load
```

## Co umiesz po lekcji

- przeczytac dane z CSV i JSON,
- zasymulowac API payload bez prawdziwej uslugi,
- sprawdzic required fields,
- uzyc Pydantic do walidacji payloadu,
- zamienic poprawny payload na `dataclass Order`,
- rozdzielic accepted i rejected records,
- policzyc prosta metryke,
- zapisac wynik jako JSON,
- powiedziec, gdzie w pipeline jest blad: extract, validate, transform czy load.

## Glowny artefakt

```text
homework/lesson_06/
├── pipeline_workflow.py
├── orders.csv
├── api_orders.json
├── pipeline_output.json
├── test_pipeline_workflow.py
├── notes.md
└── interview_answer.md
```

## Najwazniejsza mysl

Python w Data Engineeringu nie jest tylko skladnia. Python opisuje proces:

```text
skad dane przyszly,
czy maja oczekiwany ksztalt,
jak je normalizujemy,
gdzie zapisujemy wynik,
jak testujemy calosc.
```

W tej lekcji `dict` jest formatem raw inputu, Pydantic jest bramka walidacyjna, a `dataclass` jest czytelnym rekordem uzywanym dalej w pipeline.

## Jak uruchomic lab

Jesli masz Pydantic w srodowisku:

```bash
python student/lab/de_pipeline_workflow.py
```

Jesli robisz szybki run przez `uv` bez instalowania paczki w projekcie:

```bash
uv run --with pydantic python student/lab/de_pipeline_workflow.py
```
