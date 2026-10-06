from __future__ import annotations

from datetime import timedelta
from typing import Any, Optional

import pendulum
from airflow.decorators import dag, task
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from airflow.utils.task_group import TaskGroup

from pipeline_config import CLOUD_ENVIRONMENT, DATA_SOURCES, SIMULATE_FAILURE_FOR


class CloudJobTriggerOperator(BaseOperator):
    """Educational mock of a cloud integration operator."""

    template_fields = ("job_name", "payload")

    def __init__(self, *, job_name: str, payload: Optional[dict[str, Any]] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.job_name = job_name
        self.payload = payload or {}

    def execute(self, context: Context) -> dict[str, str]:
        run_id = context["run_id"]
        self.log.info("Would trigger cloud job: %s", self.job_name)
        self.log.info("Target environment: %s", CLOUD_ENVIRONMENT)
        self.log.info("Payload: %s", self.payload)
        self.log.info("Airflow run_id: %s", run_id)
        return {
            "job_name": self.job_name,
            "cloud_run_id": f"mock-{run_id}",
        }


default_args = {
    "owner": "data-engineering",
    "retries": 1,
    "retry_delay": timedelta(seconds=20),
}


@dag(
    dag_id="ecommerce_modern_stack_pipeline",
    description="Educational DAG for dbt/Airflow orchestration foundations.",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["data-engineering", "module-04", "airflow"],
)
def ecommerce_modern_stack_pipeline() -> None:
    @task
    def build_run_context(**context: Any) -> dict[str, str]:
        logical_date = context["logical_date"].to_date_string()
        run_id = context["run_id"]
        print(f"Preparing run context for logical_date={logical_date}, run_id={run_id}")
        return {
            "logical_date": logical_date,
            "run_id": run_id,
            "environment": CLOUD_ENVIRONMENT,
        }

    @task
    def extract_source(source_name: str) -> dict[str, str]:
        print(f"Extracting source={source_name}")

        if SIMULATE_FAILURE_FOR == source_name:
            raise ValueError(f"Simulated source failure for {source_name}")

        return {
            "source_name": source_name,
            "status": "extracted",
        }

    @task
    def validate_source(extract_result: dict[str, str]) -> dict[str, str]:
        source_name = extract_result["source_name"]
        print(f"Validating source={source_name}")
        return {
            "source_name": source_name,
            "status": "validated",
        }

    @task
    def summarize_inputs(validated_sources: list[dict[str, str]]) -> dict[str, int]:
        source_count = len(validated_sources)
        print(f"Validated sources count={source_count}")
        return {
            "validated_sources_count": source_count,
        }

    run_context = build_run_context()

    with TaskGroup(group_id="extract_and_validate") as extract_and_validate:
        extracted_sources = extract_source.expand(source_name=sorted(DATA_SOURCES))
        validated_sources = validate_source.expand(extract_result=extracted_sources)
        input_summary = summarize_inputs(validated_sources)

    with TaskGroup(group_id="transform_and_quality") as transform_and_quality:
        run_dbt_models = CloudJobTriggerOperator(
            task_id="run_dbt_models",
            job_name="dbt_run",
            payload={
                "command": "dbt run --select marts",
                "environment": CLOUD_ENVIRONMENT,
            },
        )

        run_dbt_tests = CloudJobTriggerOperator(
            task_id="run_dbt_tests",
            job_name="dbt_test",
            payload={
                "command": "dbt test --select marts",
                "environment": CLOUD_ENVIRONMENT,
            },
        )

        # Lab Task 7 asks you to add refresh_bi_dataset after run_dbt_tests.
        run_dbt_models >> run_dbt_tests

    run_context >> extract_and_validate >> transform_and_quality


ecommerce_modern_stack_pipeline()
