# ADR-0021: Observability Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `06-observability` 계층에 대해 즉시 적용 가능한 하드닝(게이트웨이 체인+SSO, health 의존성 강화, 컨테이너 런타임 하드닝, CI 기준선)을 우선 적용하고, 카탈로그 기반 HA 확장은 단계적으로 추진하는 결정을 기록한다.

## Context

관측성 계층은 다수의 관리 경로를 제공하며, 보안 체인 누락/기동 순서 불안정/런타임 하드닝 부족 시 장애가 확산되기 쉽다. 운영 회귀를 PR 단계에서 차단하기 위한 계층 전용 검증 자동화가 필요하다.

## Decision

- 즉시 하드닝을 수행한다.
  - 관측성 공개 라우터에 `gateway-standard-chain@file` + `sso-errors@file,sso-auth@file`를 적용한다.
  - Alloy/Grafana의 Loki/Tempo 의존성을 `service_healthy`로 상향한다.
  - cAdvisor healthcheck를 추가한다.
  - Loki/Tempo 커스텀 이미지에 non-root 실행/secret guard를 명시한다.
  - `check-observability-hardening.sh` 및 CI `observability-hardening` job을 도입한다.
  - PRD~Runbook 문서 세트를 생성해 양방향 추적성을 확보한다.
- 카탈로그 확장(샘플링/장기보관/모듈화)은 정책 승인 절차에 따라 단계적으로 도입한다.

## Explicit Non-goals

- 즉시 멀티리전 observability 클러스터 전환
- 애플리케이션 코드 계측 로직 일괄 개편

## Consequences

- **Positive**:
  - 관리 경로 보안 경계가 강화된다.
  - 기동 안정성과 운영 회귀 탐지력이 향상된다.
  - 문서/구성/CI의 단일 계약(SSoT)이 강화된다.
- **Trade-offs**:
  - SSO 강화로 일부 자동화 접근은 조정이 필요할 수 있다.
  - 카탈로그 확장은 단계 적용이므로 단기 가시 효과는 하드닝 중심이다.

## Alternatives

### 카탈로그 확장을 즉시 전면 구현

- Good:
  - 단기간 기능 확장 효과
- Bad:
  - 변경 반경 증가로 장애 분리/롤백 난이도 상승

### 문서만 갱신하고 runtime/CI는 유지

- Good:
  - 단기 구현 부담 감소
- Bad:
  - 실제 회귀 차단 능력이 부족

## Agent-related Example Decisions (If Applicable)

- Tool gating: `check-observability-hardening.sh`를 PR 필수 게이트로 사용
- Guardrail strategy: 공개 라우터 보안 체인 필수, non-root/secret guard 필수

## Related Documents

- **PRD**: [../01.prd/2026-03-28-06-observability-optimization-hardening.md](../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../02.ard/0021-observability-optimization-hardening-architecture.md](../02.ard/0021-observability-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/06-observability/spec.md](../04.specs/06-observability/spec.md)
- **Plan**: [../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Related ADR**: [./0006-lgtm-stack-selection.md](./0006-lgtm-stack-selection.md)
