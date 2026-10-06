---
title: Lekcja 15 - DevOps w Databricks
author: Data Engineering Course
date: 2026-09-16
---

# DevOps w Databricks

```text
Dane to nie tylko SQL i notebooky.
To też system produkcyjny, który wymaga CI/CD, bezpieczeństwa i kontroli środowisk.
```

<!-- end_slide -->

# Agenda

```text
1. Problem: notebook działa, ale pipeline nie jest produkcyjny
2. DABs jako infrastruktura jako kod
3. Azure DevOps jako warstwa CI/CD
4. Staging i prod jako kontrolowane środowiska
5. Security model: service connection, app registration, service principal
6. DLT jako deklaratywny pipeline i quality checks
7. Podsumowanie
```

<!-- end_slide -->

# Problem biznesowy

Masz działający notebook, ale pojawiają się pytania:

```text
Kto deployuje ten job do produkcji?
Czy secret jest zapisany w repo?
Czy pipeline ma rollback?
Czy prod ma inną politykę niż dev?
```

To nie jest problem SQL. To jest problem operacyjny i governance.

<!-- end_slide -->

# First principles

```text
Data platform = software system
```

Każdy system produkcyjny musi mieć:
- źródło prawdy w Git,
- kontrolowany deployment,
- osobne środowiska,
- audyt zmian,
- minimalne uprawnienia,
- bezpieczne secret management.

Jeśli brakuje tych elementów, pipeline jest nieprzewidywalny.

<!-- end_slide -->

# Co daje DABs?

```text
Databricks Asset Bundles = infrastruktura jako kod dla Databricks
```

DABs pozwala: 
- trzymać joby i konfigurację w repo,
- versionować zmiany przez Git,
- prowadzić deployment do targetów (`dev`, `staging`, `prod`),
- eliminować ręczne kliknięcia w UI.

W praktyce:
- repo jest źródłem prawdy,
- deployment jest powtarzalny,
- zmiany są łatwiejsze do review i rollbacku.

<!-- end_slide -->

# Azure DevOps w tym modelu

```text
Git + PR + Azure DevOps + bundle validate + bundle deploy
```

Azure DevOps robi kilka ważnych rzeczy:
- review change request,
- uruchamia walidację bundle,
- deployuje do staging po merge,
- wstrzymuje deploy do prod wymaganą zgodą.

Czyli: to nie jest tylko „zautomatyzowany job”, to jest kontrolowany lifecycle pipeline'u.

<!-- end_slide -->

# Staging vs prod

```text
dev -> staging -> prod
```

Dlaczego to ma sens?
- dev to eksperyment i iteracja,
- staging to test operacyjny na realnym środowisku,
- prod to finalne środowisko z approval gate.

Zasada:
```text
Nie deployuj do prod z tego samego miejsca, gdzie robi się eksperymenty lokalnie.
```

<!-- end_slide -->

# Security model

```text
Secret nie idzie do repo.
```

Typowy model bezpieczeństwa:
- Azure DevOps service connection,
- App registration / managed identity,
- Databricks service principal,
- folder deployment z ograniczonymi uprawnieniami,
- Unity Catalog grants dla katalogu / schematu / tabeli.

Minimalne prawa = bezpieczniejsza platforma.

<!-- end_slide -->

# Co robi service principal?

```text
Service principal = tożsamość wykonania pipeline'u
```

Jest odpowiedzialny za:
- deploy kodu do określonego workspace,
- uruchamianie jobów,
- dostęp do folderu deployment,
- dostęp do danych w Unity Catalog.

Bez tego pipeline może działać tylko „na papierze”, a nie w produkcji.

<!-- end_slide -->

# DLT: declarative pipeline

```text
DLT = Delta Live Tables
```

DLT zamienia pipeline z “ręcznego skryptu” w strukturę deklaratywną:

```text
bronze -> silver -> gold
```

Dzięki temu:
- łatwiej definiować zależności,
- łatwiej testować jakość danych,
- widać, które tabele zależą od siebie,
- pipeline ma sensowny model produkcyjny.

<!-- end_slide -->

# Quality checks w DLT

```python
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
@dlt.table
def silver_orders():
    return dlt.read("bronze_orders").filter("id IS NOT NULL")
```

To nie jest tylko „ładny składnik techniczny”.
To jest system ochrony jakości danych w produkcji.

<!-- end_slide -->

# Architektura końcowa

```text
Git repo
  -> PR review
  -> Azure DevOps pipeline
      -> validate bundle
      -> deploy to staging
      -> approval gate
      -> deploy to prod
          -> Databricks job runs
          -> data quality checks
          -> observability / monitoring
```

To jest wzorzec dla realnego enterprise data platform.

<!-- end_slide -->

# Mini challenge

```text
Opisz architekturę CI/CD dla Databricks:
- gdzie jest kod?
- gdzie są secret / tokeny?
- gdzie jest staging?
- gdzie jest prod?
- kto ma uprawnienia do deployment?
- gdzie są quality checks?
```

Jeśli potrafisz odpowiedzieć na te pytania, zaczynasz myśleć jak platform engineer, a nie tylko data engineer.

<!-- end_slide -->

# STAŁY PATTERN — zapamiętaj

```text
PROFESSIONAL DATBRICKS DEVOPS

=== 1. Repo ===
Git jest źródłem prawdy

=== 2. Bundle ===
DABs definiuje job i środowisko

=== 3. Pipeline ===
Azure DevOps robi validate + deploy

=== 4. Środowiska ===
dev -> staging -> prod

=== 5. Security ===
sekrety poza repo, minimalne uprawnienia

=== 6. Quality ===
DLT ma expect / quality checks
```

<!-- end_slide -->

# Closing

```text
W produkcji pipeline danych nie jest skutkiem kliknięcia w UI.
To jest kontrolowany system: repo, validation, staging, approval, prod, observability i bezpieczeństwo.
```

**Databricks + Azure DevOps + DABs + DLT = gotowy model profesjonalnego data platform deployment.**

<!-- end_slide -->
