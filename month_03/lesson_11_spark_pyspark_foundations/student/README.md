# Dla uczestnika: Lekcja 11 - Spark i PySpark od podstaw

## Otworz i zrob to

1. Uruchom lokalna sesje Sparka i sprawdz, czy Java dziala.
2. Odczytaj dane z folderu [lab/](lab/).
3. Zrob prosta transformacje Bronze → Silver w pliku [lab/spark_basics.py](lab/spark_basics.py).
4. Finalna praca domowa zapisz w katalogu `homework/lesson_11/`.
5. Po lekcji przejdz [homework.md](homework.md).

Najkrotsza zasada folderow:

```text
student/lab/              = lab online, miejsce do eksperymentow
homework/lesson_11/       = tutaj tworzysz finalne rozwiazanie do review
```

Nie kopiuj katalogu `student/lab/` do `homework/`. Laby zostaja w `student/lab/`, a homework jest osobnym katalogiem na finalne odp.

[teoria.md](teoria.md) jest krotka i konkretna. Ma pomoc Ci zrozumiec why/when/where, ale nie jest pelnym kursem Sparka. Po lekcji dorobisz samodzielnie kilka problemow z dokumentacja, joinami i partitioningiem.

<!-- end_slide -->

## Cel lekcji

Po tej lekcji masz nie tylko umiec uruchomic `SparkSession`. Masz umiec powiedziec:

- kiedy Spark ma sens, a kiedy SQL/Polars wystarcza,
- czym sie roznia transformations i actions,
- jak dziala lazy evaluation,
- kiedy partycjonowanie pomaga, a kiedy tylko komplikuje pipeline,
- jak wyglada prosta transformacja danych z Bronze do Silver w jednym jobie.

<!-- end_slide -->

## Dlaczego zaczynamy od Sparka

Spark nie jest pierwszym narzedziem do wszystkiego. To narzedzie do pracy z duzymi zbiorami danych, w ktorych jedna maszyna nie jest w stanie wykonac transformacji w rozsądanym czasie. W praktyce to jest glowny przejscie z "myslenia lokalnego" do "myslenia rozproszonego".

To jest kluczowy moment w karierze Data Engineera:

- lokalny notebook z CSV na 100 MB → da sie w Pandas / Polars,
- 10 GB, 100 GB, 10 TB → trzeba myslec w partycjach, jobach, DAG, shuffle i memory footprint,
- pipeline musi byc odporny na skalowanie, nie tylko na poprawnosc pojedynczego wyniku.

<!-- end_slide -->

## Dataset

Pracujemy na danych transakcyjnych:

- `orders` / `order_events` / `customers` / `products` w wersji lokalnej,
- wejscie jest zrobione tak, aby bylo proste do zrozumienia,
- to jest minimalny case, w ktorym widać jak dane przechodza z raw do clean i dalej do analityki.

Ten dataset jest mały celowo. Chodzi o to, aby w pierwszej chwili zrozumiec model przetwarzania, a nie zginac w skali i konfiguracji.

<!-- end_slide -->

## Jak uruchomic

Komendy uruchamiaj w terminalu Linux albo WSL Ubuntu.

Jesli `java -version` nie dziala:

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
```

Nastepnie w katalogu z materiałami:

```bash
pip install pyspark==3.5.0
python student/lab/spark_basics.py
```

Dla lokalnego testu Spark można tez uruchomic:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("local_demo") \
    .master("local[2]") \
    .getOrCreate()
```

Warto sprawdzic, czy Spark UI jest dostepne po uruchomieniu joba: `localhost:4040`.

<!-- end_slide -->

## Co oddajesz po lekcji

Oddajesz finalny katalog `homework/lesson_11/`.

Najczęstszy output to:

```text
homework/lesson_11/
├── spark_bronze_to_silver.py
├── tests/
│   └── test_transform.py
├── output/
│   └── silver/
└── README.md
```

Twoje zadanie w praktyce:

- utworzyć `SparkSession`,
- odczytać dane z raw/bronze,
- znormalizować status, typy i format danych,
- usunąć braki danych lub niefunkcyjne rekordy,
- zapisać wynik jako partitioned Parquet / Spark output,
- dodać co najmniej 3 testy logicznych zasad danych.

<!-- end_slide -->

## Zasada pracy

Najpierw napisz oczekiwany wynik slowami. Dopiero potem pisz kod.

Przyklad:

```text
Chce zrobic jeden stable row na zamowienie.
Wymagam status lowercase i trimmed.
Total amount musi byc liczba, nie string.
Rekord bez order_id nie przechodzi do Silver.
```

W PySpark to rozpisanie logiczne jest tak samo ważne jak sam `withColumn()`.

<!-- end_slide -->

## Pytanie kontrolne

Czy wiesz już, czym sie roznia:

- `Transformation` vs `Action`?
- `select` vs `withColumn`?
- `repartition` vs `coalesce`?
- `partitionBy` vs `bucket by`?

Jesli tak, to masz dobry poziom wejscia do kolejnych lekcji. Jesli nie, wróc do [teoria.md](teoria.md) i przeczytaj to jeszcze raz w kontekście konkretnego joba.

<!-- end_slide -->
