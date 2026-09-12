# Praca domowa: Lekcja 05

## Cel

Masz pokazac, ze rozumiesz podstawy Pythona na malych danych e-commerce.

Nie uzywaj duzych bibliotek ani klas. Ta praca domowa ma sprawdzic fundamenty jezyka:

```text
zmienne -> typy -> if -> for -> list/dict -> funkcje -> csv -> assert
```

## Krok 0: przygotuj srodowisko projektowe

Najpierw przejdz [setup.md](setup.md). W tej lekcji uzywamy:

```text
pyenv  -> wersja Pythona
pipx   -> instalacja Poetry jako narzedzia CLI
Poetry -> venv i zaleznosci projektu
```

W swoim repo przygotuj katalog homeworku:

```bash
mkdir -p homework/lesson_05
cd homework/lesson_05
pyenv local 3.13.0
poetry init --name lesson-05-python-intro --python "^3.13" --no-interaction
poetry add --group dev pytest
```

Przygotuj pliki:

```bash
touch python_basics.py test_python_basics.py notes.md
```

Skopiuj `orders.csv` z labu do `homework/lesson_05/orders.csv`.

Po tym kroku katalog powinien wygladac tak:

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

## Krok 1: funkcje na pojedynczym rekordzie

W `python_basics.py` napisz funkcje:

```python
def normalize_status(status: str) -> str:
    ...

def is_completed(order: dict[str, str]) -> bool:
    ...

def parse_amount(value: str) -> float:
    ...

def classify_amount(amount: float) -> str:
    ...
```

Wymagania:

- `normalize_status(" Completed ")` zwraca `"completed"`.
- `is_completed(order)` zwraca `True` tylko dla statusu `completed`.
- `parse_amount("120.50")` zwraca `120.5`.
- `classify_amount(120.5)` zwraca:
  - `"small"` dla kwoty `< 200`,
  - `"medium"` dla kwoty od `200` do `< 500`,
  - `"large"` dla kwoty `>= 500`.

## Krok 2: funkcje na liscie rekordow

Dodaj funkcje:

```python
def calculate_completed_revenue(orders: list[dict[str, str]]) -> float:
    ...

def count_orders_by_status(orders: list[dict[str, str]]) -> dict[str, int]:
    ...

def collect_completed_order_ids(orders: list[dict[str, str]]) -> list[str]:
    ...
```

Wymagania:

- `calculate_completed_revenue` sumuje `total_amount` tylko dla completed orders.
- `count_orders_by_status` zwraca slownik, np. `{"completed": 2, "cancelled": 1}`.
- `collect_completed_order_ids` zwraca liste `order_id` tylko dla completed orders.

Nie uzywaj list comprehensions na sile. Normalna petla `for` jest tutaj dobra, bo uczysz sie mechaniki.

## Krok 3: czytanie CSV

Dodaj funkcje:

```python
from pathlib import Path


def read_orders(path: Path) -> list[dict[str, str]]:
    ...


def main() -> None:
        ...
```

`read_orders` ma uzyc standardowej biblioteki `csv.DictReader`.

`main()` ma:

1. wczytac `orders.csv`,
2. policzyc completed revenue,
3. policzyc status counts,
4. wypisac wyniki przez `print`.

## Krok 4: testy

W `test_python_basics.py` napisz testy:

1. `normalize_status` usuwa spacje i robi lowercase.
2. `is_completed` rozpoznaje completed order.
3. `parse_amount` zamienia tekst na `float`.
4. `classify_amount` zwraca `small`, `medium`, `large` dla trzech przykladow.
5. `calculate_completed_revenue` liczy tylko completed orders.
6. `count_orders_by_status` zlicza statusy.
7. `collect_completed_order_ids` zwraca tylko ID zakonczonych zamowien.

Testy moga tworzyc dane w kodzie:

```python
orders = [
    {"order_id": "1001", "status": "completed", "total_amount": "100.00"},
    {"order_id": "1002", "status": "cancelled", "total_amount": "50.00"},
]
```

## Krok 5: notes.md

W `notes.md` odpowiedz krotko:

```text
1. Czym rozni sie `list` od `dict`?
2. Po co funkcji `return`, skoro mozna uzyc `print`?
3. Dlaczego kwote z CSV zamieniasz przez `float`?
4. Jak dziala petla `for` na liscie orders?
5. Ktory test najlepiej sprawdza, ze revenue liczy sie poprawnie?
```

Kazda odpowiedz: 3-5 zdan. Nie pisz eseju.

## Krok 6: uruchomienie

Z katalogu repo:

```bash
cd homework/lesson_05
poetry run python python_basics.py
poetry run pytest
```

## Kryteria akceptacji

```text
[ ] Kod ma type hints.
[ ] Projekt ma `.python-version`, `pyproject.toml` i `poetry.lock`.
[ ] Kod uzywa funkcji, petli, list i dict.
[ ] Nie ma duzych bibliotek ani klas.
[ ] `read_orders` uzywa `csv.DictReader`.
[ ] Testy przechodza lokalnie przez `poetry run pytest`.
[ ] notes.md pokazuje rozumienie podstaw Pythona, nie tylko definicje.
```