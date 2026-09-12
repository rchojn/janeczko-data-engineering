"""Lab: Ekosystem DE — Boto3 mock, Avro, HTTP API z paginacją.

Uruchomienie:
    python ecosystem_demo.py

Nie wymaga prawdziwego AWS — S3 jest zamockowany przez monkeypatching.
fastavro i httpx muszą być zainstalowane:
    pip install fastavro httpx
"""

import json
import logging
from io import BytesIO
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import fastavro
import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)


# =============================================================================
# CZĘŚĆ 1: Avro — zapis i odczyt
# =============================================================================

ORDER_SCHEMA: dict[str, Any] = {
    "type": "record",
    "name": "Order",
    "namespace": "com.example.orders",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "status", "type": "string"},
        {"name": "total_amount", "type": "double"},
    ],
}

SAMPLE_ORDERS = [
    {"order_id": "1001", "status": "completed", "total_amount": 120.5},
    {"order_id": "1002", "status": "pending", "total_amount": 80.0},
    {"order_id": "1003", "status": "completed", "total_amount": 240.0},
]


def write_avro(records: list[dict[str, Any]], schema: dict[str, Any]) -> bytes:
    """Serializuje rekordy do Avro bytes. W produkcji: wysyłane do Kafka."""
    buf = BytesIO()
    parsed_schema = fastavro.parse_schema(schema)
    fastavro.writer(buf, parsed_schema, records)
    return buf.getvalue()


def read_avro(data: bytes) -> list[dict[str, Any]]:
    """Deserializuje Avro bytes do listy rekordów."""
    buf = BytesIO(data)
    return list(fastavro.reader(buf))


# =============================================================================
# CZĘŚĆ 2: Boto3 — zapis na S3 (mockowany)
# =============================================================================

def upload_to_s3(
    data: bytes,
    bucket: str,
    key: str,
    s3_client: Any,  # boto3.client — Any bo nie instalujemy boto3 w labie
) -> None:
    """Wgrywa dane na S3. s3_client przekazywany z zewnątrz (testowalność)."""
    s3_client.put_object(Bucket=bucket, Key=key, Body=data)
    logger.info("Uploaded to S3", extra={"bucket": bucket, "key": key})


def demo_s3_upload(avro_bytes: bytes) -> None:
    """Pokazuje upload na S3 z zamockowanym klientem."""
    mock_s3 = MagicMock()
    upload_to_s3(avro_bytes, bucket="my-data-lake", key="orders/orders.avro", s3_client=mock_s3)

    # Weryfikacja że put_object został wywołany z poprawnymi argumentami
    mock_s3.put_object.assert_called_once()
    call_kwargs = mock_s3.put_object.call_args.kwargs
    logger.info(
        "S3 mock call verified",
        extra={"bucket": call_kwargs["Bucket"], "key": call_kwargs["Key"]},
    )


# =============================================================================
# CZĘŚĆ 3: HTTP API z paginacją (mockowany)
# =============================================================================

def fetch_all_orders(base_url: str, client: httpx.Client) -> list[dict[str, Any]]:
    """Pobiera wszystkie zamówienia przez paginowany REST API.

    Wzorzec cursor-based pagination:
    - każda odpowiedź ma "next" cursor albo null gdy ostatnia strona
    - pętla while True + break na None
    """
    all_records: list[dict[str, Any]] = []
    next_cursor: str | None = None

    while True:
        params: dict[str, str] = {}
        if next_cursor:
            params["cursor"] = next_cursor

        response = client.get(f"{base_url}/orders", params=params)
        response.raise_for_status()
        data = response.json()

        all_records.extend(data["results"])
        next_cursor = data.get("next")  # None gdy ostatnia strona → koniec pętli

        logger.info(
            "Fetched page",
            extra={"results_count": len(data["results"]), "has_next": next_cursor is not None},
        )

        if not next_cursor:
            break

    return all_records


def demo_api_pagination() -> list[dict[str, Any]]:
    """Symuluje dwie strony odpowiedzi API."""
    pages = [
        {"results": [{"order_id": "1001"}, {"order_id": "1002"}], "next": "cursor_abc"},
        {"results": [{"order_id": "1003"}], "next": None},
    ]

    with patch("httpx.Client.get") as mock_get:
        mock_get.side_effect = [
            MagicMock(status_code=200, json=MagicMock(return_value=page))
            for page in pages
        ]
        # raise_for_status musi być callable
        for call in mock_get.side_effect:
            call.raise_for_status = MagicMock()

        # Zamiast patch, symulujemy przez bezpośrednie mockowanie response
        responses = iter(pages)

        class FakeClient:
            def get(self, url: str, **kwargs: Any) -> Any:
                data = next(responses)
                resp = MagicMock()
                resp.json.return_value = data
                resp.raise_for_status = MagicMock()
                return resp

        return fetch_all_orders("https://api.example.com", FakeClient())  # type: ignore[arg-type]


# =============================================================================
# MAIN — uruchomienie demo
# =============================================================================

def main() -> None:
    logger.info("=== Demo: Avro write/read ===")
    avro_bytes = write_avro(SAMPLE_ORDERS, ORDER_SCHEMA)
    loaded = read_avro(avro_bytes)
    logger.info("Avro roundtrip OK", extra={"records": len(loaded), "bytes": len(avro_bytes)})
    assert loaded == SAMPLE_ORDERS, "Avro roundtrip failed"

    logger.info("=== Demo: S3 upload (mock) ===")
    demo_s3_upload(avro_bytes)

    logger.info("=== Demo: API pagination (mock) ===")
    orders = demo_api_pagination()
    logger.info("API pagination OK", extra={"total_records": len(orders)})
    assert len(orders) == 3, f"Expected 3 records, got {len(orders)}"

    logger.info("All demos passed.")


if __name__ == "__main__":
    main()
