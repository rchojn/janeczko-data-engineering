import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from de_pipeline_workflow import (
    DATA_DIR,
    Order,
    OrderPayload,
    calculate_completed_revenue,
    calculate_completed_revenue_by_source,
    run_pipeline,
    validate_and_parse_orders,
)


def test_pydantic_accepts_valid_payload() -> None:
    payload = OrderPayload.model_validate(
        {
            "order_id": "1001",
            "status": " Completed ",
            "total_amount": "120.50",
            "source": "csv",
        }
    )

    assert payload.status == "completed"
    assert payload.total_amount == 120.5


def test_pydantic_rejects_negative_amount() -> None:
    with pytest.raises(ValidationError):
        OrderPayload.model_validate(
            {
                "order_id": "1006",
                "status": "completed",
                "total_amount": "-12.00",
                "source": "csv",
            }
        )


def test_pydantic_rejects_unknown_status() -> None:
    with pytest.raises(ValidationError):
        OrderPayload.model_validate(
            {
                "order_id": "1005",
                "status": "unknown",
                "total_amount": "55.00",
                "source": "csv",
            }
        )


def test_validate_and_parse_orders_returns_dataclasses_and_rejects() -> None:
    accepted, rejected = validate_and_parse_orders(
        [
            {
                "order_id": "1001",
                "status": "completed",
                "total_amount": "120.50",
                "source": "csv",
            },
            {
                "order_id": "1005",
                "status": "unknown",
                "total_amount": "55.00",
                "source": "csv",
            },
        ]
    )

    assert accepted == [
        Order(order_id="1001", status="completed", total_amount=120.5, source="csv")
    ]
    assert len(rejected) == 1
    assert "status" in rejected[0].reason


def test_revenue_metrics_use_only_completed_orders() -> None:
    orders = [
        Order(order_id="1001", status="completed", total_amount=120.5, source="csv"),
        Order(order_id="1002", status="cancelled", total_amount=80.0, source="csv"),
        Order(order_id="2001", status="completed", total_amount=310.0, source="api"),
    ]

    assert calculate_completed_revenue(orders) == 430.5
    assert calculate_completed_revenue_by_source(orders) == {"api": 310.0, "csv": 120.5}


def test_run_pipeline_writes_accepted_and_rejected_records(tmp_path: Path) -> None:
    output_path = tmp_path / "pipeline_output.json"

    result = run_pipeline(
        DATA_DIR / "orders.csv",
        DATA_DIR / "api_orders.json",
        output_path,
    )

    output = json.loads(output_path.read_text())

    assert result.completed_revenue == 670.5
    assert output["accepted_count"] == 6
    assert output["rejected_count"] == 5
    assert output["revenue_by_source"] == {"api": 310.0, "csv": 360.5}
    assert len(output["accepted_orders"]) == 6
    assert len(output["rejected_records"]) == 5
