---
title: Lekcja 05 - Wprowadzenie do Pythona
author: Data Engineering Course
date: 2026-08-13
---

# Lekcja 05

Wprowadzenie do Pythona dla Data Engineeringu

```text
zmienne -> typy -> warunki -> petle -> list/dict -> funkcje -> CSV -> testy
```

Cel: napisac prosty program, ktory czyta zamowienia i liczy completed revenue.

<!-- end_slide -->

# Zaczynamy od srodowiska

W projekcie Python ustawiamy najpierw narzedzia:

```text
pyenv  -> wersja Pythona
pipx   -> instalacja narzedzi CLI
uv     -> szybkie install/run/tools dla Pythona
Poetry -> zaleznosci i .venv projektu
```

Bez tego kazdy uczestnik moze miec inna wersje Pythona i inne paczki.

<!-- end_slide -->

# Warstwy srodowiska

```text
system Linux / WSL
    |
    v
pyenv: Python 3.13.0
    |
    v
pipx albo uv: narzedzia CLI
    |
    v
Poetry: .venv + pytest dla projektu
```

Jedna warstwa odpowiada za jedna rzecz.

<!-- end_slide -->

# Instalacja: Linux / WSL

Ubuntu / WSL Ubuntu:

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev curl git libffi-dev
curl https://pyenv.run | bash
```

Potem wpisy w `~/.zshrc` i nowy shell.

Pelna instrukcja: `student/setup.md`.

<!-- end_slide -->

# Instalacja: macOS i Windows

macOS:

```bash
brew install pyenv pipx uv
pipx install poetry
```

Windows PowerShell:

```powershell
winget install pyenv-win.pyenv-win
python -m pip install --user pipx
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
pipx install poetry
```

Pelne kroki i debug sa w `student/setup.md`.

<!-- end_slide -->

# Python dla projektu

```bash
pyenv install 3.13.0
pyenv global 3.13.0
python --version
```

W katalogu projektu:

```bash
pyenv local 3.13.0
cat .python-version
```

`.python-version` mowi: ten projekt uzywa tej wersji Pythona.

<!-- end_slide -->

# pipx, uv i Poetry

```bash
python -m pip install --user pipx
python -m pipx ensurepath
exec zsh
curl -LsSf https://astral.sh/uv/install.sh | sh
pipx install poetry
poetry --version
uv --version
```

Dlaczego `pipx` i `uv`?

```text
pipx instaluje globalne narzedzia CLI w izolacji.
uv jest szybkim nowoczesnym narzedziem do Pythona.
Poetry prowadzi projekt tej lekcji.
```

<!-- end_slide -->

# Poetry w projekcie

```bash
poetry config virtualenvs.in-project true
mkdir -p homework/lesson_05
cd homework/lesson_05
pyenv local 3.13.0
poetry init --name lesson-05-python-intro --python "^3.13" --no-interaction
poetry add --group dev pytest
```

Efekt:

```text
.python-version
pyproject.toml
poetry.lock
.venv/
```

<!-- end_slide -->

# Uruchamianie przez Poetry

```bash
poetry run python python_basics.py
poetry run pytest
```

Zapamietaj:

```text
python             -> moze byc przypadkowy interpreter
poetry run python  -> interpreter z venv tego projektu
```

W pracy domowej uzywamy `poetry run`.

<!-- end_slide -->

# Czego dzis nie robimy

Na tej lekcji nie wchodzimy jeszcze w:

```text
duze biblioteki
klasy
architekture pipeline'ow
orkiestracje
cloud
```

Najpierw zwykly Python ma byc jasny.

<!-- end_slide -->

# Agenda 45 min

```text
0-8    setup: pyenv, pipx, uv, Poetry
8-13   po co Python w Data Engineeringu
13-20  zmienne, typy, print
20-27  if / elif / else, wciecia
27-34  list, dict, petla for
34-40  funkcje, return, csv.DictReader
40-43  assert i pytest
43-45  homework contract
```

<!-- end_slide -->

# Po co Python w DE

SQL dobrze odpowiada na pytania w bazie.

Python dobrze opisuje proces:

```text
wczytaj plik
sprawdz rekordy
policz wynik
zapisz / wypisz rezultat
uruchom to ponownie jutro
```

<!-- end_slide -->

# Najprostszy model programu

```text
input data
   |
   v
instructions
   |
   v
output result
```

Program nie zgaduje intencji. Wykonuje dokladnie instrukcje, ktore napiszesz.

<!-- end_slide -->

# Pierwszy plik .py

```python
print("hello Python")
```

Uruchomienie:

```bash
python student/lab/python_intro.py
```

`print` pokazuje cos w terminalu.

<!-- end_slide -->

# Zmienne

Zmienna to nazwa dla wartosci.

```python
order_id = 1001
status = "completed"
total_amount = 120.50
is_paid = True
```

Pytanie:

```text
Ktora z tych wartosci jest tekstem, a ktora liczba?
```

<!-- end_slide -->

# Podstawowe typy

```text
str    tekst, np. "completed"
int    liczba calkowita, np. 1001
float  liczba z przecinkiem, np. 120.50
bool   True albo False
```

W Pythonie typ widzisz po wartosci, nie po deklaracji jak w Javie.

<!-- end_slide -->

# Type check w glowie

```python
amount_text = "120.50"
amount_number = 120.50
```

To nie jest to samo.

```text
"120.50"  tekst z CSV
120.50    liczba do sumowania
```

<!-- end_slide -->

# First Principles: CSV daje tekst

CSV to plik tekstowy.

```text
order_id,status,total_amount
1001,completed,120.50
```

Po wczytaniu z CSV wartosc `120.50` zwykle przychodzi jako tekst.

Dlatego przed suma robimy konwersje.

<!-- end_slide -->

# Konwersja typow

```python
amount_text = "120.50"
amount = float(amount_text)
```

Teraz `amount` jest liczba.

```python
revenue = 0.0
revenue = revenue + amount
```

<!-- end_slide -->

# Warunek if

Warunek decyduje, ktora galaz kodu sie wykona.

```python
status = "completed"

if status == "completed":
    print("liczymy revenue")
```

`==` pyta, czy wartosci sa rowne.

<!-- end_slide -->

# if / elif / else

```python
if status == "completed":
    print("liczymy revenue")
elif status == "cancelled":
    print("pomijamy")
else:
    print("sprawdz recznie")
```

`elif` znaczy: jesli poprzedni warunek nie przeszedl, sprawdz kolejny.

<!-- end_slide -->

# Wciecia sa skladnia

Python nie uzywa `{}` jak Java.

```python
if status == "completed":
    print("inside if")

print("outside if")
```

To, co jest wcieciem pod `if`, nalezy do tej galezi.

<!-- end_slide -->

# Typowy blad: = vs ==

Zle:

```python
if status = "completed":
    print("ok")
```

Dobrze:

```python
if status == "completed":
    print("ok")
```

`=` przypisuje. `==` porownuje.

<!-- end_slide -->

# Jeden rekord jako dict

Jeden order mozemy opisac jako slownik.

```python
order = {
    "order_id": "1001",
    "status": "completed",
    "total_amount": "120.50",
}
```

`dict` to struktura: klucz -> wartosc.

<!-- end_slide -->

# Czytanie wartosci z dict

```python
status = order["status"]
amount_text = order["total_amount"]
```

Pytanie:

```text
Co zwroci order["status"]?
```

Odpowiedz:

```text
"completed"
```

<!-- end_slide -->

# Wiele rekordow jako list

```python
orders = [
    {"order_id": "1001", "status": "completed", "total_amount": "120.50"},
    {"order_id": "1002", "status": "cancelled", "total_amount": "80.00"},
]
```

`list` trzyma wiele elementow.

W tym case: wiele slownikow.

<!-- end_slide -->

# Petla for

Petla przechodzi po elementach listy.

```python
for order in orders:
    print(order["order_id"])
```

Czytaj to tak:

```text
dla kazdego order w orders wykonaj blok kodu
```

<!-- end_slide -->

# Petla + warunek

```python
for order in orders:
    if order["status"] == "completed":
        print(order["order_id"])
```

Pytanie:

```text
Czy cancelled order zostanie wypisany?
```

Nie, bo nie przejdzie warunku.

<!-- end_slide -->

# Liczenie revenue

```python
revenue = 0.0

for order in orders:
    if order["status"] == "completed":
        amount = float(order["total_amount"])
        revenue = revenue + amount
```

To jest najwazniejszy mechanizm tej lekcji.

<!-- end_slide -->

# Checkpoint

Powiedz na glos:

```text
orders to lista.
order to slownik.
for przechodzi po orderach.
if wybiera completed orders.
float zamienia tekst kwoty na liczbe.
```

<!-- end_slide -->

# Funkcja

Funkcja nazywa fragment logiki.

```python
def is_completed(order: dict[str, str]) -> bool:
    return order["status"] == "completed"
```

Nazwa funkcji mowi, co sprawdzamy.

<!-- end_slide -->

# return vs print

```python
def add(a: int, b: int) -> int:
    return a + b
```

`return` oddaje wynik programowi.

```python
result = add(2, 3)
```

`print` tylko pokazuje wartosc czlowiekowi.

<!-- end_slide -->

# Funkcja do kwoty

```python
def parse_amount(value: str) -> float:
    return float(value)
```

Po co taka funkcja?

```text
nazywa intencje
upraszcza petle
latwo ja testowac
```

<!-- end_slide -->

# Funkcja do revenue

```python
def calculate_completed_revenue(orders: list[dict[str, str]]) -> float:
    revenue = 0.0

    for order in orders:
        if is_completed(order):
            revenue = revenue + parse_amount(order["total_amount"])

    return revenue
```

<!-- end_slide -->

# Czytanie CSV

Uzywamy standardowej biblioteki.

```python
import csv
from pathlib import Path
```

Nie potrzebujemy tu jeszcze duzych bibliotek.

<!-- end_slide -->

# csv.DictReader

```python
def read_orders(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)
```

`DictReader` zamienia wiersze CSV na slowniki.

<!-- end_slide -->

# CSV -> list[dict]

```text
orders.csv
  |
  v
csv.DictReader
  |
  v
list[dict[str, str]]
```

Kazdy wiersz CSV staje sie jednym `dict`.

<!-- end_slide -->

# Mini demo flow

```python
orders = read_orders(DATA_DIR / "orders.csv")

completed_revenue = calculate_completed_revenue(orders)
status_counts = count_orders_by_status(orders)
completed_order_ids = collect_completed_order_ids(orders)

print("Completed revenue:", completed_revenue)
```

<!-- end_slide -->

# Zliczanie statusow

```python
counts: dict[str, int] = {}

for order in orders:
    status = order["status"]

    if status not in counts:
        counts[status] = 0

    counts[status] = counts[status] + 1
```

<!-- end_slide -->

# Dlaczego status normalizujemy

```python
def normalize_status(status: str) -> str:
    return status.strip().lower()
```

Przyklady:

```text
" Completed " -> "completed"
"COMPLETED"   -> "completed"
```

<!-- end_slide -->

# Test przez assert

Najprostszy test:

```python
assert normalize_status(" Completed ") == "completed"
assert parse_amount("120.50") == 120.5
```

Jesli warunek jest falszywy, test pada.

<!-- end_slide -->

# pytest mental model

Test to pytanie do kodu.

```python
def test_cancelled_order_is_ignored() -> None:
    orders = [
        {"status": "completed", "total_amount": "100.00"},
        {"status": "cancelled", "total_amount": "50.00"},
    ]

    assert calculate_completed_revenue(orders) == 100.0
```

<!-- end_slide -->

# Najwazniejszy test tej lekcji

```text
completed revenue liczy completed orders
i ignoruje cancelled / refunded / pending
```

To sprawdza logike biznesowa, nie tylko skladnie Pythona.

<!-- end_slide -->

# Typowe bledy

```text
= zamiast ==
brak wciecia
brak float przy kwocie z CSV
print zamiast return
jedna wielka funkcja bez nazwanych krokow
```

<!-- end_slide -->

# Co juz umiemy zrobic

Na labie zbudowalismy male klocki:

```text
normalize_status              porzadkuje tekst statusu
is_completed                  sprawdza, czy order jest completed
parse_amount                  zamienia tekst kwoty na liczbe
calculate_completed_revenue   sumuje kwoty completed orders
read_orders                   czyta CSV do list[dict]
```

Homework to nie jest nowy temat.

Homework to samodzielna wersja tych samych klockow.

<!-- end_slide -->

# Co budujesz w homeworku

Budujesz jeden prosty program:

```text
orders.csv
    |
    v
read_orders()
    |
    v
list[dict]
    |
    v
funkcje z petla for i if
    |
    v
wyniki w terminalu + testy
```

Cel programu:

```text
policzyc metryki dla zamowien ze statusu completed
```

<!-- end_slide -->

# Jakie pliki oddajesz

W katalogu homeworku maja byc te pliki:

```text
homework/lesson_05/
├── python_basics.py       twoj kod
├── test_python_basics.py  pytania do kodu
├── orders.csv             male dane wejsciowe
└── notes.md               krotkie odpowiedzi slowami
```

W wersji z Poetry beda tez:

```text
.python-version
pyproject.toml
poetry.lock
```

<!-- end_slide -->

# Co jest w python_basics.py

Ten plik ma miec funkcje:

```text
normalize_status(status)
is_completed(order)
parse_amount(value)
classify_amount(amount)
calculate_completed_revenue(orders)
count_orders_by_status(orders)
collect_completed_order_ids(orders)
read_orders(path)
main()
```

Czytaj to od gory:

```text
najpierw male funkcje na jednej wartosci,
potem funkcje na liscie orders,
na koncu read_orders i main.
```

<!-- end_slide -->

# Co sprawdzaja testy

Testy maja odpowiedziec na proste pytania:

```text
Czy " Completed " zamienia sie na "completed"?
Czy cancelled order nie liczy sie do revenue?
Czy "120.50" zamienia sie na 120.5?
Czy statusy sa poprawnie zliczone?
Czy lista completed IDs ma tylko completed orders?
```

Test nie jest dodatkiem.

Test pokazuje, ze funkcja naprawde robi to, co mowisz.

<!-- end_slide -->

# Jak poznasz, ze jest dobrze

Z katalogu `homework/lesson_05` uruchamiasz:

```bash
poetry run python python_basics.py
poetry run pytest
```

Oczekujesz dwoch rzeczy:

```text
program wypisuje wyniki dla orders.csv
testy przechodza bez bledu
```

Jesli test pada, czytaj komunikat:

```text
ktora funkcja?
jaka wartosc oczekiwana?
jaka wartosc dostalem?
```

<!-- end_slide -->

# Closing check

Powiedz na glos:

```text
orders.csv to plik tekstowy.
csv.DictReader daje list[dict].
Kazdy order jest dict.
for przechodzi po orderach.
if wybiera completed orders.
float zamienia kwote z tekstu na liczbe.
return oddaje wynik do testu.
```

<!-- end_slide -->

# Nastepna lekcja

Teraz rozumiesz mechanike:

```text
plik -> rekordy -> funkcje -> wynik -> testy
```

W lekcji 06 zrobimy z tego maly pipeline:

```text
extract -> validate -> transform -> load
```
