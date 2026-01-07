# Keycloak IAM Service

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 오픈소스 ID 및 접근 관리(IAM) 솔루션입니다.  
최신 애플리케이션과 서비스를 위한 Single Sign-On (SSO), ID 중개(Identity Brokering), 사용자 연동(User Federation) 기능을 제공합니다.

## 2. 주요 기능 (Key Features)
- **Single Sign-On (SSO)**: 한 번의 로그인으로 연결된 모든 애플리케이션(Grafana, Harbor, Traefik 등)에 접근할 수 있습니다.
- **Identity Brokering**: Google, GitHub 등 소셜 로그인을 통합하여 지원합니다.
- **Standard Protocols**: OpenID Connect, OAuth 2.0, SAML 2.0 등 표준 프로토콜을 완벽하게 지원합니다.
- **Admin Console**: 웹 기반의 강력한 관리 콘솔을 통해 Realm, Client, User를 손쉽게 관리합니다.

## 3. 기술 스택 (Tech Stack)
- **Image**: `quay.io/keycloak/keycloak:26.4.6`
- **Database**: PostgreSQL 17 (`mng-pg` 클러스터 사용)
- **Runtime**: Quarkus (Java) based logic
- **Mode**: Development Profile (`start-dev`)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 시스템 구조
1.  **User**: 서비스 접근 시도.
2.  **Traefik/App**: 인증되지 않은 요청을 Keycloak으로 리다이렉트.
3.  **Keycloak**: 사용자 로그인 화면 제공 및 인증 처리 (PostgreSQL 조회).
4.  **Token**: 인증 성공 시 JWT(Access/Refresh Token) 발급.
5.  **Access**: 애플리케이션은 토큰을 검증하여 사용자 접근 허용.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **주의**: 데이터베이스(`postgresql`)가 준비되어 있어야 정상적으로 구동됩니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 관리자 콘솔 접속
1.  **주소**: `https://keycloak.${DEFAULT_URL}/admin`
2.  **로그인**: `admin` / `admin` (초기 설정된 `KEYCLOAK_ADMIN` 환경변수 참조)
3.  **기능**: Realm 생성, Client 등록, 사용자 추가 등.

### 6.2 필수 초기 설정 (Initial Setup Guide)
본 인프라 서비스들(Grafana, OAuth2 Proxy)의 SSO 연동을 위한 설정 절차입니다.

#### 1. Realm 생성
- **Name**: `hy-home.realm` (기본값, `.env`의 `KEYCLOAK_REALM`과 일치 필요)

#### 2. Client 생성 (OAuth2 Proxy & Grafana)
- **Client ID**: `proxy-client` (또는 `.env`의 `OAUTH2_PROXY_CLIENT_ID` 값)
- **Client Authentication**: `On` (Confidential Access Type)
- **Standard Flow**: `Checked`
- **Direct Access Grants**: `Unchecked` (보안 권장)
- **Valid Redirect URIs**:
    - `https://auth.${DEFAULT_URL}/oauth2/callback` (OAuth2 Proxy)
    - `https://grafana.${DEFAULT_URL}/login/generic_oauth` (Grafana)
- **Web Origins**: `+` (CORS 허용)

#### 3. Client Scope 설정 (그룹 연동)
Grafana에서 Keycloak의 Group 정보를 읽어 Admin/Editor 권한을 매핑하기 위해 필요합니다.
1.  **Client Scopes** 메뉴 -> `Create client scope` -> Name: `groups`
2.  **Mappers** 탭 -> `Configure a new mapper` -> `Group Membership` 선택.
    - **Token Claim Name**: `groups`
    - **Full group path**: `On` (필수)
    - **Add to ID token / Access token / Userinfo**: 모두 `On`.
3.  **Clients** -> `proxy-client` -> **Client Scopes** 탭 -> `Add client scope` -> `groups`를 `Default`로 추가.

#### 4. 사용자 및 그룹 생성
1.  **Groups**: `admins` (Grafana Admin용), `editors` (Grafana Editor용) 생성.
2.  **Users**: 사용자 생성 후 **Groups** 탭에서 해당 그룹에 멤버로 추가.

#### 5. Client Secret 적용
1.  **Clients** -> `proxy-client` -> **Credentials** 탭에서 `Client Secret` 복사.
2.  `.env` 파일의 `OAUTH2_PROXY_CLIENT_SECRET` 변수에 값 적용 후 서비스 재시작.

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `KEYCLOAK_ADMIN`: 초기 관리자 ID.
- `KEYCLOAK_ADMIN_PASSWORD`: 초기 관리자 비밀번호.
- `KC_DB`: `postgres`
- `KC_DB_URL`: JDBC 포맷 DB 연결 주소.
- `KC_HOSTNAME`: 서비스되는 외부 도메인 주소 (`https://keycloak.${DEFAULT_URL}`).
- `KC_PROXY_HEADERS`: `xforwarded` (Reverse Proxy 환경에서 필수).

### 네트워크 포트 (Ports)
- **HTTP**: 8080 (`https://keycloak.${DEFAULT_URL}`)
- **Management**: 9000 (헬스체크 및 메트릭)

## 8. 통합 및 API 가이드 (Integration Guide)
**Well-Known Endpoint**:
- OIDC 설정을 위한 메타데이터 주소입니다.
- `https://keycloak.${DEFAULT_URL}/realms/{realm-name}/.well-known/openid-configuration`

**Token Endpoint**:
- `/realms/{realm}/protocol/openid-connect/token`

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- `/health` 엔드포인트 활성화 (`KC_HEALTH_ENABLED=true`).
- **Liveness**: `/health/live`
- **Readiness**: `/health/ready` (DB 연결 상태 포함).

**Metrics**:
- `/metrics` 엔드포인트 활성화 (`KC_METRICS_ENABLED=true`).
- Prometheus 포맷으로 JVM 및 Keycloak 내부 메트릭을 제공합니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**DB 백업**:
- Keycloak의 모든 설정(Realm, Client, User)은 PostgreSQL에 저장되므로 DB 백업이 가장 중요합니다.

**Export/Import**:
- 관리자 콘솔 또는 CLI(`kc.sh export`)를 사용하여 특정 Realm을 JSON 파일로 추출 및 복원할 수 있습니다.

## 11. 보안 및 강화 (Security Hardening)
- **Production Mode**: 현재는 `start-dev` 모드입니다. 운영 환경에서는 `start` 명령어를 사용하고 HTTPS 인증서를 Keycloak에 직접 설정하거나, 신뢰할 수 있는 Proxy 뒤에 배치해야 합니다.
- **Admin Console**: 외부 인터넷에서 `/admin` 경로 접근을 제한하는 것이 좋습니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **HTTPS/SSL 오류**: `KC_HOSTNAME` 설정이 실제 접속 도메인과 다르면 발생합니다.
- **Infinite Loop (리다이렉트 반복)**: `KC_PROXY_HEADERS=xforwarded` 설정이 누락되었거나, 프록시(Traefik)가 올바른 헤더(X-Forwarded-Proto)를 전달하지 않을 때 발생합니다.
- **Slow Startup**: DB 연결 풀 초기화 지연으로 인한 문제일 수 있습니다 `KC_DB_POOL_*` 설정을 확인하세요.

---
**공식 문서**: [https://www.keycloak.org/documentation](https://www.keycloak.org/documentation)
