# Interview Questions: Lekcja 13b - Spark na Databricks

## Pytania rekrutacyjne

1. **Jak wyglada podstawowy workflow Spark w Databricks?**

   Dobra odpowiedz: najpierw tworzysz albo wybierasz compute, potem rozwijasz logike w notebooku, czytasz dane, zapisujesz output jako Delta table i finalnie opakowujesz to w job z harmonogramem i monitoringiem.

2. **Czym rozni sie notebook od joba?**

   Dobra odpowiedz: notebook jest dobry do developmentu i exploracji, a job daje repeatability, harmonogram, retries, status runow i ownership. Sam notebook nie jest jeszcze operacyjnym pipeline.

3. **Po co jest checkpoint przy incremental ingest?**

   Dobra odpowiedz: checkpoint przechowuje stan przetwarzania, czyli co juz zostalo obsluzone. Bez niego pipeline moze przetwarzac te same dane ponownie albo nie wiedziec, jak wznowic po awarii.

4. **Co daje Delta jako output ETL?**

   Dobra odpowiedz: Delta daje trwaly tabelaryczny output, ktory mozna ponownie czytac, kontrolowac i wykorzystywac dalej. To juz nie jest tylko tymczasowy DataFrame w notebooku.

5. **Jaka jest roznica miedzy compute a notebookiem?**

   Dobra odpowiedz: notebook to kod i workflow developmentu, a compute to zasob wykonujacy ten kod. Notebook bez compute nie wykona transformacji.

## Pytania procesowe

1. Co trzeba zrobic, zeby eksperymentalny notebook stal sie produkcyjnym runem?
   Odpowiedz: ustalic compute, output table, checkpoint, parametry runu i scheduler joba.

2. Co bys pokazal reviewerowi po przejsciu tutoriala?
   Odpowiedz: mape workflow, role compute, miejsce checkpointu i uzasadnienie przejscia notebook -> job.
