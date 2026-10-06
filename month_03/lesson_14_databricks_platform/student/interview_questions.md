# Interview Questions: Lekcja 14 — Databricks + Unity Catalog

## Pytania rekrutacyjne

1. **Co to jest Unity Catalog i jaki problem rozwiązuje?**

   Dobra odpowiedź: Unity Catalog = centralny metastore dla całego Databricks account. Przed UC: każdy workspace miał własny Hive metastore → chaos przy udostępnianiu danych między teamami. Po UC: jeden punkt governance — permissions, lineage, data discovery, column masking — dla całej firmy. Namespace: `catalog.schema.table` zamiast `hive_metastore.schema.table`.

2. **Co to jest small files problem w Delta Lake i jak go naprawić?**

   Dobra odpowiedź: Każdy append write tworzy nowy plik Parquet. Po wielu appendach (100+ batchów/dziennie) masz setki małych plików. Read = otwiera każdy plik → metadata overhead → wolno. Fix: `OPTIMIZE` (compaction małych plików w duże). Na Databricks można zaplanować auto-optimize. ZORDER dodatkowo sortuje dane kolumnowo dla partition pruning.

3. **Co robi VACUUM i kiedy go uruchamiasz?**

   Dobra odpowiedź: VACUUM usuwa pliki Parquet które nie są już referencjonowane przez aktywną wersję tabeli — czyli stare wersje z time travel. Domyślny retention: 7 dni (168h). Po VACUUM nie możesz cofnąć się do wersji starszych niż threshold. Uruchamia się periodycznie (np. raz w tygodniu) żeby S3/ADLS nie rósł bez ograniczeń.

4. **Czym różni się Control Plane od Data Plane w Databricks?**

   Dobra odpowiedź: Control Plane = Databricks-zarządzany cloud — UI, Jobs scheduler, REST API, access control. Nigdy nie przechowuje Twoich danych. Data Plane = Twoje konto cloud (AWS/Azure/GCP) — Spark clusters, S3/ADLS gdzie są dane. Separation of concerns: Databricks zarządza compute orchestration, Ty kontrolujesz dane.

5. **Kiedy potrzebujesz column masking w Unity Catalog?**

   Dobra odpowiedź: Gdy różne role powinny widzieć tę samą tabelę ale nie te same kolumny — np. analityk widzi `amount` ale nie `credit_card_number`, GDPR compliance dla PII danych. Implementacja: `ALTER TABLE ... ALTER COLUMN ... SET MASK function`. Alternatywa: dynamic views (wolniejsze, trudniejsze do maintenance).

---

## Extra

```text
Q: "Jaka jest różnica między Hive Metastore a Unity Catalog?"
- Hive: jeden per workspace, brak cross-workspace sharing, brak column-level security
- Unity Catalog: jeden per Databricks account, multi-workspace, pełny governance stack

Q: "Jak często uruchamiać OPTIMIZE?"
- Tabele z częstymi appendami (streaming, micro-batch): daily lub po każdym większym loadziku
- Tabele static: rzadziej, po serii bulk loads
- Na Databricks: Delta Auto Optimize (predictive I/O) może być włączony na table-level
```
