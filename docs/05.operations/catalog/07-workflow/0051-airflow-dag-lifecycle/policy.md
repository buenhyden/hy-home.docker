---
title: DAG Deployment Operations Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0052
parent_ids:
  - AD-0007
created: 2026-03-25
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md -->

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

Compliance is checked via the Airflow static/runtime checks documented in [Airflow Procedure](../0050-airflow/runbook.md), and monthly audits of the Airflow metadata DB.

## Review Cadence

- Quarterly

---

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Traceability

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](guide.md) (`GDE-0051`)

## Related Documents

- [Operations index](../../../README.md)
- [Airflow DAG basics guide](../0051-airflow-dag-lifecycle/guide.md)
