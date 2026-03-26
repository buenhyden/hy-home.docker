# Spec: Security Tier (03-security)

## Overview (KR)

`03-security` 티어는 HashiCorp Vault를 사용하여 플랫폼의 민감 정보를 중앙에서 관리한다. 본 명세는 Vault 서버의 Raft 기반 고가용성 구성, AppRole을 이용한 서비스 인증, 그리고 Vault Agent를 통한 비밀 정보 주입 템플릿 구성을 상세히 정의한다.

## Inputs

- **PRD**: `[../01.prd/2026-03-26-03-security.md]`
- **ARD**: `[../02.ard/0003-security-architecture.md]`
- **ADR**: `[../03.adr/0003-vault-as-secrets-manager.md]`

## Component Specification

### 1. Vault Server (`vault`)
- **Image**: `hashicorp/vault:1.21.4`
- **Config**: `/vault/config/vault.hcl`
- **Port**: 8200 (API/UI), 8201 (Cluster)
- **Features**:
    - Raft Storage enabled (`/vault/data`).
    - TLS Termination at Traefik (Internal HTTP).
    - UI enabled for admin management.

### 2. Vault Agent (`vault-agent`)
- **Role**: 인증 캐싱 및 템플릿 렌더링.
- **Auth Method**: `approle`
    - RoleID Location: `/vault/agent/role_id`
    - SecretID Location: `/vault/agent/secret_id`
- **Rendering Targets**:
    - `postgres/postgres_password`
    - `keycloak/kc_db_password`, `admin_username`, `admin_password`
    - `oauth2-proxy/client_secret`, `cookie_secret`
    - `grafana/admin_password`, `db_password`, `oauth_client_secret`

## Interface and Security

### Traefik Ingress Labels
- `traefik.http.routers.vault.rule`: `Host(\`vault.\${DEFAULT_URL}\`)`
- `traefik.http.routers.vault.entrypoints`: `websecure`
- `traefik.http.routers.vault.tls`: `true`

### Security Hardening
- **IPC_LOCK**: 하드웨어 메모리 락 기능을 사용하여 시크릿이 스왑 메모리로 빠져나가는 것을 방지.
- **Policy Enforcement**: 모든 AppRole은 최소 권한 원칙(Principle of Least Privilege)에 따라 전용 ACL 정책 할당.

## Data Model (KV Engine)

- **Path Schema**: `secret/data/hy-home/{tier-name}/{service-name}`
- **Example**: `secret/data/hy-home/data/postgres`

## Verification Plan

### Automated Verification
- `docker exec vault vault status`: Unseal 및 HA 상태 확인.
- `docker exec vault-agent ls /vault/out/app/app.env`: 템플릿 렌더링 결과 파일 존재 확인.

### Manual Verification
- Vault UI 접속 (`https://vault.${DEFAULT_URL}`) 및 로그인 확인.
- 감사 로그 활성화 확인: `vault audit list`.
