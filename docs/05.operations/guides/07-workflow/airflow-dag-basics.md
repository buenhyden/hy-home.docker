---
status: active
---
<!-- Target: docs/05.operations/guides/07-workflow/airflow-dag-basics.md -->

# Airflow Dag Basics Operations

## Usage

### Overview

이 문서는 `hy-home.docker` 환경에서 Airflow DAG를 작성하는 기본 방법과 권장 패턴을 설명합니다. 현재 compose는 DAG 파일을 repo 내부 Airflow 하위 경로가 아니라 `${DEFAULT_WORKFLOW_DIR}/airflow/dags`에서 bind mount합니다.

### Airflow DAG Basics Usage

> Fundamental patterns for writing Airflow DAGs in the `hy-home.docker` stack.

---

#### Usage Type

`how-to | system-guide`

#### Target Audience

- Developer
- Data Engineer

#### Purpose

To ensure all DAGs written for the project follow consistent patterns and utilize the shared infrastructure (PostgreSQL, MinIO) correctly.

#### Prerequisites

- Access to `${DEFAULT_WORKFLOW_DIR}/airflow/dags`.
- Basic understanding of Python and Apache Airflow TaskFlow API.

#### Step-by-step Instructions

##### 1. DAG Definition Pattern

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

##### 2. File Placement

Place your `.py` files in `${DEFAULT_WORKFLOW_DIR}/airflow/dags`. The `airflow-scheduler`, `airflow-dag-processor`, and `airflow-worker` pick them up through the configured bind volume.

#### Common Pitfalls

- **Relative Imports**: Avoid relative imports within DAGs; use the `plugins/` directory for shared logic.
- **Heavy Initialization**: Do not perform heavy computations or database queries at the top level of the DAG file; keep it within `@task`.

## Common Checks

- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- Runtime이 실행 중이면 `docker compose exec airflow-apiserver airflow dags list`

## Runbook Handoff

N/A — 이 가이드에 대응하는 runbook이 없습니다.

## Related Documents

- [Operations index](../../README.md)
- [Airflow system guide](./airflow.md)
- [DAG deployment policy](../../policies/07-workflow/dag-deployment.md)
- [Airflow recovery runbook](../../runbooks/07-workflow/airflow.md)
