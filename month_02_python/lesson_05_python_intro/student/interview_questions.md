# Interview questions: Lekcja 05

Odpowiadaj na glos. Kazda odpowiedz powinna miec 30-60 sekund.

## Pytania

1. Jak opiszesz jeden rekord zamowienia jako `dict`?
2. Czym rozni sie `list` od `dict`?
3. Do czego sluzy `if / elif / else`?
4. Dlaczego dane z CSV czesto sa tekstem?
5. Po co funkcji `return`?
6. Jak dziala petla `for order in orders`?
7. Jaki test napisalbys dla funkcji liczacej completed revenue?

## Dobra odpowiedz - wzorzec

```text
Lista trzyma wiele elementow, a dict trzyma jeden rekord jako klucz -> wartosc.
W CSV jeden wiersz moge reprezentowac jako dict, np. order["status"].
Petla for przechodzi po kazdym order i pozwala sprawdzic warunek.
Jesli status jest completed, zamieniam total_amount z tekstu na float i dodaje do sumy.
Test powinien sprawdzic konkretny wynik, np. ze cancelled order nie wchodzi do revenue.
```