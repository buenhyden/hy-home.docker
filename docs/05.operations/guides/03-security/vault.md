---
status: active
---
<!-- Target: docs/05.operations/guides/03-security/vault.md -->

# 03-Security Vault Usage Guide

## Usage

### Overview (KR)

이 문서는 `03-security` Vault 운영/개발 가이드다. Vault Agent 템플릿 경로 규약, AppRole 부트스트랩, 렌더 출력 확인 절차를 중심으로 optimization/hardening 기준을 설명한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Security Operators
- Infra/DevOps Engineers
- Service Developers

### Purpose

- `secret/data/hy-home/...` 시크릿 경로/키 계약을 일관되게 사용한다.
- Vault Agent 렌더링 결과를 서비스에 안전하게 연결한다.
- 하드닝 회귀를 사전 검증한다.

### Prerequisites

- `infra/03-security/vault` 구성 파일 접근
- Vault 초기화/Unseal 가능한 운영 권한
- AppRole RoleID/SecretID 발급 권한

### Step-by-step Instructions

1. Vault 기본 상태 확인
   - `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/hardening/check-all-hardening.sh 03-security`
   - Runtime-only: `docker compose --profile security exec vault vault status`
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

   docker compose --profile security exec -T vault vault policy write vault-agent-policy - <<'EOF'
   path "secret/data/hy-home/*" {
     capabilities = ["read", "list"]
   }
   EOF

   docker compose --profile security exec -T vault vault auth enable approle || true
   docker compose --profile security exec -T vault vault write auth/approle/role/vault-agent \
     secret_id_ttl=0 \
     token_num_uses=0 \
     token_ttl=0 \
     token_max_ttl=0 \
     secret_id_num_uses=0 \
     token_policies="vault-agent-policy"

   docker compose --profile security exec -T vault vault read -field=role_id auth/approle/role/vault-agent/role-id > "$agent_dir/role_id"
   docker compose --profile security exec -T vault vault write -f -field=secret_id auth/approle/role/vault-agent/secret-id > "$agent_dir/secret_id"
   chmod 600 "$agent_dir/role_id" "$agent_dir/secret_id"
   docker run --rm -v "$agent_dir:/agent" alpine sh -c 'chown -R 100:1000 /agent 2>/dev/null || true'
   docker compose --profile security restart vault-agent >/dev/null
   ```

   - token sink(`/vault/agent/token`) 생성 확인
3. 시크릿 경로 규약 적용
   - `secret/data/hy-home/04-data/mng-db` -> `password`
   - `secret/data/hy-home/02-auth/keycloak` -> `db_password`, `admin_username`, `admin_password`
   - `secret/data/hy-home/02-auth/oauth2-proxy` -> `client_secret`, `cookie_secret`
   - `secret/data/hy-home/06-observability/grafana` -> `admin_password`, `db_password`, `grafana_client_secret`
4. 렌더 출력 확인
   - Runtime-only: `docker compose --profile security exec vault-agent ls -la /vault/out`
   - 서비스별 파일 존재/권한(0600) 점검
5. 정적 하드닝 검증
   - `bash scripts/hardening/check-all-hardening.sh 03-security`
   - `bash scripts/validation/check-template-security-baseline.sh`

### Common Pitfalls

- placeholder 경로(`secret/data/example`)를 템플릿에 남겨두는 실수
- KV 경로와 키 이름 불일치로 빈 렌더 파일 생성
- `role_id`/`secret_id` 누락으로 Agent 인증 실패

## Common Checks

- `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 03-security`
- `bash scripts/validation/check-template-security-baseline.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/03-security/vault.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/03-security/vault.md)
- [Recovery runbook](../../runbooks/03-security/vault.md)
