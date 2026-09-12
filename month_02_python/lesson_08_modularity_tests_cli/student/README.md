# Dla uczestnika: Lekcja 08 - Production readiness w Python DE

## Otworz i zrob to

1. Otwórz [slides.presenterm.md](slides.presenterm.md).
2. Przeczytaj [teoria.md](teoria.md) do sekcji `STALY PATTERN`.
3. Uruchom lab [lab/mini_etl_cli.py](lab/mini_etl_cli.py).
4. Po lekcji zrób [homework.md](homework.md).
5. Przećwicz odpowiedzi z [interview_questions.md](interview_questions.md).

Najkrótsza zasada folderów:

```text
student/lab/              = mini demo CLI i rozgrzewka architektury
homework/lesson_08/       = finalny mini ETL project do review
```

Nie kopiuj katalogu `student/lab/` do `homework/`. Laby są do testowania pomysłu, a finalny projekt trafia do katalogu homework.

## Cel lekcji

Po lekcjach 06-07 masz pipeline i kontrakt danych. Teraz uczysz sie opakowac to w mini projekt, ktory da sie uruchomic, testowac i debugowac.

Najwazniejszy flow lekcji:

```text
raw JSON -> extract -> normalize -> transform -> load -> CLI output
```

To nie jest tylko „skrypt, który działa raz”. To jest pierwszy projekt Python DE z wyraźnym rozdzieleniem odpowiedzialności, testowaniem i logowaniem.

Ta lekcja mapuje sie bezposrednio na kompetencje z programu szkoleniowego:

- Pytest i testy automatyczne,
- typowanie statyczne (`mypy`),
- observability (`logging`, run metadata, runbook),
- modularna implementacja pipeline'u.

## Co umiesz po lekcji

- opisac `src/` layout,
- napisac CLI przez `argparse`,
- dodac logging,
- dodac retry z limitem,
- oddzielic extract/transform/load,
- napisac runbook dla awarii,
- odpalic `mypy` i poprawic bledy typow,
- odpowiedziec na pytanie o produkcyjny Python w DE.

## Glowny artefakt

```text
homework/lesson_08/
├── pyproject.toml
├── README.md
├── runbook.md
├── data/orders.json
├── src/pipeline/
└── tests/
```

## Minimalna komenda

```bash
python -m pipeline.cli --input data/orders.json --output output/result.json
```
