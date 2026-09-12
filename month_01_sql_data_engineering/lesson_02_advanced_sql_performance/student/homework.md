# Praca domowa: Lekcja 02

## Cel

Masz pokazać, że umiesz przetłumaczyć pytanie biznesowe na SQL od pierwszych zasad.

Nie zaczynasz od `EXPLAIN`. Najpierw pytasz:

```text
Co ma oznaczać jeden rekord wyniku?
Z których tabel biorę potrzebne kolumny?
Czy JOIN zmienia grain?
Czy potrzebuję GROUP BY czy window function?
Czy filtr jest częścią definicji metryki?
```

W tej pracy ćwiczysz:

```text
pytanie biznesowe -> grain -> tabele -> join -> filtr -> agregacja/window -> wynik
```

Window functions nie są dodatkiem. To jest główna „advanced” część tej lekcji.

Pracujesz tylko na danych z lekcji:

```text
customers    = klienci
orders       = zamowienia
order_items  = pozycje zamówień
products     = produkty
```

Do zrobienia minimum wystarczy [teoria.md](teoria.md), [README.md](README.md) i finalny homework.

Katalog `lab/` jest tylko krótkim treningiem i drogą dojścia do homeworku. Jeśli chcesz, możesz zrobić lab jako ćwiczenie rozgrzewkowe, ale główny nacisk i główny plik do oddania to homework.

Jeśli robisz lab, wpisuj odpowiedzi w [lab/in_class_tasks.sql](lab/in_class_tasks.sql), ale nie traktuj go jako głównego deliverable. Możesz go dodać do PR jako dodatkowe wsparcie, ale homework jest najważniejszy.

Jeśli utkniesz, najpierw wróć do małych pytań:

```text
Jaki ma być jeden rekord wyniku?
W której tabeli są potrzebne kolumny?
Czy potrzebuję JOIN-a?
Czy JOIN zmienia grain?
Czy potrzebuję GROUP BY czy window function?
Czy filtr jest częścią definicji metryki?
```

## Krok 0: przygotuj bazę

Na Windowsie uruchom to w WSL Ubuntu, nie w PowerShell.

Opcja A: terminal:

```bash
cd student/lab
sqlite3 lesson_02.db < schema.sql
sqlite3 lesson_02.db < seed_data.sql
sqlite3 lesson_02.db
```

Opcja B: DB Browser for SQLite:

```text
1. Otwórz DB Browser for SQLite.
2. Kliknij New Database w lewym górnym rogu.
3. Zapisz plik jako lesson_02.db w katalogu student/lab/.
4. Wejdź w Execute SQL.
5. Wklej zawartość schema.sql i uruchom.
6. Wklej zawartość seed_data.sql i uruchom.
7. Kliknij Write Changes, jeśli program o to prosi.
```

Te dwa pliki tylko przygotowują bazę:

```text
schema.sql    = tworzy tabele i indeksy do ćwiczeń
seed_data.sql = ładuje małe dane treningowe
```

Przygotuj katalog i puste pliki do oddania.

Ważne: zrób to w swoim repo albo katalogu roboczym, w którym oddajesz pracę. Nie twórz `homework/lesson_02/` wewnątrz `student/lab/`.

```bash
mkdir -p homework/lesson_02
touch homework/lesson_02/01_solution.sql
touch homework/lesson_02/02_validation_checks.sql
touch homework/lesson_02/03_grain_map.md
touch homework/lesson_02/04_interview_answers.md
```

Jeśli pracujesz w SQLite CLI, wyjdź z bazy komendą `.quit`, zanim zaczniesz tworzyć pliki homeworku.

Jeśli pracujesz w DB Browser, query możesz pisać i testować w zakładce Execute SQL, ale finalnie zapisz je w plikach z `homework/lesson_02/`.

## Krok 1: zobacz dane i plan

Najpierw sprawdź, jakie tabele i dane są w bazie.

W DB Browser wejdź w zakładkę `Database Structure`.

W SQLite CLI albo DB Browser możesz też użyć zwykłego SQL:

```sql
SELECT name
FROM sqlite_schema
WHERE type = 'table';
```

To jest tylko rozgrzewka, nie glowny artefakt homeworku. Nie musisz zapisywac w `01_solution.sql` prostych query typu `SELECT *` ani samego liczenia rekordow w kazdej tabeli.

W `01_solution.sql` zapisz tylko baseline do planu:

1. Policz liczbę zamówień per `status`.
2. Uruchom `EXPLAIN QUERY PLAN` dla liczby zamówień per `status`.

Przed query dopisz komentarz z grainem wyniku. Napisz query samodzielnie, bez wklejania gotowego rozwiązania.

Po tym kroku powinieneś umieć powiedzieć:

```text
SCAN orders USING COVERING INDEX idx_orders_status = SQLite czyta indeks po statusie.
USE TEMP B-TREE FOR GROUP BY = SQLite robi pomocniczą strukturę do grupowania, jeśli jej potrzebuje.
```

Nie spędzaj na tym długo. Wystarczy, że rozumiesz intuicję planu.

## Krok 2: query biznesowe

W tym samym `01_solution.sql` dopisz:

1. Paid revenue per channel.
2. To samo query przez CTE:
   - `paid_orders`,
   - `order_revenue`,
   - final aggregation per `channel`.
3. Daily paid revenue.
4. Daily paid revenue z running total po `order_date`.
5. Mini-porównanie: revenue per channel bez filtra `paid` i z filtrem `paid`.
6. Ranking channeli po paid revenue przez `RANK()`.

Zasada revenue:

```text
revenue = quantity * unit_price
paid revenue liczymy tylko dla orders.status = 'paid'
```

Najważniejsze: przed każdym query napisz w komentarzu jedno zdanie:

```text
-- Grain wyniku: jeden rekord = ...
```

Dodatkowo przy window function dodaj komentarz:

```text
-- Window function: zachowuję wiersze i liczę metrykę w oknie.
```

## Krok 3: proste checki

W `02_validation_checks.sql` napisz 4 query:

1. Czy `orders.order_id` jest unikalny.
2. Czy `order_items.order_item_id` jest unikalny.
3. Czy `quantity` w `order_items` jest dodatnie.
4. Ile rekordów jest w `orders` przed i po joinie z `order_items`.

Dopisz też 2 krótkie komentarze:

```text
-- Czy join orders -> order_items zmienia grain?
-- Który check pomaga to zobaczyć?
```

Nie chodzi o perfekcyjny system testów. Chodzi o to, żeby zobaczyć, że query można sprawdzać.

## Krok 4: krótki opis grain

W `03_grain_map.md` uzupełnij:

```text
customers: jeden rekord = ...
orders: jeden rekord = ...
order_items: jeden rekord = ...
products: jeden rekord = ...
paid_revenue_per_channel: jeden rekord = ...
daily_paid_revenue: jeden rekord = ...
running_total: jeden rekord = ...
ranked_channel_revenue: jeden rekord = ...
```

Dopisz 3 zdania:

```text
Gdzie join zmienia grain?
Czym różni się GROUP BY od window function?
Dlaczego running total wymaga ORDER BY order_date?
```

## Krok 5: odpowiedzi ustne

W `04_interview_answers.md` odpowiedz krótko na 6 pytań:

1. Jak tłumaczysz pytanie biznesowe na SQL?
2. Czym różni się `GROUP BY` od window function?
3. Co pokazuje `EXPLAIN QUERY PLAN`, a czego nie pokazuje?
4. Dlaczego `SELECT *` jest ryzykowne w data pipeline?
5. Czym różni się `RANK()` od `ROW_NUMBER()`, gdy są remisy?
6. Dlaczego `SUM(total_price_usd) / SUM(stay_length)` może być lepsze niż `AVG(total_price_usd / stay_length)` dla pytania `average price per night`?

Każda odpowiedź: 3-5 zdań. Nie pisz eseju; odpowiedź ma brzmieć tak, jakbyś tłumaczył to na review.

Pytania 1-4 oprzyj na tabelach z tej lekcji: `orders`, `order_items`, `status = 'paid'`, `quantity * unit_price`, running total po `order_date`.

Przy pytaniu 5 pokaż mini-przykład z remisem, np. trzy tytuły albo trzy channele z wynikami `100, 100, 80`.

Pytanie 6 jest celowo interview-style spoza lokalnej bazy. Pokaż mini-przykład liczbowy, np. rezerwacja 1 noc za 100 USD i rezerwacja 30 nocy za 300 USD.

## Co oddać

Oddajesz finalne pliki homeworku. Lab jest opcjonalnym treningiem, który może wspierać Twoje rozwiązanie, ale nie jest głównym celem zadania.

```text
homework/lesson_02/
├── 01_solution.sql
├── 02_validation_checks.sql
├── 03_grain_map.md
└── 04_interview_answers.md
```

Jeśli chcesz, możesz dodać też swoje odpowiedzi z labu:

```text
student/lab/in_class_tasks.sql
```

Ale to jest dodatkowe, nie obowiązkowe.

Nie oddajesz `student/lab/lesson_02.db`.

## Checklista przed oddaniem

- [ ] Query w `01_solution.sql` działają.
- [ ] Każde finalne query ma komentarz z grainem.
- [ ] Checki w `02_validation_checks.sql` są uzupełnione.
- [ ] `03_grain_map.md` i `04_interview_answers.md` są uzupełnione.
- [ ] Do PR nie dodajesz pliku `lesson_02.db`.
