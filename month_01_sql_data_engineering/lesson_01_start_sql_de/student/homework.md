# Praca domowa: Lekcja 01

## Cel

Masz pokazac, ze rozumiesz podstawy SQL na malym modelu danych.

Nie robimy jeszcze duzego projektu. Pracujesz tylko na danych z lekcji:

```text
customers    = klienci
orders       = zamowienia
order_items  = pozycje zamowien
products     = produkty
```

Do zrobienia minimum wystarczy [teoria.md](teoria.md), [README.md](README.md) i cwiczenia pomocnicze z [lab/](lab/).

[teoria.md](teoria.md) jest krotka i konkretna. Nie jest encyklopedia SQL. Po lekcji poszerzaj wiedze samodzielnie w internecie: doczytaj szczegolnie `JOIN`, `GROUP BY`, grain, walidacje i CTE. W homeworku nie kopiuj gotowych rozwiazan; chodzi o to, zebys rozumial swoje query.

Katalog `lab/` to trening i droga dojscia do homeworku. Jesli robisz laby, wpisuj odpowiedzi w plikach z `student/lab/` i dodaj je do pull requesta razem z finalnym homeworkiem.

Jesli utkniesz, uzyj tylko tych fragmentow labow:

```text
Zobacz dane           -> lab/04_sql_basics_extra_tasks.sql, zadania 1-6
Revenue i joiny       -> lab/02_join_revenue_tasks.sql, zadania 0-8
Grain i walidacje     -> lab/03_modeling_workshop.md
```

Jesli utkniesz, najpierw wroc do malych query. Nie przeskakuj od razu do finalnego SELECT-a.

## Krok 0: przygotuj baze

Na Windowsie uruchom to w WSL Ubuntu, nie w PowerShell.

Opcja A: terminal:

```bash
cd student/lab
sqlite3 lesson_01.db < schema.sql
sqlite3 lesson_01.db < seed_data.sql
sqlite3 lesson_01.db
```

Opcja B: DB Browser for SQLite:

```text
1. Otworz DB Browser for SQLite.
2. Kliknij New Database w lewym gornym rogu.
3. Zapisz plik jako lesson_01.db w katalogu student/lab/.
4. Wejdz w Execute SQL.
5. Wklej zawartosc schema.sql i uruchom.
6. Wklej zawartosc seed_data.sql i uruchom.
7. Kliknij Write Changes, jesli program o to prosi.
```

Te dwa pliki tylko przygotowuja baze:

```text
schema.sql    = tworzy tabele: customers, products, orders, order_items
seed_data.sql = laduje male dane treningowe do tych tabel
```

Przygotuj tez katalog i puste pliki do oddania.

Wazne: zrob to w swoim repo albo katalogu roboczym, w ktorym oddajesz prace. Nie tworz `homework/lesson_01/` wewnatrz `student/lab/`.

```bash
mkdir -p homework/lesson_01
touch homework/lesson_01/01_solution.sql
touch homework/lesson_01/02_validation_checks.sql
touch homework/lesson_01/03_grain_map.md
touch homework/lesson_01/04_data_product_brief.md
touch homework/lesson_01/05_interview_answers.md
```

Jesli pracujesz w SQLite CLI, wyjdz z bazy komenda `.quit`, zanim zaczniesz tworzyc pliki homeworku.

Jesli pracujesz w DB Browser, query mozesz pisac i testowac w zakladce Execute SQL, ale finalnie zapisz je w plikach z `homework/lesson_01/`.

## Krok 1: zobacz dane

Najpierw sprawdz, jakie tabele sa w bazie:

```text
SQLite CLI: wpisz .tables
DB Browser: wejdz w zakladke Database Structure
```

Nie wklejaj `.tables` w DB Browser do zakladki Execute SQL. To komenda SQLite CLI, nie zwykle query SQL.

Potem w `01_solution.sql` napisz query:

1. Policz rekordy w kazdej tabeli.
2. Pokaz wszystkie rekordy z `customers`.
3. Pokaz wszystkie rekordy z `orders`.
4. Pokaz wszystkie rekordy z `order_items`.
5. Pokaz wszystkie rekordy z `products`.

Po tym kroku masz umiec powiedziec, co oznacza jeden rekord w kazdej tabeli.

## Krok 2: podstawowe query biznesowe

W tym samym `01_solution.sql` dopisz:

1. Zamowienia ze statusem `paid`.
2. Liczbe zamowien dla kazdego statusu.
3. `customers` polaczone z `orders`.
4. Revenue/przychod dla kazdego zamowienia.
5. Revenue/przychod dla kazdego klienta, tylko dla zamowien `paid`.
6. Finalne query `customer_order_summary`.

Finalny wynik ma miec grain:

```text
jeden rekord = jeden klient
```

Kolumny finalnego wyniku:

```text
customer_id
customer_name
orders_count
total_revenue
last_order_date
```

Zasada revenue:

```text
revenue = quantity * unit_price
liczymy tylko zamowienia ze statusem paid
```

## Krok 3: proste checki

W `02_validation_checks.sql` napisz 4 query:

1. Czy `customers.customer_id` jest unikalny.
2. Czy `orders.order_id` jest unikalny.
3. Czy `quantity` w `order_items` jest dodatnie.
4. Ile rekordow jest w `orders` przed i po joinie z `order_items`.

Nie chodzi o perfekcyjny system testow. Chodzi o to, zeby zobaczyc, ze query mozna sprawdzac.

## Krok 4: krotki opis grain

W `03_grain_map.md` uzupelnij:

```text
customers: jeden rekord = ...
orders: jeden rekord = ...
order_items: jeden rekord = ...
products: jeden rekord = ...
customer_order_summary: jeden rekord = ...
```

Dopisz 2 zdania:

```text
Gdzie join moze zwiekszyc liczbe rekordow?
Ktory join moze zgubic klienta bez zamowien?
```

## Krok 5: mini brief

W `04_data_product_brief.md` odpowiedz krotko:

```text
Pytanie biznesowe:
Dla kogo jest wynik:
Tabele zrodlowe:
Tabela wynikowa:
Grain wyniku:
Metryki:
Najwazniejsze zalozenie:
Najlatwiejszy blad:
```

Dla `customer_order_summary` tabelami zrodlowymi sa `customers`, `orders` i `order_items`. Tabela `products` jest w bazie do ogladania danych i dodatkowych cwiczen, ale nie jest potrzebna do finalnego summary klientow.

## Krok 6: odpowiedzi ustne

W `05_interview_answers.md` odpowiedz krotko na 2 pytania:

1. Co moze pojsc zle przy joinie `orders` i `order_items`?
2. Co to jest grain tabeli i dlaczego ma znaczenie?

Kazda odpowiedz: 5-8 zdan, na przykladzie tabel z tej lekcji.

## Jak oddac prace przez GitHub

Prace oddajesz jako pull request. Bede sprawdzal kod i komentarze na GitHubie.

W swoim repo albo forku zrob osobny branch:

```bash
git checkout -b lesson-01-homework
git add homework/lesson_01
git add student/lab/04_sql_basics_extra_tasks.sql
git add student/lab/02_join_revenue_tasks.sql
git add student/lab/03_modeling_workshop.md
# opcjonalnie, jesli robiles warm-up DDL/DML:
git add student/lab/01_ddl_dml_warmup.sql
git commit -m "Add lesson 01 homework"
git push -u origin lesson-01-homework
```

Potem na GitHubie kliknij `Compare & pull request` i utworz PR.

W opisie PR napisz krotko:

```text
Co zrobilem:
Co bylo trudne:
Czego nie jestem pewien:
```

Nie dodawaj do PR pliku `lesson_01.db`. To lokalna baza do cwiczen, nie plik z rozwiazaniem.

## Co oddac

Oddajesz finalne pliki homeworku oraz rozwiazane laby, ktore pokazale jak doszedles do wyniku.

Finalne pliki tworzysz samodzielnie w swoim repo albo katalogu roboczym.

Oddaj katalog:

```text
homework/lesson_01/
├── 01_solution.sql
├── 02_validation_checks.sql
├── 03_grain_map.md
├── 04_data_product_brief.md
└── 05_interview_answers.md
```

Oddaj tez swoje odpowiedzi w labach:

```text
student/lab/04_sql_basics_extra_tasks.sql
student/lab/02_join_revenue_tasks.sql
student/lab/03_modeling_workshop.md
student/lab/01_ddl_dml_warmup.sql  # opcjonalnie, jesli robiles warm-up
```

Nie oddajesz `student/lab/lesson_01.db`.

## Wersja ambitna

Tylko po zrobieniu minimum:

1. Przepisz finalne query na CTE.
2. Znajdz produkty, ktore nigdy nie zostaly kupione w zamowieniu `paid`.

## Checklista przed oddaniem

- [ ] Baza jest utworzona z `schema.sql` i `seed_data.sql`.
- [ ] Query w `01_solution.sql` dzialaja od zera.
- [ ] Finalny wynik ma jeden rekord na klienta.
- [ ] Revenue liczy `quantity * unit_price`.
- [ ] Revenue liczy tylko `status = 'paid'`.
- [ ] `02_validation_checks.sql` ma 4 proste checki.
- [ ] Umiesz powiedziec, dlaczego join `orders -> order_items` moze zwiekszyc liczbe rekordow.
