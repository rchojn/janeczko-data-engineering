from __future__ import annotations

from collections import defaultdict


def deduplicate_orders(orders: list[dict[str, str]]) -> list[dict[str, str]]:
    seen_ids: set[str] = set()
    unique_orders: list[dict[str, str]] = []

    for order in orders:
        order_id = order.get("order_id", "")
        if order_id in seen_ids:
            continue
        seen_ids.add(order_id)
        unique_orders.append(order)

    return unique_orders


def revenue_by_customer(orders: list[dict[str, str]]) -> dict[str, float]:
    revenue: dict[str, float] = defaultdict(float)

    for order in orders:
        status = order.get("status", "").strip().lower()
        if status != "completed":
            continue
        customer_id = order.get("customer_id", "unknown")
        amount = float(order.get("total_amount", "0") or 0)
        revenue[customer_id] += amount

    return dict(revenue)


def count_by_customer_day(orders: list[dict[str, str]]) -> dict[tuple[str, str], int]:
    counter: dict[tuple[str, str], int] = defaultdict(int)

    for order in orders:
        key = (order.get("customer_id", "unknown"), order.get("order_date", "unknown"))
        counter[key] += 1

    return dict(counter)


def main() -> None:
    orders = [
        {"order_id": "1001", "status": "completed", "total_amount": "120.5", "customer_id": "C1", "order_date": "2026-09-01"},
        {"order_id": "1002", "status": "completed", "total_amount": "80.0", "customer_id": "C1", "order_date": "2026-09-01"},
        {"order_id": "1001", "status": "completed", "total_amount": "120.5", "customer_id": "C1", "order_date": "2026-09-01"},
        {"order_id": "1003", "status": "pending", "total_amount": "45.0", "customer_id": "C2", "order_date": "2026-09-02"},
    ]

    unique = deduplicate_orders(orders)
    revenue = revenue_by_customer(unique)
    counts = count_by_customer_day(unique)

    print("Unique orders:", len(unique))
    print("Revenue by customer:", revenue)
    print("Count by customer/day:", counts)


if __name__ == "__main__":
    main()
