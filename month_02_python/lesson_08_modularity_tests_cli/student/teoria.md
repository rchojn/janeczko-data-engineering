# Teoria: Lekcja 08 — ściąga do pracy domowej

Ten plik to ściąga do użycia PODCZAS pracy domowej.
Teoria jest na slajdach — tu masz wzorzec i checklistę.

## STALY PATTERN - zapamietaj to

```text
PRODUCTION PYTHON ETL - staly pattern

=== src layout ===
src/pipeline/
  cli.py
  extract.py
  transform.py
  load.py
# Kod jest importowalny i testowalny.

=== CLI ===
python -m pipeline.cli --input data/orders.json --output output/result.json
# Parametry ida z zewnatrz, nie przez edycje kodu.

=== Logging ===
logger.info("Loaded records", extra={"count": count})
# Run zostawia slad.

=== Retry ===
retry(operation, attempts=3)
# Tylko dla bledow przejsciowych, nie dla zlego schematu.

=== Tests ===
tests/test_transform.py
# Testujemy logike bez prawdziwego scheduler'a.

=== Runbook ===
What failed? How to rerun? Where are logs? Who owns source?
# Operator wie, co zrobic po awarii.

CHECKLIST:
[ ] Czy pipeline uruchamia sie z CLI?
[ ] Czy input/output sa parametrami?
[ ] Czy transformacje maja testy?
[ ] Czy logi mowia, ile rekordow przetworzono?
[ ] Czy retry ma limit?
[ ] Czy runbook opisuje rerun?
```
