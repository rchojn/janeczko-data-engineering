# Patterns: Spark na Databricks

```text
SPARK ON DATABRICKS — staly wzorzec

=== Workflow ===
workspace
  -> notebook
  -> compute
  -> read / transform
  -> Delta write
  -> job

=== Development vs production ===
manual notebook run = development
scheduled job       = operacyjny pipeline

=== Incremental ingest ===
new files
  -> Auto Loader
  -> checkpoint
  -> Delta table

=== Pytania kontrolne ===
Gdzie wykonuje sie kod?
Gdzie zyje output?
Jak pipeline pamieta progres?
Kto odpala run i jak go monitoruje?

=== Checklist ===
[ ] umiem nazwac compute
[ ] umiem nazwac notebook role
[ ] umiem wyjasnic Delta output
[ ] umiem wyjasnic checkpoint
[ ] umiem pokazac przejscie notebook -> job
```
