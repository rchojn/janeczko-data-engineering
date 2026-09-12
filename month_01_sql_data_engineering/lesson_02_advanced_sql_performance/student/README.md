# Dla uczestnika: Lekcja 02 - zaawansowany SQL i performance mindset

## Co robisz w tej lekcji

Ta lekcja uczy, jak patrzeć na SQL jak Data Engineer:

```text
wynik -> grain -> czytelność -> EXPLAIN -> koszt -> jedna poprawka
```

Nie chodzi o to, żeby znać magiczne sztuczki performance. Chodzi o to, żeby umieć wyjaśnić, co query liczy, jaką pracę robi silnik i jaki masz dowód, że poprawka ma sens.

## Co otworzyć

1. Otwórz [teoria.md](teoria.md) jako główny materiał lekcji.
2. Jeśli wolisz wersję do czytania albo wysłania dalej, użyj [teoria.pdf](teoria.pdf).
3. Uruchom SQLite lab z plików w [lab/](lab/).
4. Wykonaj zadania z [lab/in_class_tasks.sql](lab/in_class_tasks.sql).
5. Po lekcji zrób [homework.md](homework.md).
6. Przy zadaniach zapisuj krótko: cel, grain, tabele, koszt i check poprawności.

`README.md` jest tylko mapą lekcji. Treść, przykłady i rytm pracy są w [teoria.md](teoria.md).

## Co masz zrozumieć

Po tej lekcji masz umieć powiedzieć:

- dlaczego najpierw sprawdzasz poprawność metryki, a dopiero potem performance,
- co oznacza grain wyniku i dlaczego jest ważny po joinach,
- co pokazuje `EXPLAIN QUERY PLAN`, a czego nie pokazuje,
- kiedy `SELECT *` jest wygodne, a kiedy jest ryzykiem w pipeline,
- jak CTE pomaga nazwać kroki query,
- jak działa running total przez window function,
- czym różni się `RANK()` od `ROW_NUMBER()`,
- dlaczego przy dużej skali pytasz o partition key i aggregate layer,
- dlaczego weighted average bywa lepsze niż `AVG(...)`.

## Jak uruchomić lab

Z katalogu `student/lab/`:

```bash
sqlite3 lesson_02.db < schema.sql
sqlite3 lesson_02.db < seed_data.sql
sqlite3 lesson_02.db < in_class_tasks.sql
```

Interaktywnie:

```bash
sqlite3 lesson_02.db
```

Reset:

```bash
rm -f lesson_02.db
sqlite3 lesson_02.db < schema.sql
sqlite3 lesson_02.db < seed_data.sql
```

## Materiały rekomendowane

Wybierz jedno źródło jako kontekst, nie jako pełny kurs:

- [SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) - oficjalne źródło do tego, co pokazuje SQLite.
- [Use The Index, Luke: SQL execution plans](https://use-the-index-luke.com/sql/explain-plan) - intuicja, po co czytać plan query.
- [Mode SQL Tutorial: SQL window functions](https://mode.com/sql-tutorial/sql-window-functions/) - powtórka window functions przed kosztem sortowania.
- YouTube: kanał [Data With Zach](https://www.youtube.com/@datawithzach), temat `SQL optimization` albo `analytical SQL` - oglądaj po to, żeby umieć nazwać koszt: scan, join, sort, window.
