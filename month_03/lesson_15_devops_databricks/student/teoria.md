# Teoria: Lekcja 15 - DevOps w Databricks (ELI5)

Ta lekcja odpowiada na pytanie: "jak zbudować profesjonalny pipeline Databricks, który można wdrażać bez ręcznego klikania w UI?"

## Minimum tej lekcji

```text
1. Rozumiem, po co są DABs.
2. Rozumiem, po co są DLT i quality checks.
3. Rozumiem, jak działa Azure DevOps + Databricks w produkcji.
4. Wiem, gdzie trzymać secrets i jak zabezpieczyć środowiska.
```

## 1. DABs (Databricks Asset Bundles)

DABs = "infrastruktura jako kod" dla Databricks.

Zamiast:
- tworzyć job w UI,
- ręcznie konfigurować parametry,
- kopiować tę samą ustawioną logikę dla środowisk,

robisz:
- plik `databricks.yml` w repo,
- bundle z job definition, variables i targets,
- deploy za pomocą CLI lub pipeline.

Korzyść:
- każda zmiana jest widoczna w PR,
- łatwo odtworzyć i zdeployować to samo do `dev`, `staging` i `prod`,
- mniej „magii” i mniej błędów wynikających z ręcznych ustawień w UI.

## 2. Co robi Azure DevOps w tej architekturze

Azure DevOps jest warstwą automatyzacji i kontroli procesu:

```text
git push
-> PR review
-> Azure DevOps pipeline
-> databricks bundle validate
-> deploy to staging
-> approval
-> deploy to prod
```

To jest ważne, bo w produkcji nie chodzi o to, żeby ktoś kliknął "Run". Chodzi o to, żeby pipeline:

- był walidowany,
- był zautomatyzowany,
- miał osobne środowiska,
- miał wymaganą zgodę na deploy do produkcji.

## 3. DLT (Delta Live Tables)

DLT = deklaratywny pipeline.

Zamiast pisać krok po kroku "read -> transform -> write" w sposób imperatywny, opisujesz tabelę i zależności:

```text
bronze -> silver -> gold
```

DLT daje:
- prostsze utrzymanie,
- automatyczne zależności między tabelami,
- quality checks (`expect`, `expect_or_drop`, `expect_or_fail`),
- lepszy observability i audyt.

## 4. Profesjonalny model bezpieczeństwa

W firmowym pipeline nie ma miejsca na hardcoded tokeny i sekrety w repo.

Dobre rozwiązanie to:

- Azure DevOps service connection,
- App registration / managed identity,
- Databricks service principal,
- folder deployment z odpowiednimi uprawnieniami,
- Unity Catalog grants dla katalogów i schematów.

Dla danych oznacza to:

```text
repo = source of truth
deployment = kontrolowana operacja
secrets = poza repo, w CI / secret store / workload identity
```

## 5. Dlaczego staging i prod są osobne

W produkcji nie zwykle deployuje się bezpośrednio do prod z każdej gałęzi.

Wzorzec jest zwykle taki:

- `dev` — iteracja i eksperymenty,
- `staging` — test operacyjny na danych i jobach,
- `prod` — finalne środowisko z approval gate.

To pozwala na:

- kontrolę jakości integracji,
- sprawdzenie działania jobów przed produkcją,
- bezpieczniejsze wdrożenia.

## 6. Jak to omówić po ludzku

Możesz to powiedzieć tak:

> Databricks w firmie nie jest miejscem, w którym job jest tworzony klikaniem w UI. To jest system, który działa przez Git, bundle deployment, pipeline validation i kontrolowane środowiska. DABs definiuje konfigurację, Azure DevOps robi automatyzację, a service principal dostarcza uprawnień do uruchomienia w odpowiednim workspace.

## STALY PATTERN - zapamietaj to

```text
PROFESSIONAL DATBRICKS DEVOPS

1) repo jest źródłem prawdy
2) bundle definiuje job i środowisko
3) Azure DevOps robi validate + deploy
4) staging jest testem operacyjnym
5) prod wymaga approval
6) DLT ma quality checks i observability
7) tokeny i secrets są poza repo
```

Zdanie na prezentację:

```text
DABs to infrastruktura jako kod dla Databricks, Azure DevOps to warstwa automatyzacji i kontroli, a DLT to deklaratywny sposób opisu pipeline'ów danych w środowisku produkcyjnym.
```

## Najprostsza wersja do nauki

```text
Nie piszemy jobów w UI, bo to nie jest produkcja.
Piszemy kod w repo, walidujemy go, deployujemy do staging, potem do prod.
DABs opisuje co ma zostać wdrożone.
DLT opisuje jak dane są transformowane.
Azure DevOps decyduje kiedy to ma się stać.
```

