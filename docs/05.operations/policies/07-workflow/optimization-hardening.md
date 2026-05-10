# 07-Workflow Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `07-workflow` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, health 기반 의존성, n8n 컨테이너 하드닝, 카탈로그 기반 확장 승인 기준을 통제한다.

## Policy Scope

- `infra/07-workflow/airflow/docker-compose.yml`
- `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,docker-entrypoint.sh}`
- `scripts/check-workflow-hardening.sh`

## Applies To

- **Systems**: Airflow, Flower, n8n, n8n-worker, n8n-task-runner, workflow Valkey
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Airflow/Flower/n8n 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - Airflow 핵심 서비스는 `airflow-valkey` `service_healthy` dependency를 사용한다.
  - n8n worker/task-runner healthcheck를 필수로 유지한다.
  - n8n task-runner는 `n8n`/`n8n-valkey` health 기반 의존성을 유지한다.
  - n8n compose 기본 이미지는 custom image(`hyhome/n8n:2.15.0-local`)를 사용한다.
  - n8n runtime은 non-root이며 entrypoint secret guard를 유지한다.
  - workflow 변경은 `check-workflow-hardening.sh` 및 CI `workflow-hardening`을 통과해야 한다.
  - 문서(PRD~Procedure)는 optimization-hardening 링크를 유지한다.
- **Allowed**:
  - Airflow DAG quality gate/worker autoscale 기준의 단계적 강화
  - n8n workflow Git backup/Vault credential 연계의 단계적 강화
  - airbyte infra artifact gap 해소를 위한 backlog/설계 작업
- **Disallowed**:
  - 무승인 middleware 완화
  - root runtime 복귀
  - 검증 게이트 우회 배포

## Exceptions

- 장애 대응 시 일시적 접근제어 완화는 허용될 수 있다.
- 단, 변경 승인 기록과 동일 릴리스 내 원상 복구/재검증이 필수다.

## Verification

- `docker compose -f infra/07-workflow/airflow/docker-compose.yml config`
- `docker compose -f infra/07-workflow/n8n/docker-compose.yml config`
- `bash scripts/check-workflow-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`

## Review Cadence

- 월 1회 정기 검토
- Airflow/n8n 버전 변경 또는 인증/보안 이슈 발생 시 수시 검토

## Catalog Expansion Approval Gates

- **Airflow 승인 조건**:
  - DAG parse/schedule/delay 기준 품질 게이트 문서화 및 CI 반영
  - worker autoscale 트리거(큐 지연, 실행 대기 수, CPU/memory) 기준 합의
- **n8n 승인 조건**:
  - workflow Git backup 표준 운영 절차 수립
  - credential store Vault 연계 모델 및 롤백 절차 문서화
- **airbyte 승인 조건**:
  - infra artifact(Compose/README) 정식 정의
  - connector 승격 기준(실험 -> 운영) 및 검증 체크리스트 수립

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: workflow hardening + 공통 기준선 통과 필수
- **Log / Trace Retention**: workflow 서비스 기본 보존 정책 준수
- **Safety Incident Thresholds**: 인증 실패 급증, queue 정체 장기화, scheduler/worker 반복 재시작 발생 시 runbook 전환

## Related Documents

- **PRD**: [../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md](../../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md)
- **ADR**: [../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../03.specs/07-workflow/spec.md](../../../03.specs/07-workflow/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Usage**: [../../05.operations/07-workflow/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/07-workflow/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Usage

> Migrated from `docs/05.operations/07-workflow/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 07-Workflow Optimization Hardening Usage

#### Overview (KR)

이 문서는 `07-workflow` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. compose 보안 경계, health 기반 startup 계약, n8n 이미지 하드닝, 검증 절차를 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Workflow Maintainer

#### Purpose

- Airflow/n8n 관리 경로를 gateway+SSO 정책에 정렬한다.
- startup 안정성을 높이고 장애 전파를 줄인다.
- workflow 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목의 운영 기준(Airflow/n8n/airbyte)을 문서화한다.

#### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/07-workflow` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

#### Step-by-step Instructions

1. 정적 구성 점검
   - `docker compose -f infra/07-workflow/airflow/docker-compose.yml config`
   - `docker compose -f infra/07-workflow/n8n/docker-compose.yml config`
2. Gateway/SSO 경계 정렬
   - Airflow, Flower, n8n 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. Health 기반 의존성 강화
   - Airflow 핵심 서비스가 `airflow-valkey` `service_healthy`를 사용하도록 확인한다.
   - n8n worker/task-runner healthcheck와 task-runner dependency gating을 확인한다.
4. n8n 이미지 하드닝 확인
   - compose가 custom image(`hyhome/n8n:2.15.0-local`)를 사용하도록 확인한다.
   - Dockerfile non-root runtime(`USER node`)와 entrypoint secret guard를 확인한다.
5. 기준선 검증 실행
   - `bash scripts/check-workflow-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`
6. 카탈로그 확장 운영 기준 반영
   - Airflow DAG quality gate와 worker autoscale 기준을 정책 문서에 반영한다.
   - n8n workflow Git backup/Vault credential 기준을 정책 문서에 반영한다.
   - airbyte infra artifact gap을 backlog로 추적한다.

#### Common Pitfalls

- 일부 라우터에만 SSO 체인을 적용하는 실수
- worker/task-runner healthcheck 없이 startup 불안정을 방치하는 실수
- n8n custom image를 compose에서 사용하지 않아 hardening drift가 생기는 실수
- 카탈로그 확장 항목을 문서만 기록하고 task로 분해하지 않는 실수

#### Related Documents

- **PRD**: [../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md](../../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md)
- **Spec**: [../../03.specs/07-workflow/spec.md](../../../03.specs/07-workflow/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Operation**: [../../05.operations/07-workflow/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/07-workflow/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Procedure

> Migrated from `docs/05.operations/07-workflow/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 07-Workflow Optimization Hardening Procedure

#### Overview (KR)

이 런북은 `07-workflow` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, health dependency 회귀, n8n image/entrypoint drift, CI 게이트 실패를 중심으로 점검/복구한다.

#### Purpose

- workflow 관리 경로 보안과 startup 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

#### Canonical References

- [Spec](../../../03.specs/07-workflow/spec.md)
- [Operations Policy](./optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)

#### When to Use

- `workflow-hardening` CI가 실패할 때
- Airflow/Flower/n8n 경로 접근 정책이 비정상일 때
- Airflow worker/scheduler startup이 불안정할 때
- n8n worker/task-runner 재시작 루프가 발생할 때

#### Procedure or Checklist

##### Checklist

- [ ] 실패 항목(middleware, healthcheck, depends_on, image, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(스케줄링, 자동화, 큐 지연) 평가

##### Procedure

1. 정적 구성 점검
   - `docker compose -f infra/07-workflow/airflow/docker-compose.yml config`
   - `docker compose -f infra/07-workflow/n8n/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/check-workflow-hardening.sh`
3. 증상별 복구
   - middleware 회귀:
     - Airflow/Flower/n8n 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - Airflow startup race:
     - 핵심 서비스의 `airflow-valkey` `service_healthy` dependency 복원
   - n8n worker/task-runner 이상:
     - healthcheck/depends_on 계약 복원
   - n8n image drift:
     - compose custom image 설정 복원
     - Dockerfile `USER node`, entrypoint secret guard 복원
4. 재검증
   - `bash scripts/check-workflow-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

#### Verification Steps

- [ ] workflow compose static validation 통과
- [ ] workflow hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

#### Observability and Evidence Sources

- **Signals**: CI `workflow-hardening`, container health, queue lag, scheduler heartbeat
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/Dockerfile/docs diff

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/07-workflow/airflow/docker-compose.yml`
  - `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,docker-entrypoint.sh}`
  - `scripts/check-workflow-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: workflow 자동 변경 파이프라인 일시 중지(승인 필요)
- **Eval Re-run**:
  - `check-workflow-hardening`
  - `check-template-security-baseline`
  - `check-doc-traceability`
- **Trace Capture**: CI logs + compose config + health 상태

#### Related Operational Documents

- **Usage**: [../../05.operations/07-workflow/optimization-hardening.md](./optimization-hardening.md)
- **Operation**: [../../05.operations/07-workflow/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
