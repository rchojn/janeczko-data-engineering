import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError, field_validator

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
REQUIRED_FIELDS = {"order_id", "status", "total_amount"}
ALLOWED_STATUSES = {"completed", "cancelled", "pending", "refunded"}


@dataclass(frozen=True)
class Order:
    order_id: str
    status: str
    total_amount: float
    source: str

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"


@dataclass(frozen=True)
class RejectedRecord:
    record: dict[str, Any]
    reason: str


@dataclass(frozen=True)
class PipelineResult:
    accepted: list[Order]
    rejected: list[RejectedRecord]
    completed_revenue: float
    revenue_by_source: dict[str, float]

    def to_output_payload(self) -> dict[str, Any]:
        return {
            "accepted_count": len(self.accepted),
            "rejected_count": len(self.rejected),
            "completed_revenue": self.completed_revenue,
            "revenue_by_source": self.revenue_by_source,
            "accepted_orders": [asdict(order) for order in self.accepted],
            "rejected_records": [asdict(record) for record in self.rejected],
        }


class OrderPayload(BaseModel):
    order_id: str
    status: str
    total_amount: float = Field(ge=0)
    source: str = "unknown"

    @field_validator("status")
    @classmethod
    def normalize_and_validate_status(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in ALLOWED_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_STATUSES))
            raise ValueError(f"status must be one of: {allowed}")
        return normalized


def read_orders_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as file:
        return list(csv.DictReader(file))


def read_orders_api_payload(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text())


def validate_required_fields(
    records: list[dict[str, Any]], required_fields: set[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for record in records:
        has_required_fields = all(record.get(field) for field in required_fields)
        if has_required_fields:
            accepted.append(record)
        else:
            rejected.append(record)

    return accepted, rejected


def pydantic_errors_to_reason(error: ValidationError) -> str:
    messages: list[str] = []
    for item in error.errors():
        field = ".".join(str(part) for part in item["loc"])
        messages.append(f"{field}: {item['msg']}")
    return "; ".join(messages)


def validate_and_parse_orders(records: list[dict[str, Any]]) -> tuple[list[Order], list[RejectedRecord]]:
    accepted: list[Order] = []
    rejected: list[RejectedRecord] = []

    for record in records:
        try:
            payload = OrderPayload.model_validate(record)
        except ValidationError as error:
            rejected.append(
                RejectedRecord(record=record, reason=pydantic_errors_to_reason(error))
            )
            continue

        accepted.append(
            Order(
                order_id=payload.order_id,
                status=payload.status,
                total_amount=payload.total_amount,
                source=payload.source,
            )
        )

    return accepted, rejected


def calculate_completed_revenue(records: list[Order]) -> float:
    revenue = 0.0
    for record in records:
        if record.is_completed:
            revenue = revenue + record.total_amount
    return revenue


def calculate_completed_revenue_by_source(records: list[Order]) -> dict[str, float]:
    revenue_by_source: dict[str, float] = {}
    for record in records:
        if not record.is_completed:
            continue
        if record.source not in revenue_by_source:
            revenue_by_source[record.source] = 0.0
        revenue_by_source[record.source] = revenue_by_source[record.source] + record.total_amount
    return dict(sorted(revenue_by_source.items()))


def write_json_output(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def run_pipeline(csv_path: Path, api_path: Path, output_path: Path) -> PipelineResult:
    raw_records = read_orders_csv(csv_path) + read_orders_api_payload(api_path)
    accepted_records, missing_field_rejects = validate_required_fields(raw_records, REQUIRED_FIELDS)
    accepted_orders, contract_rejects = validate_and_parse_orders(accepted_records)

    rejected_records = [
        RejectedRecord(record=record, reason="missing required field")
        for record in missing_field_rejects
    ] + contract_rejects

    result = PipelineResult(
        accepted=accepted_orders,
        rejected=rejected_records,
        completed_revenue=calculate_completed_revenue(accepted_orders),
        revenue_by_source=calculate_completed_revenue_by_source(accepted_orders),
    )
    write_json_output(result.to_output_payload(), output_path)
    return result


def main() -> None:
    result = run_pipeline(
        DATA_DIR / "orders.csv",
        DATA_DIR / "api_orders.json",
        OUTPUT_DIR / "pipeline_output.json",
    )
    print(json.dumps(result.to_output_payload(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
