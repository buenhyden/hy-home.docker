---
profile_id: requirements-package
status: active
artifact_id: REQ-0022
artifact_type: requirements-package
parent_ids: []
created: 2026-03-28
updated: 2026-09-01
---
# 11-Laboratory Optimization & Hardening Product Requirements

## Problem and Goals

이 문서는 `infra/11-laboratory`(dashboard, dozzle, portainer, redisinsight, open-notebook) 계층의 최적화/하드닝 요구사항을 정의한다. 목표는 관리 UI를 기본적으로 안전한 경계(TLS+SSO+IP allowlist) 뒤에 배치하고, 실험성 서비스의 운영 드리프트를 CI 단계에서 차단하며, 카탈로그 기반 확장 정책을 실행 로드맵으로 정착시키는 것이다.

## Stakeholders and User Needs

Laboratory tier를 "운영자 생산성은 높이고, 프로덕션 영향 반경은 최소화하는" 안전한 관리/실험 계층으로 표준화한다.

## Problem Statement

- dashboard 서비스가 호스트 `ports`로 노출되어 Traefik/SSO 보호 경로를 우회할 수 있다.
- `infra_net` 선언이 서비스별로 일관되지 않아 compose 정적 검증/운영 환경에서 drift가 발생한다.
- admin UI 라우터에 gateway 표준 체인(rate-limit/retry/circuit-breaker) 적용이 누락되어 보호 강도가 불균일하다.
- 실험성 관리 도구에 대한 IP allowlist 경계가 표준화되어 있지 않다.
- `11-laboratory` tier 하드닝은 현재 통합 `infrastructure-hardening` CI gate와 `scripts/hardening/check-all-hardening.sh 11-laboratory`로 관리된다.

## Personas

- **Platform SRE**: 관리 도구를 안전하게 운영하면서 사고 반경을 줄여야 한다.
- **DevOps Engineer**: 운영자 UI 접근 통제와 최소권한 구성을 일관되게 유지해야 한다.
- **Security Reviewer**: 로그/세션/접근 정책이 예외 없이 적용되는지 감사해야 한다.

## Key Use Cases

- **STORY-LAB-01**: 운영자는 Laboratory UI가 gateway+SSO+allowlist 정책을 준수하는지 점검한다.
- **STORY-LAB-02**: 팀은 dashboard/dozzle/portainer/redisinsight/open-notebook 변경 회귀를 PR 단계에서 차단한다.
- **STORY-LAB-03**: 실험성 서비스 만료/승인/접근제어 정책을 문서 기반으로 운영한다.

## Functional Requirements

- **REQ-0022-FR-0001**: 모든 Laboratory 라우터는 `gateway-standard-chain@file` + SSO 체인을 적용해야 한다.
- **REQ-0022-FR-0002**: 모든 Laboratory 라우터는 서비스별 IP allowlist middleware를 적용해야 한다.
- **REQ-0022-FR-0003**: dashboard는 direct host `ports` 노출을 제거하고 Traefik 경유 노출만 허용해야 한다.
- **REQ-0022-FR-0004**: `infra/11-laboratory` compose는 root `infra_net` context에 합류하는 static IP network block을 유지해야 한다.
- **REQ-0022-FR-0005**: dozzle은 `docker.sock`을 read-only로 마운트해야 한다.
- **REQ-0022-FR-0006**: `scripts/hardening/check-all-hardening.sh 11-laboratory` 및 CI `infrastructure-hardening` job을 제공해야 한다.
- **REQ-0022-FR-0007**: `docs/{01.requirements,02.architecture,03.specs,05.operations}` optimization-hardening 문서 세트와 README 인덱스를 동기화해야 한다.
- **REQ-0022-FR-0008**: 카탈로그 기반 확장 항목을 운영 로드맵에 반영해야 한다.
- **REQ-0022-FR-0009**: open-notebook UI route는 gateway+allowlist+large-body+SSO 경계를 적용하고, Docker Secret 기반 credential 주입을 유지해야 한다.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.
## Acceptance Criteria

- **REQ-0022-FR-0001**: `bash scripts/hardening/check-all-hardening.sh 11-laboratory` 실패 0건.
- **REQ-0022-FR-0002**: root `admin` profile compose 정적 검증과 optional service hardening checks가 통과.
- **REQ-0022-FR-0003**: Requirement Package~Runbook optimization 문서 간 양방향 링크 정합성 확보.
- **REQ-0022-FR-0004**: 카탈로그 `11-laboratory` 항목이 Plan/Tasks/Operations에 반영.

## Constraints

- **In Scope**:
  - `infra/11-laboratory/*/docker-compose.yml`
  - `.env.example` (allowlist 변수)
  - `scripts/hardening/check-all-hardening.sh 11-laboratory`
  - `.github/workflows/ci-quality.yml`
  - `docs/{01.requirements,02.architecture,03.specs,05.operations}` optimization-hardening 문서/README
- **Out of Scope**:
  - 신규 Laboratory 서비스 도입
  - 관리 도구 major version migration
- **Non-goals**:
  - Keycloak realm/policy 내부 설계 변경
  - Traefik 엔트리포인트 구조 변경

## Risks

- IP allowlist 기본값은 사설망 기준이므로 외부 운영자 접속 시 환경변수 조정이 필요하다.
- `01-gateway` middleware 및 `02-auth` SSO availability에 의존한다.
- Catalog 확장 항목은 정책/운영 절차 중심으로 단계적 적용한다.

## AI Agent Requirements

- **Allowed Actions**: Laboratory compose/script/docs/ci hardening 변경과 정적 검증 실행
- **Disallowed Actions**: 무승인 인증 우회, 직접 인터넷 노출 복원, 검증 게이트 우회
- **Human-in-the-loop Requirement**: allowlist 완화/권한 확장/감사정책 예외는 승인 필수
- **Evaluation Expectation**: lab hardening + 공통 baseline + doc traceability 통과

## Traceability

- **Architecture Description**: [../02.architecture/descriptions/0025-laboratory-optimization-hardening-architecture.md](../02.architecture/descriptions/0025-laboratory-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/012-laboratory/spec.md](../03.specs/0012-laboratory/spec.md)
- **ADR**: [../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../05.operations/catalog/11-laboratory/0074-optimization-hardening/guide.md](../05.operations/catalog/11-laboratory/0074-optimization-hardening/guide.md)
- **Policy**: [../05.operations/catalog/11-laboratory/0074-optimization-hardening/policy.md](../05.operations/catalog/11-laboratory/0074-optimization-hardening/policy.md)
- **Runbook**: [../05.operations/catalog/11-laboratory/0074-optimization-hardening/runbook.md](../05.operations/catalog/11-laboratory/0074-optimization-hardening/runbook.md)
