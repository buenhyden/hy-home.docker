# OpenSearch Dashboards OIDC 로그인 콜백 401 (Keycloak) 해결 가이드

## TL;DR

증상: `opensearch-dashboards`에서 OIDC 로그인 콜백(`/auth/openid/login`)이 `401 Unauthorized`로 반복 실패.

핵심 원인(복합):

1) OpenSearch Security의 `basic_internal_auth_domain`이 `challenge: true`이면 `Authorization: Bearer <token>` 요청도 BASIC 챌린지로 처리되어 OIDC/JWT 인증 도메인이 정상 동작하지 못할 수 있습니다.
2) OpenSearch Security(OIDC/JWKS 리프레시)가 Keycloak의 OIDC discovery/JWKS를 가져오는 과정에서 **TLS 신뢰(PKIX)** 에 실패하면, OIDC 인증기가 `AuthenticatorUnavailableException`으로 내려가고 최종적으로 401이 발생합니다.

해결은 아래 3가지를 같이 맞추는 것입니다:

- OpenSearch: `basic` 챌린지 비활성화 + OIDC를 먼저 평가(order 조정)
- OpenSearch: Keycloak OIDC endpoint에 대한 TLS 신뢰 설정(`openid_connect_idp.*`)
- Traefik + oauth2-proxy: OpenSearch API는 ForwardAuth SSO로 보호하고 `Authorization`(Bearer)을 백엔드로 전달

---

## 구성(권장 아키텍처)

- **Dashboards(UI)**: OpenSearch Dashboards Security plugin의 **native OIDC** 사용 (Keycloak로 리다이렉트)
- **OpenSearch API**(Traefik 경유): **oauth2-proxy SSO**(ForwardAuth)로 보호 → `Authorization: Bearer ...`를 OpenSearch로 전달 → OpenSearch는 JWT-by-OIDC로 검증

관련 컴포넌트:

- `traefik` (reverse proxy)
- `oauth2-proxy` (ForwardAuth, OIDC client)
- `keycloak` (OIDC provider)
- `opensearch` (Security plugin, JWT-by-OIDC)
- `opensearch-dashboards` (Security plugin, OIDC client)

---

## 증상/로그 상관관계

다음 로그 조합이 같이 보이면, 이 문서의 케이스일 확률이 높습니다.

- `opensearch-dashboards`: `OpenId authentication failed: Error: Authentication Exception` 직후 콜백 401
- `opensearch`: `Authentication finally failed` (과거에는 `WWW-Authenticate: Basic` 포함 401도 흔함)
- `opensearch`: `AuthenticatorUnavailableException ... PKIX path building failed` (Keycloak OIDC URL 호출 시점)

---

## 원인 1) BASIC 챌린지가 Bearer를 가로채는 문제

OpenSearch Security의 `basic_internal_auth_domain.http_authenticator.challenge`가 `true`이면,
Bearer 토큰 요청까지 BASIC 401 챌린지로 처리되어 OIDC/JWT 도메인이 동작하지 못합니다.

### 해결

- `basic_internal_auth_domain.http_authenticator.challenge: false`
- `order` 조정: `openid`가 먼저(0), `basic`가 나중(1)

파일:

- `infra/04-data/opensearch/opensearch/config/opensearch-security/config.yml:12`

---

## 원인 2) OpenSearch가 Keycloak OIDC discovery/JWKS를 TLS(PKIX)로 신뢰하지 못함

OpenSearch Security의 OIDC/JWT 검증은 내부적으로 Keycloak의 OIDC discovery에서 `jwks_uri`를 얻고,
주기적으로 JWKS를 리프레시합니다.

이때 Keycloak이 mkcert/self-signed 등 사설 CA를 쓰고 있고, OpenSearch JVM이 해당 CA를 신뢰하지 못하면:

- `AuthenticatorUnavailableException: Error while getting .../.well-known/openid-configuration`
- `SSLHandshakeException ... PKIX path building failed`

가 발생하며 인증이 최종 401로 떨어집니다.

### 해결(중요)

OIDC IDP 호출 전용 SSL 설정을 `openid_connect_idp` 아래로 명시합니다.

파일:

- `infra/04-data/opensearch/opensearch/config/opensearch-security/config.yml:23`

예시(현재 repo 적용 형태):

```yaml
openid_auth_domain:
  http_authenticator:
    type: openid
    config:
      openid_connect_url: "https://keycloak.127.0.0.1.nip.io/realms/<realm>/.well-known/openid-configuration"
      openid_connect_idp:
        enable_ssl: true
        verify_hostnames: false
        pemtrustedcas_filepath: /usr/share/opensearch/config/certs/rootCA.pem
```

주의:

- `pemtrustedcas_filepath`는 컨테이너 내부 경로 기준으로 작성해야 합니다.
  - 이 구성에서는 `../../../secrets/certs`가 `/usr/share/opensearch/config/certs`로 마운트됩니다.
- `verify_hostnames: false`는 mkcert 기반으로 SAN/hostname 불일치가 있는 환경에서 필요할 수 있습니다(운영에서는 권장하지 않음).

---

## OpenSearch Security 설정 반영(파일만 수정하면 끝이 아닐 수 있음)

OpenSearch Security의 설정은 `.opendistro_security` 인덱스에 적재됩니다.
즉, `config.yml`을 수정해도 **이미 생성된 보안 인덱스에는 자동 반영되지 않을 수** 있습니다.

이 repo는 개발 편의를 위해 REST API로 securityconfig를 수정할 수 있게 허용합니다(dev only):

- `infra/04-data/opensearch/opensearch/config/opensearch.yml:30`
  - `plugins.security.unsupported.restapi.allow_securityconfig_modification: true`

### 권장 절차(dev)

1) 위 설정을 일시적으로 켠 상태에서
2) `/_plugins/_security/api/securityconfig/config`에 `PUT`으로 `dynamic` 설정을 업데이트하고
3) 정상 동작 확인 후, 운영 환경에서는 다시 비활성화하는 것을 권장합니다.

---

## OpenSearch API를 Traefik + oauth2-proxy SSO로 보호(ForwardAuth)

목표: 브라우저에서 `https://opensearch.${DEFAULT_URL}` 접속 시 SSO를 거치고,
최종적으로 OpenSearch 백엔드가 `Authorization: Bearer ...`를 받아 인증/인가합니다.

### Traefik: ForwardAuth 응답 헤더 전달

ForwardAuth가 내려준 `Authorization`/토큰 헤더를 백엔드로 전달해야 합니다.

파일:

- `infra/01-gateway/traefik/dynamic/middleware.yml:15`

키 포인트:

- `sso-auth.forwardAuth.authResponseHeaders`에 `Authorization` 포함
- 필요 시 `X-Auth-Request-Access-Token`, `X-Auth-Request-Id-Token`도 포함

### oauth2-proxy: Authorization 헤더 생성

ForwardAuth 응답에 `Authorization: Bearer <access_token>`를 넣어주도록 설정합니다.

파일:

- `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg:56`
  - `set_authorization_header = true`
  - (`pass_access_token`, `set_xauthrequest`는 함께 사용)

### OpenSearch 라우터: SSO 미들웨어 적용

파일:

- `infra/04-data/opensearch/docker-compose.yml:60`
  - `traefik.http.routers.opensearch.middlewares=sso-auth@file`

---

## 검증 시나리오(최소)

아래는 “문제가 해결되었는지”를 빠르게 확인하는 최소 체크입니다.

### 1) OpenSearch가 Keycloak OIDC discovery를 신뢰하는지

OpenSearch 컨테이너에서:

- CA로 OIDC discovery 호출이 성공해야 함(200 + JSON)
- OpenSearch 로그에 PKIX 에러가 더 이상 발생하지 않아야 함

### 2) OpenSearch가 Bearer 토큰을 받아들이는지

OpenSearch 컨테이너에서, `access_token`을 준비한 뒤:

```bash
curl -ks -H "Authorization: Bearer <access_token>" \
  https://localhost:9200/_plugins/_security/authinfo
```

기대값:

- 200 OK + 사용자 정보(JSON)

### 3) Dashboards OIDC 로그인 플로우가 401 없이 진행되는지

Traefik을 통해 Dashboards의 로그인 엔드포인트를 확인:

- `https://opensearch-dashboard.${DEFAULT_URL}/auth/openid/login` 요청이 Keycloak로 302 되어야 함
- 로그인 후 콜백에서 401이 재발하지 않아야 함

---

## (추가) OIDC 로그인 후 `Missing Role` 페이지가 뜨는 경우

증상:

- Dashboards에서 OIDC 로그인 자체는 성공했지만,
  `Missing Role` / `No roles available for this user` 페이지로 이동함
- Dashboards 로그에서 403이 반복되며, OpenSearch 응답에 아래와 같은 디테일이 보임:
  - `no permissions for [...] and User [name=<user>, backend_roles=[...]]`

원인:

- OpenSearch Security는 JWT 클레임(예: Keycloak `groups`)을 `backend_roles`로 받아도,
  **roles mapping(`rolesmapping`)에서 OpenSearch role에 매핑되지 않으면** 사용 가능한 role이 없어 Missing Role이 뜹니다.
- Keycloak Group Membership mapper 설정에 따라 `groups` 값이 `/admins` 처럼 **슬래시(/) 포함 full path** 로 내려올 수 있는데,
  이 값이 OpenSearch의 `rolesmapping`에 없으면 권한이 0으로 평가됩니다.

### 1) 먼저 “내 backend_roles가 뭔지” 확인

OpenSearch에서 현재 토큰이 어떤 `backend_roles`로 인식되는지 확인합니다:

```bash
curl -ks -H "Authorization: Bearer <access_token>" \
  https://localhost:9200/_plugins/_security/authinfo
```

여기서 `backend_roles` 예시가 `["/admins"]`라면, roles mapping에 **정확히 동일한 문자열(`/admins`)** 이 들어가야 매칭됩니다.

### 2) roles mapping에 Keycloak 그룹을 매핑

개발 환경에서는 아래 API로 즉시 반영 가능합니다.

예: `/admins`(또는 `admins`)를 관리 권한(`all_access`)에 매핑:

```bash
curl -ksu admin:$OPENSEARCH_INITIAL_ADMIN_PASSWORD \
  -H "Content-Type: application/json" \
  -XPUT https://localhost:9200/_plugins/_security/api/rolesmapping/all_access \
  -d '{
    "backend_roles": ["admin","opensearch_admin","opensearch-admin","admins","/admins"],
    "users": ["admin"],
    "hosts": []
  }'
```

캐시 플러시(권장):

```bash
curl -ksu admin:$OPENSEARCH_INITIAL_ADMIN_PASSWORD \
  -XDELETE https://localhost:9200/_plugins/_security/api/cache
```

그 다음 **로그아웃 후 재로그인**(또는 시크릿 창)하면 Missing Role이 해소되어야 합니다.

### 3) Keycloak Mapper 정리(권장)

장기적으로는 Keycloak 쪽 Group Membership mapper에서:

- Token Claim Name: `groups`
- “Full group path”: **OFF**

로 고정하면, OpenSearch roles mapping에서 `/` 변형을 여러 개 넣지 않아도 됩니다.

---

## 보안/운영 주의사항

- `plugins.security.unsupported.restapi.allow_securityconfig_modification: true`는 **개발 편의 옵션**입니다.
  - 운영에서는 비활성화하거나, 접근을 엄격히 제한하세요.
- OpenSearch의 직접 포트 노출(`localhost:9200` 등)은 운영 전 반드시 차단/정책화(방화벽/네트워크 분리)하는 것을 권장합니다.
- 클라이언트 시크릿/패스워드는 문서에 직접 기입하지 말고 `.env` 또는 Secret 관리(Vault 등)로 분리하세요.

---

## 관련 설정 파일(요약)

- OpenSearch Security authc: `infra/04-data/opensearch/opensearch/config/opensearch-security/config.yml:12`
- OpenSearch 설정(dev REST 수정 허용): `infra/04-data/opensearch/opensearch/config/opensearch.yml:30`
- Dashboards OIDC 설정: `infra/04-data/opensearch/opensearch-dashboards/config/opensearch_dashboards.yml:14`
- Traefik ForwardAuth: `infra/01-gateway/traefik/dynamic/middleware.yml:15`
- oauth2-proxy 헤더 설정: `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg:54`
- OpenSearch 라우터 미들웨어: `infra/04-data/opensearch/docker-compose.yml:60`
