# ADR-0025: Laboratory Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `11-laboratory` 계층에서 즉시 적용 가능한 하드닝(ingress 경계 강화, direct 노출 제거, 네트워크 계약 정렬, 최소권한 개선, CI 게이트 도입)을 우선 시행하고, 카탈로그 확장 항목은 단계적으로 도입하는 결정을 기록한다.

## Context

Laboratory tier는 운영자 생산성에 큰 영향을 주지만 권한이 강한 UI를 제공한다. 따라서 보안/운영 표준이 느슨하면 core tier 전체에 우회 경로를 만들 수 있다. 단기적으로는 경계 하드닝이 필요하고, 중기적으로는 실험성 서비스 운영 거버넌스(만료/승인/감사) 강화가 필요하다.

## Decision

- 즉시 하드닝을 적용한다.
  - dashboard direct host `ports` 노출을 제거하고 Traefik 경유 노출만 허용한다.
  - 모든 Laboratory 라우터에 `gateway-standard-chain + service ipAllowList + sso-errors + sso-auth`를 적용한다.
  - `infra_net` external 경계를 service compose에 명시한다.
  - dozzle docker socket을 read-only로 제한한다.
  - `check-laboratory-hardening.sh` 및 CI `laboratory-hardening` job을 도입한다.
- 카탈로그 확장은 단계적으로 적용한다.
  - dashboard 만료 정책
  - dozzle 로그 접근 범위 제한
  - portainer 세션/승인 정책
  - redisinsight 최소권한/감사로그 정책

## Explicit Non-goals

- Laboratory 서비스군의 즉시 재플랫폼
- Keycloak/Traefik 코어 정책 전면 재설계
- 모든 카탈로그 확장 항목의 즉시 런타임 자동화

## Consequences

- **Positive**:
  - 관리 UI가 일관된 보안 경계 뒤에 배치된다.
  - direct 노출 우회 경로를 제거하고 운영 드리프트를 CI에서 차단한다.
  - 카탈로그 확장 항목이 Plan/Tasks/Operations에서 실행 가능한 형태가 된다.
- **Trade-offs**:
  - allowlist 기본값으로 원격 운영자 접근 시 환경변수 조정이 필요할 수 있다.
  - CI 게이트 추가로 PR 처리 시간이 소폭 증가한다.

## Alternatives

### 카탈로그 항목 즉시 전면 구현

- Good:
  - 정책 성숙도 빠른 상승
- Bad:
  - 변경 반경 확대로 단기 안정성 저하 가능

### 문서만 갱신하고 runtime/CI 하드닝 보류

- Good:
  - 단기 변경량 축소
- Bad:
  - 실제 회귀 차단 능력 부재

## Related Documents

- **PRD**: [../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../02.ard/0025-laboratory-optimization-hardening-architecture.md](../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/11-laboratory/spec.md](../04.specs/11-laboratory/spec.md)
- **Plan**: [../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Related ADR**: [./0011-laboratory-services.md](./0011-laboratory-services.md)
