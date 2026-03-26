# Vault Guide

> Comprehensive guide for Vault setup, unsealing, and secrets management within the `hy-home.docker` ecosystem.

---

## Overview (KR)

이 문서는 Vault의 초기 기동(Setup), 봉인 해제(Unseal), 그리고 Keycloak을 이용한 OIDC 인증 연동 가이드를 제공한다. 또한, 기존 로컬 `secrets/` 폴더의 데이터를 Vault KV-v2 엔진으로 마이그레이션하고 Vault Agent를 통해 애플리케이션에 전달하는 표준 절차를 다룬다.

## Guide Type

`system-guide | how-to`

## Target Audience

- SRE / DevOps
- Security Engineers
- AI Agents

## Prerequisites

- `infra/03-security/vault` 컨테이너가 실행 중이어야 함.
- Vault 접근을 위한 CLI 도구가 로컬 또는 컨테이너 내부에 준비되어 있어야 함.
- Keycloak(`infra/02-auth`) 서비스가 정상 작동 중이어야 함 (OIDC 연동 시).

## Step-by-step Instructions

### 1. Initialization and Unsealing
Vault가 처음 실행되면 초기화가 필요하며, 5개의 Unseal Key와 1개의 Root Token이 생성됨 (표준 기준):

1. **Initialize**:
   ```bash
   docker exec -it vault vault operator init
   ```
   *생성된 키들을 안전한 곳에 별도로 백업한다.*

2. **Unseal**:
   5개의 키 중 3개가 입력되어야 봉인이 해제됨 (Threshold 3/5):
   ```bash
   docker exec -it vault vault operator unseal <KEY_1>
   docker exec -it vault vault operator unseal <KEY_2>
   docker exec -it vault vault operator unseal <KEY_3>
   ```

### 2. Keycloak OIDC Integration (Vault Auth Method)
사용자가 Keycloak 계정으로 Vault에 로그인할 수 있도록 설정:

1. **Enable OIDC**:
   ```bash
   vault auth enable oidc
   ```
2. **Configure OIDC**:
   `oidc_discovery_url`을 Keycloak의 Realm URL로 설정하고, `client_id` 및 `client_secret`을 등록한다.
3. **Map Groups**:
   Keycloak의 그룹/역할을 Vault의 Policy와 매핑하여 권한을 제어한다.

### 3. Secrets Migration Strategy
기존 로컬 `secrets/` 폴더의 데이터를 Vault로 이동하는 방법:

1. **Enable KV Engine**:
   ```bash
   vault secrets enable -path=secret kv-v2
   ```
2. **Migration Example (Postgres)**:
   ```bash
   # 로컬 파일의 내용을 Vault에 쓰기
   PASSWORD=$(cat secrets/postgres_password)
   vault kv put secret/data/infra/postgres password="$PASSWORD"
   ```

### 4. Vault Agent & Templating
Vault Agent를 통해 애플리케이션 컨테이너에 비밀을 주입하는 방식:

1. **HCL Template (`.ctmpl`)**:
   ```hcl
   {{- with secret "secret/data/infra/postgres" -}}
   POSTGRES_PASSWORD={{ .Data.data.password }}
   {{- end -}}
   ```
2. **Rendering**:
   Vault Agent는 AppRole로 인증 후 위 템플릿을 실제 환경 변수 파일로 렌더링하여 공유 볼륨에 저장함.

## Common Pitfalls

- **Unseal Keys 분실**: Unseal 키를 모두 분실하면 Vault 내부 데이터를 복구할 수 없음 (강력 주의).
- **Token Expiration**: Root Token은 초기 설정용으로만 사용하고, 운영 시에는 적절한 TTL이 설정된 AppRole/User Token을 사용해야 함.

## Related Documents

- **Ops Policy**: `[../../08.operations/03-security/vault.md]`
- **Runbook**: `[../../09.runbooks/03-security/vault.md]`
- **Tech Spec**: `[../../04.specs/03-security/spec.md]`
