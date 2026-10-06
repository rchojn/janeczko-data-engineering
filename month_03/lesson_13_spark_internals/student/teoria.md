# Teoria: Lekcja 13 - Spark Internals

Ten plik jest checklista do zrozumienia homeworku i labu.
Nie uczysz sie tu skladni PySpark dla samej skladni.
Uczysz sie myslec kosztem wykonania.

Minimum tej lekcji:

```text
1. Umiesz nazwac job, stage, task i partition.
2. Rozumiesz narrow vs wide transformations.
3. Rozumiesz shuffle i jego koszt.
4. Potrafisz wykryc skew.
5. Wiesz kiedy broadcast join jest lepszy.
6. Umiesz przeczytac explain() i Spark UI.
7. Umiesz uzasadnic cache i liczbe partycji.
```

## 1. ELI5

Spark to nie jest jedna duza petla po danych.
Spark dzieli prace na kawalki, uruchamia je rownolegle i czasem musi przenosic dane miedzy workerami.

To przenoszenie jest drogie.
Najczesciej nie przegrywasz przez "zly Python".
Przegrywasz przez:

- zly rozklad danych,
- za duzo shuffle,
- zla strategie joina,
- jedna goraca wartosc klucza,
- zbyt agresywne albo bezsensowne cache.

## 2. Model mentalny

```text
Job       = cala praca odpalona przez action
Stage     = fragment joba miedzy shuffle
Task      = praca na jednej partycji
Partition = kawalek danych
Driver    = koordynator
Executor  = proces wykonujacy taski
```

Jesli jeden task trwa 10x dluzej niz inne, to nie masz "troche wolnego Sparka".
Masz konkretny bottleneck w rozkladzie pracy.

## 3. Narrow vs wide transformations

Narrow transformation:

```text
jeden output partition zalezy od jednego input partition
```

Przyklady:

- `select`,
- `withColumn`,
- `filter`,
- czesc `map`-like operacji.

Wide transformation:

```text
jeden output partition zalezy od wielu input partitions
```

Przyklady:

- `groupBy`,
- `join`,
- `distinct`,
- `orderBy`.

To jest klucz, bo wide transformations zwykle oznaczaja shuffle.

## 4. Shuffle

Shuffle to przesuniecie danych miedzy executorami.

Najprostszy model kosztu:

```text
serialize -> write -> network -> read -> deserialize
```

To boli, bo zuzywa:

- CPU,
- dysk,
- siec,
- synchronizacje miedzy stage.

Dlatego pytanie nie brzmi tylko:

```text
Czy query jest poprawne?
```

Tylko:

```text
Czy query zmusza cluster do drogiego przemieszczania danych?
```

## 5. Skew

Skew to nierowny rozklad danych po kluczu.

Przyklad:

```text
US = 180 000
PL = 10 000
DE = 10 000
```

Technicznie wszystko dziala.
Ale jedna partycja dostaje ogrom pracy, a reszta workerow konczy szybko i czeka.

Wykrycie:

```python
df.groupBy("country").count().orderBy(F.desc("count")).show()
```

W Spark UI sygnal jest prosty:

```text
jeden albo kilka taskow trwa wyraznie dluzej niz reszta
```

## 6. Broadcast join

Jesli jedna tabela jest mala, nie chcesz przerzucac obu przez siec.
Chcesz wyslac mala tabele do kazdego executora.

```python
df_large.join(F.broadcast(df_small), "key")
```

To ma sens, gdy:

- lookup table jest mala,
- join key jest sensowny,
- koszt broadcastu jest mniejszy niz koszt shuffle obu tabel.

To nie ma sensu, gdy:

- "mala" tabela juz nie jest mala,
- executor memory jest napiety,
- join i tak robi dalszy duzy shuffle po agregacji.

## 7. AQE

Adaptive Query Execution to runtime optimization.

W praktyce AQE potrafi:

- zredukowac liczbe partycji po shuffle,
- zmienic join strategy,
- rozbic skewed partycje.

Wniosek praktyczny:

```text
Najpierw wlacz AQE.
Dopiero potem recznie komplikuj pipeline.
```

## 8. Liczba partycji

Za malo partycji:

- slabe wykorzystanie rownoleglosci,
- za duzo pracy na task.

Za duzo partycji:

- scheduler overhead,
- zbyt wiele malych taskow,
- niepotrzebny koszt shuffle i output files.

Pytanie kontrolne:

```text
Czy ta liczba partycji sluzy compute,
czy tylko przypadkiem wyszla z defaultu?
```

## 9. Cache i persistence

Cache pomaga wtedy, gdy ten sam DataFrame liczysz wiele razy.

Nie pomaga, gdy:

- uzywasz go raz,
- brakuje memory,
- cached data wypycha cos wazniejszego,
- dane i tak od razu leca dalej do jednego outputu.

Wzorzec:

```text
Powtorne wykorzystanie + kosztowne przeliczenie = candidate do cache
```

## 10. Jak czytac explain()

Szukaj tych slow:

```text
Exchange          = shuffle
BroadcastHashJoin = broadcast join
SortMergeJoin     = drozszy join obu duzych tabel
HashAggregate     = agregacja
AdaptiveSparkPlan = AQE aktywne
```

Nie chodzi o to, zeby znac caly plan na pamiec.
Masz umiec znalezc najdrozsze decyzje fizyczne.

## 11. Jak czytac Spark UI

Najpierw:

1. znajdz najwolniejszy job,
2. wejdz w stage details,
3. zobacz task duration,
4. sprawdz shuffle read/write,
5. porownaj najwolniejszy task do mediany.

Jesli jeden task odstaje mocno, podejrzewaj skew.
Jesli caly stage ma duzy shuffle, podejrzewaj join / aggregation cost.

## 12. Recipe diagnozy wolnego joba

```text
1. explain(mode="formatted")
2. Czy widze Exchange?
3. Czy moge uzyc broadcast?
4. Czy klucz ma skew?
5. Czy AQE jest wlaczone?
6. Czy liczba partycji ma sens?
7. Czy cache jest uzasadniony?
8. Czy write nie tworzy zbyt wielu malych plikow?
```

## 13. Anti-patterny

1. Strojenie losowych configow bez planu i bez Spark UI.
2. Broadcast wszystkiego "bo szybciej".
3. Cache wszedzie.
4. Ignorowanie skew, bo query jest logicznie poprawne.
5. Ocenianie performance tylko po czasie lokalnego runa.
6. Zostawienie defaultow partycji bez myslenia o wolumenie.

## 14. Closing check

Powiedz na glos:

```text
Wolny Spark job to zwykle nie problem skladni.
To problem fizycznego planu wykonania:
shuffle, skew, join strategy, partitions albo memory.
```

Jesli umiesz to obronic na prostym demie, lekcja ma sens.
