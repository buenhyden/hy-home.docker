# 🔐 hy-home.docker Secrets Directory

본 디렉터리는 `hy-home.docker` 인프라에서 사용하는 모든 민감 정보(비밀번호, 키, 토큰)를 Docker Secrets 포맷(`.txt`)으로 관리하는 저장소입니다.

---

## 🏛️ 시크릿 관리 시스템

본 프로젝트는 보안과 편리함을 위해 중앙 집중형 레지스트리와 관리 스크립트를 사용합니다.

### 1. 레지스트리 (Source of Truth)

- **[SENSITIVE_ENV_VARS.md](SENSITIVE_ENV_VARS.md)**: 모든 시크릿의 마스터 명단입니다.
- 자동화 여부, 파일 경로, 대응하는 `.env` 변수, 생성/갱신 날짜를 한눈에 확인할 수 있습니다.
- 환경 초기화 시 **[SENSITIVE_ENV_VARS.md.example](SENSITIVE_ENV_VARS.md.example)**를 참조하십시오.

### 2. 자동화 스크립트

- **`gen-secrets.sh`**: 레지스트리를 기반으로 비밀번호 파일을 자동 생성합니다.
- **주요 기능**:
  - 안전한 랜덤 비밀번호(16자리) 자동 생성
  - Traefik/OpenSearch용 `htpasswd` (MD5/Apache 기반) 자동 생성 및 포매팅
  - 레지스트리(SENSITIVE_ENV_VARS.md) 실시간 업데이트 및 동기화
- **사용법**:

  ```bash
  ./scripts/gen-secrets.sh
  ```

---

## 🚀 설정 및 운영 가이드

1. **최초 구축 시**:
   - `scripts/gen-secrets.sh`를 실행하여 누락된 모든 시크릿 파일을 생성합니다.
   - 외부 연동(SMTP, Slack 등)이 필요한 항목은 `SENSITIVE_ENV_VARS.md`에서 수동으로 업데이트하십시오.
2. **비밀번호 변경 시**:
   - 개별 `.txt` 파일을 직접 수정하거나, `gen-secrets.sh --force`를 사용하여 새 비밀번호를 생성할 수 있습니다.
   - 변경 후에는 해당 서비스를 재시작해야 적용됩니다: `docker compose restart [서비스명]`

---

## 📦 서비스별 시크릿 항목 (간략)

| 분류 | Docker Secret Name | 관련 파일 경로 | 용도 |
| :--- | :--- | :--- | :--- |
| **인증** | `traefik_basicauth` | `auth/traefik_basicauth_password.txt` | Dashboard 접속 (자동 생성) |
| | `keycloak_admin` | `auth/keycloak_admin_password.txt` | Keycloak 마스터 비번 |
| | `oauth2_cookie` | `auth/oauth2_proxy_cookie_secret.txt` | 세션 암호화 키 |
| **DB** | `mng_postgres` | `db/postgres/mng_password.txt` | 관리용 DB 루트 비번 |
| | `keycloak_db` | `db/postgres/keycloak_password.txt` | Keycloak DB 접속 |
| | `mongodb_root` | `db/mongodb/mongodb_root_password.txt` | MongoDB 루트 비번 |
| **자동화** | `airflow_fernet` | `automation/airflow_fernet_key.txt` | 데이터 암호화 키 |
| | `n8n_encryption` | `automation/n8n_encryption_key.txt` | 워크플로우 암호화 |
| **스토리지** | `minio_root` | `storage/minio_root_password.txt` | MinIO 루트 비번 |
| **BaaS** | `supabase_jwt` | `data/supabase_jwt_secret.txt` | JWT 서명용 시크릿 |

> [!NOTE]
> 상세한 전체 목록과 대응하는 `.env` 변수 매핑은 **[SENSITIVE_ENV_VARS.md](SENSITIVE_ENV_VARS.md)**를 참조하십시오.

---

## 🛡️ 보안 정책

- **Git 제외**: 본 디렉터리의 모든 `.txt` 파일은 `.gitignore`에 등록되어 Git에 포함되지 않습니다.
- **백업**: `gen-secrets.sh --force` 실행 시 기존 파일은 자동으로 `.bak` 확장자로 백업됩니다.
