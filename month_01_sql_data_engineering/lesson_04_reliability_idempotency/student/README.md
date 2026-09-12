# Dla uczestnika: Lekcja 04 - niezawodnosc i idempotencja

## Otworz I Zrob To

1. Przejdz [teoria.md](teoria.md) jako prezentacje/teorie lekcji.
2. Przeczytaj case w [lab/reliability_case.md](lab/reliability_case.md).
3. Uruchom lab z [lab/](lab/) i uzupelnij [lab/in_class_tasks.sql](lab/in_class_tasks.sql).
4. W trakcie lekcji wracaj do [pytania_na_lekcji.md](pytania_na_lekcji.md).
5. Zrob [homework.md](homework.md).

Ta lekcja domyka miesiac 01: po modelowaniu danych z lekcji 03 uczysz sie, jak sprawic, zeby pipeline dal zaufany wynik po retry, duplikacie eventu, update, delete i late arriving data.

## Co Masz Zrozumiec

Po tej lekcji masz umiec powiedziec:

- co znaczy idempotentny pipeline,
- co ACID i izolacja transakcji chronia w zapisie danych,
- dlaczego ACID w systemach rozproszonych jest trudniejsze niz w lokalnej bazie,
- dlaczego retry moze tworzyc duplikaty,
- czym roznia sie surowe zmiany w Bronze od aktualnego stanu w Silver,
- czym rozni sie event key od business key,
- jak wybrac najnowszy rekord po kluczu biznesowym,
- gdzie obslugiwac `DELETE`, `refunded` i `paid`,
- czym sa spoznione dane i po co jest lookback window,
- po co sa run metadata, walidacje i runbook,
- jak mowic o data trust na interview.

## Jak Uruchomic Lab

Z katalogu `student/lab/`:

```bash
sqlite3 lesson_04.db < schema.sql
sqlite3 lesson_04.db < seed_data.sql
sqlite3 lesson_04.db
```

W SQLite uruchamiaj kolejne fragmenty z [lab/in_class_tasks.sql](lab/in_class_tasks.sql).

Reset:

```bash
rm -f lesson_04.db
sqlite3 lesson_04.db < schema.sql
sqlite3 lesson_04.db < seed_data.sql
```

## Najwazniejszy Kontrakt

W kazdym kroku pipeline'u dopisz jedno zdanie:

```text
jeden rekord = ...
```

I odpowiedz:

```text
Co stanie sie, jesli ten sam input przetworze drugi raz?
```

Jesli nie umiesz odpowiedziec, pipeline nie jest jeszcze retry-safe.

Ta lekcja pokrywa najwazniejszy fragment `Standardy Big Data` z programu: ACID/izolacja, CDC oraz praktyczna niezawodnosc pipeline'u.

## Materialy Rekomendowane

Wybierz jedno zrodlo jako kontekst do `video_notes.md`:

- [Debezium: What is change data capture?](https://debezium.io/documentation/reference/stable/architecture.html) - kontekst CDC i zmian ze zrodla.
- [Delta Lake: Upsert into a table using merge](https://docs.delta.io/latest/delta-update.html#upsert-into-a-table-using-merge) - po co istnieje `MERGE` w retry-safe load.
- [Databricks: What is a lakehouse?](https://www.databricks.com/glossary/data-lakehouse) - czemu table formats pomagaja, ale nie zastepuja logiki pipeline'u.
- YouTube: kanal [Data With Zach](https://www.youtube.com/@datawithzach), temat `data quality`, `CDC` albo `slowly changing dimensions` - ogladamy po to, zeby nazwac ryzyka: retry, duplikaty, late data, delete.