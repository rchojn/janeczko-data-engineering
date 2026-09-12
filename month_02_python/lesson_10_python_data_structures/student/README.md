# Dla uczestnika: Lekcja 10 - Struktury danych w Pythonie

## Otworz i zrob to

1. Przeczytaj [teoria.md](teoria.md).
2. Przejdz [patterns.md](patterns.md) i zapamietaj kiedy uzywac list, tuple, set, dict.
3. Uruchom [lab/python_data_structures.py](lab/python_data_structures.py).
4. Zrob [homework.md](homework.md).
5. Przecwicz odpowiedzi z [interview_questions.md](interview_questions.md).

Najkrotsza zasada folderow:

```text
student/lab/         = cwiczenie wyboru struktury danych
homework/lesson_10/  = finalny artefakt do review
```

## Cel lekcji

Po tej lekcji masz umiec odpowiedziec:

- kiedy uzyc list, a kiedy set,
- dlaczego dict to podstawowa struktura dla rekordow,
- po co tuple jako immutable key,
- jak uniknac anti-patternu: "wszystko trzymam w liscie",
- jak dobrac strukture pod operacje: lookup, dedup, agregacja.

Najwazniejszy flow tej lekcji:

```text
problem danych -> operacja -> wybor struktury -> check zlozonosci -> implementacja
```

## Co umiesz po lekcji

- rozroznic mutowalne i niemutowalne struktury,
- zrobic deduplikacje przez set,
- zrobic counting i grouping przez dict,
- uzyc tuple jako stabilnego klucza,
- uzasadnic wybor struktury w kontekscie ETL.

## Jak uruchomic lab

```bash
python student/lab/python_data_structures.py
```
