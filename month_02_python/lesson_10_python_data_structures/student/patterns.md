# Patterns: Struktury danych w Pythonie

```text
DATA STRUCTURES - staly wzorzec

=== Wybierz od operacji ===
lookup po kluczu        -> dict
sprawdzanie unikalnosci -> set
kolejnosc i iteracja    -> list
staly klucz wielopolowy -> tuple

=== ETL patterns ===
accepted_records         -> list[dict]
seen_ids                 -> set[str]
records_by_id            -> dict[str, dict]
revenue_by_customer      -> dict[str, float]
composite_key            -> tuple[str, str]

=== Anti-patterny ===
[ ] lookup na duzej liscie zamiast dict/set
[ ] mutable obiekt jako klucz dict
[ ] set tam, gdzie potrzebna kolejnosc
[ ] tuple tam, gdzie kod musi modyfikowac rekord

=== Checklist ===
[ ] umiem uzasadnic wybor struktury pod operacje
[ ] umiem zrobic dedup przez set
[ ] umiem zrobic counting/grouping przez dict
[ ] umiem uzyc tuple jako klucza zlozonego
```
