# Airflow DAG Basics Guide

> Fundamental patterns for writing Airflow DAGs in the `hy-home.docker` stack.

---

## Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Airflow DAG를 작성하는 기본 방법과 권장 패턴을 설명합니다. Docker 볼륨 마운트 시 주의사항과 커넥션 관리 방법을 제공합니다.

## Guide Type

`how-to | system-guide`

## Target Audience

- Developer
- Data Engineer

## Purpose

To ensure all DAGs written for the project follow consistent patterns and utilize the shared infrastructure (PostgreSQL, MinIO) correctly.

## Prerequisites

- Access to `infra/07-workflow/airflow/dags`.
- Basic understanding of Python and Apache Airflow TaskFlow API.

## Step-by-step Instructions

### 1. DAG Definition Pattern

Use the `@dag` decorator for modern, readable pipelines.

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule=None,
    start_date=datetime(2026, 3, 1),
    catchup=False,
    tags=['example'],
)
def my_workflow():
    @task()
    def process_data():
        return "Data processed"

    process_data()

my_workflow()
```

### 2. File Placement

Place your `.py` files in `${DEFAULT_WORKFLOW_DIR}/airflow/dags`. The `airflow-scheduler` and `airflow-worker` will pick them up automatically via volume mounts.

## Common Pitfalls

- **Relative Imports**: Avoid relative imports within DAGs; use the `plugins/` directory for shared logic.
- **Heavy Initialization**: Do not perform heavy computations or database queries at the top level of the DAG file; keep it within `@task`.

## Related Documents

- **Operation**: [DAG Deployment Policy](../../08.operations/07-workflow/01.dag-deployment.md)
- **Runbook**: [Airflow Worker Recovery](../../09.runbooks/07-workflow/airflow-worker-recovery.md)
