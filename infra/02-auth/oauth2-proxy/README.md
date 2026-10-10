---
title: "OAuth2 Proxy"
version: "1.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2025-11-29"
---

# OAuth2 Proxy

> 승인된 애플리케이션 native OIDC를 사용하지 않는 서비스를 위한 OIDC ForwardAuth 게이트웨이입니다.

## Overview

OAuth2 Proxy는 적절한 내장 OIDC 지원이 없는 서비스에 게이트웨이 인증을 제공합니다.
OIDC에는 Keycloak을, 세션 상태에는 Valkey를 사용합니다.

OAuth2 Proxy는 모든 보호 대상 서브도메인의 필수 hop이 **아닙니다**.
Airflow와 Kafbat UI는 애플리케이션 native OIDC를 사용하며 OAuth2 Proxy
ForwardAuth로 보호되지 않습니다.

## Audience

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- OAuth2 Proxy 설정
- Traefik ForwardAuth
- Valkey 세션
- secret 주입
- cookie/issuer/redirect 계약

### Out of Scope

- Keycloak identity 관리
- Native OIDC 애플리케이션 RBAC
- TLS 인증서 발급

## Structure

```text
oauth2-proxy/
├── config/
├── Dockerfile
├── dev.Dockerfile
├── docker-entrypoint.sh
├── docker-entrypoint.dev.sh
├── docker-compose.yml
└── README.md
```

## Authentication Applicability

ForwardAuth 대상:

- Flower
- n8n
- 자체 OIDC가 없는 서비스

Native OIDC 대상:

- Airflow
- Kafbat UI

Native OIDC app에는 `sso-auth@file`/`sso-errors@file`을 중복 적용하지 않는다.

## Service Readiness

| Field | Evidence |
| --- | --- |
| Service | `oauth2-proxy` |
| Session | 기본값은 공유 `mng-valkey` |
| Dedicated session | `dedicated-valkey` 아래의 `oauth2-proxy-valkey` |
| Health | `/ping` |
| OIDC client | `home-proxy-client` |
| Issuer | `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm` |

## Usage

1. Auth Operations와 integration guide를 먼저 확인.
2. new service onboarding 시 ForwardAuth vs Native OIDC를 먼저 분류.
3. ForwardAuth 대상에만 OAuth2 Proxy middleware 적용.
4. cookie/client/session secret 변경 영향 확인.
5. `Authorization` header forwarding은 upstream JWT scheme과 충돌 여부 검증.
6. callback URL을 재사용하지 않는다.

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Proxy | OAuth2 Proxy | ForwardAuth |
| Session | Valkey | Redis 호환 |
| Protocol | OIDC | Keycloak |
| Gateway | Traefik | ForwardAuth 호출자 |

## Secrets

- `oauth2_proxy_cookie_secret`
- `oauth2_proxy_client_secret`
- shared/dedicated Valkey secret

## Testing

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth
docker compose --profile auth exec oauth2-proxy   wget -qO- http://127.0.0.1:4180/ping
```

## Troubleshooting

- issuer/redirect/cookie domain
- Valkey connectivity
- ForwardAuth middleware route
- Native OIDC app에 중복 적용 여부
- upstream `Authorization` collision

## Related Documents

- [Keycloak](../keycloak/README.md)
- [Gateway](../../01-gateway/README.md)
- OAuth2 Proxy 운영 문서: `docs/05.operations/guides/0015-oauth2-proxy.md`, `docs/05.operations/policies/0015-oauth2-proxy.md`, `docs/05.operations/runbooks/0015-oauth2-proxy.md`
- 애플리케이션 인증 통합 가이드: `docs/05.operations/guides/0079-application-auth-integration.md`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../tech-stack.versions.json)은 drift 검증을 제공합니다.

빌드 소스 권한: [Dockerfile](Dockerfile), [dev.Dockerfile](dev.Dockerfile).

## SEC01 7.15.5 후보와 검증 경계

upstream 바이너리 단계는 `v7.15.5`와 공개 OCI index digest
`sha256:8498b0d0ef0a7b29686414000a08aee467f02d0299c9ed1e006a8f33fc017916`로 고정한다.
Compose의 기본 빌드 경로 `dev.Dockerfile`과 명시적 `Dockerfile` override 모두 같은
바이너리 digest를 사용한다. 기본 경로의 `oauth2proxy:oauth2proxy`·dev wrapper 및
override 경로의 `100:101`·운영 wrapper, 각 Valkey secret 경로와 기본 실행 인수는 유지한다.
[공식 릴리스](https://github.com/oauth2-proxy/oauth2-proxy/releases/tag/v7.15.5)의
경로 예외·클라이언트 IP 신뢰 경계 보안 변경에 대해 현재 Keycloak provider,
정확한 Traefik `trusted_proxy_ips`, 인증 생략 IP/경로 미설정을 소스에서 확인한다.

소스 계약 및 합성 wrapper 시험은 실제 OIDC 인증·쿠키·ForwardAuth 증거가 아니다.
이미지 build, native 설정 검증, Traefik을 통한 정상/비정상 경로 인증과 기존 쿠키
갱신 시험은 `NOT_RUN`이다. 운영 반영 전에 동일 이미지의 기능 시험과 기존 이미지로
되돌리는 인수 조건을 SPEC-0204-TSK-0009에서 충족해야 한다.
