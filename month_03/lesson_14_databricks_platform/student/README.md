# Dla uczestnika: Lekcja 14 - Databricks Platform i Unity Catalog

## Otworz i zrob to

1. Zrozum, czego brakuje zwykłemu lakehouse'owi bez platformy: governance, katalogu, kontroli dostępu.
2. Przejrzyj architekturę Databricks i pojęcia: control plane, data plane, metastore, workspace.
3. Zrób proste notatki o Unity Catalog jako 3-poziomowym katalogu danych.
4. Finalny output zapisz w katalogu `homework/lesson_14/`.

Najkrótsza zasada folderow:

```text
student/lab/              = lokalne demo / symulacja platformy
homework/lesson_14/       = notatki i scenariusze governance
```

<!-- end_slide -->

## Cel lekcji

Po tej lekcji masz umiec powiedziec:

- co daje Databricks jako platforma, a czego nie da Ci sam Spark na laptopie,
- czym jest Unity Catalog i dlaczego ma 3 poziomy: `catalog.schema.table`,
- jak wygląda governance i segregation dostępu w danych produkcyjnych,
- kiedy w pracach z lakehouse potrzebne sa `OPTIMIZE`, `ZORDER`, `VACUUM`,
- jak myśleć o danych nie jako o katalogu plikow, tylko jako o katalogu semantycznych zasobów.

<!-- end_slide -->

## Dlaczego platforma jest potrzebna

Na małym pobraniu nawet prosty katalog danych zadziała. W produkcji pojawiają sie problemy:

- kto ma dostęp do ktorej tabeli,
- czy dane sa zgodne z definicjami,
- jak znajac lineage i właściciela danych,
- jak uruchamiac pipeline'y w kontrolowany sposob,
- jak monitorowac i utrzymywac tabele z wieloma jobami.

Databricks rozwiązuje to przez platforme, a nie poprzez "zwykły folder z csv". Governance i katalog danych sa wartosciami produkcyjnymi, nie opcja UX.

<!-- end_slide -->

## First Principles: Unity Catalog

Unity Catalog dodaje warstwe organizacji danych:

```text
catalog -> schema -> table
```

To pozwala na:

- wyraźne rozdzielenie danych biznesowych, analitycznych i operacyjnych,
- przypisanie uprawnien do katalogów i tabel,
- porządek w metastore i lineage,
- proste zarzadzanie danymi w wielu workspace'ach.

Dla Data Engineer jest to nie tylko "ładna nazwa", ale mechanizm kontroli i skalowalności platformy.

<!-- end_slide -->

## Jak uruchomic

Jeśli masz dostęp do Databricks, zrób prosty run z lokalnego demo. Jeśli nie, pracuj na symulacji działania `catalog.schema.table` w lokalnym notatniku / labie.

```bash
# miejsce do eksperymentow
python student/lab/delta_production_ops.py
```

<!-- end_slide -->

## Co oddajesz po lekcji

Minimalny output:

```text
homework/lesson_14/
├── unity_catalog_notes.md
├── delta_production_ops.py
├── governance_scenario.md
└── README.md
```

W praktyce:

- opisz 3 poziomy katalogu,
- zrob prosty lokalny workflow `OPTIMIZE` / `ZORDER` / `VACUUM`,
- wymysl scenariusz dostepu: kto ma czytać, kto ma pisać, kto ma widzieć tylko wybrane kolumny.

<!-- end_slide -->

## Pytanie kontrolne

Czy potrafisz wyjasnic:

- czym sie roznia workspace, metastore i catalog?
- po co jest row-level security albo masking?
- czemu `OPTIMIZE` nie jest "szybkim fixem" bez planowania?
- jak architektura platformy zmienia model podatnosci i operacji?

Jesli tak, to zaczynasz myślec jak platform engineer / data engineer, a nie tylko jak osoba pisząca SQL w notebooku.

<!-- end_slide -->
