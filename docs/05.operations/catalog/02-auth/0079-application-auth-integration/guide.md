---
title: "Application Authentication Integration Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "operations"
artifact_id: "GDE-0079"
parent_ids:
- "POL-0079"
created: "2026-09-18"
---

# Application Authentication Integration Guide

## Usage

### 목적

Keycloak, OAuth2 Proxy, Traefik, Kafbat UI, Airflow를 중복 인증 없이 연결하고
서비스별 authorization 모델을 유지하는 방법을 설명한다.

### 1. 인증 패턴 선택

#### ForwardAuth

```text
Browser
  -> Traefik
  -> OAuth2 Proxy /oauth2/auth
  -> Keycloak
  -> OAuth2 Proxy session
  -> Upstream
```

적합:
- 자체 OIDC가 없는 서비스
- gateway-level user presence 확인만 필요한 서비스

현재 예:
- Flower
- n8n
- 기타 `sso-auth@file` 사용 서비스

#### Native OIDC

```text
Browser
  -> Traefik TLS/router
  -> Application
  -> Keycloak OIDC
  -> Application session/RBAC
```

현재:
- Kafbat UI
- Apache Airflow

Native OIDC 서비스에는 `sso-auth@file`을 중복 적용하지 않는다.

### 2. Keycloak Client Matrix

| Application | Client ID | Flow | Authorization Services |
| --- | --- | --- | --- |
| OAuth2 Proxy | `home-proxy-client` | ForwardAuth OIDC client | No |
| Kafbat UI | `home-kafbat` | Native Authorization Code | No |
| Airflow | `home-airflow` | Native Keycloak Auth Manager | Yes |

공통 realm:
`hy-home.realm`

Public issuer:
`https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`

### 3. OAuth2 Proxy

현재 역할:
- ForwardAuth
- Valkey session
- Keycloak OIDC client

중요:
- Native OIDC 앱에는 적용하지 않는다.
- `Authorization`을 upstream에 전달할 때 upstream의 자체 JWT/Bearer scheme과 충돌하는지 확인한다.
- cookie domain은 `.${DEFAULT_URL}` 경계로 유지한다.
- callback URL은 일회성 authorization flow 결과이므로 수동 재사용하지 않는다.

### 4. Kafbat UI

현재 compose/config:
- `kafbat/kafka-ui:v1.5.0`
- `auth.type: OAUTH2`
- Keycloak direct issuer
- `roles-field: groups`
- gateway-only Traefik route

Keycloak client:
- Client ID: `home-kafbat`
- Client Authentication: ON
- Standard Flow: ON
- Redirect:
  `https://kafbat-ui.${DEFAULT_URL}/login/oauth2/code/keycloak`
- Web Origin:
  `https://kafbat-ui.${DEFAULT_URL}`

Group mapping:
- `/admins` -> Kafbat admin role
- `/users` -> Kafbat readonly role

Kafbat v1.5.0 RBAC는 role의 `clusters` 값을 configured cluster name과 비교한다.
`hy-kafka-cluster` 같은 값은 실제 `KAFKA_CLUSTERS_0_NAME`과 일치해야 한다.

#### Local CA

기본 JDK truststore를 복사하고 mkcert root만 추가한다.

```text
default cacerts
  -> copy
  -> import rootCA.pem
  -> use copied truststore
```

local CA만 담긴 truststore로 기본 public CA roots를 대체하지 않는다.

### 5. Airflow

현재:
- Airflow 3.3.1
- `apache-airflow-providers-keycloak==0.9.0`
- `KeycloakAuthManager`
- `home-airflow`
- gateway-only Traefik route
- fixed Airflow API JWT secret
- certifi + local mkcert CA bundle

#### Token model

Keycloak token:
- login
- Keycloak Authorization Services 평가

Airflow internal JWT:
- Airflow session/API Core
- `AIRFLOW__API_AUTH__JWT_SECRET`으로 서명

둘은 서로 대체하지 않는다.

#### Keycloak prerequisites

Realm roles:

```text
Viewer
User
Op
Admin
SuperAdmin
```

Client settings:
- Client Authentication ON
- Authorization ON
- Standard Flow ON
- Service Accounts Roles ON
- Redirect:
  `https://airflow.${DEFAULT_URL}/*`
- Web Origin:
  `https://airflow.${DEFAULT_URL}`

#### Authorization bootstrap

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-all     --username keycloak_admin     --user-realm master     --password
```

생성:
- scopes: GET, POST, PUT, DELETE, MENU, LIST
- resources: Dag, Asset, Pool, View, ...
- role policies
- permissions

provider 0.9.0 upgrade 후 기존 non-team permission repair:

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-permissions     --username keycloak_admin     --user-realm master     --password
```

0.9.0 upgrade는 기존 Keycloak permissions를 자동 수정하지 않는다.

### 6. Airflow 장애 패턴

#### `PermissionError: /opt/airflow/config/airflow.cfg`

init/root owner와 runtime UID 불일치.

#### DB initialization/migration error

실행 version과 migration version을 맞추고:

```bash
airflow db migrate
airflow db check
```

#### `JWT token is not valid: The specified alg value is not allowed`

OAuth2 Proxy가 전달한 Keycloak Bearer token을 Airflow가 자체 JWT로 해석한 경우.

해결:
- Native OIDC 구조 사용
- Airflow router에서 ForwardAuth 제거

#### `invalid_scope [GET|LIST]`

Keycloak Authorization bootstrap 미완료.

#### `create-all` role 404

`Viewer/User/Op/Admin/SuperAdmin` role 미생성.

#### 0.8.2 Admin 403

global Admin permission의 alternative role policies가 `UNANIMOUS`로 평가될 수 있음.
0.9.0으로 upgrade 후 `create-permissions` 재실행.

#### `/auth/login_callback` 403

`_oauth_state` query/cookie mismatch.
old callback URL을 재사용하지 않고 `/auth/login`에서 새 flow를 시작한다.

#### 일부 resource만 403

예:

```text
/ui/auth/me -> 200
/api/v2/plugins -> 200
/api/v2/pools -> 403
/ui/dags -> 403
/api/v2/assets/events -> 403
```

authentication이 아니라 Keycloak resource authorization 문제다.
permission overlap, permission decision strategy, Resource Server evaluation을 확인한다.

### 7. 권한/그룹 검증

사용자 effective realm roles에서 `Admin` 확인:

```bash
kcadm.sh get   "users/$USER_ID/role-mappings/realm/composite"   -r hy-home.realm
```

Airflow permission 확인:
- Admin associated policies
- ReadOnly associated policies
- associated scopes
- Resource Server decision strategy

## Common Checks

```bash
# Auth
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh

# Messaging
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh

# Workflow
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

# Hardening
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

Kafbat:
- `/actuator/health`
- Keycloak login
- `/admins`/`/users` RBAC
- cluster name exact match
- local + public CA trust

## Runbook Handoff

장애 복구 실행 절차는 해당 서비스 runbook을 따른다.

- [Keycloak Runbook](../0014-keycloak/runbook.md)
- [OAuth2 Proxy Runbook](../0015-oauth2-proxy/runbook.md)
- [Kafka/Kafbat Runbook](../../../05-messaging/0036-kafka/runbook.md)
- [Airflow Runbook](../../../07-workflow/0050-airflow/runbook.md)

## Traceability

- Parent policy: [POL-0079](policy.md)
- Architecture decision: [ADR-0038](../../../../02.architecture/decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- Auth architecture: [AD-0002](../../../../02.architecture/descriptions/0002-auth-architecture.md)

## Related Documents

- [Keycloak Guide](../0014-keycloak/guide.md)
- [OAuth2 Proxy Guide](../0015-oauth2-proxy/guide.md)
- [Kafka/Kafbat Guide](../../../05-messaging/0036-kafka/guide.md)
- [Airflow Guide](../../../07-workflow/0050-airflow/guide.md)
