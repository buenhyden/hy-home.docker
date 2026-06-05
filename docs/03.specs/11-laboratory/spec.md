---
status: active
---
<!-- Target: docs/03.specs/11-laboratory/spec.md -->

# 11-Laboratory Optimization Hardening Technical Specification

## Overview

이 문서는 `infra/11-laboratory` 계층(dashboard, dozzle, portainer, redisinsight, open-notebook)의 최적화/하드닝 기술 명세다. 관리 UI ingress 경계 강화, 네트워크 격리 표준화, 최소권한 강화, 정책 게이트 도입, 카탈로그 기반 확장 항목을 구현 계약으로 정의한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Laboratory 라우터 middleware 계약(gateway+allowlist+SSO)
  - compose 네트워크 경계(`infra_net` external) 계약
  - dashboard direct 노출 제거 계약
  - dozzle socket 최소권한(read-only) 계약
  - open-notebook UI route SSO/allowlist/large-body 경계와 Docker Secret 주입 계약
  - `check-all-hardening.sh 11-laboratory` 정책 게이트 계약
- **Does Not Own**:
  - Keycloak realm 상세 정책
  - Traefik 코어 엔트리포인트/전역 라우팅
  - 카탈로그 확장 항목의 즉시 자동화

## Related Inputs

- **PRD**: [../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md](../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md](../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0011-laboratory-services.md](../../02.architecture/decisions/0011-laboratory-services.md)
  - [../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - 모든 Laboratory compose는 root `infra_net` context에 합류하는 static IP network block을 유지한다.
  - 모든 Laboratory UI 라우터는 `gateway-standard-chain@file,<service>-admin-ip@docker,sso-errors@file,sso-auth@file`를 적용한다. Open Notebook은 large upload support를 위해 `large-body@file`을 추가한다.
  - dashboard는 direct host `ports`를 사용하지 않고 `expose`만 사용한다.
  - dozzle docker socket은 `:ro`로 마운트한다.
  - service mount 또는 readiness 기반 healthcheck를 제공한다.
  - root-active Laboratory includes are Dozzle, RedisInsight, Open Notebook, and SurrealDB. Homer Dashboard and Portainer are optional/commented root includes until explicitly promoted.
- **Governance Contract**:
  - `scripts/hardening/check-all-hardening.sh 11-laboratory` 통과가 hardening 기준선이다.
  - CI `infrastructure-hardening` job이 PR 회귀를 차단한다.

## Core Design

- **Ingress Security Plane**:
  - Traefik TLS 종료 후 gateway 체인 + allowlist + SSO 체인을 강제한다.
- **Network Isolation Plane**:
  - root `infra_net` context에 합류하는 service network block을 유지한다.
- **Least Privilege Plane**:
  - dozzle socket read-only
  - dashboard direct host 노출 제거
- **Policy Gate Plane**:
  - lab hardening checker + CI job으로 회귀 조기 탐지

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Laboratory services do not define shared application data schemas in this spec.
  - Service-specific state remains in the corresponding Docker volumes or upstream systems.
- **Migration / Transition Plan**:
  - Preserve existing service state while tightening ingress, network, socket, and policy gate contracts.
  - Treat new data-bearing laboratory tools as separate specs when they introduce durable state or user data boundaries.

## Interfaces & Data Structures

### Laboratory Hardening Control Surface

```yaml
laboratory_hardening_controls:
  ingress_security:
    dashboard: gateway-standard-chain + homer-admin-ip + sso-errors + sso-auth
    dozzle: gateway-standard-chain + dozzle-admin-ip + sso-errors + sso-auth
    portainer: gateway-standard-chain + portainer-admin-ip + sso-errors + sso-auth
    redisinsight: gateway-standard-chain + redisinsight-admin-ip + sso-errors + sso-auth
    open_notebook: gateway-standard-chain + open-notebook-admin-ip + large-body + sso-errors + sso-auth
  network_boundary:
    compose_network: root infra_net context
  least_privilege:
    dashboard_direct_port_exposure: forbidden
    dozzle_docker_socket: read-only
  active_root_admin_services:
    - dozzle
    - redisinsight
    - surrealdb
    - open_notebook
  optional_root_admin_services:
    - homer
    - portainer
```

## Edge Cases & Error Handling

- allowlist 기본값으로 허용되지 않은 운영자 IP 접근 시 403이 발생할 수 있다.
- dozzle read-only 전환으로 기존 운영 습관(쓰기 동작)이 실패할 수 있다.
- dashboard direct 포트 제거 후 이전 북마크 접근 경로가 차단될 수 있다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: 관리 UI 접근 차단
  - **Fallback**: allowlist 환경변수 임시 조정 후 재배포
  - **Escalation**: Security/Platform 승인자
- **Failure Mode**: hardening gate 실패
  - **Fallback**: 계약 항목(middleware/network/port/socket) 복구
  - **Escalation**: DevOps on-call

## Verification

- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

Service-local standalone compose rendering is not readiness evidence for these
leaves because the compose files depend on the root `infra_net`, secret, and
common template context.

## Success Criteria & Verification Plan

- **VAL-LAB-001**: Laboratory compose 정적 검증 통과
- **VAL-LAB-002**: Laboratory hardening 기준선 script 실패 0건
- **VAL-LAB-003**: PRD~Runbook optimization-hardening 링크 정합성 유지
- **VAL-LAB-004**: 카탈로그 `11-laboratory` 확장 항목이 Plan/Tasks/Operations에 반영

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/11-laboratory/optimization-hardening.md](../../05.operations/guides/11-laboratory/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/11-laboratory/optimization-hardening.md](../../05.operations/policies/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/11-laboratory/optimization-hardening.md](../../05.operations/runbooks/11-laboratory/optimization-hardening.md)
- **Catalog**: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
