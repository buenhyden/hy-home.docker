---
title: "Keycloak IAM"
version: "1.1.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-11-12"
---

# Keycloak IAM

관련 구성요소의 현재 선언은 [버전 레지스트리](../../tech-stack.versions.json)가 가리키는 Compose 원본에서 확인합니다. 로컬 빌드의 기준 이미지는 [Dockerfile](Dockerfile)에서 확인합니다.

> Central Identity and Access Management provider for `hy-home.docker`.

## Overview

Keycloak은 중앙 IdP다. 사용자 인증, 세션, OIDC/SAML token 발행과
Airflow Authorization Services를 제공한다.

Runtime image: [Keycloak Compose declaration](docker-compose.yml).

Canonical realm:
`hy-home.realm`

## Audience

- Infrastructure Operators
- Security Reviewers
- AI Agents

## Scope

### In Scope

- Keycloak runtime wiring
- non-secret environment keys
- readiness
- OIDC client integration
- realm role/group/policy operational contract

### Out of Scope

- credential/token values
- application business logic
- application-internal RBAC implementation

## Structure

```text
keycloak/
├── docker-compose.yml
└── README.md
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Service | `keycloak` |
| Image | [Compose declaration](docker-compose.yml) |
| Profiles | `core`, `auth`, `dev` |
| Database | `mng-pg` |
| Network | `infra_net` |
| Public Host | `keycloak.${DEFAULT_URL}` |
| Health | management port `/health/ready` |
| Secrets | `keycloak_db_password`, `keycloak_admin_password` |

## Application Client Matrix

| Application | Client ID | Authentication Pattern |
| --- | --- | --- |
| OAuth2 Proxy | `home-proxy-client` | Gateway ForwardAuth |
| Kafbat UI | `home-kafbat` | Application-native OAuth2/OIDC |
| Airflow | `home-airflow` | Native Keycloak Auth Manager + Authorization Services |

## Airflow Authorization Contract

Required realm roles:

```text
Viewer
User
Op
Admin
SuperAdmin
```

Expected scopes after bootstrap:

```text
GET
POST
PUT
DELETE
MENU
LIST
```

Provider upgrades from 0.8.2 to 0.9.0 require permission repair; see the [upstream migration note](https://airflow.apache.org/docs/apache-airflow-providers-keycloak/stable/changelog.html). <!-- runtime-version-exception: migration — identifies the provider release requiring existing permission repair -->
For non-team installations, rerun `create-permissions` without `--teams`; provider installation alone does not update stored permissions.

## Kafbat Identity Contract

Kafbat uses Keycloak `groups` claim.

Current application mappings:

- `/admins`
- `/users`

## How to Work in This Area

1. Keycloak operations guide/policy/runbook 확인.
2. secret은 Docker Secret.
3. `/health/ready` UP 확인 후 dependent service 검증.
4. application client는 canonical realm `hy-home.realm` 사용.
5. ForwardAuth/Native OIDC 목적을 client별로 구분.
6. realm/client/role 변경 후 해당 application login/RBAC 검증.

## Configuration

- `KC_HOSTNAME=keycloak.${DEFAULT_URL}`
- `KC_PROXY_HEADERS=xforwarded`
- PostgreSQL backend
- public HTTP behind Traefik TLS

## Validation

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth
```

Runtime:

- readiness
- OIDC discovery
- application redirect/client settings
- Airflow authorization resources/scopes
- Kafbat groups claim

## Troubleshooting

- DB/readiness 먼저 확인.
- redirect/issuer mismatch를 확인.
- Airflow `invalid_scope`는 Authorization bootstrap을 확인.
- Kafbat RBAC mismatch는 `groups` claim과 cluster name을 확인.
- token/secret raw value는 출력하지 않는다.

## Related Documents

- **Guide**: `docs/05.operations/catalog/02-auth/0014-keycloak/guide.md`
- **Policy**: `docs/05.operations/catalog/02-auth/0014-keycloak/policy.md`
- **Runbook**: `docs/05.operations/catalog/02-auth/0014-keycloak/runbook.md`
- **Integration**: `docs/05.operations/catalog/02-auth/0079-application-auth-integration/guide.md`
- [Documentation index](../../../docs/README.md)
