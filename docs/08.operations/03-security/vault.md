# 03-Security Vault Operations Policy

## Overview (KR)

이 문서는 `03-security` Vault 운영 정책을 정의한다. 즉시 적용 하드닝 기준(템플릿 계약, healthcheck, 검증 자동화)과 단계적 확장 정책(auto-unseal, 원격 audit)을 명시한다.

## Policy Scope

- `infra/03-security/vault/docker-compose.yml`
- `infra/03-security/vault/config/vault-agent.hcl`
- `infra/03-security/vault/config/templates/*.ctmpl`
- `scripts/check-security-hardening.sh`

## Applies To

- **Systems**: Vault server, Vault Agent
- **Agents**: Infra/Security/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Vault Agent 템플릿은 `secret/data/hy-home/...` 경로 규약을 사용해야 한다.
  - `vault-agent`는 PID 기반 healthcheck를 유지해야 한다.
  - 렌더 출력은 `/vault/out` persistent volume에 저장해야 한다.
  - `scripts/check-security-hardening.sh`를 CI `security-hardening` 게이트로 강제한다.
  - 운영 모드는 fail-closed를 기본으로 유지한다.
- **Allowed**:
  - 외부 TLS는 Traefik 종료, 내부 `infra_net` HTTP 통신 모델 유지.
  - auto-unseal/원격 audit는 승인 절차 후 단계적 도입.
- **Disallowed**:
  - placeholder 시크릿 경로(`secret/data/example`) 사용
  - 평문 시크릿 하드코딩
  - 승인 없는 auto-unseal/원격 audit 실적용

## Exceptions

- 단기 테스트 환경에서 임시 로컬 audit만 사용 가능.
- 단, 운영 환경 승격 전 원격 audit 전환 계획/검증 기준을 문서화해야 한다.

## Verification

- `bash scripts/check-security-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `docker compose -f infra/03-security/vault/docker-compose.yml config`
- `docker inspect --format '{{json .State.Health}}' vault`
- `docker inspect --format '{{json .State.Health}}' vault-agent`

## Review Cadence

- 월 1회 정기 점검
- Vault 버전/구성/정책 변경 시 수시 점검

## Auto-unseal & Remote Audit Adoption Gate

- **Auto-unseal 승인 조건**:
  - KMS/HSM 키 관리 책임자 지정
  - 장애 시 수동 unseal fallback 절차 검증
  - runbook 전환 체크리스트 승인
- **Remote Audit 승인 조건**:
  - 전송 대상(예: SIEM, object storage) 보존 정책 확정
  - 감사 로그 무결성/지연 모니터링 기준 수립
  - 로컬 + 원격 이중화 검증 완료

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: security-hardening/auth-hardening/doc-traceability 통과
- **Log / Trace Retention**: audit/healthcheck/검증 로그 보존 정책 준수
- **Safety Incident Thresholds**: seal 상태 지속, 렌더 실패 지속, audit 비활성 상태 감지 시 runbook 즉시 수행

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-03-security-optimization-hardening.md](../../01.prd/2026-03-28-03-security-optimization-hardening.md)
- **ARD**: [../../02.ard/0018-security-optimization-hardening-architecture.md](../../02.ard/0018-security-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md](../../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/03-security/spec.md](../../04.specs/03-security/spec.md)
- **Plan**: [../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/03-security/vault.md](../../07.guides/03-security/vault.md)
- **Runbook**: [../../09.runbooks/03-security/vault.md](../../09.runbooks/03-security/vault.md)
