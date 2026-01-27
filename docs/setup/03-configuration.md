# ⚙️ Configuration Reference

이 문서는 `.env` 파일의 주요 변수 그룹과 `secrets/` 관리 방법에 대한 상세 가이드를 제공합니다.

## 1. `.env` 변수 그룹 설명

### 🏗️ Global Configuration

- `DEFAULT_URL`: 각 서비스의 Traefik 라우팅을 위한 베이스 도메인.
- `DEFAULT_MOUNT_VOLUME_PATH`: 모든 영구 데이터 저장용 호스트 경로. (예: `D:/docker-volumes`)
- `DEFAULT_ENV`: 실행 환경 (`dev`, `prod`, `test`).

### 📦 Infrastructure Versions

- 각 서비스의 이미지 태그를 관리합니다 (예: `TRAEFIK_VERSION`, `POSTGRES_VERSION`).

### 🔒 Ingress & SSL

- `TRAEFIK_CERT_RESOLVER`: Let's Encrypt 사용 여부.
- `ACME_EMAIL`: 인증서 갱신용 이메일.

### 📊 Observability Settings

- `GRAFANA_ADMIN_USER` / `GRAFANA_ADMIN_PASSWORD`: 초기 관리자 계정.
- `SLACK_ALERTMANAGER_WEBHOOK_URL`: 알림 연동을 위한 Slack 웹훅.

## 2. Secrets Management

Docker Secrets 기능을 활용하여 민감 정보를 컨테이너 내부로 안전하게 전달합니다.
`infra/docker-compose.yml`에서 정의된 secrets는 `secrets/` 디렉토리의 텍스트 파일과 매핑됩니다.

| Secret Name | File Path | Usage |
| :--- | :--- | :--- |
| `postgres_password` | `secrets/postgres_password.txt` | PG 클러스터 superuser 비밀번호 |
| `redis_password` | `secrets/redis_password.txt` | Redis 클러스터 인증 패스워드 |
| `minio_root_password` | `secrets/minio_root_password.txt` | Minio 관리자 비밀번호 |
| `keycloak_db_password` | `secrets/keycloak_db_password.txt` | Keycloak용 DB 사용자 암호 |

### ⚠️ 주의사항

- `secrets/*.txt` 파일 끝에 개행 문자(New Line)가 포함되지 않도록 주의하십시오. 일부 서비스에서 인증 실패의 원인이 됩니다.
- `.gitignore`에 의해 `secrets/` 폴더 내의 콘텐츠는 버전 관리에서 제외됩니다.

## 3. 서비스 활성화/비활성화 (Profiles)

현재는 `infra/docker-compose.yml`의 `include` 섹션에서 주석처리를 통해 서비스를 선택적으로 로드합니다.

```yaml
include:
  - traefik/docker-compose.yml
  - mng-db/docker-compose.yml
  # - sonarqube/docker-compose.yml  <-- 주석 해제로 활성화
```

향후 Docker Compose Profile을 도입하여 더욱 유연한 관리가 가능하도록 개선될 예정입니다.
