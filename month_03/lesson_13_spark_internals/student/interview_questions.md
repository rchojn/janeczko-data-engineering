# Interview Questions: Lekcja 13 - Spark Internals

## Pytania rekrutacyjne

1. **Co to jest shuffle i dlaczego jest drogi?**

   Dobra odpowiedz: shuffle to przemieszczanie danych miedzy executorami. Pojawia sie przy `groupBy`, `join`, `distinct`, `orderBy`. Jest drogi, bo wymaga serializacji, write/read z dysku i transferu po sieci. W praktyce to najczestszy koszt duzych jobow.

2. **Czym rozni sie narrow transformation od wide transformation?**

   Dobra odpowiedz: narrow nie wymaga mieszania danych miedzy partycjami, wide zwykle wymaga shuffle. `filter` i `withColumn` sa zwykle narrow. `groupBy` i wiele joinow jest wide.

3. **Kiedy broadcast join jest lepszy od sort-merge join?**

   Dobra odpowiedz: gdy jedna tabela jest naprawde mala i mozna ja skopiowac do executorow taniej niz shufflowac obie strony. Broadcast redukuje network cost. Sort-merge ma sens, gdy obie strony sa duze.

4. **Co to jest data skew i jak je wykrywasz?**

   Dobra odpowiedz: skew to nierowny rozklad klucza, np. jedna wartosc ma 90% rekordow. Wykrywam to przez `groupBy(key).count()`, explain i Spark UI, gdzie widac task outliers.

5. **Czym rozni sie repartition od coalesce?**

   Dobra odpowiedz: `repartition` robi shuffle i sluzy do rownomiernego rozkladu lub zwiekszenia liczby partycji. `coalesce` zwykle zmniejsza partycje bez shuffle i jest tansze, ale nie daje tak rownego rozkladu.

6. **Kiedy cache pomaga, a kiedy szkodzi?**

   Dobra odpowiedz: pomaga, gdy ten sam DataFrame liczysz wielokrotnie. Szkodzi, gdy dane sa uzywane raz albo cache wypiera inne potrzebne dane z memory i prowokuje spills.

7. **Co daje Adaptive Query Execution?**

   Dobra odpowiedz: AQE pozwala Sparkowi zmieniac plan po runtime stats. Potrafi lepiej dobrac join strategy, zredukowac partycje po shuffle i ograniczac skew. To pierwszy bezpieczny mechanizm przed recznym tuningiem.

## Pytania procesowe

1. Masz wolny Spark job. Od czego zaczynasz diagnoze?
   Odpowiedz: od `explain()`, Spark UI, task duration, shuffle read/write i rozkladu kluczy.

2. Co bys pokazal reviewerowi zamiast powiedziec "job jest wolny"?
   Odpowiedz: plan z `Exchange`, czas stage, rozklad klucza i hipoteze konkretnego bottlenecku.

3. Kiedy nie ruszasz configu i zmieniasz model danych?
   Odpowiedz: gdy problem wynika z logiki joinu, grain, skewed key albo niepotrzebnego przemieszczania danych.
