# 03-Security Optimization Hardening Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 Vault 기반 `03-security` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. 현재 단일 노드 운영 모델을 안정화하고, 향후 raft 3-node + auto-unseal 확장 경로를 아키텍처 계약으로 명시한다.

## Summary

현재는 단일 Vault + Vault Agent 구조를 유지한다. 이번 단계에서 템플릿 경로 계약, agent 헬스체크, 검증 자동화를 고정하고, 다음 단계에서 auto-unseal/원격 audit/HA 확장을 전환 절차로 연결한다.

## Boundaries & Non-goals

- **Owns**:
  - Vault 시크릿 저장/조회 계약
  - Vault Agent 렌더/토큰 sink 계약
  - 03-security 하드닝 검증 게이트
- **Consumes**:
  - `01-gateway` 외부 TLS 종료/라우팅
  - `04-data`, `02-auth`, `06-observability` 서비스 시크릿 소비 요구
- **Does Not Own**:
  - 애플리케이션별 런타임 설정 파싱 로직
  - 외부 KMS/HSM 운영체계 자체
- **Non-goals**:
  - 이번 릴리스에서 auto-unseal 즉시 적용
  - 이번 릴리스에서 원격 audit sink 즉시 적용

## Quality Attributes

- **Performance**: Vault API/Agent 렌더 경로의 예측 가능한 응답 유지
- **Security**: placeholder 경로 제거, 최소 권한 정책, fail-closed 운영
- **Reliability**: healthcheck + 지속 볼륨 + 명시적 복구 런북
- **Scalability**: 단일 노드에서 3-node raft로 무중단에 가까운 단계적 전환 준비
- **Observability**: health 상태, audit 활성화 여부, 렌더 결과 확인 가능
- **Operability**: CI 게이트와 문서 정책/절차 일치

## System Overview & Context

현재 구조:

- External Client -> Traefik (TLS termination) -> Vault (`http://vault:8200`)
- Vault Agent -> AppRole auth -> Vault
- Vault Agent -> `/vault/out/*` 템플릿 렌더 결과 제공

목표 확장 구조:

- Vault raft 3-node cluster (quorum 2/3)
- auto-unseal (KMS/HSM) 적용
- audit device remote sink 병행(로컬 + 원격)

## Data Architecture

- **Key Entities / Flows**:
  - KV-v2 시크릿(`secret/data/hy-home/<tier>/<service>`)
  - Agent token sink(`/vault/agent/token`)
  - Template outputs(`/vault/out/<service>/<key>`)
- **Storage Strategy**:
  - Vault raft data: `/vault/data`
  - Agent state: `/vault/agent`
  - Rendered outputs: `/vault/out` (persistent volume)
- **Data Boundaries**:
  - 시크릿 원본은 Vault KV-v2에만 저장
  - 템플릿 출력은 소비 서비스 최소 범위로만 노출

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Docker Compose + `template-stateful-med`
  - `vault`, `vault-agent`
- **Deployment Model**:
  - Phase 1: 단일 노드 안정화 + 검증 자동화
  - Phase 2: auto-unseal 정책 승인 후 전환
  - Phase 3: raft 3-node + 원격 audit 확장
- **Operational Evidence**:
  - `scripts/check-security-hardening.sh`
  - `scripts/check-template-security-baseline.sh`
  - `scripts/check-doc-traceability.sh`

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: N/A
- **Tooling Boundary**: 03-security 변경 시 하드닝/문서 게이트 필수 통과
- **Memory & Context Strategy**: PRD~Runbook 링크를 기준 컨텍스트로 사용
- **Guardrail Boundary**: placeholder 경로, 평문 시크릿, 무승인 auto-unseal 구현 금지
- **Latency / Cost Budget**: N/A

## Related Documents

- **PRD**: [../01.prd/2026-03-28-03-security-optimization-hardening.md](../01.prd/2026-03-28-03-security-optimization-hardening.md)
- **Spec**: [../04.specs/03-security/spec.md](../04.specs/03-security/spec.md)
- **Plan**: [../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md](../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Operation**: [../08.operations/03-security/vault.md](../08.operations/03-security/vault.md)
- **Runbook**: [../09.runbooks/03-security/vault.md](../09.runbooks/03-security/vault.md)
