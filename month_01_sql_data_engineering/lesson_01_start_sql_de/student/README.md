# Dla uczestnika: Lekcja 01 - SQL od podstaw do myslenia Data Engineera

## Otworz i zrob to

1. Uruchom baze SQLite z plikow w [lab/](lab/).
2. Przejdz lekcje ze slajdami.
3. Po lekcji zrob [homework.md](homework.md).

[teoria.md](teoria.md) jest krotka i konkretna. Ma pomoc Ci zrobic lekcje i homework, ale nie jest pelnym kursem SQL. Po lekcji poszerzaj wiedze samodzielnie: dokumentacja SQLite, artykuly o SQL, JOIN, GROUP BY, grain i CTE beda dobrym uzupelnieniem.

Pliki w [lab/](lab/) sa cwiczeniami prowadzacymi do homeworku. Jesli je robisz, wpisujesz odpowiedzi w tych plikach i tez dodajesz je do pull requesta. Najlepsza kolejnosc pracy:

```text
lab/04_sql_basics_extra_tasks.sql  -> zobaczenie danych i proste SELECT-y
lab/02_join_revenue_tasks.sql      -> JOIN, revenue i customer_order_summary
lab/03_modeling_workshop.md        -> grain, ryzyka i walidacje slowami
lab/01_ddl_dml_warmup.sql          -> opcjonalny DDL/DML warm-up
```

## Cel lekcji

Po tej lekcji masz nie tylko znac skladnie SQL. Masz umiec powiedziec:

- co oznacza jeden rekord w tabeli,
- dlaczego join moze zmienic liczbe rekordow,
- kiedy `GROUP BY` zmienia poziom szczegolowosci,
- ze CTE jest dodatkiem, nie wymaganiem podstawowym.

<!-- end_slide -->

## Dlaczego zaczynamy od SQLite

SQLite jest tu tylko startem. Jest szybki, prosty i nie wymaga serwera. Dzieki temu pierwsza lekcja skupia sie na SQL i mysleniu, a nie na konfiguracji serwera, Dockera albo driverow.

Inne narzedzia wroca pozniej. Teraz liczy sie zrozumienie malego modelu danych.

<!-- end_slide -->
## Dataset

Pracujemy na malym sklepie:

- `customers` - klienci,
- `orders` - zamowienia,
- `order_items` - pozycje zamowien,
- `products` - produkty.

Ten dataset jest maly celowo. Masz umiec powiedziec, co oznacza jeden rekord w kazdej tabeli.

<!-- end_slide -->

## Jak uruchomic

Komendy uruchamiaj w terminalu Linux albo WSL Ubuntu. Na Windowsie nie odpalaj ich w PowerShell.

Jesli `sqlite3 --version` nie dziala na Ubuntu/WSL Ubuntu:

```bash
sudo apt update
sudo apt install -y sqlite3
```

Z katalogu `student/lab/`:

```bash
sqlite3 lesson_01.db < schema.sql
sqlite3 lesson_01.db < seed_data.sql
sqlite3 lesson_01.db
```

Mozesz tez uzyc DB Browser for SQLite:

```text
1. Kliknij New Database w lewym gornym rogu.
2. Zapisz plik jako lesson_01.db w katalogu student/lab/.
3. Wejdz w Execute SQL.
4. Wklej i uruchom schema.sql.
5. Wklej i uruchom seed_data.sql.
```

W konsoli SQLite CLI:

```text
.tables
```

Potem uruchom zwykle query SQL:

```sql
SELECT * FROM customers;
SELECT * FROM orders;
```

Reset bazy:

```bash
rm -f lesson_01.db
sqlite3 lesson_01.db < schema.sql
sqlite3 lesson_01.db < seed_data.sql
```

<!-- end_slide -->

## Co oddajesz po lekcji

Oddajesz finalny katalog `homework/lesson_01/` oraz rozwiazane cwiczenia z `student/lab/`.

Prace oddajesz przez pull request na GitHubie. Tam dostaniesz review i poprawki.

Te pliki tworzysz samodzielnie podczas pracy nad homeworkiem:

```text
homework/lesson_01/
├── 01_solution.sql
├── 02_validation_checks.sql
├── 03_grain_map.md
├── 04_data_product_brief.md
└── 05_interview_answers.md
```

Do PR dodaj tez swoje odpowiedzi w plikach:

```text
student/lab/04_sql_basics_extra_tasks.sql
student/lab/02_join_revenue_tasks.sql
student/lab/03_modeling_workshop.md
student/lab/01_ddl_dml_warmup.sql  # opcjonalnie, jesli robiles DDL/DML warm-up
```

Nie dodawaj do PR pliku `lesson_01.db`.

<!-- end_slide -->

## Zasada pracy

Najpierw napisz oczekiwany wynik slowami. Dopiero potem pisz SQL.

Przyklad:

```text
Chce jeden rekord na klienta.
Revenue licze tylko z zamowien paid.
Revenue pochodzi z order_items: quantity * unit_price.
Klienci bez zamowien paid maja zostac w wyniku.
```
