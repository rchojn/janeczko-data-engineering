# Dla uczestnika: Lekcja 03 - modelowanie danych, Medallion, Kimball i OLAP

## Otwórz I Zrób To

1. Przeczytaj [teoria.md](teoria.md).
2. Przeczytaj case w [lab/modeling_case.md](lab/modeling_case.md).
3. Uruchom lab z [lab/](lab/).
4. Zrób [homework.md](homework.md).

Homework wymaga rdzenia modelu: Silver views, `dim_customer`, `dim_product`, `fact_sales`, `gold_daily_sales` oraz bardziej analitycznego `gold_sales_by_region_category`.

Najważniejsze rozszerzenie względem minimum: masz porównać star schema z gotowym Goldem i podjąć mini-decyzję, czy zmieniające się wymiary wymagają historii.

SCD Type 1/2 i pełny SQL historyczny są opcjonalnym bonusem 03b. Najpierw masz rozumieć decyzję: nadpisać aktualną wartość czy zachować historię.

Jeśli po tej lekcji chcesz uporządkować bardziej zaawansowane słowa z modelowania, przejdź opcjonalnie [Bonus 03b](../../lesson_03b_modeling_advanced_bonus/student/README.md): SCD, surrogate keys, conformed dimensions, typy fact tables i semantic layer.

## Co Masz Zrozumieć

Po tej lekcji masz umieć powiedzieć:

- czym różnią się Bronze, Silver i Gold,
- skąd historycznie wzięło się podejście Kimball/fact/dim,
- jak Medallion łączy się z Kimball i star schema,
- czym star schema różni się od gotowej tabeli Gold,
- co istnieje obok star schema: normalizacja/3NF, wide Gold, snowflake schema, historia wymiaru i Data Vault jako różne typy decyzji,
- czym lokalna historia wymiaru różni się od Data Vault,
- gdzie w tym obrazie siedzi OLAP/dashboard,
- kiedy gotowa tabela Gold jest praktyczna, a kiedy potrzebujesz bardziej elastycznego fact/dim,
- kiedy zmiana atrybutu w dimension table wymaga historii, a kiedy wystarczy aktualny opis,
- dlaczego grain jest decyzją projektową,
- jak zamodelować prosty case e-commerce albo Netflix-style analytics.

## Jak Uruchomić Lab

Z katalogu `student/lab/`:

```bash
sqlite3 lesson_03.db < schema.sql
sqlite3 lesson_03.db < seed_data.sql
sqlite3 lesson_03.db
```

Reset:

```bash
rm -f lesson_03.db
sqlite3 lesson_03.db < schema.sql
sqlite3 lesson_03.db < seed_data.sql
```

## Materiały Rekomendowane

Wybierz jedno źródło jako kontekst do krótkiej odpowiedzi technicznej:

- [Databricks: Medallion architecture](https://www.databricks.com/glossary/medallion-architecture) - Bronze/Silver/Gold w lakehouse.
- [Microsoft Learn: Medallion lakehouse architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion) - praktyczne wyjaśnienie warstw.
- [Kimball Group: Fact tables and dimension tables](https://www.kimballgroup.com/2003/01/fact-tables-and-dimension-tables/) - klasyczne źródło fact/dim.
- YouTube: [Data With Zach](https://www.youtube.com/datawithzach), temat dimensional modeling, fact/dim albo analytics modeling.

## Najważniejszy Kontrakt

W każdej tabeli modelu dopisz jedno zdanie:

```text
jeden rekord = ...
```

Jeśli nie umiesz tego zdania napisać, model nie jest jeszcze gotowy.