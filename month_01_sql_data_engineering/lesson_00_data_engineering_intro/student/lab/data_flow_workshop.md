# Lab: pierwszy przeplyw danych

<!-- end_slide -->

## Cel

Masz zbudowac pierwszy obrazek w glowie: skad dane startuja, gdzie sa przetwarzane i gdzie koncza jako metryka albo dashboard.

Nie musisz jeszcze znac SQL, Sparka, dbt ani Airflow. W tym labie wystarczy prosty diagram i kilka zdan wlasnymi slowami.

Ten lab jest dla chetnych do utrwalenia po spotkaniu. Jesli go robisz, wpisuj odpowiedzi bezposrednio w tym pliku i dodaj go do pull requesta.

<!-- end_slide -->

## Jak pracowac aktywnie

Nie przepisuj diagramu mechanicznie. Po kazdym zadaniu dopisz jedno zdanie:

```text
Teraz rozumiem, ze...
Nadal myli mi sie...
Sprawdze to przez...
```

Lab jest zaliczony dopiero wtedy, gdy umiesz przerysowac finalny flow z pamieci i powiedziec, gdzie dane sa raw, gdzie trusted, a gdzie staja sie produktem danych.

<!-- end_slide -->

## Zanim zaczniesz

Przeczytaj tylko te fragmenty:

1. [../teoria.md](../teoria.md) - sekcje `Jak szeroko masz to rozumiec teraz?`, `OLTP vs OLAP`, `Data flow`.
2. Wroc do tych sekcji, jesli podczas rysowania nie wiesz, czym jest source, transformacja albo odbiorca danych.

Wybierz jeden material jako kontekst. Nie rob z tego researchu na 3 godziny.

- [IBM: What is data engineering?](https://www.ibm.com/think/topics/data-engineering) - jesli chcesz zrozumiec role Data Engineera.
- [Google Cloud: Data lake vs data warehouse](https://cloud.google.com/learn/data-lake-vs-data-warehouse) - jesli myla Ci sie lake, warehouse i raportowanie.

<!-- end_slide -->

## Zadanie 1: najprostszy przeplyw aplikacji

Narysuj to ponizej. Mozesz uzyc ASCII albo Excalidraw, ale w tym pliku zostaw wersje tekstowa albo link/screenshot:

```text
Uzytkownik
  -> Aplikacja
  -> Baza produkcyjna
```

Dopisz po jednym przykladzie danych, ktore moga tam powstac:

- utworzono klienta,
- utworzono zamowienie,
- zakonczono platnosc,
- wyswietlono produkt.

Na koncu dopisz 2 zdania:

```text
Baza produkcyjna jest potrzebna, bo...
Dashboard nie powinien zwykle czytac prosto z bazy produkcyjnej, bo...
```

<!-- end_slide -->

## Zadanie 2: dodaj analityke

Rozszerz diagram. Nie chodzi o ladny rysunek, tylko o to, zebys umial powiedziec, po co jest kazdy krok:

```text
Uzytkownik
  -> Aplikacja
  -> Baza produkcyjna
  -> Dzienny eksport / ingestion
  -> Bronze
  -> Silver
  -> Gold
  -> Dashboard
```

Pod diagramem napisz po jednym zdaniu:

```text
Bronze = ...
Silver = ...
Gold = ...
```

Nie szukaj idealnych definicji. Ma byc zrozumiale dla Ciebie.

<!-- end_slide -->

## Zadanie 3: oznacz typ elementu

Przepisz tabelke i wypelnij druga kolumne jednym z typow:

```text
zrodlo / ingestion / storage / transformacja / produkt
```

| Element | Typ | Jedno zdanie |
|---|---|---|
| Baza produkcyjna |  |  |
| Dzienny eksport |  |  |
| Bronze: surowe dane |  |  |
| Silver: oczyszczone dane |  |  |
| Gold: dzienny revenue |  |  |
| Dashboard |  |  |

<!-- end_slide -->

## Zadanie 4: transakcja czy event?

Wypelnij prosto:

| Przyklad | Transakcja czy event? | Dlaczego? |
|---|---|---|
| utworzono zamowienie |  |  |
| zakonczono platnosc |  |  |
| wyswietlono produkt |  |  |
| wykonano wyszukiwanie |  |  |

Podpowiedz:

```text
Transakcja = cos zmienia stan biznesowy, np. zamowienie albo platnosc.
Event = cos sie wydarzylo i chcemy to zapamietac, np. klikniecie albo wyszukiwanie.
```

<!-- end_slide -->

## Zadanie 5: dwa proste ryzyka

Wybierz tylko dwa ryzyka i dopisz, jak moglbys je zauwazyc:

| Ryzyko | Jak to zauwazymy? |
|---|---|
| zduplikowane rekordy |  |
| brakujacy `customer_id` |  |
| zla definicja revenue |  |
| dashboard pokazuje nieaktualne dane |  |

<!-- end_slide -->

## Zadanie 6: przerysuj z pamieci

Zamknij material na 3 minuty i narysuj finalny flow od zera. Potem porownaj z poprzednia wersja.

Ponizej dopisz:

```text
Co zapomnialem za pierwszym razem:
Co poprawilem po porownaniu:
Ktory etap jest dla mnie nadal niejasny:
```

<!-- end_slide -->

## Zadanie 7: mini-debug diagramu

Wybierz jeden incident i zaznacz, gdzie go wykryjesz:

```text
Incident A: revenue na dashboardzie jest 2x wyzsze niz zwykle.
Incident B: nie ma danych z wczoraj.
Incident C: customer_id jest pusty dla czesci zamowien.
```

Dopisz:

```text
Pierwszy etap do sprawdzenia:
Dlaczego ten etap:
Jaki prosty check bym uruchomil:
```

<!-- end_slide -->

## Co dodac do PR

Jesli robisz ten lab, dodaj do PR:

```text
student/lab/data_flow_workshop.md
```

Nie tworz osobnego `homework/lesson_00/` dla tej lekcji. Lesson 00 jest labem do utrwalenia, nie osobnym homeworkiem.

Minimalna zawartosc labu:

- 2 diagramy ASCII,
- 3 definicje: Bronze/Silver/Gold,
- tabelka elementow flow,
- tabelka transaction/event,
- 2 ryzyka,
- przerysowany flow z pamieci,
- 1 mini-debug incidentu.

Na koncu dopisz:

- 5 pytan, ktore nadal sa niejasne.

<!-- end_slide -->

## Stretch, tylko jesli podstawy sa jasne

Dodaj drugi wariant flow z event stream:

```text
Akcja uzytkownika
  -> Aplikacja
  -> Event stream
  -> Data lake
  -> Metrics
```

Napisz 3 zdania: kiedy event stream ma sens, a kiedy zwykly daily export wystarczy.
