# 11-Laboratory Optimization Hardening Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `11-laboratory` 계층 최적화/하드닝 참조 아키텍처를 정의한다. 관리 UI를 gateway 보안 체인, SSO 인증, IP allowlist 경계 뒤에 배치하고 실험성 서비스 운영 드리프트를 CI 게이트로 통제하는 아키텍처 계약을 명시한다.

## Summary

Laboratory tier는 운영자 생산성을 위한 관리 도구 계층이지만, 권한이 큰 UI를 다루므로 "보안 경계 우선" 설계가 필요하다.

- Dashboard: homer
- Container/Log Admin UI: portainer, dozzle
- Data Admin UI: redisinsight

## Boundaries & Non-goals

- **Owns**:
  - Laboratory UI ingress 경계 계약(gateway chain + SSO + allowlist)
  - `infra_net` external 네트워크 경계 계약
  - dashboard direct host exposure 금지 계약
  - dozzle 최소권한(socket read-only) 계약
  - laboratory hardening CI 정책 게이트
- **Consumes**:
  - `01-gateway` Traefik middleware
  - `02-auth` SSO middleware
  - Docker Engine / Valkey-Redis endpoints
- **Does Not Own**:
  - Keycloak realm 상세 정책
  - Traefik global entrypoints
- **Non-goals**:
  - 실험성 서비스를 프로덕션 워크로드 계층으로 승격
  - 관리 도구 전체 재플랫폼

## Quality Attributes

- **Security**: direct host 노출 제거, allowlist+SSO 이중 경계 적용
- **Reliability**: compose 계약 및 healthcheck 기반 최소 런타임 안정성 확보
- **Operability**: CI hardening gate와 runbook 기반 회귀 복구 표준화
- **Scalability**: 카탈로그 기반 정책(만료/승인/감사)을 단계적으로 확장

## System Overview & Context

- **Ingress path**:
  - Operator -> Traefik(websecure) -> homer/dozzle/portainer/redisinsight
- **Control path**:
  - dozzle/portainer -> Docker socket
  - redisinsight -> valkey/redis endpoints

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose (`infra/11-laboratory/*`)
- **Deployment Model**:
  - Service별 compose + 공통 template(`infra/common-optimizations.yml`)
- **Operational Evidence**:
  - compose static checks
  - `scripts/check-laboratory-hardening.sh`
  - CI `laboratory-hardening` job

## Catalog-aligned Expansion Targets

- **dashboard**: SSO+allowlist 유지, 실험성 서비스 자동 만료 정책(태그 기반 정리) 적용
- **dozzle**: 로그 열람 범위 제한(운영 로그 접근 차단 규칙), 권한 최소화 지속 점검
- **portainer**: 관리자 계정/세션 정책 강화, 엔드포인트 등록 승인 절차 문서화
- **redisinsight**: 접근권한 최소화, 운영 캐시 직접 변경 금지와 감사로그 정책 강화

## Related Documents

- **PRD**: [../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **Spec**: [../04.specs/11-laboratory/spec.md](../04.specs/11-laboratory/spec.md)
- **Plan**: [../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/11-laboratory/optimization-hardening.md](../07.guides/11-laboratory/optimization-hardening.md)
- **Operation**: [../08.operations/11-laboratory/optimization-hardening.md](../08.operations/11-laboratory/optimization-hardening.md)
- **Runbook**: [../09.runbooks/11-laboratory/optimization-hardening.md](../09.runbooks/11-laboratory/optimization-hardening.md)
