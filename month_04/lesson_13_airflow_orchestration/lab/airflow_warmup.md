# Warmup: Jak Rozbic Pipeline Na Taski?

Zanim uruchomisz Airflow, potraktuj pipeline jak prosty problem projektowy.

## Kontekst

Firma e-commerce chce codziennie rano odswiezyc dashboard sprzedazy.

Dane przychodza z trzech zrodel:

```text
orders
order_items
customers
```

Proces biznesowo wyglada tak:

```text
1. ustal date przetwarzania
2. pobierz dane z kazdego zrodla
3. sprawdz, czy dane wejsciowe sa kompletne
4. uruchom modele dbt
5. uruchom testy jakosci danych
6. opublikuj wynik dla BI
7. wyslij notyfikacje o wyniku
```

Twoim zadaniem nie jest jeszcze pisanie kodu. Najpierw zdecyduj, jak ten proces powinien wygladac jako DAG.

## Zadanie 1: Osobne Taski

Zaznacz, ktore kroki powinny byc osobnymi taskami.

Podpowiedz: osobny task ma sens, gdy chcesz osobno widziec status, logi albo retry danego kroku.

| Krok | Osobny task? | Dlaczego? |
| --- | --- | --- |
| ustal date przetwarzania | tak / nie | |
| pobierz `orders` | tak / nie | |
| pobierz `order_items` | tak / nie | |
| pobierz `customers` | tak / nie | |
| sprawdz dane wejsciowe | tak / nie | |
| uruchom `dbt run` | tak / nie | |
| uruchom `dbt test` | tak / nie | |
| opublikuj wynik dla BI | tak / nie | |
| wyslij notyfikacje | tak / nie | |

## Zadanie 2: Task Groups

Pogrupuj taski tak, zeby graf byl czytelny.

Mozesz uzyc takich grup albo zaproponowac wlasne:

```text
extract_and_validate
transform_and_quality
publish_and_notify
```

Wpisz po 1-3 taski, ktore dalbys do kazdej grupy.

## Zadanie 3: Co Moze Byc Dynamiczne?

Popatrz na zrodla:

```text
orders
order_items
customers
```

Czy pisalbys osobny kod taska dla kazdego zrodla, czy jeden task uruchamiany wiele razy z roznym parametrem?

Odpowiedz jednym zdaniem.

## Zadanie 4: Retry I Blokowanie Downstream

Dla ponizszych sytuacji zdecyduj:

- czy retry ma sens,
- czy kolejne kroki powinny sie zatrzymac.

| Sytuacja | Retry ma sens? | Czy zatrzymac downstream? |
| --- | --- | --- |
| chwilowy timeout API | tak / nie | tak / nie |
| brak wymaganej kolumny w danych | tak / nie | tak / nie |
| `dbt test` wykrywa duplikaty | tak / nie | tak / nie |
| BI refresh chwilowo nie odpowiada | tak / nie | tak / nie |

## Zadanie 5: Rola Narzedzi

Dopasuj narzedzie do roli:

| Element procesu | Najlepsze miejsce |
| --- | --- |
| orkiestracja kolejnosci krokow | Airflow / dbt / Databricks |
| transformacje SQL i testy modeli | Airflow / dbt / Databricks |
| ciezkie przetwarzanie Spark | Airflow / dbt / Databricks |
| odpalenie calego procesu wedlug harmonogramu | Airflow / dbt / Databricks |

Na koniec odpowiedz jednym zdaniem:

```text
Dlaczego Airflow nie powinien byc miejscem na ciezka transformacje danych?
```
