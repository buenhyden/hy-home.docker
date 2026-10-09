---
title: "02-Auth OAuth2 Proxy Usage Guide"
version: "1.2.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0015"
parent_ids:
- "POL-0015"
implementation_services:
  infra/02-auth/oauth2-proxy/docker-compose.yml:
  - oauth2-proxy
  - oauth2-proxy-valkey
  - oauth2-proxy-valkey-exporter
created: "2026-05-10"
---

# 02-Auth OAuth2 Proxy Usage Guide

## Overview

이 문서는 OAuth2 Proxy를 Traefik `ForwardAuth` 표준으로 운영하는 방법을 설명한다. `oauth2-proxy`의 lifecycle class는 **HOME**이고, `oauth2-proxy-valkey`와 `oauth2-proxy-valkey-exporter` helper의 class는 **OPTIONAL**이다. Keycloak OIDC provider, redis/Valkey session storage, cookie와 token의 차이, callback/logout 경계를 함께 다룬다. 이 문서의 구성값은 tracked source 기준이며, 이 문서의 2026-09-19 확인 범위에서 실측된 것은 OpenBao native OIDC였다. 이후 다른 앱의 날짜별 검증은 [인증 통합 Guide](0079-application-auth-integration.md)가 연결하며, 이번 감사는 로그인 실측을 반복하지 않았다. OAuth2 Proxy 전체 login/logout acceptance는 별도 런북 증거가 필요하다.

## Audience and Goal

대상은 Infra/DevOps 엔지니어, 운영자, 기여자다. 목적은 세 가지다.

- 인증 프록시를 표준 하드닝 상태로 유지한다.
- 신규 서비스의 gateway SSO 연동 시 issuer, callback, cookie, session 회귀를 줄인다.
- OAuth2 Proxy session logout과 Keycloak SSO logout을 구분한다.

사전 조건은 다음과 같다.

- `infra/02-auth/keycloak` 정상 동작
- `infra/02-auth/oauth2-proxy` 구성 파일 접근
- 공유 `mng-valkey` 또는 `dedicated-valkey` profile의 `oauth2-proxy-valkey` 세션 저장소 준비
- 사용할 저장소에 맞는 `OAUTH2_PROXY_VALKEY_HOST` 및 이미지/entrypoint의 세션 시크릿
  경로 확인. Profile은 서비스를 추가할 뿐 Proxy의 기본 호스트나 이미지를 전환하지 않는다.
  공유 경로는 `dev.Dockerfile`/`docker-entrypoint.dev.sh`의 `mng_valkey_password`,
  전용 경로는 `Dockerfile`/`docker-entrypoint.sh`의 `oauth2_valkey_password`를 사용한다.
  이미지 선택은 기존 `OAUTH2_PROXY_DOCKERFILE` 구성에 따른다.

## Usage

구현 소스는 [infra/02-auth/oauth2-proxy/docker-compose.yml](../../../infra/02-auth/oauth2-proxy/docker-compose.yml)이다. `oauth2-proxy-valkey-exporter`는 OAuth2 session-store metric을 제공하며, 활성화 여부는 작성된 Compose profile을 따른다.

### Build selection and effective startup

Compose build context는 이 패키지의 `.`이며 기본 선택은
[dev.Dockerfile](../../../infra/02-auth/oauth2-proxy/dev.Dockerfile)이다.
build args/target은 없고, upstream OAuth2 Proxy image의 `/bin/oauth2-proxy`만
Alpine 최종 stage로 복사한다. 추가 package 설치는 없다. non-root 계정을 만들고
[dev entrypoint](../../../infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh)를
0555로 복사해 실행한다. Compose가 command를 덮어쓰지 않으므로 스크립트가
`--config /etc/oauth2-proxy.cfg`를 추가한다. 공유 Valkey password는 파일에서
주입하지만 이미 설정된 `OAUTH2_PROXY_REDIS_PASSWORD`가 있으면 보존한다.

`OAUTH2_PROXY_DOCKERFILE=Dockerfile`인 대안은 같은 upstream/Alpine FROM,
UID 100/GID 101과 [전용 entrypoint](../../../infra/02-auth/oauth2-proxy/docker-entrypoint.sh)를
사용해 `oauth2_valkey_password`를 읽는다. private override의 실제 선택은 미확인이다.
어느 선택도 `dedicated-valkey` profile이 자동 변경하지 않는다. 이미지 생성 결과와
설치 버전은 build를 실행하기 전까지 미검증이다.

### Services, inputs and persistence

| 서비스 | 선택·연결·상태·정상 신호 |
| --- | --- |
| `oauth2-proxy` | HOME, `core`/`auth`/`dev`/`local`; `edge_net`, `obs_net`, `mng_data_net`; host port 없음. Keycloak과 선택 Valkey가 필요하지만 `depends_on` 없음. `/ping`은 process, `/ready`는 backend 연결, 인증된 callback/거부는 별도 검사. 내부 metrics 44180은 route하지 않는다. |
| `oauth2-proxy-valkey` | OPTIONAL, `dedicated-valkey`; `mng_data_net`에서 6379, password 인증과 AOF 활성화. bind-backed `/data`는 `${DEFAULT_AUTH_DIR}/valkey`, UID/GID 999. `PONG` health는 연결 검사이며 session 복구 검증이 아니다. |
| `oauth2-proxy-valkey-exporter` | OPTIONAL, 같은 profile; 전용 Valkey healthy를 기다린다. `mng_data_net`과 `obs_net`에서 metrics listener, host port/route/영속 volume 없음. Compose healthcheck가 없으므로 실행 상태와 scrape 성공을 별도로 본다. |

필수 입력은 `OAUTH2_PROXY_CLIENT_ID`, `DEFAULT_URL`, `DEFAULT_CERT_DIR`와
client/cookie Secret, 선택 저장소 password다. 전용 대안은 `DEFAULT_AUTH_DIR`,
`OAUTH2_PROXY_VALKEY_HOST`, Dockerfile 선택, exporter의 `VALKEY_EXPORTER_PORT`를
함께 확인한다. exporter command에는 포트 fallback이 없고 Valkey server는 6379로
고정된다. `VALKEY_PORT`/`OAUTH2_PROXY_PORT`만 변경하면 expose·probe와 실제
listener가 불일치한다. 모든 입력 확인은 값 공개 없이 수행한다.

Proxy의 cfg와 CA는 읽기 전용, 세션은 외부 Valkey가 소유한다. Proxy는 CPU 1/
512 MiB, 두 helper는 각각 CPU 0.5/256 MiB를 공통 template에서 상속한다.
Valkey에 별도 `maxmemory` 선언은 없어 AOF·세션 증가와 OOM·디스크 여유를 함께
본다. exporter는 `redis_up`과 target `UP`을 구분한다. Secret을 password 인자로
전달하는 기존 helper 구현 때문에 전체 process/inspect/health 출력은 수집하지 않는다.
전용 helper의 healthcheck 부재는 공통 health 요구의 구현 한계이며 예외 승인으로
취급하지 않는다. 영속성·삭제·자원 기준은 [Policy](../policies/0015-oauth2-proxy.md)가 소유한다.

공식 [선언 릴리스의 endpoint 문서](https://raw.githubusercontent.com/oauth2-proxy/oauth2-proxy/v7.15.4/docs/docs/features/endpoints.md)와 <!-- runtime-version-exception: compatibility — official evidence pinned to the declared release; not an installed runtime observation -->
[provider 문서](https://raw.githubusercontent.com/oauth2-proxy/oauth2-proxy/v7.15.4/docs/docs/configuration/providers/keycloak_oidc.md), <!-- runtime-version-exception: compatibility — official evidence pinned to the declared release; not an installed runtime observation -->
[exporter 설정](https://raw.githubusercontent.com/oliver006/redis_exporter/v1.91.1/README.md)을 <!-- runtime-version-exception: compatibility — official evidence pinned to the declared release; not an installed runtime observation -->
대조했다. Valkey의 AOF 선언은 backup·HA 보장이 아니다.

### Tracked Configuration Snapshot

| 항목 | 추적된 값 | 출처 |
| --- | --- | --- |
| Provider | `keycloak-oidc` | `config/oauth2-proxy.cfg` |
| Client ID | `home-proxy-client`이며 `OAUTH2_PROXY_CLIENT_ID`에서 가져옴 | `.env.example`, compose 환경 설정 |
| Issuer | `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm` | compose 환경 설정 |
| Redirect URL | `https://auth.${DEFAULT_URL}/oauth2/callback` | compose 환경 설정 |
| Cookie domain | `.${DEFAULT_URL}`; 공개 기본 domain은 `hy.home.arpa` | compose 환경 설정 |
| Cookie 이름 | `__Secure-sso-cookie` | config 파일 |
| Cookie 수명 | refresh `1h`, 만료 `12h` | config 파일 |
| Session store | Valkey에 `redis` protocol로 연결 | compose 환경 설정과 공식 session-storage 문서 |
| Session backend | 기본값은 `mng-valkey`; `dedicated-valkey`는 `oauth2-proxy-valkey`와 해당 exporter만 추가함 | compose 환경 설정/profile |
| Provider CA | `/etc/ssl/certs/rootCA.pem`, `ssl_insecure_skip_verify=false` | compose 환경 설정/config 파일 |
| Callback route | `Host(auth.${DEFAULT_URL}) && PathPrefix(/oauth2)` | Traefik label |

### Cookie, Token, and Session Distinctions

OAuth2 Proxy는 browser cookie로 사용자를 추적한다. `session_store_type=redis`일 때 browser cookie는 짧은 ticket이며, 암호화된 session data는 Redis/Valkey에 저장된다. access, ID, refresh token은 backend session data에 있을 수 있으며 browser cookie와는 다르다. `oauth2_proxy_cookie_secret`을 회전하면 기존 proxy cookie가 무효화된다. Keycloak client secret 회전은 token 교환에, Valkey credential 회전은 session 조회에 영향을 준다. 각각 별개의 incident로 다룬다.

The tracked config requests `openid email profile offline_access groups`, uses PKCE `S256`, passes authorization/access-token headers, and enables `set_xauthrequest`. Proxy 자체의 헤더 생성과 실제 전달은 다르다. 현재 Traefik `sso-auth`는 사용자·이메일·preferred username만 전달하며 Authorization/access token은 전달하지 않는다. gateway SSO는 앱 RBAC를 대신하지 않는다.

### Logout Boundary

공식 OAuth2 Proxy endpoint 문서에 따르면 `/oauth2/sign_out`은 OAuth2 Proxy cookie만 삭제한다. 사용자는 여전히 Keycloak에 로그인된 상태일 수 있으며 즉시 다시 로그인될 수도 있다. Keycloak SSO logout에는 허용된 `rd` 목적지와 일치하는 whitelist 설정을 사용하여 provider end-session endpoint로 redirect하는 과정이 필요하다. 현재 추적되는 설정은 `OAUTH2_PROXY_WHITELIST_DOMAINS=.${DEFAULT_URL}`을 지정하지만, 모든 서비스의 logout 버튼이 Keycloak end-session redirect를 호출한다는 증거는 아니다. 현재 logout이 Keycloak SSO까지 종료한다고 일괄적으로 주장하지 않는다.

### Common Checks

1. Compose 런타임 계약 확인
   - `template-infra-readonly-med` 사용
   - 기본 경로는 `docker-compose.yml`, `dev.Dockerfile`, `docker-entrypoint.dev.sh`, 공유 `mng-valkey`를 사용
   - `dedicated-valkey` profile은 같은 `docker-compose.yml`에서 `oauth2-proxy-valkey`와 그 exporter를 추가로 선택
   - Compose command override는 없고 선택 entrypoint가 기본 `--config /etc/oauth2-proxy.cfg`를 추가하는지 확인
   - `OAUTH2_PROXY_OIDC_ISSUER_URL`, `OAUTH2_PROXY_REDIRECT_URL`, `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS` 확인
2. 엔트리포인트 시크릿 주입 확인
   - root-active `docker-entrypoint.dev.sh`에서 `mng_valkey_password`를 읽어 환경 변수에 export하는지 확인
   - local/full `docker-entrypoint.sh`에서 `oauth2_valkey_password`를 읽어 환경 변수에 export하는지 확인
3. 이미지 권한 모델 확인
   - local/full `Dockerfile`에서 UID 100/GID 101을 명시적으로 생성하고 `USER 100:101`을 적용하는지 확인
   - root-active `dev.Dockerfile`에서 `USER oauth2proxy:oauth2proxy`를 적용하는지 확인
4. 정적 검증
   - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/hardening/check-all-hardening.sh 02-auth`

### Pitfalls

- `DEFAULT_URL`, Keycloak realm issuer, OAuth2 Proxy callback 도메인 불일치
- `ssl_insecure_skip_verify=false` 상태에서 root CA mount가 깨져 discovery/JWKS fetch가 실패하는 경우
- 세션 비밀 변경 후 기존 쿠키 재사용으로 인한 인증 실패
- `/ping`은 process health이고 `/ready`는 Redis 등 backend 연결까지 본다는 차이를 놓치는 경우
- `/oauth2/sign_out`을 Keycloak SSO 종료로 오해하는 경우
- `trusted_ips` 또는 `trusted_proxy_ips`를 넓게 두고 forwarded header spoofing 위험을 검토하지 않는 경우

프로세스 인자로 전달되는 Valkey credential의 증거 취급 기준은 [Policy](../policies/0015-oauth2-proxy.md#rules)가 소유한다.

검증 명령 모음은 다음과 같다.

- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 02-auth`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0015-oauth2-proxy.md)을 따른다.

Valkey 세션과 cookie/client/저장소 자격 증명은 서로 다른 복구 입력이다.
세션 손실은 업무 DB 복구 대신 명시적 재로그인이 기본이며, 기존 2026-09-20 미실행
복구 한계는 [Runbook](../runbooks/0015-oauth2-proxy.md#rollback-or-recovery)에 남긴다.
이미지 변경·PKCE·logout·session 만료 검증과 helper 기동/중지는 같은 Runbook이 소유한다.

### Traceability

- Declared parent: [02-Auth OAuth2 Proxy Operations Policy](../policies/0015-oauth2-proxy.md) (`POL-0015`)
- Governing authority: [02-Auth Architecture Description](../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Policy](../policies/0015-oauth2-proxy.md) (`POL-0015`), [Runbook](../runbooks/0015-oauth2-proxy.md) (`RUN-0015`)

## Related Documents

- [Official OAuth2 Proxy Keycloak OIDC provider](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc/)
- [Official OAuth2 Proxy configuration overview](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview/)
- [Official OAuth2 Proxy session storage](https://oauth2-proxy.github.io/oauth2-proxy/configuration/session_storage/)
- [Official OAuth2 Proxy endpoints](https://oauth2-proxy.github.io/oauth2-proxy/features/endpoints/)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0015-oauth2-proxy.md)
- [Recovery runbook](../runbooks/0015-oauth2-proxy.md)
