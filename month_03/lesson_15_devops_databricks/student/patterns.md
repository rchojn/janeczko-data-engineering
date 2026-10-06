# Patterns: DevOps w Databricks

```yaml
# DATABRICKS ASSET BUNDLES — stały wzorzec

# databricks.yml
bundle:
  name: my_pipeline
targets:
  dev:
    mode: development
    workspace:
      root_path: /Shared/dev/${bundle.name}
  prod:
    mode: production
resources:
  jobs:
    my_job:
      tasks:
        - task_key: step1
          python_file: src/step1.py
        - task_key: step2
          depends_on: [{task_key: step1}]
          python_file: src/step2.py
```

```python
# DELTA LIVE TABLES — stały wzorzec
import dlt
from pyspark.sql import functions as F

@dlt.table(name="bronze")
def bronze():
    return spark.read.json(path)

@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
@dlt.table(name="silver")
def silver():
    return dlt.read("bronze").withColumn("col", F.lower("col"))

@dlt.table(name="gold")
def gold():
    return dlt.read("silver").groupBy("key").agg(F.sum("val"))
```

```bash
# DABs CLI — stały workflow
databricks bundle validate --target dev    # sprawdź YAML
databricks bundle deploy  --target dev     # deploy
databricks bundle run     --target dev my_job
databricks bundle deploy  --target prod    # po approve
```

## Kiedy co

| Potrzebuję | Narzędzie |
|------------|-----------|
| Wdrożyć pipeline jako kod | DABs (`databricks.yml`) |
| Deklaratywny pipeline z data quality | DLT (`@dlt.table`, `@dlt.expect`) |
| Triggerowanie z zewnętrznego systemu | REST API (`/api/2.1/jobs/run-now`) |
| Testy przed deploy | pytest lokalny + `bundle validate` |
| Secrets w pipeline | Databricks Secrets API (`dbutils.secrets`) |
