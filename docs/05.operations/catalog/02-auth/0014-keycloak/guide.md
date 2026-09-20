---
title: "02-Auth Keycloak Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0014"
parent_ids:
- "POL-0014"
implementation_services:
  infra/02-auth/keycloak/docker-compose.yml:
  - keycloak
created: "2026-05-10"
---

# 02-Auth Keycloak Usage Guide

## Usage

### Implementation Sources

- [infra/02-auth/keycloak/docker-compose.yml](../../../../../infra/02-auth/keycloak/docker-compose.yml)

### Overview

이 문서는 `02-auth`의 Keycloak 운영 구성과 OIDC 발급자 계약을 설명한다. Keycloak의 lifecycle class는 **HOME**이다. DB/관리자 시크릿 주입, hostname/proxy header, health endpoint, OAuth2 Proxy 및 native OIDC client 정합성을 구분한다. 이 문서의 구성값은 tracked source 기준이며, 현재 실측으로 완료된 OIDC 로그인은 OpenBao native OIDC뿐이다. Keycloak/OAuth2 Proxy 전체 SSO 플로우는 별도 런북 증거가 필요하다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

### Purpose

- Keycloak의 issuer, redirect URI, proxy header, health 계약을 안정적으로 유지한다.
- OAuth2 Proxy ForwardAuth와 application native OIDC client를 혼동하지 않는다.
- 로그인, 로그아웃, token/session 장애의 진단 기준을 공식 Keycloak 동작과 tracked config에 맞춘다.

### Tracked Configuration Snapshot

| Item | Tracked value | Source |
| --- | --- | --- |
| Public hostname | `keycloak.${DEFAULT_URL}`; public default domain is `hy.home.arpa` | `KC_HOSTNAME`, Traefik host rule |
| Realm | `hy-home.realm` | `.env.example`, OAuth2 Proxy issuer URL |
| Frontend issuer | `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm` | OAuth2 Proxy compose env |
| Container listener | HTTP enabled on `${KEYCLOAK_PORT:-8080}` behind Traefik TLS | `KC_HTTP_ENABLED`, Keycloak compose |
| Management health | `${KEYCLOAK_MANAGEMENT_PORT:-9000}` and `/health/ready` | Keycloak compose healthcheck |
| Proxy headers | `KC_PROXY_HEADERS=xforwarded` | Keycloak compose |
| Database | PostgreSQL at `jdbc:postgresql://mng-pg:${POSTGRES_PORT:-5432}/${KEYCLOAK_DBNAME}` | Keycloak compose |
| Bootstrap admin | username from `KEYCLOAK_ADMIN_USER`, password from Docker Secret file | Keycloak compose; do not print value |

Official Keycloak hostname docs state that hostname is security-sensitive because Keycloak publishes URLs through OIDC discovery and email/action links. Reverse-proxy docs require the proxy to overwrite forwarded headers, and warn not to expose management port `9000` externally. Verification date: 2026-09-19.

### OIDC Concepts for This Host

- `issuer`: the exact realm URL that clients use to discover authorization, token, JWKS and logout metadata. For this host it is `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`.
- `client`: one application integration, such as `home-proxy-client` for OAuth2 Proxy or `home-openbao` for OpenBao native OIDC. Client secrets are secret material and are not document content.
- `redirect URI`: the callback URL Keycloak allows after authentication. OAuth2 Proxy uses `https://auth.${DEFAULT_URL}/oauth2/callback`; OpenBao uses its own native OIDC callback and is not the OAuth2 Proxy callback.
- `gateway SSO`: Traefik/OAuth2 Proxy protects HTTP entry to an app. It does not grant the app's native roles unless the app trusts forwarded headers or has its own OIDC integration.
- `native OIDC`: the application validates tokens directly against Keycloak and maps claims to its own roles. OpenBao native OIDC has been verified separately; do not generalize that proof to every app.

### Step-by-step Instructions

1. Compose 설정 확인
   - `template-infra-high` 적용 여부 확인
   - `KC_DB_PASSWORD_FILE`, `keycloak_db_password`, `keycloak_admin_password` 연결 확인
   - `KC_HOSTNAME=keycloak.${DEFAULT_URL}`, `KC_HTTP_ENABLED=true`, `KC_PROXY_HEADERS=xforwarded` 확인
2. hostname/proxy 계약 확인
   - Traefik이 `https://keycloak.${DEFAULT_URL}`로 TLS를 종료하고 Keycloak에는 HTTP `8080`으로 전달하는지 확인
   - `X-Forwarded-*` 헤더가 proxy에서 overwrite되는지 확인한다. Client가 직접 Keycloak container에 접근해 forged header를 보낼 수 있으면 안 된다.
   - management port `9000`은 외부 proxy 대상이 아니다.
3. OIDC client 정합 확인
   - OAuth2 Proxy client `home-proxy-client`의 Valid Redirect URI가 `https://auth.${DEFAULT_URL}/oauth2/callback`과 일치해야 한다.
   - OpenBao client `home-openbao`는 OpenBao native OIDC callback을 사용하며 OAuth2 Proxy callback과 다르다.
   - PKCE를 쓰는 client는 해당 client의 flow와 redirect URI가 서로 맞아야 한다.
4. 헬스체크 계약 확인
   - readiness는 management port `/health/ready`에서 확인한다.
   - readiness success는 DB와 Keycloak process readiness 신호이며 application login acceptance 증거가 아니다.
5. 정적 검증
   - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/hardening/check-all-hardening.sh 02-auth`

### Common Pitfalls

- `KC_HOSTNAME`, OAuth2 Proxy issuer, Keycloak realm frontend URL이 서로 다른 host/scheme를 가리키는 경우
- reverse proxy가 `X-Forwarded-*`를 append만 하고 overwrite하지 않아 forged issuer/redirect 문제가 생기는 경우
- management port `9000`을 외부 route에 붙이는 경우
- OAuth2 Proxy logout을 Keycloak SSO logout으로 오해하는 경우
- CA trust가 깨져 OAuth2 Proxy가 issuer/JWKS를 가져오지 못하는 경우
- OpenBao native OIDC 검증 성공을 다른 client의 login 검증으로 확대하는 경우

## Common Checks

- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 02-auth`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

### Data Protection and Upgrade

Keycloak의 권위 상태는 외부 `mng-pg` PostgreSQL 데이터베이스에 있다. realm
export는 검토 가능한 설정 이관 자료지만 트랜잭션 시점 복구를 대신하지 않는다.
공식 export/import는 모든 노드를 중지한 상태를 권장하고, override import와
startup import의 동작도 다르므로 실행 중인 단일 컨테이너 export를 일관된
백업으로 기록하지 않는다. 복구 세트에는 PostgreSQL 백업, 동일 Keycloak 이미지
선언, realm/export 보조 자료, secret owner가 별도 보관한 자격 증명이 포함된다.

업그레이드는 공식 upgrading guide와 migration notes를 검토하고, 먼저 PostgreSQL
백업을 검증한 뒤 격리 복제본에서 schema migration, readiness, 관리자 로그인,
OAuth2 Proxy 및 대표 native OIDC client를 확인한다. rollback은 이전 이미지와
업그레이드 전 데이터베이스를 함께 복원해야 하며 새 schema에 이전 이미지만
연결하지 않는다. 이 백업·복구 rehearsal은 2026-09-20 문서 교정 중 실행되지 않았다.

## Traceability

- Declared parent: [02-Auth Keycloak Operations Policy](policy.md) (`POL-0014`)
- Governing authority: [02-Auth Architecture Description](../../../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Policy](policy.md) (`POL-0014`), [Runbook](runbook.md) (`RUN-0014`)

## Related Documents

- [Official Keycloak container guide](https://www.keycloak.org/server/containers)
- [Official Keycloak hostname guide](https://www.keycloak.org/server/hostname)
- [Official Keycloak reverse proxy guide](https://www.keycloak.org/server/reverseproxy)
- [Official Keycloak health checks](https://www.keycloak.org/observability/health)
- [Official Keycloak OIDC application guide](https://www.keycloak.org/securing-apps/oidc-layers)
- [Official Keycloak import and export](https://www.keycloak.org/server/importExport)
- [Official Keycloak upgrading guide](https://www.keycloak.org/docs/latest/upgrading/index.html)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
