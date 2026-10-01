---
title: "DAG Deployment Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0052"
parent_ids:
- "AD-0007"
created: "2026-03-25"
---

# DAG Deployment Operations Policy

## Overview

이 문서는 Airflow DAG의 배포 및 승격 정책을 정의합니다. 소스 코드 관리, 정적 분석 필수 항목 및 운영 환경 반영 절차를 규정합니다.

## Policy Scope

`hy-home.docker` ecosystem 내 모든 Apache Airflow DAG의 lifecycle을 관장한다.

- **Systems**: Apache Airflow (07-workflow)
- **Environments**: Staging, Production

## Controls

- **Required**:
  - 모든 DAG는 `ruff` 또는 `flake8` linting을 통과해야 한다.
  - 특별히 필요한 경우가 아니면 `catchup=False`를 명시적으로 설정해야 한다.
- **Allowed**:
  - TaskFlow API(`@dag`, `@task`) 사용.
  - `AIRFLOW__CORE__FERNET_KEY_CMD` (`cat /run/secrets/airflow_fernet_key`)를 통한 secret mounting.
- **Disallowed**:
  - Hardcoded credential(대신 Airflow Connection을 사용한다).
  - task 밖의 top-level database connection.

## Verification

Compliance는 [Airflow Procedure](../runbooks/0050-airflow.md)에 문서화된 Airflow static/runtime check와 Airflow metadata DB의 monthly audit으로 확인한다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

## Review Cadence

- Quarterly

---

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Traceability

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](../guides/0051-airflow-dag-lifecycle.md) (`GDE-0051`)

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Airflow DAG basics guide](../guides/0051-airflow-dag-lifecycle.md)
