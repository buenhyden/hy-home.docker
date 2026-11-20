---
title: "Keycloak IAM"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-11-12"
---

# Keycloak IAM

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

관련 구성요소의 현재 선언은 [버전 레지스트리](../../tech-stack.versions.json)가 가리키는 Compose 원본에서 확인합니다. 로컬 빌드의 기준 이미지는 [Dockerfile](Dockerfile)에서 확인합니다.

> `hy-home.docker`의 중앙 ID/접근 관리 제공자입니다.

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

Keycloak은 중앙 IdP다. 사용자 인증, 세션, OIDC/SAML token 발행과
Airflow Authorization Services를 제공한다.

Runtime image: [Keycloak Compose 선언](docker-compose.yml).

Canonical realm:
`hy-home.realm`

###### Audience
<!-- core-payload-level:4 -->

- Infrastructure Operators
- Security Reviewers

###### Scope
<!-- core-payload-level:4 -->

###### In Scope
<!-- core-payload-level:5 -->

- Keycloak runtime 배선
- non-secret 환경 키
- readiness
- OIDC client 통합
- realm role/group/policy 운영 계약

###### Out of Scope
<!-- core-payload-level:5 -->

- credential/token 값
- 애플리케이션 비즈니스 로직
- 애플리케이션 내부 RBAC 구현

###### Structure
<!-- core-payload-level:4 -->

```text
keycloak/
├── docker-compose.yml
└── README.md
```

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| 공개 호스트 `keycloak.${DEFAULT_URL}`(앱 `${KEYCLOAK_PORT:-8080}`) | `keycloak` | OAuth2 Proxy(`home-proxy-client`), Kafbat UI(`home-kafbat`), Airflow(`home-airflow`) | Traefik TLS 뒤 공개 HTTP로 canonical realm `hy-home.realm`의 OIDC/SAML token을 발행한다. | redirect/issuer mismatch를 확인하고 token/secret raw value는 출력하지 않는다. |
| management `${KEYCLOAK_MANAGEMENT_PORT:-9000}/health/ready` | `keycloak` | Prometheus·Gatus와 container healthcheck | `keycloak_management_net`의 `10.250.44.2`(alias `keycloak-management`)에만 bind하는 readiness endpoint다. | DB/readiness를 먼저 확인하고 UP 확인 뒤 의존 서비스를 검증한다. |
| Airflow Authorization Services | `keycloak` | Airflow(`home-airflow`) | realm role `Viewer`·`User`·`Op`·`Admin`·`SuperAdmin`과 scope `GET`~`LIST`를 제공한다. | `invalid_scope`는 Authorization bootstrap을 확인하고 provider 업그레이드 뒤 `create-permissions`를 다시 실행한다. |
| `groups` claim | `keycloak` | Kafbat UI | Kafbat은 `groups` claim의 `/admins`, `/users` 매핑을 사용한다. | Kafbat RBAC mismatch는 `groups` claim과 cluster name을 확인한다. |

###### Application Client Matrix
<!-- core-payload-level:4 -->

| Application | Client ID | Authentication Pattern |
| --- | --- | --- |
| OAuth2 Proxy | `home-proxy-client` | Gateway ForwardAuth |
| Kafbat UI | `home-kafbat` | 애플리케이션 native OAuth2/OIDC |
| Airflow | `home-airflow` | Native Keycloak Auth Manager + Authorization Services |

이 표는 `02-auth` tier 안에서 확인 가능한 client만 담습니다. Open WebUI, Gatus, OpenBao 같은 다른 tier의 native OIDC 통합은 각 서비스의 compose/config가 근거 문서입니다.

###### Configuration
<!-- core-payload-level:4 -->

- `KC_HOSTNAME=keycloak.${DEFAULT_URL}`
- `KC_PROXY_HEADERS=xforwarded`
- PostgreSQL backend
- Traefik TLS 뒤의 공개 HTTP
- `KEYCLOAK_ADMIN_PASSWORD_FILE`: 비어 있으면 `/run/secrets/keycloak_admin_password`, OpenBao 소비 시
  `/run/openbao/auth/keycloak_admin_password.txt`. Agent의 `out/auth`가 읽기 전용으로 bind됩니다.
- `KC_BOOTSTRAP_ADMIN_PASSWORD`는 관리자가 없을 때만 적용됩니다. 파일 경로를 바꿔도 실제 관리자
  비밀번호는 바뀌지 않으며, 전환·되돌리기 절차는
  [OpenBao 소비자 이관 안내](../../03-security/openbao/consumer-migration/README.md)를 따릅니다.

###### Airflow Authorization Contract
<!-- core-payload-level:4 -->

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

###### Kafbat Identity Contract
<!-- core-payload-level:4 -->

Kafbat은 Keycloak `groups` claim을 사용합니다.

현재 애플리케이션 매핑:

- `/admins`
- `/users`

#### Usage

##### Prerequisites

런타임은 `infra/02-auth/keycloak/docker-compose.yml`의 `keycloak` 서비스로 정의되며, 이미지와 태그는 해당 Compose 선언이 소유한다. 활성화 프로파일은 `auth`, `core`, `dev`, `local`이다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

1. Keycloak 운영 guide/policy/runbook을 확인합니다.
2. secret은 Docker Secret을 사용합니다.
3. `/health/ready`가 UP인지 확인한 뒤 의존 서비스를 검증합니다.
4. application client는 canonical realm `hy-home.realm`을 사용합니다.
5. ForwardAuth/Native OIDC 목적을 client별로 구분합니다.
6. realm/client/role 변경 후 해당 application login/RBAC을 검증합니다.

#### Checks

##### Readiness

###### Validation
<!-- core-payload-level:4 -->

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

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

- **Guide**: `docs/05.operations/01.guides/03.identity-and-access/0014-keycloak.md`
- **Policy**: `docs/05.operations/02.policies/03.identity-and-access/0014-keycloak.md`
- **Runbook**: `docs/05.operations/03.runbooks/03.identity-and-access/0014-keycloak.md`
- **Integration**: `docs/05.operations/01.guides/03.identity-and-access/0079-application-auth-integration.md`
- [문서 인덱스](../../../docs/README.md)

###### Service Readiness
<!-- core-payload-level:4 -->

| Field | Evidence |
| --- | --- |
| Service | `keycloak` |
| Image | [Compose 선언](docker-compose.yml) |
| Profiles | `core`, `auth`, `dev` |
| Database | `mng-pg` |
| Network | `edge_net`, `mng_data_net`, `obs_net` |
| Public Host | `keycloak.${DEFAULT_URL}` |
| Listener | 앱 `${KEYCLOAK_PORT:-8080}`, management `${KEYCLOAK_MANAGEMENT_PORT:-9000}` |
| Health | management 포트 `${KEYCLOAK_MANAGEMENT_PORT:-9000}/health/ready`. management listener는 Prometheus·Gatus만 함께 붙는 `keycloak_management_net`의 `10.250.44.2`(alias `keycloak-management`)에만 bind하며, container healthcheck도 그 주소를 씀(SPEC-0267) |
| Secrets | `keycloak_db_password`, `keycloak_admin_password` 또는 OpenBao Agent 출력(`KEYCLOAK_ADMIN_PASSWORD_FILE`) |

###### Troubleshooting
<!-- core-payload-level:4 -->

- DB/readiness 먼저 확인.
- redirect/issuer mismatch를 확인.
- Airflow `invalid_scope`는 Authorization bootstrap을 확인.
- Kafbat RBAC mismatch는 `groups` claim과 cluster name을 확인.
- token/secret raw value는 출력하지 않는다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
