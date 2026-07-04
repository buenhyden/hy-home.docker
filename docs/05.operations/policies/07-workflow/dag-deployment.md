---
status: active
---
<!-- Target: docs/05.operations/policies/07-workflow/dag-deployment.md -->

# DAG Deployment Operations Policy

## Overview

이 문서는 Airflow DAG의 배포 및 승격 정책을 정의합니다. 소스 코드 관리, 정적 분석 필수 항목 및 운영 환경 반영 절차를 규정합니다.

## Policy Scope

Governs the lifecycle of all Apache Airflow DAGs within the `hy-home.docker` ecosystem.

- **Systems**: Apache Airflow (07-workflow)
- **Environments**: Staging, Production

## Controls

- **Required**:
  - All DAGs must pass `ruff` or `flake8` linting.
  - `catchup=False` must be explicitly set unless specifically required.
- **Allowed**:
  - Use of the TaskFlow API (`@dag`, `@task`).
  - Mounting secrets via `AIRFLOW__CORE__FERNET_KEY`.
- **Disallowed**:
  - Hardcoded credentials (use Airflow Connections).
  - Top-level database connections outside of tasks.

## Verification

Compliance is checked via the Airflow static/runtime checks documented in [Airflow Procedure](../../runbooks/07-workflow/airflow.md), including `docker compose exec airflow-apiserver airflow dags list`, and monthly audits of the Airflow metadata DB.

## Review Cadence

- Quarterly

---

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Related Documents

- [Operations index](../../README.md)
- [Airflow DAG basics guide](../../guides/07-workflow/airflow-dag-basics.md)
- [Airflow recovery runbook](../../runbooks/07-workflow/airflow.md)
