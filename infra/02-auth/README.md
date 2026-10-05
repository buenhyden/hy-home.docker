---
title: "Auth Tier (02-auth)"
version: "1.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-12"
---

# Auth Tier (02-auth)

> ID/접근 관리, Gateway ForwardAuth, 애플리케이션 native OIDC 통합.

## Overview

`02-auth` tier는 `hy-home.docker` 생태계의 보안 기반을 맡습니다. Keycloak은 중앙
Identity Provider입니다. OAuth2 Proxy는 적절한 내장 OIDC가 없는 서비스에 Gateway
ForwardAuth를 제공하며 Airflow, Kafbat UI, Open WebUI, Gatus, OpenBao 같은 승인된
애플리케이션은 애플리케이션 native OIDC로 Keycloak에 직접 인증합니다.

## Audience

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- Keycloak: IAM 제공자
- OAuth2 Proxy: ForwardAuth 게이트웨이
- ForwardAuth vs Native OIDC 선택
- OIDC client 통합
- PostgreSQL identity 영속성
- OAuth2 Proxy용 Valkey 세션 저장

### Out of Scope

- TLS 종료(`01-gateway`)
- 네트워크 방화벽
- 애플리케이션 비즈니스 로직
- 애플리케이션 내부 RBAC 구현 세부 사항

## Structure

```text
02-auth/
├── keycloak/
├── oauth2-proxy/
└── README.md
```

## Authentication Patterns

### Gateway ForwardAuth

```text
Browser -> Traefik -> OAuth2 Proxy -> Keycloak -> Service
```

현재 예:

- Flower
- n8n
- 자체 OIDC가 없는 내부 UI

### Application-native OIDC

```text
Browser -> Traefik -> Application -> Keycloak
```

현재:

- Airflow
- Kafbat UI
- Open WebUI
- Gatus
- OpenBao

Native OIDC 서비스 앞에 OAuth2 Proxy ForwardAuth를 기본적으로 중복 적용하지 않는다.

## Usage

1. [Auth Operations](../../docs/README.md)를 먼저 확인한다.
2. Keycloak/OAuth2 Proxy compose/config를 변경하기 전에 guide/policy/runbook을 확인한다.
3. 신규 서비스를 `Gateway ForwardAuth` 또는 `Application-native OIDC`로 분류한다.
4. 승인된 Native OIDC 서비스 앞에 OAuth2 Proxy ForwardAuth를 중복 적용하지 않는다.
5. secret은 `scripts/operations/gen-secrets.sh`와 Docker Secret 경계를 사용한다.
6. root profile validation/hardening을 실행한다.

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| IAM | Keycloak | 중앙 OIDC/SAML IdP |
| ForwardAuth | OAuth2 Proxy | Gateway 인증 |
| Native OIDC | Airflow, Kafbat UI, Open WebUI, Gatus, OpenBao | Keycloak 직접 client |
| Database | PostgreSQL | Identity 영속성 |
| Session | Valkey | OAuth2 Proxy 세션 |
| Gateway | Traefik | TLS/라우팅/미들웨어 |

## Configuration

| Variable | Required | Description |
| --- | ---: | --- |
| `DEFAULT_URL` | Yes | 루트 도메인 |
| `KEYCLOAK_REALM` | Yes | `hy-home.realm` |
| `KEYCLOAK_URL` | Yes | 공개 Keycloak URL |
| `OAUTH2_PROXY_CLIENT_ID` | Yes | ForwardAuth client |
| `KAFBAT_OAUTH_CLIENT_ID` | Yes | Kafbat Native OIDC client |
| `AIRFLOW_KEYCLOAK_CLIENT_ID` | Yes | Airflow Native OIDC client |

## Testing

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth
```

런타임:

```bash
docker compose --profile auth exec keycloak sh -c   'exec 3<>/dev/tcp/127.0.0.1/9000; printf "GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n" >&3; cat <&3'
docker compose --profile auth exec oauth2-proxy   wget -qO- http://127.0.0.1:4180/ping
```

## Change Impact

- Keycloak realm/client 변경은 여러 application에 영향.
- OAuth2 Proxy 변경은 ForwardAuth target에 영향.
- Native OIDC client 변경은 해당 application login/RBAC에 영향.
- secret rotation은 session/client 재로그인을 요구할 수 있다.

## Related Documents

- [Gateway](../01-gateway/README.md)
- [Data](../04-data/README.md)
- Keycloak 운영 문서: `docs/05.operations/guides/0014-keycloak.md`, `docs/05.operations/policies/0014-keycloak.md`, `docs/05.operations/runbooks/0014-keycloak.md`
- OAuth2 Proxy 운영 문서: `docs/05.operations/guides/0015-oauth2-proxy.md`, `docs/05.operations/policies/0015-oauth2-proxy.md`, `docs/05.operations/runbooks/0015-oauth2-proxy.md`
- 애플리케이션 인증 통합 가이드: `docs/05.operations/guides/0079-application-auth-integration.md`
- [문서 인덱스](../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../tech-stack.versions.json)은 drift 검증을 제공합니다.
