# Keycloak Identity Access Management

## 1. 개요 (Overview)
이 디렉토리는 통합 인증 접근 관리(IAM) 솔루션인 Keycloak을 정의합니다. 사용자 인증, 인가, SSO(Single Sign-On)를 처리하며, 외부 PostgreSQL 데이터베이스를 사용합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **keycloak** | IAM Server | OpenID Connect, SAML, OAuth2 등을 지원하는 인증 서버입니다. |

## 3. 구성 및 설정 (Configuration)

### 데이터베이스 연결
외부 PostgreSQL 데이터베이스(`POSTGRES_HOSTNAME`)에 접속하여 사용자 및 설정 데이터를 저장합니다.
- `KC_DB`: Database vendor (postgres)
- `KC_DB_URL`: JDBC 연결 URL
- Quarkus 기반의 Agroal 커넥션 풀 설정을 통해 DB 연결 유효성을 주기적으로 검사합니다(`idle-removal-interval`, `background-validation-interval`).

### 모니터링
- `KC_METRICS_ENABLED`: 메트릭 활성화
- `KC_HEALTH_ENABLED`: 헬스 체크 활성화

### 로드밸런싱 (Traefik)
- **URL**: `https://keycloak.${DEFAULT_URL}`
- `manage` 포트가 노출되어 있으며 프록시 헤더 처리가 설정되어 있습니다.

### 환경 변수
관리자 계정(`KEYCLOAK_ADMIN`)과 DB 접근 정보는 환경 변수를 통해 주입됩니다.
