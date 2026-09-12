# Teoria: Lekcja 05 - Wprowadzenie do Pythona dla Data Engineeringu

## Cel materiału

Ten materiał wprowadza podstawy Pythona w kontekście pracy z małymi danymi tabelarycznymi. Celem nie jest poznanie całego języka, tylko zrozumienie minimalnego zestawu mechanizmów potrzebnych do napisania prostego programu Data Engineering.

Po tej lekcji uczestnik powinien umieć:

```text
uruchomić plik .py,
rozpoznać podstawowe typy danych,
przejść po liście rekordów,
użyć warunku if,
zapisać logikę w funkcjach,
wczytać mały plik CSV,
policzyć prostą metrykę,
napisać podstawowy test.
```

## Kontekst ekosystemu

> Czytaj to pierwsze.

W Data Engineeringu Python często występuje jako język, który opisuje proces pracy z danymi:

```text
pobierz dane,
sprawdź dane,
przekształć rekordy,
policz wynik,
zapisz albo pokaż rezultat.
```

Na późniejszych etapach pojawią się biblioteki, orkiestratory i większe systemy. W tej lekcji pracujemy świadomie bez dużych bibliotek, żeby zobaczyć podstawową mechanikę programu.

Najważniejsze pojęcia:

| Pojęcie | Znaczenie w tej lekcji |
|---|---|
| Program | Lista instrukcji wykonywanych przez komputer |
| Zmienna | Nazwa przypisana do wartości |
| Typ danych | Informacja, czy wartość jest tekstem, liczbą, listą itd. |
| Rekord | Jeden wiersz danych reprezentowany jako `dict` |
| Lista rekordów | Wiele rekordów reprezentowanych jako `list[dict]` |
| Funkcja | Nazwany fragment logiki, który może zwrócić wynik |
| Test | Automatyczne pytanie: czy kod zwraca oczekiwany wynik? |

## ELI5

Program w Pythonie to przepis. Dane są składnikami, instrukcje są krokami, a wynik jest potrawą, którą dostajesz na końcu.

W tej lekcji przykład jest prosty:

```text
orders.csv -> lista zamówień -> wybierz completed -> policz revenue
```

Python nie zgaduje, co autor miał na myśli. Jeśli kwota przyszła z CSV jako tekst, trzeba ją zamienić na liczbę. Jeśli status ma spacje albo wielkie litery, trzeba go uporządkować przed porównaniem.

## First Principles

Każdy prosty program do danych można rozbić na cztery pytania:

```text
1. Jakie dane mam na wejściu?
2. W jakim typie są te dane?
3. Jaką regułę chcę zastosować?
4. Jaki wynik ma zwrócić program?
```

Dla tej lekcji:

```text
Dane wejściowe: orders.csv
Rekord: dict z polami order_id, status, total_amount
Reguła: revenue liczymy tylko dla statusu completed
Wynik: liczba typu float
```

To jest ważniejsze niż zapamiętanie składni na pamięć. Składnia jest sposobem zapisania reguły.

## Podstawowy model danych

W tej lekcji jeden wiersz CSV traktujemy jako jeden słownik:

```python
order = {
    "order_id": "1001",
    "status": "completed",
    "total_amount": "120.50",
}
```

Wiele wierszy CSV traktujemy jako listę słowników:

```python
orders = [
    {"order_id": "1001", "status": "completed", "total_amount": "120.50"},
    {"order_id": "1002", "status": "cancelled", "total_amount": "80.00"},
]
```

Wzorzec do zapamiętania:

```text
orders = lista
order = jeden element listy
order["status"] = wartość z jednego pola rekordu
```

## Typy danych

Najczęstsze typy w tej lekcji:

| Typ | Przykład | Kiedy używać |
|---|---|---|
| `str` | `"completed"` | Tekst, np. status albo ID z CSV |
| `int` | `1001` | Liczba całkowita |
| `float` | `120.50` | Kwota albo dystans |
| `bool` | `True` | Wynik pytania tak/nie |
| `list` | `[order1, order2]` | Wiele elementów |
| `dict` | `{ "status": "completed" }` | Rekord klucz -> wartość |

CSV jest plikiem tekstowym. Dlatego wartości z CSV często przychodzą jako `str`, nawet jeśli wyglądają jak liczby.

Przykład:

```python
amount_text = "120.50"
amount = float(amount_text)
```

## Warunki

Warunek wybiera, która część kodu ma się wykonać.

```python
if order["status"] == "completed":
    print("count this order")
else:
    print("ignore this order")
```

W Pythonie wcięcie jest częścią składni. Kod pod `if` musi być wcięty.

Najczęstsza pomyłka:

```text
=   przypisuje wartość
==  porównuje wartości
```

## Pętle

Pętla `for` przechodzi po elementach kolekcji.

```python
for order in orders:
    print(order["order_id"])
```

Czytaj to tak:

```text
dla każdego order w orders wykonaj blok kodu
```

W Data Engineeringu to podstawowy wzorzec przy pracy z małą listą rekordów.

## Funkcje

Funkcja nazywa fragment logiki.

```python
def is_completed(order: dict[str, str]) -> bool:
    return order["status"] == "completed"
```

Dobra funkcja:

```text
ma jasną nazwę,
przyjmuje dane przez parametry,
zwraca wynik przez return,
robi jedną rzecz.
```

`return` jest ważniejszy niż `print`, bo wynik zwrócony przez funkcję można użyć dalej i przetestować.

## Przykład: completed revenue

Najważniejsza logika lekcji:

```python
def calculate_completed_revenue(orders: list[dict[str, str]]) -> float:
    revenue = 0.0

    for order in orders:
        if order["status"] == "completed":
            revenue = revenue + float(order["total_amount"])

    return revenue
```

Co robi ten kod:

```text
zaczyna od revenue = 0.0,
przechodzi po każdym zamówieniu,
sprawdza status,
zamienia kwotę z tekstu na float,
dodaje kwotę tylko dla completed,
zwraca wynik.
```

## Czytanie CSV

Do małego CSV wystarczy standardowa biblioteka Pythona.

```python
import csv
from pathlib import Path


def read_orders(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)
```

Co tu się dzieje:

```text
Path opisuje ścieżkę do pliku,
with bezpiecznie otwiera i zamyka plik,
csv.DictReader czyta wiersze jako słowniki,
list(reader) zamienia wynik na listę rekordów.
```

## Testowanie

Test sprawdza, czy funkcja zwraca oczekiwany wynik.

```python
def test_completed_revenue_ignores_cancelled_orders() -> None:
    orders = [
        {"status": "completed", "total_amount": "100.00"},
        {"status": "cancelled", "total_amount": "50.00"},
    ]

    assert calculate_completed_revenue(orders) == 100.0
```

Test jest wartościowy, bo sprawdza regułę biznesową:

```text
cancelled order nie powinien zwiększać revenue
```

## Socratic Questions

**Dlaczego `total_amount` z CSV trzeba zamienić na `float`?**

Bo CSV przechowuje tekst. Wartość `"120.50"` wygląda jak liczba, ale dla Pythona jest tekstem, dopóki nie wykonasz `float("120.50")`.

**Dlaczego funkcja powinna zwracać wynik przez `return`?**

Bo `return` oddaje wartość programowi. Dzięki temu wynik można przekazać dalej albo sprawdzić w teście. `print` tylko pokazuje tekst człowiekowi.

**Dlaczego nie zaczynamy od Pandas?**

Bo Pandas ukrywa pętle, typy i warunki za wysokopoziomowymi operacjami. To jest przydatne później, ale najpierw trzeba rozumieć, co dzieje się na poziomie pojedynczego rekordu.

**Dlaczego nie zaczynamy od klas?**

Bo na pierwszej lekcji najważniejsze są funkcje, typy, pętle i rekordy. Klasy pojawią się wtedy, gdy zaczniemy modelować większe struktury danych.

## STALY PATTERN - zapamietaj to

```text
PYTHON BASICS FOR DATA - staly pattern

=== Input ===
orders = read_orders(Path("orders.csv"))
# Dane z pliku CSV wchodzą do programu jako lista rekordów.

=== Record ===
order = {"status": "completed", "total_amount": "120.50"}
# Jeden dict reprezentuje jeden rekord danych.

=== Condition ===
if order["status"] == "completed":
    ...
# if wybiera rekordy, które spełniają regułę.

=== Conversion ===
amount = float(order["total_amount"])
# Kwota z CSV jest tekstem; przed sumowaniem zamieniamy ją na float.

=== Loop ===
revenue = 0.0
for order in orders:
    if order["status"] == "completed":
        revenue = revenue + float(order["total_amount"])
# Pętla przechodzi po wszystkich rekordach i sumuje wybrane wartości.

=== Function ===
def calculate_completed_revenue(orders: list[dict[str, str]]) -> float:
    revenue = 0.0
    for order in orders:
        if order["status"] == "completed":
            revenue = revenue + float(order["total_amount"])
    return revenue
# Funkcja nazywa logikę i zwraca wynik do programu lub testu.

=== Test ===
assert calculate_completed_revenue(orders) == 100.0
# Test sprawdza, czy reguła działa na kontrolnym przykładzie.

CHECKLIST:
[ ] Czy wiem, jaki typ ma moja wartość?
[ ] Czy rekord jest słownikiem, a zbiór rekordów listą?
[ ] Czy porównuję przez ==, a nie przypisuję przez =?
[ ] Czy wartości liczbowe z CSV zamieniam na int albo float?
[ ] Czy funkcja zwraca wynik przez return?
[ ] Czy mam test dla najważniejszej reguły biznesowej?
```

## Typowe błędy i jak je rozpoznać

| Błąd | Objaw | Jak naprawić |
|---|---|---|
| `=` zamiast `==` | Python zgłasza błąd składni w warunku | Użyj `==` do porównania |
| Brak wcięcia | Kod nie należy do `if`, `for` albo `def` | Wcięty blok daj pod instrukcją z `:` |
| Dodawanie tekstu zamiast liczb | Wynik jest błędny albo pojawia się `TypeError` | Użyj `float(...)` albo `int(...)` |
| `print` bez `return` | Test dostaje `None` | Zwróć wynik przez `return` |
| Jedna wielka funkcja | Kod trudno testować | Podziel na małe funkcje |

## Minimalny standard oddania

Po lekcji kod powinien spełniać te wymagania:

```text
funkcje mają type hints,
revenue liczy tylko completed orders,
CSV jest czytany przez csv.DictReader,
kwoty z CSV są konwertowane na float,
testy sprawdzają najważniejsze reguły,
notes.md pokazuje rozumienie, nie tylko definicje.
```
