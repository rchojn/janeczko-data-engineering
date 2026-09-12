# Dla uczestnika: Lekcja 05 - Wprowadzenie do Pythona dla Data Engineeringu

## Otworz i zrob to

1. Przygotuj srodowisko wedlug [setup.md](setup.md): `pyenv`, `pipx`, `uv`, `poetry`.
2. Otworz [teoria.md](teoria.md) i przeczytaj sekcje do konca wzorca.
3. Przejdz [lab/python_intro.py](lab/python_intro.py) i uruchom przyklady na danych z [lab/data/](lab/data/).
4. Finalna prace domowa zapisz w katalogu `homework/lesson_05/`.
5. Po lekcji przejdz [homework.md](homework.md) i [interview_questions.md](interview_questions.md).

Prezentacja:

- [slides.presenterm.md](slides.presenterm.md) - deck do odpalenia w terminalu,
- [slides.pdf](slides.pdf) - wygenerowana wersja PDF.
- [setup.presenterm.md](setup.presenterm.md) - osobny deck o instalacji Pythona i przygotowaniu srodowiska,
- [setup.pdf](setup.pdf) - wygenerowana wersja PDF setupu.

Najkrotsza zasada folderow:

```text
student/lab/              = lab online / miejsce do cwiczenia Pythona
homework/lesson_05/       = tutaj tworzysz finalne pliki pracy domowej
```

Nie kopiuj calego katalogu `student/lab/` do homeworku. Laby sa miejscem treningu. Homework jest osobnym katalogiem z kodem i testami gotowymi do review.

## Cel lekcji

Po tej lekcji masz umiec napisac prosty skrypt Python i powiedziec:

- czym roznia sie `str`, `int`, `float`, `bool`, `list` i `dict`,
- jak dziala `if / elif / else`,
- jak przejsc po liscie rekordow petla `for`,
- jak napisac funkcje z parametrami i `return`,
- jak wczytac male CSV standardowa biblioteka `csv`,
- jak policzyc proste metryki na malej liscie rekordow.

## Jak uruchomic

Komendy uruchamiaj w terminalu Linux albo WSL Ubuntu.

Najpierw zrob setup narzedzi: [setup.md](setup.md).

Z katalogu lekcji:

```bash
pyenv shell 3.13.0
python student/lab/python_intro.py
```

Wlasny homework robisz juz jako maly projekt Poetry wedlug [setup.md](setup.md) i [homework.md](homework.md).

Jesli chcesz sprawdzic wersje Pythona:

```bash
python --version
poetry --version
```

## Dataset

Pracujemy na malym sklepie:

- `orders.csv` - zamowienia,
- `customers.csv` - klienci.

W tej lekcji CSV traktujemy jako liste slownikow:

```text
orders.csv -> list[dict]
jeden dict -> jeden rekord z CSV
kolumna CSV -> klucz w dict
```

## Co oddajesz po lekcji

Oddajesz finalny katalog `homework/lesson_05/`:

```text
homework/lesson_05/
├── .python-version
├── pyproject.toml
├── poetry.lock
├── python_basics.py
├── test_python_basics.py
├── orders.csv
└── notes.md
```

Standardowo do PR dodajesz finalne pliki z homeworku razem z `pyproject.toml`, `poetry.lock` i `.python-version`. Nie dodawaj `.venv/`, `__pycache__/`, `.pytest_cache/` ani wygenerowanych plikow raportow.

## Zasada pracy w tej lekcji

Najpierw napisz rozwiazanie prosto, potem je porzadkuj.

Przyklad:

```text
Mam liste zamowien.
Kazde zamowienie to dict.
Chce policzyc sume total_amount tylko dla statusu completed.
Najpierw sprawdzam status, potem dodaje kwote do sumy.
```

Nie wchodzimy jeszcze w duze biblioteki, klasy ani architekture pipeline'ow. Najpierw Python ma byc zrozumialy.