# Praca domowa: Lekcja 04 - niezawodny pipeline i idempotencja

## Cel pracy

Twoim zadaniem jest zaprojektować i opisać batch pipeline dla zmian zamówień tak, żeby wynik był poprawny po retry, duplikacie eventu, update, delete i spóźnionych danych.

Pracujesz na danych z labu, w których `bronze_order_changes` nie jest aktualną tabelą zamówień. To jest historia zmian ze źródła. Z tej historii masz zbudować zaufany current state, a dopiero potem Gold z dziennym revenue.

Najważniejsze umiejętności z tej pracy:

1. odróżniasz event key `change_id` od business key `order_id`,
2. budujesz current state z raw changes,
3. pokazujesz, że retry nie podwaja revenue,
4. obsługujesz `DELETE`, `refunded`, `paid` i late arriving data,
5. dodajesz walidacje, run metadata i prosty runbook incidentu.

## Kontekst biznesowy

Zespół analityczny korzysta z tabeli `gold_daily_sales`, żeby raportować dzienne paid revenue. Źródło nie wysyła codziennie pełnej tabeli zamówień. Wysyła eventy zmian:

```text
INSERT
UPDATE
DELETE
```

Ten sam event może przyjść dwa razy, jedno zamówienie może zmienić status kilka razy, a spóźniona zmiana może dotyczyć starego `order_date`.

Wymaganie biznesowe:

```text
Gold ma pokazywać poprawne paid revenue per order_date.
Ponowne uruchomienie pipeline'u na tym samym input nie może zmienić wyniku.
```

## Szacowany budżet pracy

```text
1.0h  powtórka: idempotencja, CDC, event key, business key, current state
2.5h  reliable_load.sql: dedupe, current state, Silver, Gold
1.5h  validation_checks.sql: quality checks i retry checks
1.0h  pipeline_runs_design.md: run metadata i partial failure
1.0h  backfill_plan.md: late data, lookback window i backfill
1.0h  incident_runbook.md: diagnoza revenue spike z konkretnymi query
1.0h  video_notes.md: jeden materiał zewnętrzny
1.0h  interview_answer.md: odpowiedź techniczna i walkthrough
```

To zadanie jest bliższe realnej pracy Data Engineera niż zwykłemu ćwiczeniu SQL. Nie chodzi tylko o to, żeby query się wykonało. Chodzi o to, żeby umieć wyjaśnić, dlaczego wynik jest zaufany.

## Co oddajesz

Oddajesz katalog:

```text
homework/lesson_04/
├── reliable_load.sql
├── pipeline_runs_design.md
├── validation_checks.sql
├── backfill_plan.md
├── incident_runbook.md
├── video_notes.md
└── interview_answer.md
```

Nie oddajesz pliku `lesson_04.db`. Baza SQLite jest tylko lokalnym środowiskiem do uruchomienia i sprawdzenia SQL.

## Standard oddania

Każdy plik ma być czytelny dla osoby, która nie była z Tobą na lekcji. Przyjmij, że reviewer chce szybko zobaczyć:

- jaki problem rozwiązujesz,
- jaki jest grain danych na każdym etapie,
- jaki klucz kontroluje deduplikację albo current state,
- co stanie się przy drugim runie na tym samym input,
- jakie checki potwierdzają, że Gold jest poprawny,
- jak naprawisz wynik, jeśli pipeline da podejrzaną metrykę.

Nie wystarczy napisać „pipeline jest idempotentny”. Musisz pokazać, który krok daje tę gwarancję i jak to sprawdzasz.

## Krok 0: przygotuj środowisko

W katalogu `student/lab/` uruchom:

```bash
sqlite3 lesson_04.db < schema.sql
sqlite3 lesson_04.db < seed_data.sql
sqlite3 lesson_04.db
```

Utwórz katalog i pliki do oddania:

```bash
mkdir -p homework/lesson_04
touch homework/lesson_04/reliable_load.sql
touch homework/lesson_04/pipeline_runs_design.md
touch homework/lesson_04/validation_checks.sql
touch homework/lesson_04/backfill_plan.md
touch homework/lesson_04/incident_runbook.md
touch homework/lesson_04/video_notes.md
touch homework/lesson_04/interview_answer.md
```

Przed implementacją sprawdź, czy rozumiesz dane wejściowe:

```sql
SELECT *
FROM bronze_order_changes
ORDER BY order_id, change_timestamp, change_id;
```

W danych powinieneś zauważyć:

- `chg_002` występuje dwa razy,
- `order_id = 1001` przechodzi z `created` do `paid`,
- `order_id = 1002` kończy jako `refunded`,
- `order_id = 1003` kończy jako `DELETE`,
- `order_id = 1004` ma stare `order_date`, ale późne `change_timestamp`.

## Krok 1: `reliable_load.sql`

Zbuduj logiczny przepływ:

```text
bronze_order_changes
	-> deduped_order_changes
	-> current_order_state
	-> silver_orders
	-> gold_daily_sales
```

Wymagane widoki:

1. `deduped_order_changes`,
2. `current_order_state`,
3. `silver_orders`,
4. `gold_daily_sales`.

Przed każdym `CREATE VIEW` dopisz komentarz:

```sql
-- Grain: jeden rekord = ...
-- Key: ...
-- Retry guarantee: ...
```

Wymagania techniczne:

- duplicate event usuń po `change_id`,
- current state wybierz po `order_id`,
- przy wyborze latest state użyj deterministycznego sortowania, np. `change_timestamp DESC, change_id DESC`,
- `silver_orders` nie może zawierać rekordów, których aktualna operacja to `DELETE`,
- `gold_daily_sales` ma liczyć tylko `status = 'paid'`,
- Gold ma mieć grain jednego `order_date`.

Na końcu pliku dodaj minimum trzy SELECT-y pokazujące wynik:

```sql
SELECT * FROM deduped_order_changes ORDER BY change_id;
SELECT * FROM silver_orders ORDER BY order_id;
SELECT * FROM gold_daily_sales ORDER BY order_date;
```

Oczekiwany kierunek wyniku:

- `deduped_order_changes` ma jeden rekord per `change_id`,
- `silver_orders` ma aktywne zamówienia bez deleted order,
- `gold_daily_sales` nie liczy `refunded` ani `deleted`,
- paid revenue z Gold zgadza się z paid revenue z Silver.

## Krok 2: `pipeline_runs_design.md`

Zaprojektuj tabelę lub strukturę metadanych uruchomień pipeline'u.

Wymagane pola:

```text
pipeline_name
run_id
window_start
window_end
status
row_count_bronze
row_count_silver
row_count_gold
started_at
finished_at
error_message
```

Opisz krótko:

```text
Jak rozpoznaję retry?
Jak rozpoznaję partial failure?
Kiedy run jest safe do powtórzenia?
Które liczniki wierszy porównuję między runami?
Które metryki poza row countem sprawdzam?
```

Ważne: liczba wierszy sama nie wystarcza. Dwie tabele mogą mieć tę samą liczbę wierszy i nadal inną sumę revenue. Dlatego połącz liczniki wierszy z checkami metryk i freshness.

## Krok 3: `validation_checks.sql`

Dodaj checki jakości i retry safety. Każdy check opisz komentarzem:

```sql
-- Expected: 0 rows
-- Meaning: jeśli są wiersze, to ...
```

Wymagane checki:

1. duplicate `change_id` w Bronze,
2. duplicate `change_id` po dedupe,
3. więcej niż jeden current record per `order_id`,
4. null `order_id`, `customer_id` albo `order_date` w Silver,
5. ujemny `amount`,
6. nieoczekiwany `status`,
7. freshness, czyli `MAX(change_timestamp)`,
8. revenue sanity: paid revenue z Silver = revenue z Gold.

Dodaj sekcję `Retry checks` i odpowiedz SQL-em albo komentarzem kontrolnym:

```text
Czy drugi run na tym samym input zmienia Gold?
Czy liczba current records per order_id nadal wynosi 1?
Czy suma revenue nie wzrosła bez nowych zmian w source?
```

Uwaga: check duplicate `change_id` w Bronze może pokazać `chg_002`. To jest celowy problem wejściowy. Po dedupe analogiczny check powinien zwrócić 0 wierszy.

## Krok 4: `backfill_plan.md`

Opisz, jak obsługujesz late arriving data i backfill.

W pliku odpowiedz na pytania:

```text
Jaki problem wymaga backfillu?
Jak wybieram zakres dat biznesowych do przeliczenia?
Jak odróżniam order_date od change_timestamp?
Jak chronię się przed duplikatami przy backfillu?
Jakie tabele albo widoki przeliczam?
Jakie checki uruchamiam przed i po backfillu?
Jak informuję odbiorców dashboardu?
```

Uwzględnij konkretny case z labu:

```text
order_id = 1004
order_date = 2026-05-19
change_timestamp = 2026-05-22 07:00:00
```

Wyjaśnij, dlaczego taka zmiana może dotknąć starszego dnia w Gold, mimo że pipeline zobaczył event później.

## Krok 5: `incident_runbook.md`

Napisz runbook dla incidentu:

```text
Revenue w gold_daily_sales jest 40% wyższe niż oczekiwano.
```

Runbook ma być praktyczny. Ktoś inny powinien móc użyć go do diagnozy bez zgadywania, co autor pipeline'u miał na myśli.

Wymagana struktura:

```text
Incident:
Pierwsze checki:
Checki SQL:
Możliwe przyczyny:
Kroki naprawy:
Kogo poinformować:
Jak zapobiec temu następnym razem:
```

Dodaj minimum 5 konkretnych query albo pseudokwerend, np.:

- duplicate `change_id`,
- current state count per `order_id`,
- revenue by `status`,
- Silver paid revenue vs Gold revenue,
- `MAX(change_timestamp)`,
- revenue przed i po dedupe,
- porównanie wyników między runami.

Nie pisz tylko „sprawdź logi” albo „odpal ponownie”. To nie jest runbook.

## Krok 6: `video_notes.md`

Przerób jeden materiał z sekcji „Materiały Rekomendowane” w [README.md](README.md).

Może to być artykuł, dokumentacja albo wideo. Notatka ma pokazać, że umiesz połączyć materiał z failure mode'ami z tej lekcji.

Wymagana struktura:

```text
Źródło:
Link albo nazwa kanału:
O czym jest materiał:
Jedna idea reliability:
Jaki failure mode materiał pomaga nazwać:
Jedna rzecz, której nadal nie rozumiem:
Jak to łączy się z retry/idempotencją/CDC:
```

Nie streszczaj całego materiału. Wystarczy pokazać jedną konkretną ideę i powiązać ją z pipeline'em z labu.

## Krok 7: `interview_answer.md`

Odpowiedz na pytanie:

```text
Jak sprawiasz, że batch data pipeline jest niezawodny?
```

Odpowiedź powinna mieć 10-15 zdań i brzmieć jak wypowiedź na review technicznym albo rozmowie rekrutacyjnej.

Uwzględnij:

- stabilne klucze,
- deduplikację,
- idempotencję,
- current state,
- incremental window albo lookback window,
- retry-safe write,
- walidacje,
- obserwowalność i run metadata,
- runbook.

Dopisz też krótką sekcję o ACID:

```text
Co dają transakcje/ACID przy zapisie do Gold?
Czym różni się ACID w lokalnej bazie od ACID nad plikami/partycjami w lakehouse?
Czego ACID nie rozwiązuje za logikę pipeline'u?
```

Najważniejszy punkt: ACID może chronić techniczny commit, ale nie zdecyduje za Ciebie, po czym deduplikować eventy, który rekord jest current state i czy `refunded` liczy się jako revenue.

## Pytania kontrolne przed oddaniem

Przed wysłaniem pracy odpowiedz sobie na głos:

1. Co oznacza idempotentny pipeline?
2. Dlaczego retry może tworzyć duplikaty?
3. Czym różni się event key od business key?
4. Dlaczego Bronze changes nie jest current state?
5. Gdzie usuwasz duplicate `change_id`?
6. Gdzie wybierasz latest state per `order_id`?
7. Gdzie obsługujesz `DELETE`?
8. Dlaczego `refunded` nie wchodzi do paid revenue?
9. Co to jest CDC?
10. Co to jest watermark?
11. Dlaczego pipeline używa lookback window?
12. Jak wykryjesz nagły skok revenue?
13. Co oznacza atomiczny zapis do Gold?
14. Dlaczego ACID nie zastępuje deduplikacji i walidacji?
15. Dlaczego izolacja transakcji jest ważna, gdy dashboard czyta Gold w czasie zapisu?

## Checklista przed oddaniem

- [ ] `reliable_load.sql` buduje `deduped_order_changes`, `current_order_state`, `silver_orders` i `gold_daily_sales`.
- [ ] Deduplikacja eventów jest po `change_id`, nie po `order_id`.
- [ ] Current state jest po `order_id` i ma deterministyczne sortowanie latest record.
- [ ] `silver_orders` nie zawiera aktualnie usuniętych zamówień.
- [ ] `gold_daily_sales` liczy tylko `status = 'paid'`.
- [ ] `validation_checks.sql` ma checki jakości i retry checks.
- [ ] `pipeline_runs_design.md` wyjaśnia retry, partial failure i safe rerun.
- [ ] `backfill_plan.md` rozróżnia `order_date` i `change_timestamp`.
- [ ] `incident_runbook.md` ma minimum 5 konkretnych query albo pseudokwerend.
- [ ] `video_notes.md` łączy materiał zewnętrzny z failure mode'em z lekcji.
- [ ] `interview_answer.md` tłumaczy storage guarantees vs pipeline logic.
- [ ] Potrafisz wyjaśnić, dlaczego drugi run nie podwaja revenue.

## Wzorzec mocnej odpowiedzi

```text
Projektuję pipeline wokół stabilnych kluczy i kontrolowanej semantyki zapisu.
Surowe zmiany trzymam w Bronze jako append-only historię. Najpierw deduplikuję eventy po event key, np. change_id. Potem wybieram aktualny stan po business key, np. order_id, z deterministycznym sortowaniem latest record. Silver zawiera zaufany current state, a Gold liczę dopiero z Silver i tylko dla statusów zgodnych z definicją metryki.

Dla retry safety unikam blind append do tabel finalnych. Używam merge/upsert, controlled overwrite albo partition overwrite dla kontrolowanego zakresu. Do tego dodaję walidacje, run metadata i runbook, żeby wiedzieć, czy wynik jest poprawny i jak go naprawić, jeśli pipeline da podejrzaną metrykę.
```
