---
title: "Keycloak IAM"
version: "1.1.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# Keycloak IAM

관련 구성요소의 현재 선언은 [버전 레지스트리](../../tech-stack.versions.json)가 가리키는 Compose 원본에서 확인합니다. 로컬 빌드의 기준 이미지는 [Dockerfile](Dockerfile)에서 확인합니다.

> `hy-home.docker`의 중앙 ID/접근 관리 제공자입니다.

## Overview

Keycloak은 중앙 IdP다. 사용자 인증, 세션, OIDC/SAML token 발행과
Airflow Authorization Services를 제공한다.

Runtime image: [Keycloak Compose 선언](docker-compose.yml).

Canonical realm:
`hy-home.realm`

## Audience

- Infrastructure Operators
- Security Reviewers
- AI Agents

## Scope

### In Scope

- Keycloak runtime 배선
- non-secret 환경 키
- readiness
- OIDC client 통합
- realm role/group/policy 운영 계약

### Out of Scope

- credential/token 값
- 애플리케이션 비즈니스 로직
- 애플리케이션 내부 RBAC 구현

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
| Image | [Compose 선언](docker-compose.yml) |
| Profiles | `core`, `auth`, `dev` |
| Database | `mng-pg` |
| Network | `edge_net`, `mng_data_net`, `obs_net` |
| Public Host | `keycloak.${DEFAULT_URL}` |
| Health | management 포트 `/health/ready` |
| Secrets | `keycloak_db_password`, `keycloak_admin_password` |

## Application Client Matrix

| Application | Client ID | Authentication Pattern |
| --- | --- | --- |
| OAuth2 Proxy | `home-proxy-client` | Gateway ForwardAuth |
| Kafbat UI | `home-kafbat` | 애플리케이션 native OAuth2/OIDC |
| Airflow | `home-airflow` | Native Keycloak Auth Manager + Authorization Services |

이 표는 `02-auth` tier 안에서 확인 가능한 client만 담습니다. Open WebUI, Gatus, OpenBao 같은 다른 tier의 native OIDC 통합은 각 서비스의 compose/config가 근거 문서입니다.

## Airflow Authorization Contract

필수 realm role:

```text
Viewer
User
Op
Admin
SuperAdmin
```

부트스트랩 이후 예상 scope:

```text
GET
POST
PUT
DELETE
MENU
LIST
```

Provider가 0.8.2에서 0.9.0으로 업그레이드되면 권한 복구가 필요합니다. [upstream migration note](https://airflow.apache.org/docs/apache-airflow-providers-keycloak/stable/changelog.html)를 참고하십시오. <!-- runtime-version-exception: migration — identifies the provider release requiring existing permission repair -->
non-team 설치에서는 `--teams` 없이 `create-permissions`를 다시 실행하십시오. provider 설치만으로는 저장된 권한이 갱신되지 않습니다.

## Kafbat Identity Contract

Kafbat은 Keycloak `groups` claim을 사용합니다.

현재 애플리케이션 매핑:

- `/admins`
- `/users`

## How to Work in This Area

1. Keycloak 운영 guide/policy/runbook을 확인합니다.
2. secret은 Docker Secret을 사용합니다.
3. `/health/ready`가 UP인지 확인한 뒤 의존 서비스를 검증합니다.
4. application client는 canonical realm `hy-home.realm`을 사용합니다.
5. ForwardAuth/Native OIDC 목적을 client별로 구분합니다.
6. realm/client/role 변경 후 해당 application login/RBAC을 검증합니다.

## Configuration

- `KC_HOSTNAME=keycloak.${DEFAULT_URL}`
- `KC_PROXY_HEADERS=xforwarded`
- PostgreSQL backend
- Traefik TLS 뒤의 공개 HTTP

## Validation

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth
```

런타임:

- readiness
- OIDC discovery
- 애플리케이션 redirect/client 설정
- Airflow authorization resource/scope
- Kafbat groups claim

## Troubleshooting

- DB/readiness 먼저 확인.
- redirect/issuer mismatch를 확인.
- Airflow `invalid_scope`는 Authorization bootstrap을 확인.
- Kafbat RBAC mismatch는 `groups` claim과 cluster name을 확인.
- token/secret raw value는 출력하지 않는다.

## Related Documents

- **Guide**: `docs/05.operations/guides/0014-keycloak.md`
- **Policy**: `docs/05.operations/policies/0014-keycloak.md`
- **Runbook**: `docs/05.operations/runbooks/0014-keycloak.md`
- **Integration**: `docs/05.operations/guides/0079-application-auth-integration.md`
- [문서 인덱스](../../../docs/README.md)
