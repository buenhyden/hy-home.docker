# Vault System Guide

> Comprehensive guide for Vault setup, unsealing, and secrets management for `hy-home.docker`.

---

## Overview (KR)

이 문서는 Vault의 초기 기동(Setup), 봉인 해제(Unseal), 그리고 Keycloak을 이용한 OIDC 인증 연동 가이드를 제공한다. 또한, 기존 로컬 `secrets/` 폴더의 데이터를 Vault KV-v2 엔진으로 마이그레이션하고 Vault Agent를 통해 애플리케이션에 전달하는 표준 절차를 다룬다.

## Guide Type

`system-guide | how-to | security-guide`

## Target Audience

- **Developer**: Vault Agent를 통한 비밀 주입 방식 이해
- **Operator**: 초기화, 봉인 해제, 마이그레이션 수행
- **AI Agents**: 자동화된 시크릿 관리 및 인증 설정

## Purpose

Vault의 생명주기 관리와 `hy-home.docker` 표준 보안 모델(OIDC + AppRole)을 일관되게 적용할 수 있도록 돕는다.

## Prerequisites

- `infra/03-security/vault` 컨테이너가 실행 중이어야 함.
- Vault 접근을 위한 CLI 도구(`vault`)가 설치되어 있어야 함.
- Keycloak(`infra/02-auth`) 서비스가 정상 작동 중이어야 함 (OIDC 연동 시).

## Step-by-step Instructions

### 1. Initialization and Unsealing

Vault가 처음 실행되면 초기화가 필요하며, 5개의 Unseal Key와 1개의 Root Token이 생성됨:

1.  **Initialize**:
    ```bash
    docker exec -it vault vault operator init
    ```
    *생성된 키들을 안전한 곳에 별도로 백업한다.*

2.  **Unseal**:
    5개의 키 중 3개가 입력되어야 봉인이 해제됨 (Threshold 3/5):
    ```bash
    docker exec -it vault vault operator unseal <KEY_1>
    docker exec -it vault vault operator unseal <KEY_2>
    docker exec -it vault vault operator unseal <KEY_3>
    ```

### 2. Keycloak OIDC Integration

사용자가 Keycloak 계정으로 Vault에 로그인할 수 있도록 설정:

1.  **Enable OIDC**:
    ```bash
    vault auth enable oidc
    ```
2.  **Configure OIDC**:
    Keycloak Realm URL을 `oidc_discovery_url`로 설정하고, 전용 Client 정보를 등록한다.
3.  **Map Groups**:
    Keycloak의 그룹/역할을 Vault의 Policy와 매핑하여 Role-based Access Control을 구현한다.

### 3. Secrets Migration Strategy

기존 로컬 `secrets/` 데이터를 Vault KV-v2 엔진으로 이동:

1.  **Enable KV Engine**:
    ```bash
    vault secrets enable -path=secret kv-v2
    ```
2.  **Migration Example**:
    ```bash
    # Postgres 암호 마이그레이션
    PASSWORD=$(cat secrets/postgres_password)
    vault kv put secret/infra/postgres password="$PASSWORD"
    ```

### 4. Vault Agent & Templating

애플리케이션 컨테이너에 비밀을 주입하는 방식:

1.  **AppRole Setup**: 애플리케이션 전용 Role ID와 Secret ID를 생성한다.
2.  **Template (`.ctmpl`)**:
    ```hcl
    {{- with secret "secret/data/infra/postgres" -}}
    POSTGRES_PASSWORD={{ .Data.data.password }}
    {{- end -}}
    ```
3.  **Rendering**: Vault Agent가 템플릿을 실제 파일로 렌더링하여 공유 볼륨에 저장한다.

## Common Pitfalls

- **Unseal Keys Loss**: Unseal 키를 모두 분실하면 데이터를 복구할 수 없음.
- **Root Token Usage**: Root Token은 초기 설정 후 즉시 파기하거나 비활성화해야 함.
- **Path Mismatch**: `.ctmpl`의 시크릿 경로와 실제 Vault 경로가 다를 경우 렌더링이 실패함.

## Related Documents

- **Spec**: [spec.md](../../04.specs/03-security/spec.md)
- **Operation**: [vault.md](../../08.operations/03-security/vault.md)
- **Runbook**: [vault.md](../../09.runbooks/03-security/vault.md)
