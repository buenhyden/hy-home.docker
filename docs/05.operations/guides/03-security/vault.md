# 03-Security Vault Operations Policy

## Overview (KR)

이 문서는 `03-security` Vault 운영 정책을 정의한다. 즉시 적용 하드닝 기준(템플릿 계약, healthcheck, 검증 자동화)과 단계적 확장 정책(auto-unseal, 원격 audit)을 명시한다.

## Policy Scope

- `infra/03-security/vault/docker-compose.yml`
- `infra/03-security/vault/config/vault-agent.hcl`
- `infra/03-security/vault/config/templates/*.ctmpl`
- `scripts/hardening/check-all-hardening.sh 03-security`

## Applies To

- **Systems**: Vault server, Vault Agent
- **Agents**: Infra/Security/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Vault Agent 템플릿은 `secret/data/hy-home/...` 경로 규약을 사용해야 한다.
  - `vault-agent`는 PID 기반 healthcheck를 유지해야 한다.
  - 렌더 출력은 `/vault/out` persistent volume에 저장해야 한다.
  - `scripts/hardening/check-all-hardening.sh 03-security`를 CI `security-hardening` 게이트로 강제한다.
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

- `bash scripts/hardening/check-all-hardening.sh 03-security`
- `bash scripts/validation/check-template-security-baseline.sh`
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

- **PRD**: [../../01.requirements/2026-03-28-03-security-optimization-hardening.md](../../../01.requirements/2026-03-28-03-security-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md](../../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md)
- **ADR**: [../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../03.specs/03-security/spec.md](../../../03.specs/03-security/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Usage**: [../../05.operations/03-security/vault.md](./vault.md)
- **Procedure**: [../../05.operations/03-security/vault.md](./vault.md)

## Usage

> Migrated from `docs/05.operations/03-security/vault.md` during the 2026-05-10 operations taxonomy consolidation.

### 03-Security Vault Usage

#### Overview (KR)

이 문서는 `03-security` Vault 운영/개발 가이드다. Vault Agent 템플릿 경로 규약, AppRole 부트스트랩, 렌더 출력 확인 절차를 중심으로 optimization/hardening 기준을 설명한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Security Operators
- Infra/DevOps Engineers
- Service Developers

#### Purpose

- `secret/data/hy-home/...` 시크릿 경로/키 계약을 일관되게 사용한다.
- Vault Agent 렌더링 결과를 서비스에 안전하게 연결한다.
- 하드닝 회귀를 사전 검증한다.

#### Prerequisites

- `infra/03-security/vault` 구성 파일 접근
- Vault 초기화/Unseal 가능한 운영 권한
- AppRole RoleID/SecretID 발급 권한

#### Step-by-step Instructions

1. Vault 기본 상태 확인
   - `docker compose -f infra/03-security/vault/docker-compose.yml config`
   - `docker compose -f infra/03-security/vault/docker-compose.yml up -d vault vault-agent`
   - `docker exec vault vault status`
2. AppRole bootstrap
   - Vault가 unsealed 상태인지 확인한 뒤 아래 절차로 Agent 인증 및 접근 권한을 설정한다.
   - 명령은 `role_id`와 `secret_id`를 파일로 직접 리다이렉션해야 하며, 생성값을 문서/PR/로그에 붙여넣지 않는다.

   ```bash
   set -euo pipefail
   set +u
   [ -f .env ] && . ./.env
   set -u
   default_security_dir="${DEFAULT_SECURITY_DIR:-./volumes/security}"
   agent_dir="${default_security_dir}/vault/agent"
   mkdir -p "$agent_dir"
   umask 077

   docker exec vault vault policy write vault-agent-policy - <<'EOF'
   path "secret/data/hy-home/*" {
     capabilities = ["read", "list"]
   }
   EOF

   docker exec vault vault auth enable approle || true
   docker exec vault vault write auth/approle/role/vault-agent \
     secret_id_ttl=0 \
     token_num_uses=0 \
     token_ttl=0 \
     token_max_ttl=0 \
     secret_id_num_uses=0 \
     token_policies="vault-agent-policy"

   docker exec vault vault read -field=role_id auth/approle/role/vault-agent/role-id > "$agent_dir/role_id"
   docker exec vault vault write -f -field=secret_id auth/approle/role/vault-agent/secret-id > "$agent_dir/secret_id"
   chmod 600 "$agent_dir/role_id" "$agent_dir/secret_id"
   docker run --rm -v "$agent_dir:/agent" alpine sh -c 'chown -R 100:1000 /agent 2>/dev/null || true'
   docker restart vault-agent >/dev/null
   ```

   - token sink(`/vault/agent/token`) 생성 확인
3. 시크릿 경로 규약 적용
   - `secret/data/hy-home/04-data/mng-db` -> `password`
   - `secret/data/hy-home/02-auth/keycloak` -> `db_password`, `admin_username`, `admin_password`
   - `secret/data/hy-home/02-auth/oauth2-proxy` -> `client_secret`, `cookie_secret`
   - `secret/data/hy-home/06-observability/grafana` -> `admin_password`, `db_password`, `grafana_client_secret`
4. 렌더 출력 확인
   - `docker exec vault-agent ls -la /vault/out`
   - 서비스별 파일 존재/권한(0600) 점검
5. 정적 하드닝 검증
   - `bash scripts/hardening/check-all-hardening.sh 03-security`
   - `bash scripts/validation/check-template-security-baseline.sh`

#### Common Pitfalls

- placeholder 경로(`secret/data/example`)를 템플릿에 남겨두는 실수
- KV 경로와 키 이름 불일치로 빈 렌더 파일 생성
- `role_id`/`secret_id` 누락으로 Agent 인증 실패

#### Related Documents

- **Spec**: [../../03.specs/03-security/spec.md](../../../03.specs/03-security/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Task**: [../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Operation**: [../../05.operations/03-security/vault.md](./vault.md)
- **Procedure**: [../../05.operations/03-security/vault.md](./vault.md)

## Procedure

> Migrated from `docs/05.operations/03-security/vault.md` during the 2026-05-10 operations taxonomy consolidation.

### 03-Security Vault Procedure

: Vault Secret Management Recovery & Maintenance

#### Overview (KR)

이 런북은 Vault seal/unseal, raft 상태 점검, audit 활성/검증, Vault Agent 렌더 실패 복구, 안전 롤백 절차를 즉시 실행 가능 형태로 제공한다.

#### Purpose

- Vault 장애/오작동 상황에서 복구 시간을 줄인다.
- 하드닝 계약 위반을 빠르게 진단하고 원복한다.

#### Canonical References

- [Spec](../../../03.specs/03-security/spec.md)
- [Operations Policy](./vault.md)
- [Plan](../../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)

#### When to Use

- Vault가 `Sealed: true` 상태일 때
- raft peer 상태가 비정상일 때
- audit device가 비활성화되었을 때
- Vault Agent healthcheck 또는 템플릿 렌더가 실패할 때

#### Procedure or Checklist

##### Checklist

- [ ] `docker exec vault vault status` 확인
- [ ] `docker inspect --format '{{json .State.Health}}' vault` 확인
- [ ] `docker inspect --format '{{json .State.Health}}' vault-agent` 확인
- [ ] 최근 변경 파일/커밋 식별

##### Procedure

1. Seal/Unseal 복구
   - 상태 확인: `docker exec vault vault status`
   - 필요한 경우 unseal 키 3회 입력
2. Raft 상태 점검
   - `docker exec vault vault operator raft list-peers`
   - 비정상 peer 식별 후 정책에 따라 조치
3. Audit 활성/검증
   - `docker exec vault vault audit list`
   - 로컬 audit 활성 확인, 원격 audit는 정책 승인 상태 확인
4. Vault Agent 렌더 실패 복구
   - `docker logs vault-agent --tail=200`
   - `/vault/agent/role_id`, `/vault/agent/secret_id`, `/vault/agent/token` 확인
   - 인증 정보(`role_id`/`secret_id`) 부재/오류 시 위 AppRole bootstrap 절차를 재실행한다. 생성값은 파일로 직접 저장하고 문서/PR/로그에 노출하지 않는다.
   - `docker exec vault-agent ls -la /vault/out`로 출력 파일 재검증
5. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 03-security`
   - `bash scripts/validation/check-template-security-baseline.sh`

#### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 03-security` 통과
- [ ] `docker exec vault vault status`에서 `Sealed: false` 확인
- [ ] `docker inspect`에서 `vault`, `vault-agent` health가 정상
- [ ] `/vault/out` 하위 템플릿 파일 생성 확인

#### Observability and Evidence Sources

- **Signals**: container health, Vault status, audit list, agent render logs
- **Evidence to Capture**:
  - `docker logs vault --tail=200`
  - `docker logs vault-agent --tail=200`
  - `vault status`, `vault operator raft list-peers`, `vault audit list` 출력

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/03-security/vault/docker-compose.yml`
  - `infra/03-security/vault/config/templates/*.ctmpl`
  - `scripts/hardening/check-all-hardening.sh 03-security`
  - `.github/workflows/ci-quality.yml`
  - `scripts/hardening/check-all-hardening.sh 02-auth`
- [ ] compose 재반영
  - `docker compose -f infra/03-security/vault/docker-compose.yml up -d vault vault-agent`
- [ ] 하드닝/추적성 검증 재실행

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: CI `security-hardening` 임시 비활성은 승인 후만 수행
- **Eval Re-run**: `check-security-hardening`, `check-auth-hardening`, `check-doc-traceability`
- **Trace Capture**: CI job logs + container logs

#### Related Operational Documents

- **Usage**: [../../05.operations/03-security/vault.md](./vault.md)
- **Operation**: [../../05.operations/03-security/vault.md](./vault.md)
