# Praca domowa: Lekcja 15

## Cel

Masz pokazać, że pipeline danych to nie tylko kod, ale też środowisko operacyjne. W dat platformach niedobry deployment potrafi zniszczyć projekt równie skutecznie co zły SQL.

## Problem biznesowy

Twój pipeline działa w notebooku. W produkcji zaczyna się problem:

```text
kto kupuje deploy?
co się dzieje po merge?
czy dev i prod są w tej samej konfiguracji?
jak rollback po złej zmianie?
```

To jest moment, kiedy tracisz „works on my machine” i przechodzisz do release discipline.

## Zadania

### 1. Asset Bundle

Napisz `databricks.yml` dla pipeline z 2 taskami:

- `bronze`: czyta JSON z `/data/raw/orders/`
- `silver`: zapisuje dane jako Delta

Wymagania:
- targets: `dev` i `prod`
- różne `root_path`
- `depends_on` między taskami
- `AQE` włączone przez config

### 2. DLT pipeline

Napisz definicję `dlt_pipeline.py` z warstwami:

- `orders_bronze`
- `orders_silver`
- `revenue_gold`

Dodaj minimum jedno `@dlt.expect` i opisz, co kontroluje jakość danych.

### 3. DevOps flow

Narysuj `devops_flow.md` w ASCII:

```text
Git -> CI -> validate -> deploy dev -> approve -> deploy prod
```

Odpowiedz na 3 pytania:

- Co robi CI przed deploy?
- Jak zatrzymać prod bez ręcznego approve?
- Gdzie trzymasz secrets w CI?

## Acceptance criteria

- [ ] `databricks.yml` ma dev/prod i zależności pomiędzy taskami
- [ ] `dlt_pipeline.py` ma warstwy `bronze/silver/gold`
- [ ] istnieje przynajmniej 1 `@dlt.expect`
- [ ] `devops_flow.md` ma diagram + odpowiedzi na wszystkie pytania
- [ ] rozumiesz różnicę między kodem a gotowym release flow
