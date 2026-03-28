# 11-Laboratory Optimization Hardening Technical Specification

## Overview (KR)

이 문서는 `infra/11-laboratory` 계층(dashboard, dozzle, portainer, redisinsight)의 최적화/하드닝 기술 명세다. 관리 UI ingress 경계 강화, 네트워크 격리 표준화, 최소권한 강화, 정책 게이트 도입, 카탈로그 기반 확장 항목을 구현 계약으로 정의한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Laboratory 라우터 middleware 계약(gateway+allowlist+SSO)
  - compose 네트워크 경계(`infra_net` external) 계약
  - dashboard direct 노출 제거 계약
  - dozzle socket 최소권한(read-only) 계약
  - `check-laboratory-hardening.sh` 정책 게이트 계약
- **Does Not Own**:
  - Keycloak realm 상세 정책
  - Traefik 코어 엔트리포인트/전역 라우팅
  - 카탈로그 확장 항목의 즉시 자동화

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0011-laboratory-services.md](../../03.adr/0011-laboratory-services.md)
  - [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - 모든 Laboratory compose는 `infra_net` external 경계를 명시한다.
  - 모든 Laboratory 라우터는 `gateway-standard-chain@file,<service>-admin-ip@docker,sso-errors@file,sso-auth@file`를 적용한다.
  - dashboard는 direct host `ports`를 사용하지 않고 `expose`만 사용한다.
  - dozzle docker socket은 `:ro`로 마운트한다.
  - service mount 기반 healthcheck를 제공한다.
- **Governance Contract**:
  - `scripts/check-laboratory-hardening.sh` 통과가 hardening 기준선이다.
  - CI `laboratory-hardening` job이 PR 회귀를 차단한다.

## Core Design

- **Ingress Security Plane**:
  - Traefik TLS 종료 후 gateway 체인 + allowlist + SSO 체인을 강제한다.
- **Network Isolation Plane**:
  - `infra_net` external 경계를 서비스별 compose에 명시적으로 선언한다.
- **Least Privilege Plane**:
  - dozzle socket read-only
  - dashboard direct host 노출 제거
- **Policy Gate Plane**:
  - lab hardening checker + CI job으로 회귀 조기 탐지

## Interfaces & Data Structures

### Laboratory Hardening Control Surface

```yaml
laboratory_hardening_controls:
  ingress_security:
    dashboard: gateway-standard-chain + homer-admin-ip + sso-errors + sso-auth
    dozzle: gateway-standard-chain + dozzle-admin-ip + sso-errors + sso-auth
    portainer: gateway-standard-chain + portainer-admin-ip + sso-errors + sso-auth
    redisinsight: gateway-standard-chain + redisinsight-admin-ip + sso-errors + sso-auth
  network_boundary:
    compose_network: infra_net (external)
  least_privilege:
    dashboard_direct_port_exposure: forbidden
    dozzle_docker_socket: read-only
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

```bash
for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done
for f in infra/11-laboratory/dozzle/docker-compose.yml infra/11-laboratory/redisinsight/docker-compose.yml; do docker compose --profile admin -f "$f" config >/dev/null; done
bash scripts/check-laboratory-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-LAB-001**: Laboratory compose 정적 검증 통과
- **VAL-LAB-002**: Laboratory hardening 기준선 script 실패 0건
- **VAL-LAB-003**: PRD~Runbook optimization-hardening 링크 정합성 유지
- **VAL-LAB-004**: 카탈로그 `11-laboratory` 확장 항목이 Plan/Tasks/Operations에 반영

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/11-laboratory/optimization-hardening.md](../../07.guides/11-laboratory/optimization-hardening.md)
- **Operation**: [../../08.operations/11-laboratory/optimization-hardening.md](../../08.operations/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/11-laboratory/optimization-hardening.md](../../09.runbooks/11-laboratory/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
