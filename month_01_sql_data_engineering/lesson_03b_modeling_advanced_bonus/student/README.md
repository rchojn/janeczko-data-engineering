# Dla uczestnika: Bonus 03b - zaawansowane pojęcia modelowania

Ten bonus jest dla osób, które zrobiły lekcję 03 i chcą lepiej rozumieć słowa pojawiające się w rozmowach o data modelingu.

Nie jest wymagany do zaliczenia miesiąca 01.

To tutaj wchodzimy w SCD Type 1/2. W głównej lekcji 03 zostaje tylko intuicja: czy zmiana wymiaru ma być widoczna historycznie, czy wystarczy aktualny opis.

## Otwórz I Zrób To

1. Przeczytaj [teoria.md](teoria.md).
2. Przejdź aktywnie przez [lab/in_class_tasks.sql](lab/in_class_tasks.sql).
3. Jeśli chcesz utrwalić temat, zrób [homework.md](homework.md).

## Co Masz Zrozumieć

Po bonusie masz umieć powiedzieć:

- czym różni się business key od surrogate key,
- czym różni się SCD Type 1 od SCD Type 2,
- po co istnieją conformed dimensions,
- jakie są podstawowe typy fact tables,
- czym różnią się additive, semi-additive i non-additive measures,
- co to jest degenerate dimension,
- kiedy potrzebna jest bridge table,
- czym semantic layer różni się od Gold table,
- których tematów nie implementujemy jeszcze w miesiącu 01.

## Granica Bonusu

To jest mapa pojęć i mini-przykłady, nie pełny projekt hurtowni.

W miesiącu 01 wystarczy:

```text
grain -> fact/dim -> Gold -> checks -> reliability basics
```

Te zaawansowane pojęcia wrócą mocniej przy dbt, semantic layer, projekcie końcowym i rozmowach interview.
