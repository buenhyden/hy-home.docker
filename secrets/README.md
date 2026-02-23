# Docker Secrets Registry

이 디렉토리는 인프라 내 서비스에서 사용하는 민감한 정보(비밀번호, API 키, 토큰 등)를 카테고리별로 관리하는 저장소입니다. 모든 파일은 Docker Secrets 기능을 통해 컨테이너 내부로 안전하게 전달됩니다.

## 📁 디렉토리 구조

```text
secrets/
├── auth/          # 인증 및 게이트웨이 (Traefik, Keycloak, OAuth2 Proxy)
├── db/            # 데이터베이스 클러스터 (PostgreSQL, Valkey, Redis)
├── storage/       # 오브젝트 스토리지 (MinIO)
├── data/          # 데이터 플랫폼 (OpenSearch, Supabase)
├── observability/ # 모니터링 및 알림 (Grafana, Prometheus, InfluxDB, CouchDB)
├── automation/    # 워크플로우 자동화 (Airflow, n8n)
├── tools/         # 개발 및 배포 도구 (SonarQube, Terrakube)
└── common/        # 공통 환경설정 및 유틸리티
```

## 📂 카테고리별 시크릿 목록

### 1. 인증 및 게이트웨이 (`auth/`)

| 파일 경로 | 용도 |
|---|---|
| `auth/traefik_basicauth_password.txt` | Traefik 대시보드 접근 (htpasswd) |
| `auth/traefik_opensearch_basicauth_password.txt` | OpenSearch API 접근 (htpasswd) |
| `auth/keycloak_admin_password.txt` | Keycloak 관리자 비밀번호 |
| `db/postgres/keycloak_password.txt` | Keycloak DB 접속 비밀번호 |
| `auth/oauth2_proxy_client_secret.txt` | OAuth2 Client Secret |
| `auth/oauth2_proxy_cookie_secret.txt` | OAuth2 세션 쿠키 암호화 (base64) |
| `db/valkey/oauth2_password.txt` | OAuth2 세션 저장용 Valkey 비밀번호 |

### 2. 데이터베이스 클러스터 (`db/`)

| 파일 경로 | 용도 |
|---|---|
| `db/postgres/service_password.txt` | 서비스용 PostgreSQL 루트 비밀번호 |
| `db/postgres/mng_password.txt` | 관리용(MNG) PostgreSQL 비밀번호 |
| `db/valkey/service_password.txt` | 서비스용 Valkey 클러스터 비밀번호 |
| `db/valkey/mng_password.txt` | 관리용(MNG) Valkey 비밀번호 |

### 3. 오브젝트 스토리지 (`storage/`)

| 파일 경로 | 용도 |
|---|---|
| `storage/minio_root_username.txt` | MinIO 관리자 ID |
| `storage/minio_root_password.txt` | MinIO 관리자 비밀번호 |
| `storage/minio_app_username.txt` | 앱 전용 MinIO ID |
| `storage/minio_app_user_password.txt` | 앱 전용 MinIO 비밀번호 |

### 4. 데이터 플랫폼 (`data/`)

| 파일 경로 | 용도 |
|---|---|
| `data/opensearch_admin_password.txt` | OpenSearch admin 비밀번호 |
| `data/opensearch_dashboard_password.txt` | OpenSearch Dashboards 내부 비밀번호 |
| `data/opensearch_exporter_password.txt` | OpenSearch Prometheus Exporter 비밀번호 |
| `db/postgres/supabase_db_password.txt` | Supabase PostgreSQL 비밀번호 |
| `data/supabase_jwt_secret.txt` | Supabase인증용 JWT Secret |
| `data/supabase_anon_key.txt` | Supabase 익명 클라이언트 키 |
| `data/supabase_service_key.txt` | Supabase 서비스 롤(Admin) 키 |
| `data/supabase_dashboard_password.txt` | Supabase Kong 대시보드 비밀번호 |
| `data/supabase_secret_key_base.txt` | Supabase Phoenix 앱 시크릿 키 |
| `data/supabase_vault_enc_key.txt` | Supabase Vault 암호화 키 |
| `data/supabase_pg_meta_crypto_key.txt` | Supabase PG Meta 암호화 키 |

### 5. 모니터링 및 알림 (`observability/`)

| 파일 경로 | 용도 |
|---|---|
| `observability/grafana_admin_password.txt` | Grafana 관리자 비밀번호 |
| `common/smtp_password.txt` | Alertmanager 이메일 비밀번호 |
| `common/slack_webhook.txt` | Alertmanager Slack Webhook URL |
| `db/influxdb/influxdb_password.txt` | InfluxDB 비밀번호 |
| `db/influxdb/influxdb_api_token.txt` | InfluxDB API 토큰 |
| `db/couchdb/couchdb_password.txt` | CouchDB 비밀번호 |
| `db/couchdb/couchdb_cookie.txt` | CouchDB 클러스터 쿠키 |

### 6. 워크플로우 자동화 (`automation/`)

| 파일 경로 | 용도 |
|---|---|
| `db/postgres/n8n_password.txt` | n8n DB 접속 비밀번호 |
| `automation/n8n_encryption_key.txt` | n8n 내부 데이터 암호화 키 |
| `automation/n8n_runner_auth_token.txt` | n8n Task Runner 인증 토큰 |
| `db/valkey/n8n_password.txt` | n8n 용 Valkey 비밀번호 |
| `db/postgres/airflow_password.txt` | Airflow DB 접속 비밀번호 |
| `automation/airflow_fernet_key.txt` | Airflow Fernet Key |
| `automation/airflow_www_password.txt` | Airflow Web UI 관리자 비밀번호 |

### 7. 개발 및 배포 도구 (`tools/`)

| 파일 경로 | 용도 |
|---|---|
| `tools/sonarqube_admin_password.txt` | SonarQube 관리자 비밀번호 |
| `db/postgres/sonarqube_password.txt` | SonarQube DB 접속 비밀번호 |
| `db/postgres/terrakube_password.txt` | Terrakube API DB 비밀번호 |
| `tools/terrakube_internal_secret.txt` | Terrakube 내부 통신 시크릿 |
| `tools/terrakube_minio_secret_key.txt` | Terrakube MinIO Secret Key |
| `tools/terrakube_valkey_password.txt` | Terrakube Valkey 비밀번호 |
| `tools/terrakube_pat_secret.txt` | Terrakube PAT 암호화 키 |

### 8. 공통 (`common/`)

| 파일 경로 | 용도 |
|---|---|
| `common/smtp_username.txt` | 시스템 공통 SMTP 계정 |

---

## 🔄 유지관리 및 재생성

본 디렉토리의 시크릿들은 보안 강화를 위해 생성 스크립트를 통해 일괄 관리됩니다.

- **생성일**: 2026-02-24
- **정책**:
  - 비밀번호: 32자 영문/숫자 혼합
  - 키/토큰: 64자 Hex 또는 32바이트 Base64
  - Traefik: `admin` 계정 기준 MD5-Crypt 해시 (`password321`)
- **주의**: 외부 서비스(Slack Webhook, SMTP 등)와 연동되는 시크릿은 실제 서비스 값으로 수동 교체해야 합니다.
