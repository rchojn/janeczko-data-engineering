# Dla uczestnika: Lekcja 12 - Lakehouse: Delta Lake i Iceberg

## Otworz i zrob to

1. Zrozum problem plain Parquet i dlaczego dane lakehouse potrzebuja transakcji.
2. Uruchom demo z [lab/lakehouse_demo.py](lab/lakehouse_demo.py).
3. Zobacz, jak Delta zapisuje commit log i jak działa time travel.
4. Finalna praca domowa zapisz w katalogu `homework/lesson_12/`.
5. Po lekcji przejdz [homework.md](homework.md).

Najkrótsza zasada folderow:

```text
student/lab/              = lokalne demo, eksperymenty i mini-proby
homework/lesson_12/       = finalny pipeline z Delta / Iceberg do review
```

Ważna granica:
- `student/lab/` służy do nauki i sprawdzania pomyslu,
- `homework/lesson_12/` to finalny artefakt, ktory ma byc spójny, testowalny i gotowy do review.

Nie myl `Parquet` z `Delta` — Parquet jest formatem plików, a Delta/Lakehouse dodaje warstwe katalogu metadanych, transakcji i historii.

<!-- end_slide -->

## Cel lekcji

Po tej lekcji masz umiec powiedziec:

- dlaczego zwykly folder z Parquetem nie wystarcza w produkcji,
- czym sie roznia `Parquet`, `Delta Lake` i `Iceberg`,
- jak działa ACID w lakehouse na poziomie tabeli,
- po co jest schema evolution i time travel,
- kiedy warto przejsc z plain data lake do table formatu.

<!-- end_slide -->

## Dlaczego "plain Parquet" nie jest wystarczające

Plain Parquet daje bardzo dobry format do odczytu i zapisu, ale to dalej jest tylko plik. Gdy kilka jobow zapsiuje do tego samego katalogu jednoczesnie, pojawia sie problem:

- nadpisanie rewritow do tej samej tabeli,
- brak jednoznacznej historii zmian,
- trudnosci z rollbackiem po zlym jobie,
- brak semantyki transakcyjnej przy wielu writerach.

W praktyce taka sytuacja oznacza, ze dane zyskuja "wyplywy" i tracą zaufanie. Delta Lake i Iceberg dodaja warstwe kontrolna: walidacje, manifesty, mechanizmy commitow i bezpieczne odczyty.

<!-- end_slide -->

## First Principles: co robi table format

Table format rozwiązuje konkretne problemy:

```text
1. commit history          — wiemy, co zostało zapisane i kiedy
2. transaction safety     — nie ma przypadkowego nadpisania przez dwa joby
3. schema evolution       — dodajemy kolumny bez destrukcyjnej przebudowy
4. time travel            — wracamy do poprzedniej wersji danych
5. metadata layer         — joby czytaja tabele a nie przypadkowe pliki
```

Delta Lake i Iceberg robią to w podobny sposob, lecz maja inne decyzje architektoniczne i kompromisy. W pracy na platformie nie chodzi o "wybrac najlepszy format", tylko o "dobrac format do konkretnego modelu pracy i operacji".

<!-- end_slide -->

## Dlaczego to ma znaczenie w produkcji

W firmowym pipeline dane zwykle przechodza przez kilka etapow:

```text
bronze raw -> silver cleaned -> gold aggregated -> downstream dashboards
```

Na tym etapie zly zapis, brak kontrolnej wersji, albo brak przewidzenia schema drift stają sie realnym problemem biznesowym: raporty sie rozjeżdżaja, tablice tracą sens, dane sa "byly poprawne do wczoraj". Delta i Iceberg pozwalaja utrzymac porzadek przy dużej skali.

<!-- end_slide -->

## Jak uruchomic

```bash
pip install pyspark==3.5.0 delta-spark==3.2.0
python student/lab/lakehouse_demo.py
```

W labie zrobisz:

- odczyt danych w formacie Delta,
- zapis tabeli z transakcja,
- porownanie `Parquet` vs `Delta` w praktyce,
- przykładowy `time travel` i `schema evolution`.

<!-- end_slide -->

## Co oddajesz po lekcji

Oddajesz finalny katalog `homework/lesson_12/`.

Typowy output:

```text
homework/lesson_12/
├── delta_pipeline.py
├── schema_evolution_case.md
├── tests/
│   └── test_delta.py
└── README.md
```

Twoje zadanie w praktyce:

- zapisać DataFrame jako Delta table,
- dodać kolumnę i sprawdzić schema evolution,
- zrobic update na jednym rekordzie,
- odczytac poprzednia wersje danych (time travel),
- opisać, kiedy Delta ma sens w porownaniu do plain Parquet.

<!-- end_slide -->

## Zasada pracy

Najpierw zadaj pytanie biznesowe, potem implementuj technicznie.

```text
Czy to ma byc tabela do analityki? Czy wymagana jest historia zmian?
Czy niektore kolumny beda sie zmieniac w czasie?
Czy musze wykonać rollback po zlym jobie?
```

Jeśli odpowiedź brzmi "tak", to table format jest już nie dodatkiem, tylko podstawą architektury.

<!-- end_slide -->

## Pytanie kontrolne

Czy potrafisz wyjasnic róznice pomiedzy:

- `Parquet` a `Delta`?
- `schema evolution` a `schema enforcement`?
- `time travel` a `rollback`?
- `ACID` a `append-only`?

To jest wlasnie moment, w ktorym przechodzisz z "umiem zapisac plik" na "umiem zarzadzac table w lakehouse".

<!-- end_slide -->
