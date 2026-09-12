---
title: Lekcja 08 - Production readiness w Pythonie
author: Data Engineering Course
date: 2026-08-14
---

# Lekcja 08

Gotowość produkcyjna w Pythonie

```text
układ src -> CLI -> testy -> logowanie -> retry -> runbook
```

To nie jest „większy framework”, tylko porządek. Porządek pozwala komuś innemu uruchomić pipeline, zrozumieć logi i naprawić go bez zgadywania.

<!-- end_slide -->

# TL;DR

Skrypt, który działa lokalnie, nie musi być gotowy do review. Minimalny standard produkcyjny wygląda tak:

```text
- czytelny układ src
- jawny punkt wejścia (CLI)
- testy dla logiki
- sensowne logi
- ograniczone retry dla błędów przejściowych
- README + runbook dla operacji
```

Jeśli czegoś z tego nie ma, pipeline jest tylko demo.

<!-- end_slide -->

# Problem

Skrypt działa lokalnie, ale nie da się go bezpiecznie uruchomić w pracy. Zwykle pojawiają się pytania:

```text
jak podałem dane wejściowe?
gdzie zapisuje wynik?
gdzie są logi?
jak zrobić ponowne uruchomienie po błędzie?
czy transformacja ma testy?
```

Jeśli brak odpowiedzi, to nie ma odpowiedzialności i nie ma zaufania do procesu.

<!-- end_slide -->

# Dlaczego to jest ważne

W pracy nie chodzi o to, czy kod jest „ładny” albo „czy działa na moim laptopie”. Chodzi o to, czy ktoś inny potrafi:

```text
- uruchomić job
- zrozumieć wejście i wyjście
- odtworzyć problem
- sprawdzić, czy błędy są przejściowe czy biznesowe
- prowadzić działający pipeline bez tajemnic
```

To jest kluczowy poziom dojrzałości inżynierii danych.

<!-- end_slide -->

# Minimalny standard projektu

```text
src/
tests/
README.md
runbook.md
CLI
logging
retry policy
```

Nie potrzebujesz ciężkiego frameworku. Potrzebujesz czytelnego minimum architektonicznego, które można sensownie utrzymywać.

<!-- end_slide -->

# Układ src

```text
src/pipeline/
  cli.py
  extract.py
  transform.py
  load.py

tests/
  test_transform.py
  test_contracts.py
```

Moduły są małe, mają jedną odpowiedzialność i łatwiej je review'ować. To ważne nie tylko dla Pythona, ale dla całego data engineering.

<!-- end_slide -->

# Co oznacza dobrze zorganizowany moduł

```text
extract.py -> pobiera dane i wykonuje parsowanie
transform.py -> normalizuje i agreguje
load.py -> zapisuje wynik na końcu
models.py -> kontrakty i typy danych
cli.py -> punkt wejścia i parsowanie argumentów
```

Dobrze podzielony moduł jest łatwiejszy do testowania, debugowania i wyjaśniania problemów bez zgadywania.

<!-- end_slide -->

# CLI

```bash
python -m pipeline.cli --input data/orders.json --output output/result.json
```

CLI robi dwie rzeczy: usuwa ręczne „edytowanie kodu pod konkretne dane” i daje jasno zdefiniowany punkt wejścia. To jest bardzo ważne przy pracy w zespole.

<!-- end_slide -->

# Logowanie

```python
logger.info("Loaded records", extra={"count": len(records)})
```

Log powinien powiedzieć:

```text
co startowało
ile rekordów weszło
co zapisano
czy wystąpił błąd i na którym etapie
```

Dobrze napisany log jest pomostem między developerem a operatorem pipeline.

<!-- end_slide -->

# Logowanie kontra debugowanie

```text
debugging: pokazuje szczegóły techniczne
logging: pokazuje stan operacyjny
```

Dobrze ustawiony log nie musi być ogromny. Ma pokazać „co się działo” w sensie operacji, nie tylko „stack trace w środku nocy”.

<!-- end_slide -->

# Retry

```text
błąd przejściowy I/O / timeout -> retry ma sens
niepoprawny payload -> retry nie ma sensu
```

Błąd z sieci to inna klasa problemu niż błąd danych. Retry nie jest rozwiązaniem na wszystko.

<!-- end_slide -->

# Polityka retry: ograniczona i sensowna

```text
- max 3-5 prób
- exponential backoff
- tylko dla błędów typu 429 / timeout / 5xx
- nie retry dla 400 / 401 / błędu kontraktu
```

To jest ważne, bo retry „na siłę” zamienia problem jakości danych w zjawisko operacyjne i zwiększa koszty.

<!-- end_slide -->

# Testy

```python
def test_completed_revenue_counts_only_completed() -> None:
    records = [
        {"status": "completed", "total_amount": 100.0},
        {"status": "pending", "total_amount": 50.0},
    ]
    assert calculate_completed_revenue(records) == 100.0
```

Testy powinny sprawdzać czystą logikę bez realnego schedulera, AWS i zewnętrznych zależności. To daje zaufanie do transformacji.

<!-- end_slide -->

# Jaki poziom testów ma sens

```text
- unit tests dla funkcji transformacji
- testy dla reguł walidacji
- małe golden tests dla znanych danych wejściowych
- brak testów dla zewnętrznego systemu w środowisku produkcyjnym
```

Celem nie jest „testować wszystkiego”, tylko mieć zaufane, małe fragmenty logiki, które można szybko sprawdzić.

<!-- end_slide -->

# Runbook

Runbook to instrukcja po awarii. Powinien zawierać:

```text
jak uruchomić job
jak wykonać rerun po błędzie
gdzie są wejścia i wyjścia
gdzie są logi
najczęstsze błędy
właściciel danych / kontakt do źródła
```

Dobre runbooki są zwykle bardziej cenione niż błyskotliwe demo.

<!-- end_slide -->

# Definition of Done

```text
[ ] projekt ma czytelny układ src
[ ] pipeline ma CLI
[ ] logi są sensowne i operacyjne
[ ] retry jest ograniczony do błędów przejściowych
[ ] testy obejmują transformacje i kontrakty
[ ] README i runbook mówią, jak uruchomić i naprawić projekt
```

To jest pierwszy krok od „demo” do „prawie produkcyjnego projektu”.

<!-- end_slide -->

# Odpowiedź na pytanie rekrutacyjne

Pytanie:

```text
Jak zbudować mały produkcyjny projekt ETL w Pythonie?
```

Odpowiedź:

```text
Dzielę pobieranie danych, transformację i ładowanie na małe moduły w src.
Eksponuję przepływ przez CLI z jasnymi argumentami wejściowymi i wyjściowymi.
Zachowuję czystą logikę pod testami i zapisuję logi dla punktów wejścia i błędów.
Błędy sieciowe mają ograniczone retry, a niepoprawne dane są odrzucane, a nie retryowane w nieskończoność.
README i runbook opisują, jak uruchomić i odzyskać job.
```

<!-- end_slide -->

# Checklist do powtórki

```text
[ ] Czy potrafisz opisać minimalny produkcyjny układ projektu?
[ ] Czy rozumiesz, dlaczego CLI jest ważne?
[ ] Czy umiesz odróżnić błąd przejściowy od błędu kontraktu?
[ ] Czy wiesz, po co są runbook i README?
[ ] Czy rozumiesz, że testy są częścią bezpieczeństwa operacyjnego, nie tylko „dobrego stylu”?
```

<!-- end_slide -->
