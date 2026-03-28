# 03-Security Optimization Hardening Specification

## Overview (KR)

이 문서는 `infra/03-security/vault`의 최적화/하드닝 구현 계약을 정의한다. 템플릿 시크릿 경로 정규화, `vault-agent` 헬스체크/출력 볼륨, 하드닝 검증 자동화, 단계적 HA 확장 정책을 명시한다.

## Strategic Boundaries & Non-goals

- 본 Spec은 Vault/Vault Agent 운영 하드닝 계약을 소유한다.
- KMS/HSM auto-unseal 및 원격 audit sink 실구현은 다음 단계로 이관한다.

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-03-security-optimization-hardening.md](../../01.prd/2026-03-28-03-security-optimization-hardening.md)
- **ARD**: [../../02.ard/0018-security-optimization-hardening-architecture.md](../../02.ard/0018-security-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0003-vault-as-secrets-manager.md](../../03.adr/0003-vault-as-secrets-manager.md)
  - [../../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md](../../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - `vault`, `vault-agent`는 `template-stateful-med` 상속을 유지한다.
  - `vault-agent`는 PID 파일(`/tmp/vault-agent.pid`) 기반 healthcheck를 제공한다.
  - agent 렌더링 결과는 `/vault/out` persistent volume에 기록한다.
- **Data / Interface Contract**:
  - 템플릿 시크릿 경로는 `secret/data/hy-home/<tier>/<service>` 규약을 따른다.
  - 서비스별 키 계약:
    - `04-data/mng-db`: `password`
    - `02-auth/keycloak`: `db_password`, `admin_username`, `admin_password`
    - `02-auth/oauth2-proxy`: `client_secret`, `cookie_secret`
    - `06-observability/grafana`: `admin_password`, `db_password`, `oauth_client_secret`
- **Governance Contract**:
  - `scripts/check-security-hardening.sh`를 CI `security-hardening` job으로 강제한다.
  - `scripts/check-auth-hardening.sh`는 최신 02-auth 계약 기준으로 유지한다.

## Core Design

- **Component Boundary**:
  - Vault: KV-v2 시크릿 저장/정책/감사
  - Vault Agent: AppRole 인증 + template 렌더링
- **Key Dependencies**:
  - `01-gateway/traefik` (외부 TLS 종료)
  - 시크릿 소비 계층(`02-auth`, `04-data`, `06-observability`)
- **Tech Stack**:
  - `hashicorp/vault:1.21.4`
  - Docker Compose + `common-optimizations.yml`

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - KV-v2 path: `secret/data/hy-home/...`
- **Migration / Transition Plan**:
  - placeholder 템플릿 제거 후 경로/키 계약 고정
  - Phase-2에서 auto-unseal/원격 audit 전환 절차 적용

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface VaultTemplateContract {
  sourcePath: string;
  destinationPath: string;
  secretKey: string;
  placeholderForbidden: true;
}
```

## Edge Cases & Error Handling

- AppRole role_id/secret_id 누락 시 agent 렌더 실패
- path/키 불일치 시 템플릿 빈 출력 또는 오류
- Vault sealed 상태에서 template refresh 실패

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `vault-agent` healthcheck fail 또는 렌더 산출물 미생성
- **Fallback**: runbook 절차로 seal 상태/AppRole 파일/템플릿 경로 점검 후 재기동
- **Human Escalation**: Security Operator + Infra on-call 동시 호출

## Verification

```bash
docker compose -f infra/03-security/vault/docker-compose.yml config
bash scripts/check-security-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
bash scripts/check-auth-hardening.sh
```

가능 환경에서 runtime 검증:

```bash
docker compose -f infra/03-security/vault/docker-compose.yml up -d vault vault-agent
docker exec vault vault status
docker inspect --format '{{json .State.Health}}' vault
docker inspect --format '{{json .State.Health}}' vault-agent
docker exec vault-agent ls -la /vault/out
```

## Success Criteria & Verification Plan

- **VAL-SPC-SEC-001**: `check-security-hardening` 실패 0건
- **VAL-SPC-SEC-002**: `.ctmpl` placeholder 경로 검출 0건
- **VAL-SPC-SEC-003**: CI `security-hardening` job 실행 성공
- **VAL-SPC-SEC-004**: 문서 추적성 검사 통과
- **VAL-SPC-SEC-005**: auth 하드닝 회귀 검사 통과

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/03-security/vault.md](../../07.guides/03-security/vault.md)
- **Operations**: [../../08.operations/03-security/vault.md](../../08.operations/03-security/vault.md)
- **Runbook**: [../../09.runbooks/03-security/vault.md](../../09.runbooks/03-security/vault.md)
