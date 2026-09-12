import csv
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"


def normalize_status(status: str) -> str:
    return status.strip().lower()


def is_completed(order: dict[str, str]) -> bool:
    return normalize_status(order["status"]) == "completed"


def parse_amount(value: str) -> float:
    return float(value)


def classify_amount(amount: float) -> str:
    if amount < 200:
        return "small"
    if amount < 500:
        return "medium"
    return "large"


def calculate_completed_revenue(orders: list[dict[str, str]]) -> float:
    revenue = 0.0

    for order in orders:
        if is_completed(order):
            revenue = revenue + parse_amount(order["total_amount"])

    return revenue


def count_orders_by_status(orders: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}

    for order in orders:
        status = normalize_status(order["status"])

        if status not in counts:
            counts[status] = 0

        counts[status] = counts[status] + 1

    return counts


def collect_completed_order_ids(orders: list[dict[str, str]]) -> list[str]:
    order_ids: list[str] = []

    for order in orders:
        if is_completed(order):
            order_ids.append(order["order_id"])

    return order_ids


def read_orders(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def main() -> None:
    orders = read_orders(DATA_DIR / "orders.csv")

    completed_revenue = calculate_completed_revenue(orders)
    status_counts = count_orders_by_status(orders)
    completed_order_ids = collect_completed_order_ids(orders)

    print("Completed revenue:", completed_revenue)
    print("Status counts:", status_counts)
    print("Completed order ids:", completed_order_ids)

    first_order = orders[0]
    first_amount = parse_amount(first_order["total_amount"])
    print("First order amount tier:", classify_amount(first_amount))


if __name__ == "__main__":
    main()