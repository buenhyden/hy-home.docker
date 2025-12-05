# Keycloak (통합 인증 시스템)

## 시스템 아키텍처에서의 역할

Keycloak은 **SSO(Single Sign-On) 및 신원/접근 관리(IAM)** 플랫폼으로 모든 인프라 서비스의 중앙 인증을 담당합니다.

**핵심 역할:**

- 🔐 **SSO**: 단일 로그인으로 모든 서비스 접근
- 👤 **사용자 관리**: 중앙화된 계정 관리
- 🎫 **OAuth2/OIDC**: 표준 프로토콜 지원
- 👥 **RBAC**: 역할 기반 접근 제어

## 주요 구성 요소

### 1. Keycloak

- **컨테이너**: `keycloak`
- **이미지**: `quay.io/keycloak/keycloak:26.4.6`
- **포트**: 8080 (내부)
- **Traefik**: `https://keycloak.${DEFAULT_URL}`
- **모드**: `start-dev` (개발 모드)

**데이터베이스:**

- PostgreSQL (mng-pg)
- Database: `${KEYCLOAK_DBNAME}`

### 2. MailHog (개발용)

- 이메일 인증 테스트용
- `https://mail.${DEFAULT_URL}`

## 환경 변수

```bash
KEYCLOAK_DATABASE=postgres
POSTGRES_HOSTNAME=mng-pg
POSTGRES_PORT=5432
KEYCLOAK_DBNAME=keycloak
KEYCLOAK_DB_USER=keycloak
KEYCLOAK_DB_PASSWORD=<password>
KEYCLOAK_ADMIN_USER=admin
KEYCLOAK_ADMIN_PASSWORD=<password>
DEFAULT_URL=127.0.0.1.nip.io
MAILHOG_UI_PORT=8025
```

## 접속 정보

### Admin Console

- **URL**: `https://keycloak.127.0.0.1.nip.io/admin`
- **계정**: admin / password

## 주요 설정

### 1. Realm 생성

1. Admin Console 접속
2. Realms → Create Realm
3. Name: `hy-home.realm`

### 2. Client 생성 (OAuth2)

```
Client ID: nginx-client
Client Protocol: openid-connect
Access Type: confidential
Valid Redirect URIs: https://auth.127.0.0.1.nip.io/oauth2/callback
```

### 3. 사용자 생성

Users → Add User → Set Password

### 4. 그룹 및 역할

Groups → Create Group:

- `/admins`: 관리자
- `/editors`: 편집자
- `/viewers`: 뷰어

## 서비스 통합

### Grafana 연동

```bash
GF_AUTH_GENERIC_OAUTH_ENABLED=true
GF_AUTH_GENERIC_OAUTH_CLIENT_ID=nginx-client
GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET=<secret>
GF_AUTH_GENERIC_OAUTH_AUTH_URL=https://keycloak.127.0.0.1.nip.io/realms/hy-home.realm/protocol/openid-connect/auth
```

### OAuth2-Proxy 연동

```bash
OAUTH2_PROXY_PROVIDER=keycloak-oidc
OAUTH2_PROXY_OIDC_ISSUER_URL=https://keycloak.127.0.0.1.nip.io/realms/hy-home.realm
```

## 참고 자료

- [Keycloak 문서](https://www.keycloak.org/documentation)
- [Admin Guide](https://www.keycloak.org/docs/latest/server_admin/)
