# Workflow & Orchestration Operations

> Airflow, n8n, Airbyte 운영 정책 및 통제 기준.

## Overview

이 디렉터리는 `07-workflow` 계층의 운영 정책 문서를 모은다. 각 문서는 허용/금지 행위, 변경 승인 절차, 예외 처리, 준수 검증 기준을 정의한다.

## Audience

이 README의 주요 독자:

- SRE / Platform Operators
- Security & Compliance Owners
- Change Approvers
- AI Agents under policy constraints

## Scope

### In Scope

- 워크플로 엔진 운영 정책(Airflow, n8n, Airbyte)
- 배포 승격/변경 승인 통제
- 보안/자격 증명/로그 보존 정책

### Out of Scope

- 서비스 사용 가이드 (07.operations 담당)
- 장애 조치 절차 (07.operations 담당)

## Structure

```text
07-workflow/
├── 01.dag-deployment.md # DAG 배포/승인 정책
├── airflow.md           # Airflow 운영 정책
├── n8n.md               # n8n 운영 정책
├── airbyte.md           # Airbyte 운영 정책
├── optimization-hardening.md # 07-workflow 최적화/하드닝 운영 정책
└── README.md            # This file
```

## How to Work in This Area

1. 새 정책 문서는 `../../99.templates/operation.template.md`를 사용한다.
2. `Controls`와 `AI Agent Policy Section`은 필수로 채운다.
3. 정책 변경 시 대응 Procedure과 Plan/Task 링크를 함께 갱신한다.
4. 카탈로그 확장 항목(Airflow/n8n/airbyte)의 승인 게이트를 최신 상태로 유지한다.

## Related References

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Usages**: [07-workflow Usages](../../07.operations/07-workflow/README.md)
- **Procedures**: [07-workflow Procedures](../../07.operations/07-workflow/README.md)
- **Optimization PRD**: [2026-03-28-07-workflow-optimization-hardening.md](../../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **Optimization Tasks**: [2026-03-28-07-workflow-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)

## Usage

> Migrated from `docs/07.operations/07-workflow/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Workflow & Orchestration Usages

> Airflow, n8n, Airbyte 사용/이해 중심 문서 인덱스.

#### Overview

이 디렉터리는 `07-workflow` 계층의 사용자 가이드를 제공한다. 목적은 시스템 이해, 온보딩, 실무 사용 흐름 정리이며 정책 정의나 장애 복구 절차는 포함하지 않는다.

#### Audience

이 README의 주요 독자:

- Developers
- Data Engineers
- Operators
- AI Agents

#### Scope

##### In Scope

- Airflow 시스템 이해 및 DAG 개발 가이드
- n8n 자동화 설계/운영 가이드
- Airbyte 도입 및 동기화 운영 준비 가이드

##### Out of Scope

- 운영 정책/통제 기준 (07.operations 담당)
- 장애 대응/복구 절차 (07.operations 담당)

#### Structure

```text
07-workflow/
├── 01.airflow-dag-dev.md    # Airflow DAG 개발 가이드
├── 02.n8n-automation.md     # n8n 자동화 가이드
├── airflow-dag-basics.md    # Airflow DAG 기초
├── airflow.md               # Airflow 시스템 가이드
├── n8n.md                   # n8n 시스템 가이드
├── airbyte.md               # Airbyte 운영 준비 가이드
├── optimization-hardening.md # 07-workflow 최적화/하드닝 가이드
└── README.md                # This file
```

#### How to Work in This Area

1. 새 가이드는 `../../99.templates/operation.template.md`를 사용한다.
2. 문서에는 `Overview (KR)`, `Prerequisites`, `Step-by-step Instructions`, `Common Pitfalls`를 포함한다.
3. 각 가이드에서 대응되는 Operation/Procedure 링크를 함께 유지한다.
4. 최적화/하드닝 변경은 `optimization-hardening.md`와 상위 Plan/Task 문서를 함께 갱신한다.

#### Related References

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Operations**: [07-workflow Operations](../../07.operations/07-workflow/README.md)
- **Procedures**: [07-workflow Procedures](../../07.operations/07-workflow/README.md)
- **Optimization PRD**: [2026-03-28-07-workflow-optimization-hardening.md](../../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **Optimization Plan**: [2026-03-28-07-workflow-optimization-hardening-plan.md](../../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md)

## Procedure

> Migrated from `docs/07.operations/07-workflow/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Workflow & Orchestration Procedures

> Airflow, n8n, Airbyte 장애 대응 및 복구 실행 절차.

#### Overview

이 디렉터리는 `07-workflow` 계층의 실행형 런북 모음이다. 운영자는 장애 발생 시 본문 절차를 순서대로 실행하고, 검증/증적/롤백 단계를 반드시 수행해야 한다.

#### Audience

이 README의 주요 독자:

- On-call SRE
- Platform Operators
- Incident Commander
- AI Agents with human approval

#### Scope

##### In Scope

- Airflow 서비스 복구
- Airflow Worker 장애 심화 대응
- n8n 서비스 복구
- Airbyte 동기화/워커 장애 복구

##### Out of Scope

- 정책 정의 및 승인 규칙 (07.operations 담당)
- 사용 가이드/온보딩 (07.operations 담당)

#### Structure

```text
07-workflow/
├── airflow.md                 # Airflow 서비스 복구 런북
├── airflow-worker-recovery.md # Airflow Worker 장애 심화 대응
├── n8n.md                     # n8n 서비스 복구 런북
├── airbyte.md                 # Airbyte 동기화/워커 복구 런북
├── optimization-hardening.md  # 07-workflow 최적화/하드닝 복구 런북
└── README.md                  # This file
```

#### How to Work in This Area

1. 새 런북은 `../../99.templates/operation.template.md`를 사용한다.
2. `When to Use`, `Procedure`, `Verification`, `Safe Rollback`을 항상 채운다.
3. 복구 종료 후 Incident/Postmortem 링크를 남긴다.
4. 최적화/하드닝 회귀 복구 시 `check-workflow-hardening.sh` 결과를 증적으로 남긴다.

#### Related References

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Usages**: [07-workflow Usages](../../07.operations/07-workflow/README.md)
- **Operations**: [07-workflow Operations](../../07.operations/07-workflow/README.md)
- **Incidents**: [Incidents README](../../10.incidents/README.md)
- **Optimization Plan**: [2026-03-28-07-workflow-optimization-hardening-plan.md](../../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Optimization Tasks**: [2026-03-28-07-workflow-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
