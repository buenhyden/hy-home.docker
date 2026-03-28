# ADR-0018: Vault Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `03-security` Vault 계층에 대해 즉시 하드닝 항목을 우선 적용하고, auto-unseal/원격 audit는 단계적 전환으로 관리하는 의사결정을 기록한다.

## Context

기존 Vault Agent 템플릿은 placeholder 경로를 사용하고 있었고, `vault-agent` 헬스체크/출력 지속성/전용 CI 게이트가 부재했다. 반면 auto-unseal 및 원격 audit는 운영 정책/승인/외부 의존성(KMS/HSM, 원격 저장소) 조율이 필요하여 즉시 구현 리스크가 높다.

## Decision

- 즉시 적용 항목을 우선 구현한다.
  - template placeholder 제거 및 `secret/data/hy-home/...` 경로 계약 고정
  - `vault-agent` 프로세스 기반 healthcheck 추가
  - `/vault/out` 지속 볼륨 추가
  - `scripts/check-security-hardening.sh` + CI `security-hardening` 게이트 도입
- auto-unseal/원격 audit 적재는 이번 단계에서 정책/아키텍처/런북 전환 절차로만 명시한다.
- 내부 통신 모델은 현행 유지한다.
  - 외부 TLS 종료: Traefik
  - 내부 `infra_net`: HTTP
- 기존 회귀(`scripts/check-auth-hardening.sh`)는 같은 변경 세트에서 복구한다.

## Explicit Non-goals

- 이번 변경에서 KMS/HSM auto-unseal 실구현
- 이번 변경에서 원격 audit sink 실구현
- Vault API/프로토콜 변경

## Consequences

- **Positive**:
  - 운영 계약(경로/헬스/검증)이 즉시 명확해진다.
  - CI에서 03-security 회귀를 선제 차단할 수 있다.
  - HA 확장에 필요한 전환 문맥이 문서화된다.
- **Trade-offs**:
  - auto-unseal/원격 audit 가치 실현은 다음 단계로 이연된다.
  - 단일 노드 raft 운영 리스크는 당분간 유지된다.

## Alternatives

### 즉시 auto-unseal/원격 audit까지 동시 구현

- Good:
  - 보안 성숙도를 빠르게 끌어올릴 수 있다.
- Bad:
  - 운영 승인/외부 의존성 미정 상태에서 변경 리스크가 높다.
  - 장애 시 원인 분리가 어려워진다.

### 문서만 갱신하고 인프라 변경 보류

- Good:
  - 단기 변경 리스크가 낮다.
- Bad:
  - placeholder/헬스체크/CI 회귀가 계속 남는다.

## Agent-related Example Decisions (If Applicable)

- Tool gating: `check-security-hardening.sh`를 CI merge gate로 강제
- Guardrail strategy: placeholder 경로 금지, 평문 시크릿 금지

## Related Documents

- **PRD**: [../01.prd/2026-03-28-03-security-optimization-hardening.md](../01.prd/2026-03-28-03-security-optimization-hardening.md)
- **ARD**: [../02.ard/0018-security-optimization-hardening-architecture.md](../02.ard/0018-security-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/03-security/spec.md](../04.specs/03-security/spec.md)
- **Plan**: [../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Related ADR**: [./0003-vault-as-secrets-manager.md](./0003-vault-as-secrets-manager.md)
