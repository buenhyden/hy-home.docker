---
title: "DAG Deployment Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0052"
parent_ids:
- "AD-0007"
created: "2026-03-25"
next_review_at: "2027-05-13"
---

# DAG Deployment Operations Policy

## Purpose and Scope

### Objective

이 문서는 Airflow DAG의 배포 및 승격 정책을 정의합니다. 소스 코드 관리, 정적 분석 필수 항목 및 운영 환경 반영 절차를 규정합니다.

#### Authority

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

### Applies To

`hy-home.docker` ecosystem 내 모든 Apache Airflow DAG의 lifecycle을 관장한다.

- **Systems**: Apache Airflow (07-workflow)
- **Environments**: 단일 HOME Airflow stack. Staging/production은 승격 단계이며 별도 stack이 아니다.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0052-R1 | 모든 DAG | 필수: `ruff` 또는 `flake8` linting을 통과한다 | none | none |
| POL-0052-R2 | 특별히 필요한 경우가 아닐 때 | 필수: `catchup=False`를 명시적으로 설정한다 | none | none |
| POL-0052-R3 | DAG 작성 | 허용: TaskFlow API(`@dag`, `@task`) 사용 | none | none |
| POL-0052-R4 | secret mounting | 허용: `AIRFLOW__CORE__FERNET_KEY_CMD`(`cat /run/secrets/airflow_fernet_key`)를 통한 mounting | none | none |
| POL-0052-R5 | 항상 | 금지: hardcoded credential(대신 Airflow Connection을 사용한다) | none | none |
| POL-0052-R6 | 항상 | 금지: task 밖의 top-level database connection | none | none |

- **Required**:
  - 모든 DAG는 `ruff` 또는 `flake8` linting을 통과해야 한다.
  - 특별히 필요한 경우가 아니면 `catchup=False`를 명시적으로 설정해야 한다.
- **Allowed**:
  - TaskFlow API(`@dag`, `@task`) 사용.
  - `AIRFLOW__CORE__FERNET_KEY_CMD` (`cat /run/secrets/airflow_fernet_key`)를 통한 secret mounting.
- **Disallowed**:
  - Hardcoded credential(대신 Airflow Connection을 사용한다).
  - task 밖의 top-level database connection.

### Exceptions

#### Exception Conditions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

#### Approval and Review

- Quarterly

## Enforcement

### Mechanisms

Compliance는 [Airflow Procedure](../../runbooks/08-workflows-and-automation/0050-airflow.md)에 문서화된 Airflow static/runtime check와 Airflow metadata DB의 monthly audit으로 확인한다.

### Limits

이 정책은 준수를 Airflow Procedure runbook의 static/runtime check와 Airflow metadata DB의 월간 감사로 확인한다고만 하며 어느 검사가 어느 규칙을 다루는지 지정하지 않는다.

- DAG 코드 기준(POL-0052): R1-R2, R5-R6에는 정책이 지정한 검사가 없다.
- 허용 사항(POL-0052): R3-R4에는 정책이 지정한 검사가 없다.
- 어떤 check가 어떤 규칙을 다루는지는 이 문서에서 알 수 없다.
- TaskFlow API와 Fernet key 주입 방식은 허용 사항으로만 적혀 있고 검증 수단이 없다.
- 월간 감사의 실행 기록은 이 문서에 없다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Triggers

- Subject peers: [Guide](../../guides/08-workflows-and-automation/0051-airflow-dag-lifecycle.md) (`GDE-0051`)

- [Operations index](../../README.md)
- [Airflow DAG basics guide](../../guides/08-workflows-and-automation/0051-airflow-dag-lifecycle.md)
