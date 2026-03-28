# 06-Observability Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/06-observability` 계층(Prometheus, Grafana, Loki, Tempo, Alloy, Alertmanager, Pushgateway, Pyroscope)의 최적화/하드닝 요구사항을 정의한다. 게이트웨이 경계 보안, 관리 경로 인증, 서비스 헬스 기반 의존성, 컨테이너 런타임 하드닝, 단계적 HA 확장을 목표로 한다.

## Vision

관측성 계층을 "기본적으로 안전하고(secure-by-default), 장애 전파에 강하며, 확장 가능한(HA-ready) 운영 플랫폼"으로 표준화한다.

## Problem Statement

- 일부 관측성 서비스는 게이트웨이 표준 체인/SSO 보호가 불완전해 관리 경로 노출 위험이 존재한다.
- `depends_on` 조건이 `service_started`에 머물러 초기 기동 시 race condition과 장애 전파 가능성이 있다.
- cAdvisor healthcheck가 부재해 호스트 수집기 이상 탐지가 느리다.
- Loki/Tempo 커스텀 이미지의 런타임 하드닝(비루트 강제, secret guard)이 충분히 명시되지 않았다.
- 06-observability 최적화/하드닝 문서 체계(01~09)가 부재해 실행 추적성이 약하다.

## Personas

- **SRE / Platform Operator**: 장애 신호를 빠르게 탐지하고 복구해야 한다.
- **DevOps Engineer**: 구성 하드닝/CI 게이트를 운영해야 한다.
- **Observability Consumer (Dev Team)**: 로그/메트릭/트레이스를 안정적으로 조회해야 한다.

## Key Use Cases

- **STORY-OBS-01**: 운영자는 관측성 UI/API 경로가 게이트웨이 체인+SSO 정책을 준수하는지 검증한다.
- **STORY-OBS-02**: 엔지니어는 compose 의존성을 health 기반으로 정렬해 초기 기동 실패를 줄인다.
- **STORY-OBS-03**: CI는 관측성 하드닝 회귀를 PR 단계에서 자동 차단한다.

## Functional Requirements

- **REQ-PRD-OBS-FUN-01**: 외부 노출 관측성 라우터는 `gateway-standard-chain@file`를 기본 적용해야 한다.
- **REQ-PRD-OBS-FUN-02**: 관리 UI/API 라우터는 `sso-errors@file,sso-auth@file` 체인을 강제해야 한다.
- **REQ-PRD-OBS-FUN-03**: Alloy/Grafana의 Loki/Tempo 의존성은 `service_healthy` 기준을 사용해야 한다.
- **REQ-PRD-OBS-FUN-04**: cAdvisor는 healthcheck를 제공해야 한다.
- **REQ-PRD-OBS-FUN-05**: Loki/Tempo 커스텀 이미지와 entrypoint는 비루트 실행 및 secret 존재 검증을 포함해야 한다.
- **REQ-PRD-OBS-FUN-06**: `scripts/check-observability-hardening.sh`와 CI `observability-hardening` job을 제공해야 한다.
- **REQ-PRD-OBS-FUN-07**: PRD~Runbook(01~09) 최적화/하드닝 문서를 상호 링크로 동기화해야 한다.

## Success Criteria

- **REQ-PRD-OBS-MET-01**: `bash scripts/check-observability-hardening.sh` 실패 0건.
- **REQ-PRD-OBS-MET-02**: `docker compose -f infra/06-observability/docker-compose.yml config` 검증 통과.
- **REQ-PRD-OBS-MET-03**: 관측성 공개 라우터 middleware 계약 100% 충족.
- **REQ-PRD-OBS-MET-04**: 06-observability optimization-hardening 문서 세트의 양방향 링크 정합성 확보.

## Scope and Non-goals

- **In Scope**:
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/Dockerfile`, `infra/06-observability/tempo/Dockerfile`
  - `infra/06-observability/loki/docker-entrypoint.sh`, `infra/06-observability/tempo/docker-entrypoint.sh`
  - `scripts/check-observability-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` observability optimization-hardening 문서/README
- **Out of Scope**:
  - 애플리케이션 OpenTelemetry SDK 코드 변경
  - 장기 저장소/클라우드 관리형 observability 스택 이전
- **Non-goals**:
  - 즉시 멀티리전 observability 클러스터 구축
  - 전 서비스 샘플링 정책의 동시 대개편

## Risks, Dependencies, and Assumptions

- SSO 체인 강화는 일부 자동화 접근 경로에 영향을 줄 수 있으며 예외 절차 정의가 필요하다.
- Keycloak/Traefik 미들웨어 구성의 일관성이 전제되어야 한다.
- 로컬 runtime 검증은 host Docker 환경/secret 상태에 의존한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: observability compose/script/docs/ci 변경 및 정적 검증 실행
- **Disallowed Actions**: 부동 태그 도입, 무근거 포트 노출 확대, 무검증 미들웨어 완화
- **Human-in-the-loop Requirement**: 접근제어 완화, 대규모 HA 토폴로지 변경 시 승인 필수
- **Evaluation Expectation**: `check-observability-hardening` + 공통 기준선 통과

## Related Documents

- **ARD**: [../02.ard/0021-observability-optimization-hardening-architecture.md](../02.ard/0021-observability-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/06-observability/spec.md](../04.specs/06-observability/spec.md)
- **Plan**: [../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/06-observability/optimization-hardening.md](../07.guides/06-observability/optimization-hardening.md)
- **Operation**: [../08.operations/06-observability/optimization-hardening.md](../08.operations/06-observability/optimization-hardening.md)
- **Runbook**: [../09.runbooks/06-observability/optimization-hardening.md](../09.runbooks/06-observability/optimization-hardening.md)
