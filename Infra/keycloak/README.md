# Keycloak

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: Keycloak은 오픈소스 자격 증명 및 접근 관리(IAM) 솔루션입니다. 현대적인 애플리케이션과 서비스를 위한 SSO(Single Sign-On), ID 중개, 사용자 연동 기능을 제공합니다.

**주요 기능 (Key Features)**:
- **Single Sign-On (SSO)**: 한 번의 로그인으로 여러 서비스 이용 가능.
- **Identity Brokering**: Google, GitHub 등 소셜 로그인 지원.
- **User Federation**: LDAP/Active Directory 연동.
- **Admin Console**: 웹 기반의 강력한 관리 콘솔 제공.

**기술 스택 (Tech Stack)**:
- **Image**: `quay.io/keycloak/keycloak:26.4.6`
- **Database**: PostgreSQL 17
- **Runtime**: Quarkus (Java)

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**시스템 구조도**:
```mermaid
graph TD
    User[사용자] -->|Login| Keycloak
    Keycloak -->|SQL| Postgres[DB (Mng-pg)]
    App[애플리케이션] -->|OIDC Check| Keycloak
```

**데이터 흐름 (Data Flow)**:
1. 사용자가 앱 접근 시도
2. 앱이 로그인 페이지로 리다이렉트 (Keycloak)
3. 사용자 인증 (ID/PW)
4. Keycloak이 인증 토큰(JWT) 발급
5. 앱이 토큰 검증 후 접근 허용

**의존성 (Dependencies)**:
- **PostgreSQL**: 사용자 정보 및 설정 저장소.

## 3. 시작 가이드 (Getting Started)
**사전 요구사항 (Prerequisites)**:
- PostgreSQL 데이터베이스 준비 완료 (`mng-pg`)

**실행 방법 (Deployment)**:
```bash
docker compose up -d
```

**초기 설정 (Initial Setup)**:
- 최초 실행 시 `admin` 계정으로 로그인하여 Realm, Client 설정을 진행해야 합니다.
- (상세 설정 가이드는 하단 참조)

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수 (Environment Variables)**:

| 변수명 | 설명 |
|---|---|
| `KEYCLOAK_ADMIN` | 초기 관리자 ID |
| `KEYCLOAK_ADMIN_PASSWORD` | 초기 관리자 비밀번호 |
| `KC_DB` | 데이터베이스 공급자 (`postgres`) |
| `KC_DB_URL` | DB 접속 URL (`jdbc:postgresql://...`) |
| `KC_DB_USERNAME` | DB 사용자명 |
| `KC_DB_PASSWORD` | DB 비밀번호 |
| `KC_HOSTNAME` | 외부 접속 URL (`https://keycloak.${DEFAULT_URL}`) |

**네트워크 포트 (Network Ports)**:
- **Internal**: 8080 (HTTP)
- **Internal**: 9000 (Management)

## 5. 통합 및 API 가이드 (Integration Guide)
**인증 및 인가 (Auth Strategy)**:
- OpenID Connect (OIDC) 및 SAML 2.0 표준을 사용합니다.
- OAuth2 Proxy를 통해 리버스 프록시 레벨에서 인증을 처리할 수 있습니다.

**엔드포인트 명세**:
- `/realms/{realm}/protocol/openid-connect/auth`: 인증 요청
- `/realms/{realm}/protocol/openid-connect/token`: 토큰 발급/갱신
- `/admin`: 관리자 콘솔

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인 (Health Check)**:
- Keycloak 자체 헬스체크 기능(`KC_HEALTH_ENABLED=true`) 사용.
- `/health` 엔드포인트 제공.

**모니터링 (Monitoring)**:
- `KC_METRICS_ENABLED=true` 설정으로 메트릭 수집 가능.

**로그 관리 (Logging)**:
- JSON 포맷 로깅 지원 (`driver: json-file`).

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- PostgreSQL 데이터베이스 백업이 핵심입니다 (`pg_dump`).
- Realm 설정은 json 파일로 export 하여 관리 가능합니다.

## 8. 보안 및 강화 (Security Hardening)
**보안 가이드라인**:
- 프로덕션 환경에서는 `start-dev` 대신 정식 프로덕션 모드로 실행해야 합니다.
- HTTPS 사용 필수.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **DB Connection Error**: DB 호스트명이나 계정 정보 확인.
- **Infinite Redirect**: `KC_PROXY_HEADERS` 설정 및 `KC_HOSTNAME` 확인 필요.

---

## Keycloak 설정 가이드 (Setup Guide)

본 인프라의 서비스들(Grafana, OAuth2 Proxy 등)이 정상적으로 SSO를 수행하기 위해 필요한 Keycloak 설정 방법입니다.

### 4.1 Realm 생성
- **Realm Name**: `hy-home.realm` (기본값)
- `.env` 파일의 `KEYCLOAK_REALM` 변수와 일치해야 합니다.

### 4.2 Client 생성 (OAuth2 Proxy & Grafana)
`.env` 파일에서 `OAUTH2_PROXY_CLIENT_ID`로 지정된 클라이언트(예: `oauth2-proxy`)를 생성합니다.

- **Client ID**: `oauth2-proxy`
- **Client Protocol**: `openid-connect`
- **Access Type**: `confidential` (Client Secret 필요)
- **Standard Flow**: `ON`
- **Direct Access Grants**: `OFF` (권장)
- **Valid Redirect URIs**:
    - `https://auth.${DEFAULT_URL}/oauth2/callback` (OAuth2 Proxy용)
    - `https://grafana.${DEFAULT_URL}/login/generic_oauth` (Grafana용)
- **Web Origins**:
    - `+` 또는 `https://grafana.${DEFAULT_URL}`

> **참고**: 보안을 위해 Grafana와 OAuth2 Proxy용 Client를 분리할 수도 있지만, 현재 `docker-compose.yml` 설정상 동일한 환경변수(`OAUTH2_PROXY_CLIENT_ID`)를 참조하고 있으므로 하나로 통합 설정하는 방법을 기술합니다. 분리 시 각각의 Client ID/Secret을 발급받아 `.env`를 수정하세요.

### 4.3 Client Scope 및 Mapper 설정 (Group 정보 연동)
Grafana 및 OAuth2 Proxy가 사용자의 '그룹(Group)' 정보를 받아 권한을 처리하기 위해 필요합니다.

1. **Client Scopes** 메뉴로 이동 -> `create` 클릭
2. **Name**: `groups`
3. 생성 후 **Mappers** 탭 이동 -> `Configure a new mapper` -> `Group Membership` 선택
4. 설정값:
    - **Name**: `groups`
    - **Token Claim Name**: `groups`
    - **Full group path**: `ON` (중요: Grafana가 `/admins` 경로를 체크함)
    - **Add to ID token**: `ON`
    - **Add to access token**: `ON`
    - **Add to userinfo**: `ON`
5. **Clients** 메뉴 -> `oauth2-proxy` 선택 -> **Client Scopes** 탭
6. `Add client scope` -> `groups`를 **Default** 또는 **Optional**로 추가

### 4.4 사용자 및 그룹 설정
1. **Groups** 메뉴에서 다음 그룹들을 생성합니다.
    - `admins` (Grafana Admin 권한)
    - `editors` (Grafana Editor 권한)
2. **Users** 메뉴에서 사용자를 생성하고, **Groups** 탭에서 위 그룹 중 하나에 매핑합니다.

### 4.5 Credentials 적용
1. **Clients** -> `oauth2-proxy` -> **Credentials** 탭 이동
2. **Client Secret** 복사
3. 프로젝트 루트의 `.env` 파일 내 `OAUTH2_PROXY_CLIENT_SECRET` 변수 값으로 붙여넣기
4. `docker compose up -d` 로 서비스 재배포
