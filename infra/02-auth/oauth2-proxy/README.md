---
title: "OAuth2 Proxy"
version: "1.1.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-26"
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

### SEC01 후보와 검증 경계

upstream 바이너리 태그와 공개 OCI index digest는 [Dockerfile](Dockerfile)과
[dev.Dockerfile](dev.Dockerfile)이 소유한다. Compose의 기본 빌드 경로와 명시적
운영 Dockerfile override는 같은 바이너리 digest를 사용한다. 기본 경로의
`oauth2proxy:oauth2proxy`·dev wrapper 및 override 경로의 `100:101`·운영 wrapper,
각 Valkey secret 경로와 기본 실행 인수는 유지한다.
[공식 릴리스](https://github.com/oauth2-proxy/oauth2-proxy/releases)의
경로 예외·클라이언트 IP 신뢰 경계 보안 변경에 대해 현재 Keycloak provider,
정확한 Traefik `trusted_proxy_ips`, 인증 생략 IP/경로 미설정을 소스에서 확인한다.

소스 계약 및 합성 wrapper 시험은 실제 OIDC 인증·쿠키·ForwardAuth 증거가 아니다.
이미지 build, native 설정 검증, Traefik을 통한 정상/비정상 경로 인증과 기존 쿠키
갱신 시험은 `NOT_RUN`이다. 운영 반영 전에 동일 이미지의 기능 시험과 기존 이미지로
되돌리는 인수 조건을 SPEC-0204-TSK-0009에서 충족해야 한다.

### Authentication Applicability

ForwardAuth 대상:

- Flower
- n8n
- 자체 OIDC가 없는 서비스

Native OIDC 대상:

- Airflow
- Kafbat UI

Native OIDC app에는 `sso-auth@file`/`sso-errors@file`을 중복 적용하지 않는다.

### Secrets

- `oauth2_proxy_cookie_secret`
- `oauth2_proxy_client_secret`
- shared/dedicated Valkey secret

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Proxy | OAuth2 Proxy | ForwardAuth |
| Session | Valkey | Redis 호환 |
| Protocol | OIDC | Keycloak |
| Gateway | Traefik | ForwardAuth 호출자 |

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

### 선택형 전용 Valkey 관측 계정

기본 `dedicated-valkey` 설정의 exporter는 여전히 기본 애플리케이션 비밀번호와
관리 권한을 공유합니다. 별도 계정을 준비한 뒤 루트에서
루트 파일 뒤에 Airflow, n8n, OAuth2 Proxy의 `docker-compose.monitor-acl.yml`을
각각 `-f`로 명시하면 세 전용 broker/exporter 쌍에만 최소 관측 ACL을 적용합니다.
서비스별 `monitor_password.txt` 파일 경로는 루트 Secret 선언과 공개 카탈로그가
소유합니다. 기존 기본 계정·앱 비밀번호·네트워크·AOF는 유지하며, 선택형 경로에서는
exporter가 자기 관측 파일만 마운트하고 비밀번호를 명령 인자로 넘기지 않습니다.
이 overlay 조합만으로 앱의 shared/dedicated endpoint 선택이 바뀌지는 않습니다.

관측 계정은 PING, INFO, COMMAND INFO, SLOWLOG LEN, COMMANDLOG LEN만 허용합니다.
키·채널·Lua·관리 명령은 허용하지 않으며 INFO의 전체 DB 집계 노출은 남습니다.
exporter의 선택적 SLOWLOG GET 거부는 상세 지표 부재로 기록하고 권한을 넓혀
없애지 않습니다. `/scrape`는 비활성화하고 기존 Prometheus `/metrics`를 유지합니다.
관측 파일은 의도한 UID/보조 GID가 읽을 수 있는 안전한 단일 파일이어야 하고,
broker는 자신의 기본/관측 비밀번호가 같은 경우 시작을 거부합니다. 서로 다른
서비스 간 비밀번호 분리·회전은 별도 운영 인수입니다.

공개 합성 렌더링과 ACL 파일 검사는 실제 채택·수집·앱 queue/session·AOF·회전·복구를
대신하지 않습니다. 실제 실행은 고정 이미지·정확한 대상·정리/복구 경계 검토 후
분리 검증합니다. 직접 대상과 companion 선택은 POL-0078이 소유합니다.

## Related Documents

- [Keycloak](../keycloak/README.md)
- [Gateway](../../01-gateway/README.md)
- OAuth2 Proxy 운영 문서: `docs/05.operations/guides/0015-oauth2-proxy.md`, `docs/05.operations/policies/0015-oauth2-proxy.md`, `docs/05.operations/runbooks/0015-oauth2-proxy.md`
- 애플리케이션 인증 통합 가이드: `docs/05.operations/guides/0079-application-auth-integration.md`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../tech-stack.versions.json)은 drift 검증을 제공합니다.

빌드 소스 권한: [Dockerfile](Dockerfile), [dev.Dockerfile](dev.Dockerfile).
