"""One manual DEV manifest task; registration never opens workload resources."""

from datetime import UTC, datetime, timedelta

from airflow.sdk import Param, dag, get_current_context, task


@dag(
    dag_id="source_manifest_ingest",
    start_date=datetime(2026, 10, 10, tzinfo=UTC),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    max_active_tasks=1,
    dagrun_timeout=timedelta(minutes=15),
    is_paused_upon_creation=True,
    default_args={
        "owner": "platform",
        "retries": 2,
        "retry_delay": timedelta(seconds=30),
        "retry_exponential_backoff": True,
        "max_retry_delay": timedelta(minutes=5),
    },
    params={
        "source": Param(
            "hy-home.docker",
            type="string",
            enum=["hy-home.docker", "hy-home.k8s", "Project-Template", "blog-data"],
        ),
        "business_date": Param("2026-10-10", type="string", format="date"),
    },
    tags=["dev", "manifest"],
)
def source_manifest_ingest():
    @task(
        execution_timeout=timedelta(minutes=3),
        pool="manifest_ingest",
        pool_slots=1,
        show_return_value_in_logs=False,
        multiple_outputs=False,
    )
    def validate_store_publish():
        from workflow_lib.adapters import PgPublisher, S3Store, read_private_json
        from workflow_lib.manifest import ingest

        try:
            params = get_current_context()["params"]
            with S3Store(
                read_private_json("/run/opsflow/s3.json", schema="s3")
            ) as store:
                publisher = PgPublisher(
                    read_private_json("/run/opsflow/pg.json", schema="pg")
                )
                return ingest(
                    store, publisher, params["source"], params["business_date"]
                )
        except Exception:
            # Airflow records the exception; preserve only a bounded failure code.
            raise RuntimeError("manifest_task_failed") from None

    validate_store_publish()


manifest_dag = source_manifest_ingest()
