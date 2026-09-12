# Teoria: niezawodne data pipelines

<!-- end_slide -->

## ELI5

Pipeline danych ma dawac poprawny wynik nie tylko wtedy, gdy wszystko pojdzie idealnie.

Ma byc odporny na normalne problemy:

- retry,
- duplikaty,
- update,
- delete,
- spoznione dane,
- czesciowy blad zapisu,
- nagly skok metryki.

Idempotencja znaczy: powtorzenie tego samego kroku na tym samym input daje ten sam poprawny wynik.

<!-- end_slide -->

## Problem Bez Reliability

Wyobraz sobie prosty daily pipeline:

```text
source orders -> INSERT INTO gold_daily_sales -> dashboard
```

Jesli job padnie i Airflow odpali retry, naiwny pipeline moze zrobic:

```text
run 1: INSERT revenue 470
run 2: INSERT revenue 470 jeszcze raz
dashboard: revenue 940
```

SQL sie wykonal. Dashboard dziala. Wynik jest zly.

<!-- end_slide -->

## First Principles

Pipeline psuje wynik wtedy, gdy nie ma jasnych gwarancji.

Musisz wiedziec:

```text
Co jest inputem?
Co jest jednym rekordem?
Jaki klucz identyfikuje event?
Jaki klucz identyfikuje obiekt biznesowy?
Ktory stan jest aktualny?
Co sie stanie przy retry?
Jaki check wykryje blad?
Jak naprawiamy wynik?
```

Dlatego projektujesz pod:

```text
raw changes -> dedupe -> current state -> validation -> publish -> recovery path
```

<!-- end_slide -->

## Case Z Lekcji

W labie system zrodlowy nie wysyla pelnej tabeli zamowien.

Wysyla zmiany:

```text
INSERT
UPDATE
DELETE
```

Kazda zmiana trafia do:

```text
bronze_order_changes
```

Najwazniejsza mysl:

```text
Bronze changes != current orders
```

<!-- end_slide -->

## Przyklad Raw Changes

Ten sam `order_id` moze miec kilka zmian:

```text
change_id | operation | order_id | status  | amount | change_timestamp
chg_001   | INSERT    | 1001     | created | 120    | 2026-05-20 09:00
chg_002   | UPDATE    | 1001     | paid    | 120    | 2026-05-20 10:00
chg_002   | UPDATE    | 1001     | paid    | 120    | 2026-05-20 10:00
```

Co tu widac?

```text
order_id = 1001 ma historie zmian
change_id = chg_002 jest duplikatem eventu
```

<!-- end_slide -->

## Event Key Vs Business Key

To sa dwa rozne pytania.

```text
change_id -> czy to ten sam event?
order_id  -> ktore zamowienie opisuje event?
```

Nie deduplikuj CDC od razu po `order_id`.

Dlaczego?

```text
Bo UPDATE zamowienia 1001 nie jest duplikatem INSERT-a zamowienia 1001.
To kolejna prawdziwa zmiana tego samego obiektu biznesowego.
```

<!-- end_slide -->

## Grain W Kazdej Warstwie

Bronze changes:

```text
jeden rekord = jedna surowa zmiana ze zrodla
```

Deduped changes:

```text
jeden rekord = jeden unikalny change_id
```

Current state:

```text
jeden rekord = najnowszy znany stan jednego order_id
```

Gold daily sales:

```text
jeden rekord = jeden order_date z paid active revenue
```

<!-- end_slide -->

## Dedupe Eventow

Najpierw usuwasz duplicate event.

Minimalny wzorzec:

```sql
ROW_NUMBER() OVER (
    PARTITION BY change_id
    ORDER BY change_timestamp DESC, order_id DESC
) AS row_number
```

Potem bierzesz:

```sql
WHERE row_number = 1
```

To chroni pipeline przed sytuacja, w ktorej source albo retry wyslal ten sam event drugi raz.

<!-- end_slide -->

## Current State

Po dedupe nadal masz historie zmian.

Teraz wybierasz najnowszy stan zamowienia:

```sql
ROW_NUMBER() OVER (
    PARTITION BY order_id
    ORDER BY change_timestamp DESC, change_id DESC
) AS row_number
```

Potem bierzesz:

```sql
WHERE row_number = 1
```

To odpowiada na pytanie:

```text
Jaki jest aktualny stan order_id teraz?
```

<!-- end_slide -->

## Dlaczego Potrzebny Jest Tiebreaker

Nie wystarczy powiedziec:

```sql
ORDER BY change_timestamp DESC
```

Jesli dwa eventy maja ten sam timestamp, wynik moze byc niedeterministyczny.

Dlatego dodajesz drugi warunek sortowania:

```sql
ORDER BY change_timestamp DESC, change_id DESC
```

Nie chodzi o to, ze `change_id DESC` zawsze jest idealne produkcyjnie.

Chodzi o zasade:

```text
latest state musi miec deterministyczny porzadek
```

<!-- end_slide -->

## DELETE Nie Jest Aktywnym Zamowieniem

Jesli najnowszy event dla `order_id = 1003` to:

```text
operation = DELETE
```

to ten rekord moze byc w historii zmian, ale nie powinien wejsc jako aktywne zamowienie do Silver/Gold.

Wzorzec:

```sql
FROM current_order_state
WHERE operation <> 'DELETE'
```

To nie usuwa historii ze zrodla.

To tylko mowi:

```text
Silver active orders nie zawiera usunietych zamowien.
```

<!-- end_slide -->

## Refunded Nie Jest Paid Revenue

`DELETE` to nie jedyny edge case.

Zamowienie moze byc aktualnie:

```text
created
paid
refunded
deleted
```

Gold revenue w tej lekcji liczy tylko:

```sql
WHERE status = 'paid'
```

Dlaczego?

```text
Revenue musi miec definicje biznesowa.
Nie kazdy aktywny rekord jest przychodem.
```

<!-- end_slide -->

## Finalny Przeplyw Lekcji

Docelowy pipeline logiczny:

```text
bronze_order_changes
  -> deduped_order_changes
  -> current_order_state
  -> silver_orders
  -> gold_daily_sales
```

Kazdy krok ma jedna gwarancje:

```text
dedupe -> duplicate event nie przejdzie dalej
current state -> jeden order_id ma jeden aktualny stan
silver -> DELETE nie jest aktywnym zamowieniem
gold -> revenue liczy tylko paid orders
```

<!-- end_slide -->

## Full Load Vs Incremental Load

Full load:

```text
przetwarzasz caly zakres danych od nowa
```

Incremental load:

```text
przetwarzasz tylko nowy albo zmieniony zakres danych
```

Full load jest prostszy mentalnie, ale drozszy przy duzych danych.

Incremental load jest wydajniejszy, ale wymaga:

- klucza,
- watermarku,
- obslugi late data,
- retry-safe write.

<!-- end_slide -->

## CDC

CDC, czyli Change Data Capture, oznacza czytanie zmian zamiast pelnej tabeli.

CDC odpowiada na pytanie:

```text
Co zmienilo sie w source od ostatniego razu?
```

Przykladowe operacje:

```text
INSERT order 1001
UPDATE order 1001 to paid
DELETE order 1003
```

CDC daje historie zmian.

Nie daje automatycznie poprawnego Golda.

<!-- end_slide -->

## Watermark

Watermark to znacznik, do ktorego momentu pipeline przetworzyl dane.

Przyklad:

```text
last_processed_change_timestamp = 2026-05-22 09:30:00
```

Pipeline moze potem zapytac:

```text
daj zmiany nowsze niz ostatni watermark
```

Ryzyko:

```text
jesli event przyjdzie pozno ze starym order_date,
Gold dla starego dnia moze wymagac przeliczenia
```

<!-- end_slide -->

## Spoznione Dane

Spoznione dane to dane, ktore dotycza starego dnia, ale przyszly pozniej.

Przyklad z labu:

```text
order_date        = 2026-05-19
change_timestamp = 2026-05-22
```

To sa dwie rozne daty:

```text
order_date        -> dzien biznesowy Gold
change_timestamp -> kiedy pipeline zobaczyl zmiane
```

Dlatego pipeline czesto przelicza lookback window, np. ostatnie 3-7 dni.

<!-- end_slide -->

## Lookback Window

Lookback window to zakres historii, ktory przeliczasz przy normalnym runie.

Przyklad:

```text
codziennie przelicz ostatnie 3 dni biznesowe
```

Po co?

```text
zeby late arriving data moglo poprawic starszy Gold
```

Koszt:

```text
wieksze okno = drozsze przetwarzanie
mniejsze okno = wieksze ryzyko pominiecia spoznionych zmian
```

To jest decyzja produktu danych, nie tylko SQL.

<!-- end_slide -->

## Retry-Safe Write

Najbardziej niebezpieczny wzorzec:

```sql
INSERT INTO gold_daily_sales
SELECT ...
```

Jesli ten sam run odpali sie drugi raz, moze dopisac ten sam wynik drugi raz.

Bezpieczniejsze wzorce:

```text
MERGE / UPSERT po kluczu
DELETE controlled range + INSERT
partition overwrite
CREATE OR REPLACE table/view dla kontrolowanego zakresu
```

W SQLite w tej lekcji pokazujemy logike przez widoki.

W produkcji wybierasz mechanizm zapisu zgodny z platforma.

<!-- end_slide -->

## ACID

ACID to zestaw gwarancji zapisu danych.

W tej lekcji wystarczy intuicja:

```text
Atomicity   -> zapis udal sie caly albo wcale
Consistency -> po zapisie dane nadal spelniaja reguly
Isolation   -> dwa rownolegle zapisy nie psuja sobie wyniku
Durability  -> zatwierdzony zapis nie znika po awarii
```

Najwazniejsze dla pipeline'u:

```text
odbiorca nie powinien zobaczyc polowy tabeli Gold
```

<!-- end_slide -->

## ACID W Systemach Rozproszonych

W lokalnej bazie jeden silnik kontroluje zapis, blokady i commit.

W systemie rozproszonym dane moga lezec w wielu plikach, partycjach, workerach albo regionach.

To utrudnia pytanie:

```text
Czy wszyscy widza dokladnie ten sam zatwierdzony stan danych?
```

Dlatego formaty tabel lakehouse, np. Delta Lake, Iceberg i Hudi, dodaja metadane transakcji nad plikami.

<!-- end_slide -->

## Izolacja Transakcji

Izolacja odpowiada na pytanie, co widza dwa procesy, ktore czytaja albo zapisuja dane w tym samym czasie.

Problem:

```text
job kasuje partycje Gold
job dopisuje nowe dane
dashboard czyta w srodku operacji
```

Cel:

```text
dashboard widzi poprzedni poprawny wynik albo nowy poprawny wynik
```

Nie musisz znac poziomow izolacji na pamiec. Masz rozumiec, jaki blad izolacja zatrzymuje.

<!-- end_slide -->

## ACID Nie Zastepuje Logiki

Transakcja moze ochronic zapis technicznie, ale nie zna twojej metryki.

ACID nie odpowie za ciebie:

```text
Po czym deduplikowac event?
Ktory rekord jest aktualnym stanem order_id?
Czy DELETE ma wejsc do Gold?
Czy refunded liczy sie jako revenue?
Czy retry podwoil wynik?
```

Dlatego reliability ma dwa poziomy:

```text
storage guarantees + pipeline logic
```

<!-- end_slide -->

## Validation Checks

Pipeline bez checkow wymaga wiary.

Pipeline z checkami daje dowod.

Minimalne checki w tej lekcji:

```text
duplicate change_id
duplicate current order_id
null keys
negative amount
unexpected status
freshness / max change_timestamp
Silver paid revenue vs Gold revenue
```

Check powinien mowic:

```text
Expected: 0 rows
Meaning: jesli sa wiersze, to ...
```

<!-- end_slide -->

## Run Metadata

Run metadata odpowiada na pytania operacyjne:

```text
Ktory pipeline sie odpalil?
Jaki mial run_id?
Jakie okno danych przetwarzal?
Czy skonczyl sie sukcesem?
Ile rekordow weszlo i wyszlo?
Jaki byl blad?
```

Przykladowe pola:

```text
pipeline_name
run_id
window_start
window_end
status
row_count_bronze
row_count_silver
row_count_gold
error_message
```

<!-- end_slide -->

## Partial Failure

Partial failure to sytuacja, w ktorej job zrobil czesc pracy i padl.

Przyklad:

```text
Bronze loaded
Silver rebuilt
Gold failed halfway
```

Bez run metadata nie wiesz, co zostalo zrobione.

Bez idempotencji boisz sie odpalic retry.

Poprawny cel:

```text
wiem, gdzie job padl i moge bezpiecznie powtorzyc kontrolowany zakres
```

<!-- end_slide -->

## Runbook

Runbook to instrukcja naprawy incidentu.

Nie piszesz:

```text
sprawdz dane
```

Piszesz konkretnie:

```text
1. sprawdz duplicate change_id
2. sprawdz current state per order_id
3. porownaj Silver paid revenue z Gold
4. sprawdz max change_timestamp
5. przelicz zakres dat X-Y
```

Runbook ma pozwolic naprawic pipeline wtedy, gdy nie pamietasz juz wszystkich decyzji projektowych.

<!-- end_slide -->

## Incident: Revenue +40%

Jesli Gold revenue nagle skoczylo o 40%, nie zaczynasz od przepisywania SQL.

Najpierw pytasz:

```text
Czy source wyslal duplikaty?
Czy retry dopisal Gold drugi raz?
Czy current state ma wiele rekordow per order_id?
Czy do revenue weszly statusy inne niz paid?
Czy late data zmienila starszy dzien?
```

To jest roznica miedzy debugowaniem losowym a debugowaniem przez failure modes.

<!-- end_slide -->

## Czego Nie Robimy W Tej Lekcji

Nie uczymy sie jeszcze pelnej produkcyjnej implementacji:

- Airflow DAGow,
- dbt incremental models,
- Delta Live Tables,
- Kafka offset management,
- wszystkich poziomow izolacji transakcji,
- SCD Type 2 end-to-end.

Uczymy sie fundamentu:

```text
jak rozpoznac failure mode i zaprojektowac gwarancje danych
```

<!-- end_slide -->

## Otworz I Zrob To

1. Wroc do lekcji 03, jesli nie umiesz wyjasnic Bronze/Silver/Gold.
2. Przypomnij sobie `ROW_NUMBER()` i wybieranie najnowszego rekordu per klucz biznesowy.
3. Zapisz po jednym zdaniu dla pojec z sekcji `Slownik niezawodnosci`.

<!-- end_slide -->

## Musisz Umiec Odpowiedziec Przed Labem

1. Co stanie sie, jesli ten sam batch uruchomimy dwa razy?
2. Czym rozni sie append od overwrite albo upsert?
3. Po czym poznasz duplikat eventu?
4. Czym rozni sie event key od business key?
5. Czym rozni sie surowa zmiana w Bronze od aktualnego stanu w Silver?
6. Jak pipeline powinien zareagowac na spoznione dane?
7. Co chroni ACID, a czego ACID nie wie o twojej metryce?

<!-- end_slide -->

## Fundamenty SQL

1. Jak dziala `ROW_NUMBER()`?
2. Jak wybrac najnowszy rekord per `order_id`?
3. Czym jest klucz biznesowy?
4. Czym rozni sie event od aktualnego stanu rekordu?
5. Jak sprawdzic duplikaty po `change_id`?
6. Jak porownac revenue z Silver i Gold?

<!-- end_slide -->

## Slownik Niezawodnosci

To sa pojecia, do ktorych wracasz w labie i homeworku:

- idempotencja - ten sam krok uruchomiony drugi raz daje ten sam poprawny efekt,
- retry - ponowienie kroku po bledzie,
- deduplikacja - usuniecie albo pominiecie duplikatow,
- full load - przetworzenie calego zakresu danych od nowa,
- incremental load - przetworzenie tylko nowych albo zmienionych danych,
- CDC - przechwytywanie zmian w danych zrodlowych,
- watermark - znacznik, do ktorego momentu dane zostaly przetworzone,
- late data - dane, ktore przyszly po oczekiwanym czasie,
- backfill - uzupelnienie albo przeliczenie danych historycznych,
- runbook - instrukcja, co zrobic przy awarii albo podejrzanym wyniku.

<!-- end_slide -->

## Wzorzec 1: Bronze To Nie Current State

Antywzorzec:

```text
Bronze ma order_id, wiec traktuje to jak aktualne zamowienia.
```

Lepszy wzorzec:

```text
Bronze changes -> dedupe po change_id -> latest state po order_id -> Silver current state
```

<!-- end_slide -->

## Wzorzec 2: Retry-Safe Load

Antywzorzec:

```text
Kazde ponowienie robi INSERT do tabeli docelowej.
```

Lepszy wzorzec:

```text
staging -> walidacja -> merge/upsert albo kontrolowany overwrite partycji
```

Pytanie kontrolne:

```text
Co stanie sie, jesli ten sam input przetworze drugi raz?
```

<!-- end_slide -->

## Wzorzec 3: Check Przed Zaufaniem

Nie wystarczy, ze SQL sie wykonal.

Musisz miec check:

```text
Czy wynik jest logicznie poprawny?
```

Przyklad:

```text
Silver paid revenue == Gold revenue
```

Jesli check nie przechodzi, pipeline nie publikuje zaufanego Gold.

<!-- end_slide -->

## Mini-Checklist

- Co jest grain Bronze?
- Co jest grain current state?
- Po czym deduplikujesz eventy?
- Po czym wybierasz najnowszy stan?
- Jak obslugujesz DELETE?
- Jak filtrujesz paid revenue?
- Jak retry nie podwoi danych?
- Jak obsluzysz late data?
- Co chroni ACID?
- Co zrobisz, gdy Gold revenue skoczy o 40%?

<!-- end_slide -->

## Zapamietaj

```text
Reliable pipeline = stable keys + deterministic state + retry-safe write + validation + recovery path
```

Najwazniejsza odpowiedz z lekcji:

```text
Nie ufam Gold dlatego, ze job sie odpalil.
Ufam Gold dlatego, ze wiem, jaki failure mode obsluzylem i jaki check to potwierdza.
```