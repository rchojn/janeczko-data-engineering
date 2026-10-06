# Pytania na lekcji: Lekcja 13 - Spark Internals

Ten plik sluzy do rozmowy na zywo.
Mentor nie musi przejsc przez wszystkie pytania.

Cel: sprawdzic, czy kursant umie myslec kosztem wykonania, a nie tylko skladnia PySpark.

## Pytania startowe

1. Co jest wieksza roznica miedzy month_02 a ta lekcja?
   Odpowiedz: W month_02 glownie pisalismy logike pipeline i integracje. Tutaj uczymy sie fizycznego kosztu wykonania na systemie rozproszonym.

2. Co to znaczy, ze job jest logicznie poprawny, ale fizycznie drogi?
   Odpowiedz: Wynik jest dobry, ale Spark musi zrobic duzo shuffle, ma skew albo zla strategie joina.

3. Dlaczego sam czas wykonania nie wystarcza do diagnozy?
   Odpowiedz: Bo bez planu i UI nie wiesz, czy problemem jest join, skew, partycje, cache czy write.

## Model wykonania

1. Co to jest job?
   Odpowiedz: Cala praca uruchomiona przez action.

2. Co to jest stage?
   Odpowiedz: Fragment joba miedzy punktami shuffle.

3. Co to jest task?
   Odpowiedz: Jednostka pracy na jednej partycji.

4. Co to jest partition?
   Odpowiedz: Kawalek danych przetwarzany rownolegle.

## Shuffle i skew

1. Dlaczego shuffle jest drogi?
   Odpowiedz: Bo obejmuje serializacje, I/O i network transfer.

2. Jak rozpoznajesz skew?
   Odpowiedz: Po rozkladzie klucza i po outlierach czasu taskow w UI.

3. Czy wiecej workerow zawsze rozwiazuje skew?
   Odpowiedz: Nie, bo problemem jest nierowny rozklad pracy, a nie tylko brak mocy.

## Join strategy

1. Kiedy broadcast join ma sens?
   Odpowiedz: Gdy jedna tabela jest mala i taniej ja rozeslac niz shufflowac obie strony.

2. Kiedy broadcast nie pomoze?
   Odpowiedz: Gdy tabela nie jest mala albo problem jest gdzie indziej, np. w skew.

3. Co oznacza `SortMergeJoin` w planie?
   Odpowiedz: Czesto drozszy join duzych tabel po shuffle.

## Runtime decisions

1. Kiedy cache ma sens?
   Odpowiedz: Gdy ten sam DataFrame jest uzywany kilka razy i jego przeliczenie jest drogie.

2. Kiedy wolisz `coalesce`, a kiedy `repartition`?
   Odpowiedz: `coalesce` przy zmniejszaniu i tanszym write, `repartition` gdy chcesz rownomiernego rozkladu albo wiecej partycji.

3. Co daje AQE?
   Odpowiedz: Potrafi runtime poprawic plan, partycje i skew behavior.

## Closing check

1. Od czego zaczynasz diagnoze wolnego Spark joba?
   Odpowiedz: Od `explain()`, Spark UI i rozkladu kluczy.

2. Jakim jednym zdaniem odroznisz te lekcje od zwyklego PySpark?
   Odpowiedz: To lekcja o koszcie systemu rozproszonego, a nie tylko o skladni transformacji.
