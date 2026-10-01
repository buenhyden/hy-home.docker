---
title: "02-Auth Keycloak Usage Guide"
version: "1.2.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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

- [infra/02-auth/keycloak/docker-compose.yml](../../../infra/02-auth/keycloak/docker-compose.yml)

### Overview

이 문서는 `02-auth`의 Keycloak 운영 구성과 OIDC 발급자 계약을 설명한다. Keycloak의 lifecycle class는 **HOME**이다. DB/관리자 시크릿 주입, hostname/proxy header, health endpoint, OAuth2 Proxy 및 native OIDC client 정합성을 구분한다. 이 문서의 구성값은 tracked source 기준이며, 이 문서의 2026-09-19 확인 범위에서 실측된 것은 OpenBao native OIDC였다. 이후 다른 앱의 날짜별 검증은 [인증 통합 Guide](0079-application-auth-integration.md)가 연결하며, 이번 감사는 로그인 실측을 반복하지 않았다. Keycloak/OAuth2 Proxy 전체 SSO 플로우는 별도 런북 증거가 필요하다.

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

| 항목 | 추적된 값 | 출처 |
| --- | --- | --- |
| 공개 hostname | `keycloak.${DEFAULT_URL}`; 공개 기본 domain은 `hy.home.arpa` | `KC_HOSTNAME`, Traefik host rule |
| Realm | `hy-home.realm` | `.env.example`, OAuth2 Proxy issuer URL |
| Frontend issuer | `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm` | OAuth2 Proxy compose 환경 설정 |
| Container listener | `${KEYCLOAK_PORT:-8080}`에서 HTTP를 활성화하고 앞단에 Traefik TLS를 둠 | `KC_HTTP_ENABLED`, Keycloak compose |
| 관리 health | `${KEYCLOAK_MANAGEMENT_PORT:-9000}`와 `/health/ready` | Keycloak compose healthcheck |
| Proxy header | `KC_PROXY_HEADERS=xforwarded` | Keycloak compose |
| Database | PostgreSQL 주소는 `jdbc:postgresql://mng-pg:${POSTGRES_PORT:-5432}/${KEYCLOAK_DBNAME}` | Keycloak compose |
| 초기 관리자 | 사용자 이름은 `KEYCLOAK_ADMIN_USER`, password는 Docker Secret 파일에서 가져옴 | Keycloak compose; 값을 출력하지 않음 |

공식 Keycloak hostname 문서는 Keycloak이 OIDC discovery와 email/action link에 URL을 게시하므로 hostname이 보안상 민감하다고 설명한다. reverse-proxy 문서는 proxy가 forwarded header를 덮어쓰도록 요구하며, 관리 port `9000`을 외부에 노출하지 말라고 경고한다. 확인 날짜: 2026-09-19.

### OIDC Concepts for This Host

- `issuer`: client가 authorization, token, JWKS와 logout metadata를 탐색하는 정확한 realm URL이다. 이 host에서는 `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`이다.
- `client`: OAuth2 Proxy의 `home-proxy-client`나 OpenBao native OIDC의 `home-openbao`처럼 하나의 application 연동을 나타낸다. client secret은 비밀 정보이며 문서에 담지 않는다.
- `redirect URI`: 인증 후 Keycloak이 허용하는 callback URL이다. OAuth2 Proxy는 `https://auth.${DEFAULT_URL}/oauth2/callback`을 사용한다. OpenBao는 자체 native OIDC callback을 사용하며 OAuth2 Proxy callback과 다르다.
- `gateway SSO`: Traefik/OAuth2 Proxy가 app의 HTTP 진입점을 보호한다. app이 forwarded header를 신뢰하거나 자체 OIDC 연동을 갖춘 경우가 아니라면 app의 native role까지 부여하지는 않는다.
- `native OIDC`: application이 Keycloak에 대해 직접 token을 검증하고 claim을 자체 role에 연결한다. OpenBao native OIDC는 별도로 검증했으며, 그 증거를 모든 app에 일반화하지 않는다.

### Implementation, readiness and resources

`keycloak`은 `core`/`auth`/`dev`/`local`에서 선택하며 Compose는 upstream image를
직접 사용한다. 같은 폴더의 [Dockerfile](../../../infra/02-auth/keycloak/Dockerfile)은
현재 `build`로 선택되지 않아 그 optimized build나 데모 keystore가 실행된다고
볼 수 없다. 실제 entrypoint는 `/bin/sh -ec`로 두 Secret의 개행을 제거해
`KC_BOOTSTRAP_ADMIN_PASSWORD`와 `KC_DB_PASSWORD`에 넣고 `kc.sh start`를 실행한다.
`KC_DB_PASSWORD_FILE` 선언만이 비밀 읽기를 보장하는 것은 아니다.

관리 PostgreSQL 주소는 의존하지만 `depends_on`은 없다. 기동 순서와 DB 준비는
[시스템 Guide](0099-system-operations.md#selection-and-readiness)와
[관리 DB Runbook](../runbooks/0028-management-database.md)을 따른다. Bootstrap
관리자 입력은 초기 관리자 생성용이며 기존 계정의 password 회전 수단으로 보지 않는다.
realm/client를 자동 생성하는 init job이나 startup import도 현재 선언에 없다.

필수 입력은 `KEYCLOAK_DATABASE`, `KEYCLOAK_DBNAME`, `KEYCLOAK_DB_USER`,
`KEYCLOAK_ADMIN_USER`, `DEFAULT_URL`, `DEFAULT_AUTH_DIR`, DB/Admin Secret이다.
`keycloak-{config,providers,themes}`는 각각 host의 conf/providers/themes를 읽기
전용으로 mount한다. private customization도 PostgreSQL 복구 시점과 맞춰 보존해야 한다.
컨테이너에 host port는 없으며 `edge_net`/`mng_data_net`/`obs_net`을 쓴다.
`KEYCLOAK_PORT`/`KEYCLOAK_MANAGEMENT_PORT`는 expose·route·probe 참조이며
현재 KC listener 설정 자체를 바꾸지 않는다. 기본 내부 8080/9000을 바꾸려면
양쪽 계약을 별도 변경해야 한다.

`template-infra-high`의 CPU 2, 메모리 2 GiB를 상속하고 DB pool 최대 연결은 10이다.
health/metrics가 활성화되고 관리 listener에서 readiness/metrics를 관찰한다.
HTTP/cache histogram과 사용자 event metrics, Alloy OTLP tracing도 선언되어 있지만
수집 성공은 별도 증거다. readiness·DB 오류·로그인 거부·메모리/DB 연결 포화를
구분한다. 로그 원문과 사용자·token·cookie 식별자는 증거에 넣지 않는다.

선언 tag에 대응하는 [health 문서](https://raw.githubusercontent.com/keycloak/keycloak/26.7.4/docs/guides/observability/health.adoc)와 <!-- runtime-version-exception: compatibility — official evidence pinned to the declared release; not an installed runtime observation -->
[export/import 문서](https://raw.githubusercontent.com/keycloak/keycloak/26.7.4/docs/guides/server/importExport.adoc)를 <!-- runtime-version-exception: compatibility — official evidence pinned to the declared release; not an installed runtime observation -->
확인했다. release pin은 [Compose](../../../infra/02-auth/keycloak/docker-compose.yml)가
소유하며 현재 실행 버전·provider 호환성·로그인은 다시 측정하지 않았다.

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

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0014-keycloak.md)을 따른다.

권위 상태는 `mng-pg`의 Keycloak DB와 외부 config/provider/theme 입력이다.
realm export는 세션·event 등 전체 상태와 시점 일관성을 보장하는 DB 백업이 아니다.
업그레이드·격리 migration·이전 DB와 이미지의 짝 복구는
[Runbook](../runbooks/0014-keycloak.md#rollback-or-recovery)이 소유한다.
[POL-0021](../policies/0021-backup-and-restore.md)의 Keycloak 파일 보존과 DB
백업 기준을 함께 적용하며 기존 2026-09-20 미실행 복구 한계는 그대로다.

## Traceability

- Declared parent: [02-Auth Keycloak Operations Policy](../policies/0014-keycloak.md) (`POL-0014`)
- Governing authority: [02-Auth Architecture Description](../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Policy](../policies/0014-keycloak.md) (`POL-0014`), [Runbook](../runbooks/0014-keycloak.md) (`RUN-0014`)

## Related Documents

- [Official Keycloak container guide](https://www.keycloak.org/server/containers)
- [Official Keycloak hostname guide](https://www.keycloak.org/server/hostname)
- [Official Keycloak reverse proxy guide](https://www.keycloak.org/server/reverseproxy)
- [Official Keycloak health checks](https://www.keycloak.org/observability/health)
- [Official Keycloak OIDC application guide](https://www.keycloak.org/securing-apps/oidc-layers)
- [Official Keycloak import and export](https://www.keycloak.org/server/importExport)
- [Official Keycloak upgrading guide](https://www.keycloak.org/docs/latest/upgrading/index.html)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0014-keycloak.md)
- [Recovery runbook](../runbooks/0014-keycloak.md)
