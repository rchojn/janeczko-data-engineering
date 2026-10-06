# Praca domowa: Lekcja 14

## Cel

Masz pokazać, że rozumiesz różnicę między "uruchomieniem Sparka" a "zarządzaniem platformą danych".

Platforma nie jest tylko silnikiem. To jest warstwa governance, security, isolation i operational control.

## Problem biznesowy

Twój job działa, ale pytanie brzmi:

```text
Kto ma dostęp do danych?
Gdzie jest katalog tabel?
Czy dane są wygenerowane w jednym notebook i zapisane w różnych miejscach?
```

To jest standardowy problem lakehouse, który pojawia się dopiero przy bardziej dojrzałej organizacji.

## Zadania

### 1. Unity Catalog namespace

Napisz `unity_catalog_notes.md` dla małej firmy z 3 teamami:

- `prod` i `dev`
- `finance`, `marketing`, `ml`
- minimum 2 tabele w każdym schemacie
- tabela uprawnień: rola -> read -> write

### 2. Delta production ops

Uruchom `student/lab/delta_production_ops.py` i zapisz:
- ile plików było przed `OPTIMIZE`,
- ile po `OPTIMIZE`,
- kiedy w produkcji taki krok ma sens.

### 3. Governance scenario

Przy tabeli:

```text
order_id, customer_id, amount, credit_card_number, status
```

Odpowiedz na 3 pytania:

1. Jakie granty dać `data_analyst`?
2. Jak ukryć `credit_card_number`?
3. Kiedy użyć `Row-Level Security`?

## Acceptance criteria

- [ ] `unity_catalog_notes.md` ma 3 poziomy katalogów i role
- [ ] jest przynajmniej 3 role z uprawnieniami
- [ ] `delta_production_ops.py` uruchamia się bez błędów
- [ ] widzisz różnicę między przed i po `OPTIMIZE`
- [ ] scenariusz governance ma odpowiedzi na wszystkie 3 pytania
