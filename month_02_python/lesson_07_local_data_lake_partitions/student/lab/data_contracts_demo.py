from dataclasses import dataclass
from typing import Any

try:
    from pydantic import BaseModel, Field, ValidationError, field_validator
except ImportError:  # pragma: no cover
    BaseModel = object  # type: ignore[assignment]
    Field = None  # type: ignore[assignment]
    ValidationError = Exception  # type: ignore[assignment]
    field_validator = None  # type: ignore[assignment]


RAW_PAYLOADS: list[dict[str, Any]] = [
    {"order_id": "1001", "status": "Completed", "total_amount": "120.50", "source": "api"},
    {"order_id": "1002", "status": "cancelled", "total_amount": "80.00", "source": "csv"},
    {"status": "completed", "total_amount": "99.00", "source": "api"},
    {"order_id": "1004", "status": "completed", "total_amount": "-10.00", "source": "api"},
]


@dataclass(frozen=True)
class Order:
    order_id: str
    status: str
    total_amount: float
    source: str


@dataclass(frozen=True)
class ValidationResult:
    accepted: list[Order]
    rejected: list[dict[str, Any]]

    @property
    def accepted_count(self) -> int:
        return len(self.accepted)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)


if Field is not None:

    class OrderPayload(BaseModel):
        order_id: str
        status: str
        total_amount: float = Field(ge=0)
        source: str = "unknown"

        @field_validator("status")
        @classmethod
        def normalize_status(cls, value: str) -> str:
            return value.strip().lower()

else:
    OrderPayload = None  # type: ignore[assignment]


def validate_payloads(records: list[dict[str, Any]]) -> ValidationResult:
    if OrderPayload is None:
        raise RuntimeError("Install Pydantic first: poetry add pydantic")

    accepted: list[Order] = []
    rejected: list[dict[str, Any]] = []

    for record in records:
        try:
            payload = OrderPayload.model_validate(record)
            accepted.append(
                Order(
                    order_id=payload.order_id,
                    status=payload.status,
                    total_amount=payload.total_amount,
                    source=payload.source,
                )
            )
        except ValidationError as error:
            rejected.append({"record": record, "reason": error.errors()})

    return ValidationResult(accepted=accepted, rejected=rejected)


def main() -> None:
    try:
        result = validate_payloads(RAW_PAYLOADS)
    except RuntimeError as error:
        print(error)
        return

    print(f"Accepted: {result.accepted_count}")
    print(f"Rejected: {result.rejected_count}")
    print("Accepted records:")
    for order in result.accepted:
        print(order)
    print("Rejected records:")
    for rejected in result.rejected:
        print(rejected)


if __name__ == "__main__":
    main()
