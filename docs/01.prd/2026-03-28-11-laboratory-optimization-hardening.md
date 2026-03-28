# 11-Laboratory Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/11-laboratory`(dashboard, dozzle, portainer, redisinsight) 계층의 최적화/하드닝 요구사항을 정의한다. 목표는 관리 UI를 기본적으로 안전한 경계(TLS+SSO+IP allowlist) 뒤에 배치하고, 실험성 서비스의 운영 드리프트를 CI 단계에서 차단하며, 카탈로그 기반 확장 정책을 실행 로드맵으로 정착시키는 것이다.

## Vision

Laboratory tier를 "운영자 생산성은 높이고, 프로덕션 영향 반경은 최소화하는" 안전한 관리/실험 계층으로 표준화한다.

## Problem Statement

- dashboard 서비스가 호스트 `ports`로 노출되어 Traefik/SSO 보호 경로를 우회할 수 있다.
- `infra_net` 선언이 서비스별로 일관되지 않아 compose 정적 검증/운영 환경에서 drift가 발생한다.
- admin UI 라우터에 gateway 표준 체인(rate-limit/retry/circuit-breaker) 적용이 누락되어 보호 강도가 불균일하다.
- 실험성 관리 도구에 대한 IP allowlist 경계가 표준화되어 있지 않다.
- `11-laboratory` tier에 대한 전용 hardening CI gate와 최적화 문서 체계가 부재하다.

## Personas

- **Platform SRE**: 관리 도구를 안전하게 운영하면서 사고 반경을 줄여야 한다.
- **DevOps Engineer**: 운영자 UI 접근 통제와 최소권한 구성을 일관되게 유지해야 한다.
- **Security Reviewer**: 로그/세션/접근 정책이 예외 없이 적용되는지 감사해야 한다.

## Key Use Cases

- **STORY-LAB-01**: 운영자는 Laboratory UI가 gateway+SSO+allowlist 정책을 준수하는지 점검한다.
- **STORY-LAB-02**: 팀은 dashboard/dozzle/portainer/redisinsight 변경 회귀를 PR 단계에서 차단한다.
- **STORY-LAB-03**: 실험성 서비스 만료/승인/접근제어 정책을 문서 기반으로 운영한다.

## Functional Requirements

- **REQ-PRD-LAB-FUN-01**: 모든 Laboratory 라우터는 `gateway-standard-chain@file` + SSO 체인을 적용해야 한다.
- **REQ-PRD-LAB-FUN-02**: 모든 Laboratory 라우터는 서비스별 IP allowlist middleware를 적용해야 한다.
- **REQ-PRD-LAB-FUN-03**: dashboard는 direct host `ports` 노출을 제거하고 Traefik 경유 노출만 허용해야 한다.
- **REQ-PRD-LAB-FUN-04**: `infra/11-laboratory` compose는 `infra_net` external 경계를 명시해야 한다.
- **REQ-PRD-LAB-FUN-05**: dozzle은 `docker.sock`을 read-only로 마운트해야 한다.
- **REQ-PRD-LAB-FUN-06**: `scripts/check-laboratory-hardening.sh` 및 CI `laboratory-hardening` job을 제공해야 한다.
- **REQ-PRD-LAB-FUN-07**: `docs/01~09` optimization-hardening 문서 세트와 README 인덱스를 동기화해야 한다.
- **REQ-PRD-LAB-FUN-08**: 카탈로그 기반 확장 항목을 운영 로드맵에 반영해야 한다.

## Success Criteria

- **REQ-PRD-LAB-MET-01**: `bash scripts/check-laboratory-hardening.sh` 실패 0건.
- **REQ-PRD-LAB-MET-02**: `infra/11-laboratory` compose 정적 검증 통과.
- **REQ-PRD-LAB-MET-03**: PRD~Runbook optimization 문서 간 양방향 링크 정합성 확보.
- **REQ-PRD-LAB-MET-04**: 카탈로그 `11-laboratory` 항목이 Plan/Tasks/Operations에 반영.

## Scope and Non-goals

- **In Scope**:
  - `infra/11-laboratory/*/docker-compose.yml`
  - `.env.example` (allowlist 변수)
  - `scripts/check-laboratory-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` optimization-hardening 문서/README
- **Out of Scope**:
  - 신규 Laboratory 서비스 도입
  - 관리 도구 major version migration
- **Non-goals**:
  - Keycloak realm/policy 내부 설계 변경
  - Traefik 엔트리포인트 구조 변경

## Risks, Dependencies, and Assumptions

- IP allowlist 기본값은 사설망 기준이므로 외부 운영자 접속 시 환경변수 조정이 필요하다.
- `01-gateway` middleware 및 `02-auth` SSO availability에 의존한다.
- Catalog 확장 항목은 정책/운영 절차 중심으로 단계적 적용한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: Laboratory compose/script/docs/ci hardening 변경과 정적 검증 실행
- **Disallowed Actions**: 무승인 인증 우회, 직접 인터넷 노출 복원, 검증 게이트 우회
- **Human-in-the-loop Requirement**: allowlist 완화/권한 확장/감사정책 예외는 승인 필수
- **Evaluation Expectation**: lab hardening + 공통 baseline + doc traceability 통과

## Related Documents

- **ARD**: [../02.ard/0025-laboratory-optimization-hardening-architecture.md](../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/11-laboratory/spec.md](../04.specs/11-laboratory/spec.md)
- **Plan**: [../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/11-laboratory/optimization-hardening.md](../07.guides/11-laboratory/optimization-hardening.md)
- **Operation**: [../08.operations/11-laboratory/optimization-hardening.md](../08.operations/11-laboratory/optimization-hardening.md)
- **Runbook**: [../09.runbooks/11-laboratory/optimization-hardening.md](../09.runbooks/11-laboratory/optimization-hardening.md)
