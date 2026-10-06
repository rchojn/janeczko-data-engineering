# Teoria: Lekcja 14 - Databricks Platform (ELI5)

Ta lekcja odpowiada na pytanie: "kto ma dostęp do jakich danych i jak utrzymać Delta w dobrej formie?"

## Minimum tej lekcji

```text
1. Rozumiem Control Plane vs Data Plane.
2. Rozumiem Unity Catalog: catalog.schema.table.
3. Rozumiem small files problem.
4. Wiem po co OPTIMIZE i VACUUM.
5. Umie wyjasnic governance na prostym przykładzie.
```

## 1. Control Plane vs Data Plane

```text
Control Plane = UI, Jobs, zarzadzanie
Data Plane    = Twoje dane i compute w Twoim cloud
```

Najprościej:
- Databricks pomaga zarządzać,
- dane nadal są "u Ciebie" (S3/ADLS/GCS).

## 2. Unity Catalog

Unity Catalog porządkuje wszystko jednym standardem:

```text
catalog.schema.table
```

Przykład:

```text
prod.finance.orders
dev.ml.features
```

To daje:
- spójne nazwy,
- łatwiejsze uprawnienia,
- mniej chaosu między zespołami.

## 3. Small files problem

Jeśli często robisz append, Delta ma dużo małych plików.

```text
append x100 -> 100 malych plikow
read        -> wolniej
```

## 4. OPTIMIZE i VACUUM

```text
OPTIMIZE = laczy male pliki w wieksze
VACUUM   = usuwa stare pliki niepotrzebne juz do aktualnej wersji
```

Uwaga produkcyjna:
- VACUUM za agresywnie = tracisz stary time travel.

## 5. Governance - prosty scenariusz

Scenariusz:
- analityk ma widzieć `amount`,
- nie ma widzieć `credit_card_number`.

Rozwiązanie:
- grant SELECT na tabelę,
- column masking dla PII.

## STALY PATTERN - zapamietaj to

```text
DATABRICKS GOVERNANCE CHECKLIST

1) Namespace: catalog.schema.table
2) Kto czyta? Kto pisze? (role)
3) Czy sa kolumny PII? -> masking
4) Czy tabela ma duzo malych plikow? -> OPTIMIZE
5) Czy retention VACUUM jest bezpieczny?
```

Zdanie na prezentację:

```text
"Unity Catalog porzadkuje dostep,
a OPTIMIZE/VACUUM porzadkuje fizyczne pliki Delta."
```
