---
title: Lekcja 13 - Zarzadzanie pamiecia, Shuffle, Broadcast Joins i Skew
author: Data Engineering Course
date: 2026-09-10
---

# Lekcja 13

Zarzadzanie pamiecia, Shuffle, Broadcast Joins i Skew

```text
To sa 4 rzeczy, przez ktore Spark job nagle robi sie wolny,
drozszy i mniej przewidywalny.
```

<!-- end_slide -->

# Agenda

```text
1. Memory management
2. Shuffle
3. Broadcast joins
4. Skew i jego naprawa
5. Recipe diagnozy
```

<!-- end_slide -->

# Problem biznesowy

Masz pipeline, ktory logicznie jest poprawny.
Na malych danych dziala dobrze.
Przy skali zaczyna bolec:

```text
5 min -> 25 min -> timeout
```

Najczesciej przyczyna nie jest w `select`, tylko w tym:

- jak Spark trzyma dane w pamieci,
- kiedy musi przetasowac dane,
- jak wybiera strategie joina,
- czy rozklad kluczy nie jest nierowny.

<!-- end_slide -->

# First principle

```text
Performance Spark to fizyka danych:
RAM, dysk, siec i nierowny rozklad pracy.
```

Nie pytasz najpierw:

```text
Jakiego configa jeszcze sprobowac?
```

Najpierw pytasz:

```text
Gdzie pipeline zuzywa pamiec?
Gdzie robi shuffle?
Czy join jest tani?
Czy wszystkie taski maja podobna ilosc pracy?
```

<!-- end_slide -->

# Minimalny model wykonania

```text
Job
  -> Stage
      -> Task
          -> Partition
```

Najwazniejsze zdanie tej lekcji:

```text
Stage konczy sie tam, gdzie Spark musi zrobic Exchange danych.
```

<!-- end_slide -->

# Czesc 1 - Zarzadzanie pamiecia

Pamiec w Spark nie sluzy tylko do cache.
Pamiec jest potrzebna tez do:

- shuffle buffers,
- sortowania,
- hash aggregations,
- hash joins,
- broadcast variables,
- cached DataFrames.

<!-- end_slide -->

# Dwa typy pamieci, ktore musisz rozumiec

```text
Execution memory = runtime obliczen
Storage memory   = cache / persist danych
```

Execution memory idzie na:

- join,
- groupBy,
- sort,
- shuffle.

Storage memory idzie na:

- cache(),
- persist(),
- broadcast data trzymane do reuse.

<!-- end_slide -->

# Co sie dzieje, gdy brakuje pamieci

Spark nie zawsze od razu pada.
Najpierw zwykle robi cos gorszego:

```text
memory pressure
  -> spill to disk
  -> wiecej I/O
  -> wolniejszy stage
  -> wiecej GC
  -> niestabilny runtime
```

To dlatego job "dziala", ale nagle robi sie dramatycznie wolny.

<!-- end_slide -->

# Jak rozpoznac problem z pamiecia

Szukasz symptomow:

- task spill metrics,
- dlugi GC time,
- executor lost / OOM,
- cache wypiera inne dane,
- broadcast sie nie miesci albo nie daje efektu.

Nie wystarczy powiedziec "dodajmy RAM".
Trzeba jeszcze wiedziec, kto ten RAM zuzywa.

<!-- end_slide -->

# Cache nie jest darmowy

```python
df_enriched.cache()
```

To ma sens tylko wtedy, gdy:

- ten sam DataFrame liczysz kilka razy,
- koszt ponownego liczenia jest wysoki,
- masz na to budzet pamieci.

To szkodzi, gdy:

- dataset jest uzyty raz,
- cache wypycha execution memory,
- przez cache zaczynaja sie spills.

<!-- end_slide -->

# Persist to decyzja, nie odruch

```text
MEMORY_ONLY            = szybko, ale ryzykownie przy duzych danych
MEMORY_AND_DISK        = bezpieczniej, ale wolniej
DISK_ONLY              = taniej dla RAM, ale nie przyspiesza tak mocno
SERIALIZED variants    = mniej RAM, wiecej CPU
```

Pytanie nie brzmi:

```text
Czy cache wlaczyc?
```

Pytanie brzmi:

```text
Czy reuse danych jest wart ceny w pamieci?
```

<!-- end_slide -->

# Broadcast tez zuzywa pamiec

Broadcast join jest szybki nie dlatego, ze jest "magiczny".
Jest szybki, bo unika shuffle duzej tabeli.

Cena:

```text
mala tabela musi zmiescic sie sensownie po stronie executorow
```

Jesli broadcast lookup jest za duzy, zysk znika albo pojawia sie memory pressure.

<!-- end_slide -->

# Czesc 2 - Shuffle

Shuffle to moment, w ktorym Spark zmienia rozmieszczenie danych miedzy partycjami.

To zwykle najdrozszy fragment joba.

<!-- end_slide -->

# Kiedy pojawia sie shuffle

Typowe operacje:

- groupBy,
- join,
- distinct,
- orderBy,
- repartition,
- window z mocnym repartitioning.

W planie zwykle zobaczysz:

```text
Exchange
```

<!-- end_slide -->

# Dlaczego shuffle boli

```text
serialize
  -> write local
  -> transfer over network
  -> read remote
  -> deserialize
  -> wait for all partitions
```

To uderza jednoczesnie w:

- CPU,
- disk I/O,
- network,
- synchronizacje stage.

<!-- end_slide -->

# Narrow vs wide

```text
Narrow transformations:
filter, select, withColumn

Wide transformations:
join, groupBy, distinct, orderBy
```

Regula praktyczna:

```text
Wide transformation = podejrzenie shuffle, dopoki nie udowodnisz inaczej.
```

<!-- end_slide -->

# Shuffle w explain plan

Patrz na:

```text
Exchange
HashAggregate
SortMergeJoin
BroadcastHashJoin
AQEShuffleRead
```

Nie czytaj `explain()` jak sciane tekstu.
Szukaj momentow, gdzie dane sa dzielone na nowo.

<!-- end_slide -->

# Czesc 3 - Broadcast joins

Join to bardzo czesty punkt kosztowy.
Spark ma kilka strategii, ale tutaj skupiamy sie na tej najpraktyczniejszej.

```python
fact.join(F.broadcast(dim), "customer_id")
```

<!-- end_slide -->

# Co broadcast join realnie robi

```text
mala tabela idzie do wszystkich executorow
duza tabela zostaje tam, gdzie jest
Spark nie musi shuffle'owac obu stron
```

To jest dobre, gdy jedna strona jest naprawde lookupiem.

<!-- end_slide -->

# Kiedy broadcast ma sens

- tabela wymiaru jest mala,
- join key jest sensowny,
- fakt jest duzy, lookup maly,
- chcesz uniknac SortMergeJoin na dwoch duzych tabelach.

Mental model:

```text
Przenies mala encyklopedie do wszystkich workerow,
zamiast przewozic cala fabryke przez siec.
```

<!-- end_slide -->

# Kiedy broadcast nie ma sensu

- lookup nie jest juz maly,
- executory maja ciasna pamiec,
- klucz joina ma silny skew,
- po joinie i tak od razu robisz ciezki shuffle,
- AQE samo potrafi wybrac lepsza strategie bez recznego hintu.

Broadcast nie leczy kazdego joina.

<!-- end_slide -->

# Broadcast vs SortMergeJoin

```text
BroadcastHashJoin
  + mniej shuffle
  + zwykle szybciej dla malej strony
  - wymaga sensownego rozmiaru lookupu

SortMergeJoin
  + stabilny dla duzych tabel
  - wymaga sort i shuffle obu stron
```

To nie jest ranking "lepszy/gorszy".
To jest decyzja zalezna od danych.

<!-- end_slide -->

# Czesc 4 - Skew

Skew znaczy, ze partycje nie dostaja podobnej ilosci pracy.

Przyklad:

```text
customer_id=12345 -> 40% wszystkich rekordow
reszta kluczy     -> rozlozona cienko
```

Wtedy rownolegly system przestaje byc rownolegly.

<!-- end_slide -->

# Objaw skew

```text
95 taskow konczy szybko
1 task mieli jeszcze bardzo dlugo
```

To jest klasyczny straggler.
Reszta klastra juz czeka, ale job nie moze skonczyc stage.

<!-- end_slide -->

# Jak wykryc skew

Po stronie danych:

```python
df.groupBy("join_key").count().orderBy(F.desc("count")).show(20)
```

Po stronie runtime:

- task duration outliers,
- jedna ogromna partition,
- bardzo nierowne shuffle read sizes,
- AQE sygnalizujace skew split.

<!-- end_slide -->

# Typowe miejsca skew

- join po goracym kluczu,
- groupBy po malo zroznicowanej kolumnie,
- null-heavy key,
- country / status / date z bardzo nierowna dystrybucja,
- write po zlej kolumnie partitionBy.

<!-- end_slide -->

# Jak naprawiac skew

Najczestsze techniki:

1. pre-aggregation przed join,
2. broadcast malej strony,
3. salting goracego klucza,
4. lepszy partitioning,
5. AQE skew optimization,
6. rozdzielenie hot-key path od reszty danych.

<!-- end_slide -->

# Salting

Idea:

```text
jeden goracy klucz dzielisz na kilka sztucznych bucketow,
zeby rozlozyc prace na wiecej taskow
```

Cena:

- bardziej zlozony kod,
- trzeba kontrolowac zgodnosc kluczy po obu stronach,
- to nie jest fix pierwszego wyboru, jesli AQE i broadcast wystarcza.

<!-- end_slide -->

# AQE jako pierwszy partner

Adaptive Query Execution potrafi:

- zmienic join strategy w runtime,
- scalać male shuffle partitions,
- dzielic skewed partitions.

Regula praktyczna:

```text
Najpierw sprawdz AQE, potem reczne hinty i salting.
```

<!-- end_slide -->

# Jak te 4 tematy lacza sie razem

```text
duzy join
  -> shuffle
  -> presja na execution memory
  -> spill
  -> jeszcze wolniejszy stage
  -> skew wydluza ostatnie taski
```

To nie sa osobne rozdzialy.
To jest jeden system przyczyn i skutkow.

<!-- end_slide -->

# Recipe diagnozy

```text
1. explain(mode="formatted")
2. Czy jest Exchange?
3. Jaka jest join strategy?
4. Czy mala tabela moze byc broadcast?
5. Czy widac nierowne klucze?
6. Czy sa spills / GC / OOM?
7. Czy AQE jest wlaczone i co zrobilo?
8. Dopiero potem tuning reczny
```

<!-- end_slide -->

# Mini case

Masz pipeline:

```text
orders
  -> join customers
  -> join products
  -> groupBy country
  -> write parquet
```

Pytania, ktore zadajesz:

1. Ktory join mozna zrobic broadcast?
2. Gdzie pojawi sie shuffle?
3. Czy `country` moze dawac skew?
4. Czy cache gdzies pomaga, czy tylko zabiera RAM?
5. Czy write nie generuje za duzo malych plikow?

<!-- end_slide -->

# Co oddajesz po lekcji

```text
homework/lesson_13/
  01_explain_walkthrough.md
  02_join_strategy_benchmark.py
  03_skew_investigation.md
  04_skew_fix.py
  05_runtime_tuning_notes.md
  06_interview_answers.md
```

<!-- end_slide -->

# Tutorial po lekcji

1. Apache Spark Tuning Guide
   https://spark.apache.org/docs/latest/tuning.html

<!-- end_slide -->

# Closing check

Powiedz na glos:

```text
Wolny Spark job to najczesciej kombinacja:
shuffle, presji na pamiec, zlej strategii joina i skew.
Najpierw czytam plan i metryki, dopiero potem tuninguje.
```
