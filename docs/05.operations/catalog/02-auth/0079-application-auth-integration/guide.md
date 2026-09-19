---
title: "Application Authentication Integration Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0079"
parent_ids:
- "POL-0079"
created: "2026-09-18"
---

# Application Authentication Integration Guide

## Usage

### Overview

Keycloak, OAuth2 Proxy, Traefik, Kafbat UI, Airflow를 중복 인증 없이 연결하고
서비스별 authorization model을 유지하는 방법을 설명한다.

### Usage Type

`system-guide | how-to | integration-reference`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Platform Developers
- AI Agents

### Purpose

- ForwardAuth와 Native OIDC의 책임 경계를 명확히 한다.
- Keycloak application client 설정을 일관되게 유지한다.
- Kafbat/Airflow native RBAC를 gateway auth와 충돌시키지 않는다.

### Authentication Pattern

#### Gateway ForwardAuth

```text
Browser -> Traefik -> OAuth2 Proxy -> Keycloak -> Service
```

대상:

- 자체 OIDC가 없는 서비스
- gateway-level authentication이 적절한 서비스
- 현재 Flower/n8n 등

#### Application-native OIDC

```text
Browser -> Traefik -> Application -> Keycloak
```

대상:

- Apache Airflow
- Kafbat UI

Native OIDC 서비스에는 `sso-auth@file`을 중복 적용하지 않는다.

### Keycloak Client Matrix

| Application | Client ID | Flow | Authorization Services |
| --- | --- | --- | --- |
| OAuth2 Proxy | `home-proxy-client` | Gateway ForwardAuth OIDC | No |
| Kafbat UI | `home-kafbat` | Native Authorization Code | No |
| Airflow | `home-airflow` | Native Keycloak Auth Manager | Yes |

Realm: `hy-home.realm`

Issuer:

```text
https://keycloak.${DEFAULT_URL}/realms/hy-home.realm
```

### OAuth2 Proxy

현재 역할:

- ForwardAuth provider
- Keycloak OIDC client
- Valkey-backed browser session

운영 원칙:

- Native OIDC 앱에는 적용하지 않는다.
- `Authorization` forwarding은 upstream 자체 JWT/Bearer scheme과 충돌 여부를 확인한다.
- cookie domain은 `.${DEFAULT_URL}` 경계를 유지한다.
- callback URL과 authorization code를 재사용하지 않는다.

### Kafbat UI

현재 구현:

- [kafbat/kafka-ui image declaration](../../../../../infra/05-messaging/kafka/docker-compose.yml)
- `auth.type: OAUTH2`
- direct Keycloak issuer
- `roles-field: groups`
- gateway-only Traefik route

Keycloak client:

- Client ID: `home-kafbat`
- Client Authentication: ON
- Standard Flow: ON
- Redirect: `https://kafbat-ui.${DEFAULT_URL}/login/oauth2/code/keycloak`
- Web Origin: `https://kafbat-ui.${DEFAULT_URL}`

RBAC:

- `/admins` -> admin
- `/users` -> readonly

`rbac.roles[*].clusters`는 `KAFKA_CLUSTERS_0_NAME`과 일치해야 한다.

#### Local CA Trust

```text
JDK default cacerts
  -> copy
  -> import mkcert rootCA.pem
  -> use copied truststore
```

local root CA만 담긴 새 truststore로 JDK public CA roots를 대체하지 않는다.

### Airflow

현재 구현:

- Airflow: [build declaration](../../../../../infra/07-workflow/airflow/Dockerfile)
- Keycloak provider: [build declaration](../../../../../infra/07-workflow/airflow/Dockerfile)
- `KeycloakAuthManager`
- `home-airflow`
- fixed Airflow API JWT secret
- certifi + local root CA bundle
- `--proxy-headers`
- gateway-only Airflow router

#### Token model

Keycloak tokens:

- OIDC login
- Authorization Services evaluation

Airflow internal JWT:

- Airflow browser/API session
- `AIRFLOW__API_AUTH__JWT_SECRET`으로 서명

두 token은 서로 대체하지 않는다.

#### Keycloak prerequisites

Realm roles:

```text
Viewer
User
Op
Admin
SuperAdmin
```

Client:

- Client Authentication ON
- Authorization ON
- Standard Flow ON
- Redirect: `https://airflow.${DEFAULT_URL}/*`
- Web Origin: `https://airflow.${DEFAULT_URL}`

#### Authorization bootstrap

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-all     --username keycloak_admin     --user-realm master     --password
```

생성 대상:

- scopes: `GET`, `POST`, `PUT`, `DELETE`, `MENU`, `LIST`
- resources: `Dag`, `Asset`, `Pool`, `View`, ...
- role policies
- permissions

0.9.0 upgrade 후 기존 non-team permission repair:

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-permissions     --username keycloak_admin     --user-realm master     --password
```

provider update만으로 기존 Keycloak permissions는 자동 갱신되지 않는다.

### Airflow 장애 패턴

#### Config PermissionError

`airflow-init` root-created file과 runtime UID mismatch를 확인한다.

#### DB migration

```bash
docker compose exec airflow-apiserver airflow db migrate
docker compose exec airflow-apiserver airflow db check
```

#### JWT algorithm/format error

OAuth2 Proxy Bearer token이 Airflow application JWT 경계로 유입된 경우를 의심한다.
Airflow router는 gateway-only + Native Keycloak Auth Manager를 사용한다.

#### `invalid_scope`

Keycloak Authorization Services bootstrap 미완료.

#### role 404

`Viewer`, `User`, `Op`, `Admin`, `SuperAdmin` realm role을 먼저 생성한다.

#### provider 0.8.2 Admin 403

`Admin` permission에 alternative role policies가 `UNANIMOUS`로 묶일 수 있다.
0.9.0으로 upgrade하고 `create-permissions`를 다시 실행한다.

#### `/auth/login_callback` 403

query `state`와 `_oauth_state` cookie mismatch.
old callback URL을 재사용하지 않고 `/auth/login`에서 새 flow를 시작한다.

#### 일부 resource만 403

`/ui/auth/me` 등은 200인데 Pool/DAG/Asset만 403이면 authentication이 아니라
Keycloak resource authorization 문제다.

### Common Checks

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

bash scripts/hardening/check-all-hardening.sh 02-auth
bash scripts/hardening/check-all-hardening.sh 05-messaging
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

Airflow:

```bash
docker compose exec -T airflow-apiserver airflow providers list | grep -i keycloak
docker compose exec -T airflow-apiserver airflow db check
docker compose exec -T airflow-apiserver airflow dags list
```

## Runbook Handoff

- [Keycloak Runbook](../0014-keycloak/runbook.md)
- [OAuth2 Proxy Runbook](../0015-oauth2-proxy/runbook.md)
- [Kafka/Kafbat Runbook](../../05-messaging/0036-kafka/runbook.md)
- [Airflow Runbook](../../07-workflow/0050-airflow/runbook.md)

## Common Checks

Verify each application uses its documented ForwardAuth or native OIDC path, the client ID matches provisioned Keycloak metadata, and unauthorized access is rejected. Do not print client secrets or tokens. Container health alone does not prove role authorization.

## Traceability

- Parent: [POL-0079](policy.md)
- Decision: [ADR-0038](../../../../02.architecture/decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- Architecture: [AD-0002](../../../../02.architecture/descriptions/0002-auth-architecture.md)

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [curated version projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Keycloak Guide](../0014-keycloak/guide.md)
- [OAuth2 Proxy Guide](../0015-oauth2-proxy/guide.md)
- [Kafka/Kafbat Guide](../../05-messaging/0036-kafka/guide.md)
- [Airflow Guide](../../07-workflow/0050-airflow/guide.md)
