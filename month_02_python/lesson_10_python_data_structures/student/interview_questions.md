# Interview questions: Lekcja 10 - Struktury danych w Pythonie

## Pytania

1. Kiedy w ETL wybierasz set zamiast list?
2. Jak dziala dict i czemu jest szybszy do lookupu niz list?
3. Kiedy tuple jest lepsze niz list?
4. Jak zrobic counting rekordow po kluczu customer_id?
5. Co sie stanie, jesli uzyjesz mutable list jako klucza dict?
6. Jak zaprojektujesz dedup orderow po order_id dla 5 mln rekordow?
7. Jak udowodnisz testem, ze agregacja liczy tylko completed orders?
8. Jakie anti-patterny widzisz przy wyborze struktur danych?

## Krotkie odpowiedzi wzorcowe

- set wybieram do dedup i membership check,
- dict wybieram do mapowania key -> value i agregacji,
- tuple wybieram do immutable composite key,
- list wybieram do uporzadkowanej iteracji,
- mutable object nie moze byc kluczem dict, bo nie jest hashable.
