# 03-Security (Vault) Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/03-security` Vault 계층의 최적화/하드닝 요구사항을 정의한다. 즉시 적용 가능한 구성 하드닝과 검증 자동화를 구현하고, auto-unseal 및 원격 audit 적재는 운영 정책/전환 절차로 설계 고정한다.

## Vision

`03-security`를 플랫폼의 신뢰 가능한 비밀 관리 계층으로 유지하면서, 운영 회귀를 CI에서 사전 차단하고 단계적 HA 확장(raft 3-node + auto-unseal) 준비 상태를 확보한다.

## Problem Statement

- Vault Agent 템플릿이 placeholder(`secret/data/example`)에 머물러 실제 운영 시크릿 경로 계약이 불명확하다.
- `vault-agent` 헬스체크와 렌더링 출력 지속성 계약이 미비해 장애 탐지/복구 신뢰성이 낮다.
- 03-security 하드닝을 강제하는 전용 CI 게이트가 없다.
- 문서 레이어(01~09)가 표준화 문맥 중심이라 optimization/hardening 실행 기준과 일부 불일치한다.

## Personas

- **Security Operator**: Vault 상태와 시크릿 경로 계약을 일관되게 운영/감사해야 한다.
- **Infra/DevOps Engineer**: 하드닝 회귀를 자동 검증하고 안정적으로 배포해야 한다.
- **Service Developer**: 서비스별 시크릿 경로/키 계약에 따라 Vault Agent 렌더 결과를 소비해야 한다.

## Key Use Cases

- **STORY-01**: 운영자는 Vault/Vault Agent 변경 후 CI의 `security-hardening` 게이트 통과로 회귀 여부를 즉시 확인한다.
- **STORY-02**: 개발자는 `secret/data/hy-home/...` 경로 계약에 맞춰 템플릿 렌더 결과를 서비스에 연결한다.
- **STORY-03**: 장애 대응자는 runbook 절차로 seal/unseal, raft 상태, agent 렌더 실패를 복구한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: Vault Agent 템플릿은 placeholder 경로를 금지하고 서비스별 정규 경로(`secret/data/hy-home/...`)를 사용해야 한다.
- **REQ-PRD-FUN-02**: `vault-agent`는 PID 기반 프로세스 헬스체크를 제공해야 한다.
- **REQ-PRD-FUN-03**: Vault Agent 렌더 출력은 지속 볼륨(`/vault/out`)에 기록되어야 한다.
- **REQ-PRD-FUN-04**: 03-security 하드닝 정적 검증 스크립트와 CI 게이트(`security-hardening`)를 제공해야 한다.
- **REQ-PRD-FUN-05**: auto-unseal/원격 audit 적재는 즉시 구현 대신 정책/아키텍처/런북에 단계적 전환 절차를 명시해야 한다.
- **REQ-PRD-FUN-06**: `scripts/check-auth-hardening.sh`를 최신 02-auth 계약으로 정합화해 기존 회귀를 복구해야 한다.

## Success Criteria

- **REQ-PRD-MET-01**: `bash scripts/check-security-hardening.sh`가 로컬/CI에서 성공한다.
- **REQ-PRD-MET-02**: `.ctmpl` 파일에서 `secret/data/example` 검출이 0건이다.
- **REQ-PRD-MET-03**: `vault-agent` 헬스 상태를 컨테이너 healthcheck로 확인할 수 있다.
- **REQ-PRD-MET-04**: `bash scripts/check-auth-hardening.sh`가 최신 계약 기준으로 성공한다.
- **REQ-PRD-MET-05**: 01~09 문서와 README 인덱스가 상호 링크로 동기화되어 있다.

## Scope and Non-goals

- **In Scope**:
  - `infra/03-security/vault/*` 구성 하드닝
  - `scripts/check-security-hardening.sh`, CI job 추가
  - `scripts/check-auth-hardening.sh` 회귀 수정
  - `docs/01~09` 03-security 문서/인덱스 동기화
- **Out of Scope**:
  - 즉시 auto-unseal 실구현(KMS/HSM 연동)
  - 즉시 원격 audit sink 실구현
  - 내부 TLS 모델(현재 Traefik 종료 + 내부 HTTP) 전면 변경
- **Non-goals**:
  - Vault API 기능 확장
  - 애플리케이션 비즈니스 로직 변경

## Risks, Dependencies, and Assumptions

- Vault는 단일 노드 raft 기준으로 운영 중이며, HA 확장은 단계적 전환 전제다.
- 템플릿 경로 변경 시 Vault 내부 시크릿 데이터가 사전 준비되어야 한다.
- runtime 검증(`docker compose up`)은 실행 환경 가용성에 따라 제한될 수 있다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: Vault compose/config/template/script/doc 수정 및 정적 검증 실행.
- **Disallowed Actions**: 평문 시크릿 하드코딩, fail-open 정책 강제, 무근거 자동 unseal 구현.
- **Human-in-the-loop Requirement**: 운영 전환(auto-unseal/원격 audit)은 운영 승인 후 진행.
- **Evaluation Expectation**: security/auth/doc/template baseline 스크립트 통과.

## Related Documents

- **ARD**: [../02.ard/0018-security-optimization-hardening-architecture.md](../02.ard/0018-security-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/03-security/spec.md](../04.specs/03-security/spec.md)
- **Plan**: [../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md](../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/03-security/vault.md](../07.guides/03-security/vault.md)
- **Operation**: [../08.operations/03-security/vault.md](../08.operations/03-security/vault.md)
- **Runbook**: [../09.runbooks/03-security/vault.md](../09.runbooks/03-security/vault.md)
