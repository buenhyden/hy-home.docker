# Keycloak

**Keycloak**는 최신 애플리케이션 및 서비스를 위한 오픈 소스 ID 및 액세스 관리(IAM) 솔루션입니다.
현재 구성은 개발 모드(`start-dev`)로 설정되어 있습니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **keycloak** | IAM 서버 | `18080` (Host) -> `8080` (Container) |

## 🛠 설정 및 환경 변수

- **이미지**: `quay.io/keycloak/keycloak:26.4.0`
- **모드**: `start-dev` (프로덕션 사용 시 변경 필요)
- **관리자 콘솔**: `http://localhost:18080`

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **데이터베이스**: 현재 내장 H2 데이터베이스를 사용하도록 설정되어 있을 수 있습니다. 프로덕션 환경에서는 PostgreSQL 등 외부 DB 연결을 권장합니다.
