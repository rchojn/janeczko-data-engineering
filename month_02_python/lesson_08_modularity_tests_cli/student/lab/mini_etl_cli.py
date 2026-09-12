# =============================================================================
# mini_etl_cli.py — Lekcja 08: Mini ETL pipeline
#
# Uruchomienie:
#   python mini_etl_cli.py --input data/orders.json --output output/result.json
#
# Kroki ETL:
#   1. extract     — read_json_records()           czyta dane z pliku
#   2. transform   — normalize_records()           czyści i ujednolica pola
#   3. transform   — calculate_completed_revenue() liczy sumę dla completed
#   4. load        — write_json()                  zapisuje wynik
#   5. orchestrate — run_pipeline()                uruchamia kroki po kolei
#   6. cli         — parse_args() + main()         punkt startowy z terminala
# =============================================================================

import argparse
import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

# TypeVar T mówi: "retry zwraca dokładnie ten typ co operation — nie cokolwiek".
# Bez tego Mypy nie wie co zwraca retry i traci informację o typie.
T = TypeVar("T")

# Logger zamiast print() — ma poziomy (INFO/WARNING/ERROR) i można go filtrować.
# getLogger(__name__) = logger z nazwą modułu, np. "mini_etl_cli".
logger = logging.getLogger(__name__)


# =============================================================================
# WZOR — retry
#
# Retry ma sens przy chwilowych błędach IO (sieć, dysk).
# NIE pomaga przy złym JSON albo brakującym polu — tam retry nic nie zmieni.
# Dlatego łapiemy tylko OSError, nie Exception.
# =============================================================================

# Callable[[], T] = typ funkcji bez argumentów która zwraca T.
# Przekazujemy funkcję (operation), nie wynik (operation()) —
# żeby retry mógł wywołać ją wielokrotnie.
def retry(operation: Callable[[], T], attempts: int = 3) -> T:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except OSError as error:
            last_error = error
            logger.warning("IO operation failed", extra={"attempt": attempt, "error": str(error)})
    # "from last_error" pokazuje w traceback oryginalny błąd, nie tylko RuntimeError.
    # Dzięki temu widać: "Permission denied: orders.json" → "Operation failed after retries".
    raise RuntimeError("Operation failed after retries") from last_error


# =============================================================================
# ZADANIE 1: EXTRACT
# =============================================================================

def read_json_records(path: Path) -> list[dict[str, Any]]:
    # operation() to closure — "zapamiętała" zmienną path z zewnątrz.
    # Przekazujemy ją do retry() żeby mógł ją wywołać kilka razy przy błędzie.
    def operation() -> list[dict[str, Any]]:
        return json.loads(path.read_text())

    records = retry(operation)
    if not records:
        raise ValueError("Input file is empty")  # pusty plik = błąd logiki, nie IO
    return records


# =============================================================================
# ZADANIE 2: TRANSFORM — normalizacja
# =============================================================================

def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # Normalizacja PRZED liczeniem — "Completed" i " COMPLETED " muszą stać się "completed"
    # zanim calculate_completed_revenue() szuka match po statusie.
    normalized: list[dict[str, Any]] = []
    for record in records:
        normalized.append(
            {
                "order_id": str(record["order_id"]),              # JSON może dać int lub str
                "status": str(record["status"]).strip().lower(),  # usuń spacje + małe litery
                "total_amount": float(record["total_amount"]),    # JSON może dać int lub float
            }
        )
    return normalized


# =============================================================================
# ZADANIE 3: TRANSFORM — agregacja
# =============================================================================

def calculate_completed_revenue(records: list[dict[str, Any]]) -> float:
    # Generator expression — krótszy zapis pętli for + if + suma.
    # sum(wartość for r in lista if warunek) = zsumuj wartość dla każdego r spełniającego warunek.
    return sum(
        float(record["total_amount"])
        for record in records
        if record["status"] == "completed"
    )


# =============================================================================
# ZADANIE 4: LOAD
# =============================================================================

def write_json(payload: dict[str, Any], path: Path) -> None:
    # parents=True  — tworzy całe drzewo katalogów jeśli nie istnieje (np. output/2024/)
    # exist_ok=True — nie rzuca błędu jeśli katalog już jest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


# =============================================================================
# ZADANIE 5: ORCHESTRATE
# =============================================================================

def run_pipeline(input_path: Path, output_path: Path) -> dict[str, Any]:
    # Orchestrator tylko wywołuje kroki po kolei i loguje co się dzieje.
    # Dzięki temu można testować run_pipeline() bez uruchamiania CLI.
    logger.info("Pipeline started", extra={"input_path": str(input_path)})
    raw_records = read_json_records(input_path)
    logger.info("Loaded records", extra={"count": len(raw_records)})

    normalized = normalize_records(raw_records)
    result = {
        "input_count": len(raw_records),
        "completed_revenue": calculate_completed_revenue(normalized),
    }

    write_json(result, output_path)
    logger.info("Pipeline finished", extra={"output_path": str(output_path)})
    return result


# =============================================================================
# ZADANIE 6: CLI
# =============================================================================

def parse_args() -> argparse.Namespace:
    # argparse zamiast hardkodowanych ścieżek — podajesz plik z terminala, nie edytujesz kod.
    parser = argparse.ArgumentParser(description="Run a mini Python ETL pipeline")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    # basicConfig() konfiguruje logi — wywołujemy raz, tylko tutaj, nie w modułach.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()
    result = run_pipeline(args.input, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))  # wynik na stdout


# Ten blok uruchamia się tylko gdy wywołujesz plik bezpośrednio (nie przy imporcie).
# Dzięki temu testy mogą importować funkcje bez startowania całego pipeline'u.
if __name__ == "__main__":
    main()

import argparse
import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

# -----------------------------------------------------------------------------
# TypeVar — po co to?
#
# Chcemy napisac retry() raz, dla dowolnego typu zwracanego.
# Bez TypeVar mielibysmy problem:
#
#   def retry(operation: Callable[[], Any]) -> Any:   # zle — Any "zjada" typ
#       ...
#
# Jesli uzyjesz Any, Mypy nie wie ze retry zwraca to samo co operation().
# Mozesz napisac: records: list[str] = retry(zwraca_int)  — i Mypy nic nie powie.
#
# TypeVar mowi: "T to JAKIS konkretny typ — wejscie i wyjscie musza byc tym samym T."
#
#   T = TypeVar("T")
#   def retry(operation: Callable[[], T]) -> T:
#
# Teraz Mypy wie: jesli operation zwraca list[dict], to retry tez zwraca list[dict].
# TypeVar to "placeholder" dla typu — wypelniany przy kazdym wywolaniu funkcji.
# -----------------------------------------------------------------------------
T = TypeVar("T")

# -----------------------------------------------------------------------------
# logger = logging.getLogger(__name__)   — dlaczego tak, nie print()?
#
# __name__ to nazwa biezacego modulu (tutaj: "mini_etl_cli").
# W projekcie src/ kazdy modul ma swoj logger z unikalnym imieniem.
# Dzieki temu mozna filtrowac logi: "pokazuj tylko bledy z pipeline.extract".
#
# logging vs print:
#   print("zaladowano rekordy")          — brak poziomu, brak struktury
#   logger.info("zaladowano", extra={})  — poziom INFO, strukturowany kontekst
#
# W schedulerach (Airflow, Kubernetes Jobs) logi sa zbierane jako strumien.
# print() idzie na stdout bez metadanych.
# logger.info() moze isc na stdout/stderr/plik/Datadog — z poziomem i timestampem.
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# =============================================================================
# WZOR — retry (czytaj uwazanie, wzorzec wraca w lesson 09 przy Boto3)
# =============================================================================

# Callable[[], T] — co to znaczy?
#
# Callable to typ dla funkcji. Zapis Callable[[arg1, arg2], wynik] mowi:
#   - w nawiasie kwadratowym: typy argumentow
#   - po przecinku: typ zwracany
#
# Callable[[], T] znaczy:
#   - [] — funkcja BEZ argumentow
#   - T  — zwraca T (ten sam T co w TypeVar powyzej)
#
# Dlaczego przekazujemy FUNKCJE a nie wynik?
# Gdybysmy pisali: retry(operation())  — Python wywola operation() PRZED retry().
# retry() dostaje juz gotowy wynik i nie ma co ponawiac.
# Piszemy:         retry(operation)    — Python przekazuje obiekt funkcji.
# retry() moze wywolac operation() wiele razy (attempts razy).
def retry(operation: Callable[[], T], attempts: int = 3) -> T:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except OSError as error:
            # Lapie tylko OSError (blad IO): brak dostepu, problem z secia, NFS.
            # NIE Exception — bo wtedy lapalibysmy tez ValueError (zly JSON),
            # KeyError (brak pola) — czyli trwale bledy, gdzie retry nic nie da.
            last_error = error
            # extra={} to strukturowany log.
            # Zamiast: logger.warning(f"blad przy probie {attempt}: {error}")
            # Piszemy: extra={"attempt": attempt, "error": str(error)}
            # Roznica: systemy jak Datadog parsuja extra jako JSON — mozna filtrowac
            # po konkretnych polach, np. "pokaz wszystkie logi gdzie attempt == 3".
            logger.warning("IO operation failed", extra={"attempt": attempt, "error": str(error)})

    # raise ... from last_error — co to daje?
    #
    # Bez "from": traceback pokazuje tylko RuntimeError i gdzie go rzucilismy.
    # Z "from":   traceback pokazuje LANCUCH — oryginalny OSError + RuntimeError.
    #
    # Przyklad bez "from":
    #   RuntimeError: Operation failed after retries
    #
    # Przyklad z "from":
    #   OSError: [Errno 13] Permission denied: 'data/orders.json'
    #   The above exception was the direct cause of the following exception:
    #   RuntimeError: Operation failed after retries
    #
    # "from" zachowuje kontekst — wiesz co sie stalo i gdzie, nie tylko ze cos padlo.
    raise RuntimeError("Operation failed after retries") from last_error


# =============================================================================
# ZADANIE 1: EXTRACT
# =============================================================================

def read_json_records(path: Path) -> list[dict[str, Any]]:
    # Co to closure i dlaczego tu?
    #
    # operation() to funkcja WEWNATRZ funkcji.
    # "Zamknela w sobie" zmienna path z zewnetrznego scope'u — stad nazwa closure.
    # Gdy wywolasz operation(), ona pamięta path bez potrzeby przekazywania go jako argument.
    #
    # Dlaczego closure a nie lambda?
    #   operation = lambda: json.loads(path.read_text())   # dziala, ale mniej czytelna
    #   def operation() -> list[...]:                      # jawny typ zwracany — Mypy jest happy
    #
    # Dlaczego w ogole tworzymy operation(), a nie piszemy:
    #   records = retry(json.loads(path.read_text()))   ?
    # Bo json.loads(path.read_text()) to WYNIK — Python oblicza go zanim przekaze do retry().
    # Potrzebujemy FUNKCJI ktora retry() moze wywolac wielokrotnie.
    def operation() -> list[dict[str, Any]]:
        return json.loads(path.read_text())

    records = retry(operation)  # retry wywola operation() do 3 razy jesli OSError
    if not records:
        # ValueError, NIE OSError — pusty plik to blad logiki, nie blad IO.
        # retry() lapal OSError — ten blad nie zostanie ponowiony (slusznie).
        raise ValueError("Input file is empty")
    return records


# =============================================================================
# ZADANIE 2: TRANSFORM — normalizacja
# =============================================================================

def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # Dlaczego normalizacja PRZED liczeniem metryki — a nie w trakcie?
    #
    # Opcja A (zle): licz revenue i normalizuj w jednej funkcji.
    #   Problem: mieszasz dwie odpowiedzialnosci. Trudniej testowac.
    #   Co testujesz? Normalizacje czy liczenie? Oba naraz — test jest kruchy.
    #
    # Opcja B (dobrze): najpierw normalize_records(), potem calculate_completed_revenue().
    #   calculate_completed_revenue() dostaje ZAWSZE znormalizowane dane.
    #   Mozna testowac kazda funkcje osobno, z prostymi inputami.
    #
    # Wzorzec: "normalize early, transform on clean data"
    normalized: list[dict[str, Any]] = []
    for record in records:
        normalized.append(
            {
                # str() — bo JSON moze dac order_id jako int (np. 1001) lub str ("1001").
                # Bez cast: porownania typu order_id == "1001" moga nie dzialac dla int.
                "order_id": str(record["order_id"]),
                # .strip() usuwa biale znaki z poczatku i konca: " completed " → "completed"
                # .lower() zamienia na male litery: "COMPLETED" → "completed"
                # Kolejnosc ma znaczenie: strip przed lower (chocia tu nie zmienia wyniku).
                "status": str(record["status"]).strip().lower(),
                # float() — bo JSON moze dac total_amount jako int (np. 120) lub float (120.5).
                # sum() w calculate_completed_revenue dziala na float — cast upewnia ze typ jest zgodny.
                "total_amount": float(record["total_amount"]),
            }
        )
    return normalized


# =============================================================================
# ZADANIE 3: TRANSFORM — agregacja
# =============================================================================

def calculate_completed_revenue(records: list[dict[str, Any]]) -> float:
    # Generator expression — co to i dlaczego zamiast petli for?
    #
    # Petla for (dluzsza wersja):
    #   total = 0.0
    #   for record in records:
    #       if record["status"] == "completed":
    #           total += float(record["total_amount"])
    #   return total
    #
    # Generator expression (krotsza wersja):
    #   sum(float(r["total_amount"]) for r in records if r["status"] == "completed")
    #
    # Roznica NIE jest tylko w dlugosci. Roznica w pamieci:
    #   list comprehension: [x for x in ...] — tworzy PELNA liste w pamieci
    #   generator:          (x for x in ...)  — oblicza element po elemencie, nie tworzy listy
    #
    # sum() akceptuje generator — nie potrzebuje pelnej listy.
    # Przy milionach rekordow generator uzywa O(1) pamieci, lista O(n).
    return sum(
        float(record["total_amount"])
        for record in records
        if record["status"] == "completed"
    )


# =============================================================================
# ZADANIE 4: LOAD
# =============================================================================

def write_json(payload: dict[str, Any], path: Path) -> None:
    # path.parent — katalog nadrzedny pliku.
    # Jesli path = Path("output/2024/result.json"), to path.parent = Path("output/2024").
    #
    # mkdir(parents=True, exist_ok=True) — dwa parametry, oba wazne:
    #
    #   parents=True:
    #     Tworzy CALE drzewo katalogow jesli nie istnieje.
    #     Bez tego: jesli "output/" nie istnieje, mkdir rzuca FileNotFoundError.
    #     Z tym:    stworzy "output/" i "output/2024/" naraz.
    #
    #   exist_ok=True:
    #     Nie rzuca bledu jesli katalog juz istnieje.
    #     Bez tego: jesli "output/" juz jest, mkdir rzuca FileExistsError.
    #     Z tym:    idempotentne — mozesz wywolac wiele razy bez problemu.
    path.parent.mkdir(parents=True, exist_ok=True)
    # indent=2     — ladne wciecia, czytelny JSON dla czlowieka
    # sort_keys=True — klucze w kolejnosci alfabetycznej — stabilny output dla diff/git
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


# =============================================================================
# ZADANIE 5: ORCHESTRATE
# =============================================================================

def run_pipeline(input_path: Path, output_path: Path) -> dict[str, Any]:
    # Orchestrator — dlaczego osobna funkcja?
    #
    # Mogłbys napisac caly pipeline w main() — zadziala.
    # Ale wtedy nie mozesz przetestowac pipeline'u bez uruchamiania CLI.
    #
    # run_pipeline() przyjmuje Path, zwraca dict.
    # Mozesz wywolac go w tescie:
    #   result = run_pipeline(Path("data/test.json"), tmp_path / "out.json")
    #   assert result["completed_revenue"] == 360.5
    #
    # Bez run_pipeline musialbys mockować sys.argv — to jest bolesne.
    #
    # Zasada: orchestrator nie zawiera logiki. Tylko kolejnosc wywolan + logi.
    logger.info("Pipeline started", extra={"input_path": str(input_path)})
    raw_records = read_json_records(input_path)
    logger.info("Loaded records", extra={"count": len(raw_records)})

    normalized = normalize_records(raw_records)
    result = {
        "input_count": len(raw_records),
        "completed_revenue": calculate_completed_revenue(normalized),
    }

    write_json(result, output_path)
    logger.info("Pipeline finished", extra={"output_path": str(output_path)})
    return result


# =============================================================================
# ZADANIE 6: CLI
# =============================================================================

def parse_args() -> argparse.Namespace:
    # argparse zamiast hardkodowanych sciezek.
    # Gdybys napisal: INPUT = Path("data/orders.json") na gorze pliku,
    # to za kazdym razem gdy chcesz inny plik — edytujesz kod.
    # CLI pozwala podac parametr z zewnatrz — bez dotykania kodu.
    parser = argparse.ArgumentParser(description="Run a mini Python ETL pipeline")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    # basicConfig TYLKO tutaj — dlaczego?
    #
    # logging.basicConfig() konfiguruje GLOWNY logger dla calego procesu.
    # Jesli wywolasz basicConfig() w module bibliotecznym (extract.py, transform.py),
    # to kazdy kto importuje twoj modul dostaje konfiguracje loggera "w prezencie".
    # To blad — uzytkownik twojej biblioteki chce sam kontrolowac logi.
    #
    # Zasada: basicConfig() wywoluje sie JEDEN RAZ, w punkcie wejscia programu.
    # Modulami bibliotecznymi sa: extract.py, transform.py, load.py — NIE main().
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()
    result = run_pipeline(args.input, args.output)
    # print() na koncu — dla uzytkownika i schedulera.
    # Logi (logger.*) ida domyslnie na stderr.
    # print() idzie na stdout.
    # Scheduler moze robic: python pipeline.py 2>logs/run.log 1>output/summary.json
    # — rozdziela logi od wyniku bez zadnych zmian w kodzie.
    print(json.dumps(result, indent=2, sort_keys=True))


# if __name__ == "__main__" — klasyczny Python guard.
#
# Python ustawia __name__ = "__main__" TYLKO gdy uruchamiasz plik bezposrednio:
#   python mini_etl_cli.py        → __name__ == "__main__" → main() sie uruchamia
#
# Gdy importujesz modul w tescie:
#   from mini_etl_cli import normalize_records   → __name__ == "mini_etl_cli"
#   blok if __name__ == "__main__" sie NIE uruchamia.
#
# Bez tego guardu: kazdy import uruchamialbby pipeline — testy by sie wywracialy.
if __name__ == "__main__":
    main()
