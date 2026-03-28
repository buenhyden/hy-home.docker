# ADR-0024: Tooling Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `09-tooling` 계층에 대해 즉시 적용 가능한 하드닝(공개 경로 SSO 체인 정렬, 네트워크 경계 명시, locust/k6 runtime 계약 보강, CI 게이트 도입)을 우선 시행하고, 카탈로그 확장 항목은 단계적으로 추진하는 결정을 기록한다.

## Context

Tooling tier는 플랫폼 운영 제어면(control plane)에 해당하며, 보안/품질/테스트 도구의 경계가 약하면 조직 전체 배포 안정성에 직접 영향을 준다. 동시에 카탈로그는 도구별 확장/정책 강화를 요구하고 있어, 단기 안정화와 중기 확장 분리가 필요하다.

## Decision

- 즉시 하드닝을 시행한다.
  - SonarQube/Terrakube/Syncthing 라우터를 `gateway-standard-chain + sso-errors + sso-auth`로 정렬한다.
  - tooling compose에 `infra_net` external 경계 선언을 명시한다.
  - locust-worker healthcheck를 추가하고, k6 volume 참조 drift를 정렬한다.
  - `scripts/check-tooling-hardening.sh`와 CI `tooling-hardening` job을 도입한다.
- 카탈로그 확장은 단계적으로 시행한다.
  - terraform 승인/백업/drift 자동 탐지
  - terrakube 권한/감사로그 강화
  - registry 서명/스캔 차단 정책
  - sonarqube 품질게이트 재정의
  - k6/locust 테스트 표준화
  - syncthing ACL/암호화/충돌 정책 강화

## Explicit Non-goals

- 즉시 전체 tooling stack 재플랫폼
- 즉시 카탈로그 확장 항목의 런타임 전면 구현
- 신규 도구 체인 도입

## Consequences

- **Positive**:
  - tooling 공개 경로 접근 통제가 일관화된다.
  - 운영 네트워크 경계와 테스트 runtime 안정성이 향상된다.
  - tooling tier 회귀를 PR 단계에서 자동 차단할 수 있다.
  - 카탈로그 확장 항목이 문서/태스크 단위로 실행 가능해진다.
- **Trade-offs**:
  - SSO 강화로 일부 기존 테스트 접근 경로 조정이 필요하다.
  - 정책 게이트 추가로 단기 PR 처리 시간이 증가할 수 있다.

## Alternatives

### 카탈로그 확장을 즉시 전면 구현

- Good:
  - 확장 항목의 빠른 기능 체감
- Bad:
  - 변경 반경 증가로 안정화/검증 복잡도 상승

### 문서만 갱신하고 runtime/CI 하드닝 보류

- Good:
  - 단기 구현 비용 절감
- Bad:
  - 회귀 차단 능력 부족

## Agent-related Example Decisions (If Applicable)

- Guardrail strategy: tooling 공개 라우터는 gateway+SSO 체인 필수
- Tool gating: `check-tooling-hardening.sh`를 머지 전 필수 정책 게이트로 강제

## Related Documents

- **PRD**: [../01.prd/2026-03-28-09-tooling-optimization-hardening.md](../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- **ARD**: [../02.ard/0024-tooling-optimization-hardening-architecture.md](../02.ard/0024-tooling-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/09-tooling/spec.md](../04.specs/09-tooling/spec.md)
- **Plan**: [../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Related ADR**: [./0009-tooling-services.md](./0009-tooling-services.md)
