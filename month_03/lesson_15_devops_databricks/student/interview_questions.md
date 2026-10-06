# Interview Questions: Lekcja 15 — DevOps w Databricks

## Pytania rekrutacyjne

1. **Co to są Databricks Asset Bundles i dlaczego są lepsze od ręcznego UI?**

   Dobra odpowiedź: DABs = IaC dla Databricks. Definiujesz Jobs, clusters, permissions w YAML + kod w repozytorium. Korzyści: reproducibility (każdy może odtworzyć workspace z Git), code review dla zmian w pipeline, CI/CD integration (validate → deploy dev → deploy prod). Alternatywa przed DABs: Terraform provider albo ręczny UI — oba gorsze do team collaboration.

2. **Co to jest Delta Live Tables i czym różni się od zwykłego PySpark pipeline'u?**

   Dobra odpowiedź: DLT = deklaratywny framework pipelines. Piszesz `@dlt.table` definicje zamiast sekwencji read/transform/write. Databricks automatycznie zarządza: kolejnością (zależności z `dlt.read()`), retry przy błędach, monitoringiem, data quality (`@dlt.expect`). Imperatywny PySpark: ręcznie kontrolujesz wszystko. DLT: deklarujesz CO ma być, nie JAK to zbudować.

3. **Co to są `@dlt.expect` i `@dlt.expect_or_drop`?**

   Dobra odpowiedź: Wbudowane testy danych w DLT. `@dlt.expect("name", "condition")` = zbiera rekordy łamiące constraint jako metryki, ale nie usuwa ich. `@dlt.expect_or_drop` = usuwa złe rekordy ze strumienia (quarantine). `@dlt.expect_or_fail` = zatrzymuje cały pipeline. DLT wyświetla metryki w UI: ile rekordów przeszło, ile odrzucono.

4. **Jak wygląda CI/CD dla Databricks pipeline'u?**

   Dobra odpowiedź: Git push → CI runner: `databricks bundle validate` (walidacja YAML) → `pytest` (testy lokalne z PySpark) → `databricks bundle deploy --target dev` → integration test na dev workspace → code review / approve → `databricks bundle deploy --target prod`. Token Databricks w CI jako secret (GitHub Secrets / GitLab CI Variables), nie w kodzie.

5. **Kiedy użyjesz DLT zamiast zwykłego Spark Job?**

   Dobra odpowiedź: DLT dobry gdy: chcesz wbudowaną data quality bez pisania własnych asercji, masz złożone zależności między tabelami, chcesz automatyczny monitoring i lineage w UI. Spark Job dobry gdy: potrzebujesz niestandardowej logiki której DLT nie obsługuje, masz istniejący kod który działa, DLT overhead nie jest wart dla prostego jednoetapowego pipeline'u.

---

## Extra

```text
Q: "Jak zarządzasz secretami w Databricks?"
- Databricks Secrets API: databricks secrets create-scope + put
- W kodzie: dbutils.secrets.get(scope="my-scope", key="db-password")
- NIE w databricks.yml (trafia do Git)
- NIE jako spark.conf (widoczne w UI)

Q: "Co to jest DLT Continuous vs Triggered?"
- Triggered: uruchamia się raz i kończy (jak batch Job)
- Continuous: działa non-stop jak streaming (micro-batch, Structured Streaming pod spodem)
```
