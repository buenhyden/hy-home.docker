---
profile_id: architecture-description
status: active
artifact_id: AD-0018
artifact_type: architecture-description
parent_ids:
  - REQ-0015
created: 2026-03-28
updated: 2026-08-10
---
# 03-Security Optimization Hardening Architecture Description

## Context and Stakeholders

이 문서는 Vault 기반 `03-security` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. 현재 단일 노드 운영 모델을 안정화하고, 향후 raft 3-node + auto-unseal 확장 경로를 아키텍처 계약으로 명시한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

현재는 단일 Vault + Vault Agent 구조를 유지한다. 이번 단계에서 템플릿 경로 계약, agent 헬스체크, 검증 자동화를 고정하고, 다음 단계에서 auto-unseal/원격 audit/HA 확장을 전환 절차로 연결한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

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

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: Vault API/Agent 렌더 경로의 예측 가능한 응답 유지
- **Security**: placeholder 경로 제거, 최소 권한 정책, fail-closed 운영
- **Reliability**: healthcheck + 지속 볼륨 + 명시적 복구 런북
- **Scalability**: 단일 노드에서 3-node raft로 무중단에 가까운 단계적 전환 준비
- **Observability**: health 상태, audit 활성화 여부, 렌더 결과 확인 가능
- **Operability**: CI 게이트와 문서 정책/절차 일치

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

현재 구조:

- External Client -> Traefik (TLS termination) -> Vault (`http://vault:8200`)
- Vault Agent -> AppRole auth -> Vault
- Vault Agent -> `/vault/out/*` 템플릿 렌더 결과 제공

목표 확장 구조:

- Vault raft 3-node cluster (quorum 2/3)
- auto-unseal (KMS/HSM) 적용
- audit device remote sink 병행(로컬 + 원격)

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

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

## Deployment View

- **Runtime / Platform**:
  - Docker Compose + `template-stateful-med`
  - `vault`, `vault-agent`
  - root include active via `infra/03-security/vault/docker-compose.yml`
- **Deployment Model**:
  - Phase 1: 단일 노드 안정화 + 검증 자동화
  - Phase 2: auto-unseal 정책 승인 후 전환
  - Phase 3: raft 3-node + 원격 audit 확장
- **Operational Evidence**:
  - `scripts/hardening/check-all-hardening.sh 03-security`
  - `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
  - `scripts/validation/check-template-security-baseline.sh`
  - `scripts/validation/check-document-links.py --mode traceability`

## AI Agent Architecture Descriptions (If Applicable)

- **Model/Provider Strategy**: N/A
- **Tooling Boundary**: 03-security 변경 시 하드닝/문서 게이트 필수 통과
- **Memory & Context Strategy**: PRD~Runbook 링크를 기준 컨텍스트로 사용
- **Guardrail Boundary**: placeholder 경로, 평문 시크릿, 무승인 auto-unseal 구현 금지
- **Latency / Cost Budget**: N/A

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../01.requirements/0015-security-optimization-hardening.md](../../01.requirements/0015-security-optimization-hardening.md)
- **Spec**: [../03.specs/003-security/spec.md](../../03.specs/0003-security/spec.md)
- **Plan**: ../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md
- **ADR**: [../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../decisions/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Tasks**: ../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md
- **Policy**: [../../05.operations/policies/03-security/vault.md](../../05.operations/catalog/03-security/ops-0016-vault/policy.md)
- **Runbook**: [../../05.operations/runbooks/03-security/vault.md](../../05.operations/catalog/03-security/ops-0016-vault/runbook.md)
