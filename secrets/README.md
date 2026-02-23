# Docker Secrets Registry

이 디렉토리는 인프라 내 서비스에서 사용하는 민감한 정보(비밀번호, API 키, 토큰 등)를 관리하는 저장소입니다. 모든 파일은 Docker Secrets 기능을 통해 컨테이너 내부로 안전하게 전달됩니다.

## ⚠️ 중요 주의사항

- **보안**: 이 폴더 내의 `.txt` 파일들은 민감한 정보를 포함하고 있으므로 **Git에 커밋되지 않도록** 주의하십시오. (루트 `.gitignore`에 등록됨)
- **플레이스홀더**: 신규 생성된 파일 중 `CHANGE_ME_*`로 시작하는 내용은 실제 운영 환경에 맞는 값으로 교체해야 합니다.

---

## 📂 카테고리별 시크릿 목록

### 1. 인프라 코어 & 인증 (Gateway, Auth)

| 파일명 | 용도 |
|---|---|
| `traefik_basicauth_password.txt` | Traefik 대시보드 접근을 위한 HTTP Basic Auth 자격증명 (htpasswd 형식) |
| `traefik_opensearch_basicauth_password.txt` | OpenSearch API 접근을 위한 HTTP Basic Auth 자격증명 (htpasswd 형식, 대시보드 계정과 별개) |
| `keycloak_admin_password.txt` | Keycloak 마스터 렐름 관리자 비밀번호 |
| `keycloak_db_password.txt` | Keycloak이 DB에 접속할 때 사용하는 비밀번호 |
| `oauth2_proxy_client_secret.txt` | Vault 및 Grafana SSO 연동을 위한 OAuth2 Client Secret |
| `oauth2_proxy_cookie_secret.txt` | OAuth2 Proxy 세션 쿠키 암호화용 시크릿 (32바이트 base64) |
| `oauth2_valkey_password.txt` | OAuth2 Proxy 세션 저장용 Valkey 비밀번호 |

### 2. 공통 데이터베이스 (Global/Shared)

| 파일명 | 용도 |
|---|---|
| `service_postgres_password.txt` | 주요 서비스용 PostgreSQL 클러스터 루트 비밀번호 |
| `service_valkey_password.txt` | 주요 서비스용 Valkey 클러스터 비밀번호 |
| `mng_postgres_password.txt` | 관리용(MNG) PostgreSQL 비밀번호 |
| `mng_valkey_password.txt` | 관리용(MNG) Valkey 비밀번호 |
| `postgres_password.txt` | (Legacy) 단일 인스턴스용 PostgreSQL 비밀번호 |
| `redis_password.txt` | (Legacy) 단일 인스턴스용 Redis 비밀번호 |

### 3. 오브젝트 스토리지 (MinIO)

| 파일명 | 용도 |
|---|---|
| `minio_root_username.txt` | MinIO 서버 루트(관리자) ID |
| `minio_root_password.txt` | MinIO 서버 루트(관리자) 비밀번호 |
| `minio_app_username.txt` | 어플리케이션(Loki, Tempo 등) 전용 MinIO ID |
| `minio_app_user_password.txt` | 어플리케이션 전용 MinIO 비밀번호 |
| `minio_app_password.txt` | `minio_app_user_password.txt`와 동일 (하위 스택 호환용) |

### 4. 데이터 플랫폼 (OpenSearch, Supabase)

| 파일명 | 용도 |
|---|---|
| `opensearch_admin_password.txt` | OpenSearch 클러스터 admin 비밀번호 |
| `opensearch_dashboard_password.txt` | Dashboards 접근용 내부 비밀번호 |
| `opensearch_exporter_password.txt` | 메트릭 수집을 위한 Exporter 비밀번호 |
| `supabase_db_password.txt` | Supabase 내부 PostgreSQL(postgres user) 비밀번호 |
| `supabase_jwt_secret.txt` | Supabase API 인증용 JWT Secret |
| `supabase_anon_key.txt` | Supabase 익명 클라이언트 키 |
| `supabase_service_key.txt` | Supabase 서비스 롤(Admin) 키 |
| `supabase_dashboard_password.txt` | Supabase Kong 대시보드 Basic Auth 비밀번호 |
| `supabase_secret_key_base.txt` | Supabase Realtime/Supavisor Phoenix 앱 시크릿 키 |
| `supabase_vault_enc_key.txt` | Supabase Supavisor Vault 암호화 키 |
| `supabase_pg_meta_crypto_key.txt` | Supabase PG Meta / Studio 데이터 암호화 키 |

### 5. 관제 및 알림 (Observability)

| 파일명 | 용도 |
|---|---|
| `grafana_admin_password.txt` | Grafana 초기 관리자(admin) 비밀번호 |
| `alertmanager_smtp_password.txt` | Alertmanager 이메일 발송용 계정 비밀번호 |
| `alertmanager_slack_webhook.txt` | Alertmanager 알림 전송용 Slack Webhook URL |

### 6. 워크플로우 자동화 (n8n, Airflow)

| 파일명 | 용도 |
|---|---|
| `n8n_db_password.txt` | n8n DB(PostgreSQL) 접속 비밀번호 |
| `n8n_encryption_key.txt` | n8n 내부 데이터 암호화 키 (32자 이상 권장) |
| `n8n_runner_auth_token.txt` | n8n Task Runner 인증 토큼 |
| `n8n_valkey_password.txt` | n8n Queue/세션용 Valkey 비밀번호 |
| `airflow_db_password.txt` | Airflow 메타데이터 DB(PostgreSQL) 비밀번호 |
| `airflow_fernet_key.txt` | Airflow Connection 암호화용 Fernet Key |
| `airflow_www_password.txt` | Airflow Web UI 초기 관리자 비밀번호 |

### 7. 도구 및 자동화 (SonarQube, Terrakube)

| 파일명 | 용도 |
|---|---|
| `sonarqube_admin_password.txt` | SonarQube 초기 관리자 비밀번호 |
| `sonarqube_db_password.txt` | SonarQube DB(PostgreSQL) 비밀번호 |
| `terrakube_db_password.txt` | Terrakube API 서버용 DB 비밀번호 |
| `terrakube_internal_secret.txt` | Terrakube 컴포넌트 간 내부 통신용 시크릿 |
| `terrakube_minio_secret_key.txt` | Terrakube가 MinIO를 백엔드로 쓸 때 사용하는 Secret Key |
| `terrakube_redis_password.txt` | Terrakube 세션/메시지 브로커용 Redis 비밀번호 |
| `terrakube_pat_secret.txt` | Terrakube Personal Access Token 암호화 키 |

---

## 🛠 사용 방법

모든 시크릿은 루트 `docker-compose.yml`에서 다음과 같이 정의되어 있습니다.

```yaml
secrets:
  service_postgres_password:
    file: ./secrets/service_postgres_password.txt
```

하위 스택에서는 이 시크릿을 `external: true`로 참조합니다.

```yaml
services:
  myapp:
    secrets:
      - service_postgres_password
```
