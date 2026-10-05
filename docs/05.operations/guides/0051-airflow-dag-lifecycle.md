---
title: "Airflow Dag Basics Operations"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0051"
parent_ids:
- "POL-0052"
created: "2026-03-25"
---

# Airflow Dag Basics Operations

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 문서는 `hy-home.docker` 환경에서 Airflow DAG를 작성하는 기본 방법과 권장 패턴을 설명합니다. 현재 compose는 DAG 파일을 repo 내부 Airflow 하위 경로가 아니라 `${DEFAULT_WORKFLOW_DIR}/airflow/dags`에서 bind mount합니다.

### Airflow DAG Basics Usage

> `hy-home.docker` stack에서 Airflow DAG를 작성하는 기본 pattern이다.

---

#### Usage Type

`how-to | system-guide`

#### Target Audience

- Developer
- Data Engineer

#### Purpose

프로젝트용으로 작성한 모든 DAG가 일관된 pattern을 따르고 공유 infrastructure(PostgreSQL, SeaweedFS)를 올바르게 사용하도록 보장한다.

#### Prerequisites

- `${DEFAULT_WORKFLOW_DIR}/airflow/dags` 접근 권한.
- Python과 Apache Airflow TaskFlow API에 대한 기본 이해.

#### Step-by-step Instructions

##### 1. DAG Definition Pattern

pipeline을 현대적이고 읽기 쉽게 작성하려면 `@dag` decorator를 사용한다.

```python
from airflow.sdk import dag, task
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

`.py` file을 `${DEFAULT_WORKFLOW_DIR}/airflow/dags`에 배치한다. `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`가 설정된 bind volume으로 이 file을 pick up한다.

#### Common Pitfalls

- **Relative Imports**: DAG 내부에서 relative import를 피한다. 공유 로직에는 `plugins/` 디렉터리를 사용한다.
- **Heavy Initialization**: DAG file의 top level에서 무거운 연산이나 database query를 수행하지 않는다. `@task` 안에 유지한다.

### Common Checks

- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- Runtime이 실행 중이면 `docker compose exec airflow-apiserver airflow dags list`

### Public DAG interface

선언된 Airflow의 `airflow.sdk` TaskFlow API를 사용한다. Task code가 Airflow metadata DB를 직접 조회해서는 안 된다. 업무용 PostgreSQL 작업은 별도 Connections와 transaction/idempotency 통제를 따른다. Staging/production은 승격 단계이며 별도 stack 존재를 증명하지 않는다. 복구는 [RUN-0050](../runbooks/0050-airflow.md)을 공유하고 기존 GDE-0051/POL-0052 ID 예외를 유지한다.

### Runbook Handoff

N/A — 이 가이드에 대응하는 runbook이 없다.

### Traceability

- Declared parent: [DAG Deployment Operations Policy](../policies/0052-airflow-dag-lifecycle.md) (`POL-0052`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Policy](../policies/0052-airflow-dag-lifecycle.md) (`POL-0052`)

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Airflow system guide](0050-airflow.md)
- [DAG deployment policy](../policies/0052-airflow-dag-lifecycle.md)
- [Airflow recovery runbook](../runbooks/0050-airflow.md)
