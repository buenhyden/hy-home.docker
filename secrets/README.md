# Docker Secrets Registry

이 디렉토리는 인프라 내 서비스에서 사용하는 민감한 정보(비밀번호, API 키, 토큰 등)를 저장하고 관리합니다. 모든 파일은 `./docker-compose.yml`의 `secrets` 섹션에 정의되어 있으며, 컨테이너 실행 시 `/run/secrets/` 경로로 전달됩니다.

## 📁 디렉토리 구조

```text
secrets/
├── auth/          # 인증 및 게이트웨이 (Traefik, Keycloak, OAuth2 Proxy)
├── automation/    # 워크플로우 자동화 (Airflow, n8n)
├── certs/         # SSL/TLS 인증서 및 키
├── common/        # 공통 설정 (SMTP, Slack)
├── data/          # 데이터 플랫폼 (OpenSearch, Supabase)
├── db/            # 데이터베이스 (PostgreSQL, Valkey, InfluxDB, CouchDB)
├── observability/ # 모니터링 (Grafana)
├── storage/       # 오브젝트 스토리지 (MinIO)
├── tools/         # 개발 및 배포 도구 (SonarQube, Terrakube)
└── README.md      # 본 문서
```

---

## 🔐 시크릿 상세 레지스트리

모든 시크릿 이름은 `./docker-compose.yml`에 정의된 `secrets` 이름을 기준으로 합니다.

### 1. 공통 및 가용성 (`common/`)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `smtp_password` | `common/smtp_password.txt` | 알림 및 메일 발송용 SMTP 비밀번호 |
| `slack_webhook` | `common/slack_webhook.txt` | Slack Alert 전용 Webhook URL |
| `smtp_username` | `common/smtp_username.txt` | 알림용 공용 SMTP 서버 계정명 |
| `stalwart_password` | `common/stalwart_password.txt` | Stalwart Mail Server 관리자 비밀번호 |
| `supabase_smtp_password` | `common/supabase_smtp_password.txt` | Supabase Auth(GoTrue) SMTP 비밀번호 |

### 2. 게이트웨이 및 인증 (`auth/`)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `traefik_basicauth_password` | `auth/traefik_basicauth_password.txt` | Traefik 대시보드 Basic Auth (bcrypt) |
| `traefik_opensearch_basicauth_password` | `auth/traefik_opensearch_basicauth_password.txt` | OpenSearch API 전용 Basic Auth |
| `keycloak_admin_password` | `auth/keycloak_admin_password.txt` | Keycloak Master Realm 관리자 비밀번호 |
| `oauth2_proxy_client_secret` | `auth/oauth2_proxy_client_secret.txt` | Keycloak/OAuth2 Proxy Client Secret |
| `oauth2_proxy_cookie_secret` | `auth/oauth2_proxy_cookie_secret.txt` | OAuth2 Proxy 세션 암호화 쿠키 시크릿 |
| `pg_haproxy_stats_password` | `auth/pg_haproxy_stats_password.txt` | PostgreSQL HAProxy Stats 비밀번호 |

### 3. 관측성 (`observability/`)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `grafana_admin_password` | `observability/grafana_admin_password.txt` | Grafana 초기 관리자(admin) 비밀번호 |

### 4. 관계형 데이터베이스 (PostgreSQL)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `service_postgres_password` | `db/postgres/service_password.txt` | PostgreSQL 서비스용 루트 관리 비밀번호 |
| `mng_postgres_password` | `db/postgres/mng_password.txt` | PostgreSQL 관리용(MNG) 관리 비밀번호 |
| `keycloak_db_password` | `db/postgres/keycloak_password.txt` | Keycloak DB 접속용 비밀번호 |
| `airflow_db_password` | `db/postgres/airflow_password.txt` | Airflow 메타데이터 DB 접속 비밀번호 |
| `n8n_db_password` | `db/postgres/n8n_password.txt` | n8n DB 접속 비밀번호 |
| `sonarqube_db_password` | `db/postgres/sonarqube_password.txt` | SonarQube DB 접속 비밀번호 |
| `terrakube_db_password` | `db/postgres/terrakube_password.txt` | Terrakube API DB 비밀번호 |
| `supabase_db_password` | `db/postgres/supabase_password.txt` | Supabase 내부 DB 비밀번호 |
| `patroni_superuser_password` | `db/postgres/patroni_superuser_password.txt` | PostgreSQL HA(Spilo/Patroni) superuser 비밀번호 |
| `patroni_replication_password` | `db/postgres/patroni_replication_password.txt` | PostgreSQL HA(Spilo/Patroni) replication 비밀번호 |

### 5. 인메모리 및 NoSQL (Valkey, InfluxDB, CouchDB, Cassandra, MongoDB, Neo4j)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `service_valkey_password` | `db/valkey/service_password.txt` | 서비스용 Valkey 클러스터 비밀번호 |
| `mng_valkey_password` | `db/valkey/mng_password.txt` | 관리용(MNG) Valkey 비밀번호 |
| `n8n_valkey_password` | `db/valkey/n8n_password.txt` | n8n 용 Valkey 전용 비밀번호 |
| `terrakube_valkey_password` | `db/valkey/terrakube_password.txt` | Terrakube Valkey 저장소 비밀번호 |
| `airflow_valkey_password` | `db/valkey/airflow_password.txt` | Airflow Celery broker(Redis/Valkey) 비밀번호 |
| `influxdb_password` | `db/influxdb/influxdb_password.txt` | InfluxDB 관리자(admin) 비밀번호 |
| `influxdb_api_token` | `db/influxdb/influxdb_api_token.txt` | InfluxDB 관리자 액세스 토큰 |
| `couchdb_password` | `db/couchdb/couchdb_password.txt` | CouchDB 클러스터 관리자 비밀번호 |
| `couchdb_cookie` | `db/couchdb/couchdb_cookie.txt` | CouchDB Erlang 노드 간 인증 쿠키 |
| `cassandra_password` | `db/cassandra/cassandra_password.txt` | Cassandra 클러스터 사용자 비밀번호 |
| `mongodb_root_password` | `db/mongodb/mongodb_root_password.txt` | MongoDB ReplicaSet root 비밀번호 |
| `mongo_express_basicauth_password` | `db/mongodb/mongo_express_basicauth_password.txt` | Mongo Express UI Basic Auth 비밀번호 |
| `neo4j_password` | `db/neo4j/neo4j_password.txt` | Neo4j 관리자 비밀번호 |

### 6. 오브젝트 스토리지 (`storage/`)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `minio_root_username` | `storage/minio_root_username.txt` | MinIO 서버 루트 관리자 ID |
| `minio_root_password` | `storage/minio_root_password.txt` | MinIO 서버 루트 관리자 비밀번호 |
| `minio_app_username` | `storage/minio_app_username.txt` | 애플리케이션(Loki/Tempo 등) 전용 ID |
| `minio_app_user_password` | `storage/minio_app_user_password.txt` | 애플리케이션 전용 계정 비밀번호 |

### 7. 검색 및 로그 스토리지 (OpenSearch)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `opensearch_admin_password` | `data/opensearch_admin_password.txt` | OpenSearch 초기 admin 비밀번호 |
| `opensearch_dashboard_password` | `data/opensearch_dashboard_password.txt` | Dashboards 내장 유저 비밀번호 |
| `opensearch_exporter_password` | `data/opensearch_exporter_password.txt` | Prometheus용 OpenSearch Exporter 비밀번호 |

### 8. 워크플로우 자동화 (`automation/`)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `airflow_fernet_key` | `automation/airflow_fernet_key.txt` | Airflow Fernet 암호화 키 |
| `airflow_www_password` | `automation/airflow_www_password.txt` | Airflow WebUI 초기 관리자 비밀번호 |
| `n8n_encryption_key` | `automation/n8n_encryption_key.txt` | n8n 내부 데이터 암호화 키 |
| `n8n_runner_auth_token` | `automation/n8n_runner_auth_token.txt` | n8n Worker 호스트 인증 토큰 |

### 9. 개발 및 배포 도구 (`tools/`)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `sonarqube_admin_password` | `tools/sonarqube_admin_password.txt` | SonarQube 초기 관리자 비밀번호 |
| `terrakube_pat_secret` | `tools/terrakube_pat_secret.txt` | Terrakube PAT 암호화 키 |
| `terrakube_internal_secret` | `tools/terrakube_internal_secret.txt` | Terrakube API 서비스 간 통신 시크릿 |
| `syncthing_password` | `tools/syncthing_password.txt` | Syncthing GUI 계정 비밀번호 |

### 10. BaaS 플랫폼 (Supabase)

| Docker Secret Name | 파일 경로 | 용도 |
|:---:|---|---|
| `supabase_jwt_secret` | `data/supabase_jwt_secret.txt` | Supabase 인증용 고유 JWT Secret |
| `supabase_anon_key` | `data/supabase_anon_key.txt` | Public 익명 클라이언트 API 키 |
| `supabase_service_key` | `data/supabase_service_key.txt` | Private 서비스 롤(관리) API 키 |
| `supabase_dashboard_password` | `data/supabase_dashboard_password.txt` | Supabase Kong 대시보드 Basic Auth 비밀번호 |
| `supabase_secret_key_base` | `data/supabase_secret_key_base.txt` | Supabase 내부 Elixir/Phoenix 앱 시크릿 |
| `supabase_vault_enc_key` | `data/supabase_vault_enc_key.txt` | Supabase Vault 확장 암호화 키 |
| `supabase_pg_meta_crypto_key` | `data/supabase_pg_meta_crypto_key.txt` | PG Meta 서버 암호화 키 |
| `supabase_db_enc_key` | `data/supabase_db_enc_key.txt` | Supabase Realtime DB 암호화 키 |
| `supabase_openai_api_key` | `data/supabase_openai_api_key.txt` | Supabase Studio SQL Assistant(OpenAI) API 키 |
| `supabase_logflare_private_token` | `data/supabase_logflare_private_token.txt` | Supabase Analytics(Logflare) private token |

---

## ✅ 보안 정책 및 주의사항

- **생성 일시**: 2026-02-24
- **관리 원칙**:
  - 본 디렉토리의 모든 파일은 `.gitignore`에 의해 Git 추적 대상에서 제외됩니다.
  - 모든 시크릿은 `./docker-compose.yml`에서 파일 기반으로 정의되어 관리됩니다.
  - 신규 서비스 추가 시 관련 컨테이너 내부의 `/run/secrets/` 경로를 통해 시크릿을 읽어오도록 구성하십시오.
- **수동 교체 대상**:
  - `slack_webhook`, `smtp_username/password` 등 외부 연동이 필요한 시크릿은 생성 스크립트 실행 후 수동으로 실제 값을 채워 넣어야 합니다.

## (옵션) Dedicated / Standalone 스택에서만 사용하는 시크릿

루트 `docker-compose.yml` 기준 목록 외에, 일부 스택은 독립 실행(dedicated) 구성에서 추가 시크릿을 사용합니다.

| Docker Secret Name | 파일 경로 | 용도 | 비고 |
|:---:|---|---|---|
| `oauth2_valkey_password` | `db/valkey/oauth2_password.txt` | OAuth2 Proxy 세션 저장용 Valkey 비밀번호 | `infra/02-auth/oauth2-proxy/docker-compose.dedicated.yml` 전용 |
