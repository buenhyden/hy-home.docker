# ADR-0022: Workflow Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `07-workflow` 계층에 대해 즉시 적용 가능한 하드닝(경계 보안, health 기반 의존성, n8n 이미지 하드닝, CI 게이트)을 우선 시행하고, 카탈로그 확장 항목은 단계적으로 추진하는 결정을 기록한다.

## Context

Workflow tier는 운영 영향 범위가 넓고, 관리 경로 노출/기동 race condition/image drift가 누적되면 장애 전파 가능성이 높다. 동시에 카탈로그는 Airflow/n8n/airbyte 확장 항목을 요구하고 있어, 단기 안정화와 중기 확장을 분리한 의사결정이 필요하다.

## Decision

- 즉시 하드닝을 시행한다.
  - Airflow/n8n 관리 경로 middleware를 `gateway-standard-chain + sso-errors + sso-auth`로 정렬한다.
  - Airflow 핵심 서비스에 Valkey health 기반 의존성을 부여한다.
  - n8n worker/task-runner healthcheck와 dependency gating을 추가한다.
  - n8n custom image를 compose 기본 이미지로 승격하고 non-root + secret guard를 강제한다.
  - `scripts/check-workflow-hardening.sh`와 CI `workflow-hardening` job을 도입한다.
- 카탈로그 확장은 단계적으로 시행한다.
  - Airflow DAG quality gate/worker autoscale 기준 문서화 및 점진 도입
  - n8n workflow Git backup/Vault credential 연계 표준화
  - airbyte infra artifact gap은 별도 backlog로 추적

## Explicit Non-goals

- 즉시 multi-cluster workflow 아키텍처 전환
- Airbyte full production rollout 동시 추진
- 개별 DAG/workflow 비즈니스 로직 리팩터링

## Consequences

- **Positive**:
  - workflow 관리 경계 보안과 startup 안정성이 향상된다.
  - workflow tier 변경 회귀를 PR 단계에서 자동 차단할 수 있다.
  - 카탈로그 확장 항목이 문서/태스크 단위로 실행 가능해진다.
- **Trade-offs**:
  - SSO 강화로 기존 자동화 접근 방식 일부 조정이 필요하다.
  - custom image build가 CI/개발 환경에서 추가 빌드 시간을 유발할 수 있다.

## Alternatives

### 카탈로그 확장을 즉시 전면 구현

- Good:
  - 단기간 기능 확장 체감
- Bad:
  - 변경 반경이 커져 안정화/롤백 난이도 상승

### 문서만 갱신하고 runtime/CI 하드닝은 보류

- Good:
  - 구현 비용 단기 절감
- Bad:
  - 실제 회귀 차단 능력 부족

## Agent-related Example Decisions (If Applicable)

- Guardrail strategy: workflow 관리 경로는 gateway+SSO 체인 필수
- Tool gating: workflow 하드닝 검증 스크립트를 정책 게이트로 강제

## Related Documents

- **PRD**: [../01.prd/2026-03-28-07-workflow-optimization-hardening.md](../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD**: [../02.ard/0022-workflow-optimization-hardening-architecture.md](../02.ard/0022-workflow-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/07-workflow/spec.md](../04.specs/07-workflow/spec.md)
- **Plan**: [../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Related ADR**: [./0007-airflow-n8n-hybrid-workflow.md](./0007-airflow-n8n-hybrid-workflow.md)
