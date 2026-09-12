# Interview questions: Lekcja 08

1. Jak wyglada maly produkcyjny projekt Python ETL?
2. Po co `src/` layout?
3. Dlaczego CLI jest lepsze niz edycja zmiennych w kodzie?
4. Co logujesz w pipeline runie?
5. Kiedy retry pomaga, a kiedy szkodzi?
6. Jak testujesz transformacje bez prawdziwego API?
7. Co powinno byc w runbooku dla pipeline'u?

Dobra odpowiedz: pokaz strukture projektu, opis flow runu i wspomnij o testach oraz runbooku.

---

## Pytania — Python internals (czesto na rekrutacji)

8. Co to jest closure?

   Funkcja ktora "zapamietuje" zmienne z zewnetrznego scope'u.
   Przyklad z tego kodu: `operation()` wewnatrz `read_json_records` pamięta `path` bez argumentu.
   Klasyczne uzycie: factory functions, dekoratory, retry patterns.

9. Czym rozni sie generator od list comprehension?

```python
[x*2 for x in range(1000000)]  # lista — cala w RAM
(x*2 for x in range(1000000))  # generator — oblicza element po elemencie
```

   W pipeline'ach sum(), any(), all() akceptuja generator — nie potrzebujesz listy posredniej.

10. Co to TypeVar i po co?

    Pozwala napisac funkcje generyczna ktora dziala dla wielu typow bez utraty informacji typowej.
    `Callable[[], T] -> T` mowi: "zwracam to samo co dostaje". Bez TypeVar musialbys zwrocic `Any`.

11. Dlaczego `if __name__ == "__main__"` jest wazne w testach?

    Gdy importujesz modul w tescie, Python NIE uruchamia tego bloku.
    Bez guardu: kazdy `import pipeline` startowałby cały pipeline — testy by padaly.
