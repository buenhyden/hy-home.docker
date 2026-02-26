# Infra Compose Optimization & Env Audit

## Scope

- `docker-compose.yml` (root)
- `infra/**/docker-compose*.yml`
- `infra/**/docker-compose*.yaml`

## What Was Audited

- Compose interpolation variables (`${VAR}`) used in active (non-comment) lines.
- Runtime shell variables using escaped syntax (`$${VAR}`) to avoid false positives.
- Basic compose validity with `docker compose --env-file .env.example config`.

## Optimization Changes Applied

1. `infra/04-data/supabase/docker-compose.yml`

- Replaced ambiguous `${POSTGRES_HOST}` references with `${SUPABASE_POSTGRES_HOST}` in connection strings and DB host env.
- Replaced generic `${POSTGRES_PORT}` / `${POSTGRES_DB}` references in Supabase connection strings with `${SUPABASE_POSTGRES_PORT}` / `${SUPABASE_POSTGRES_DB}`.
- Escaped realtime healthcheck bearer token interpolation (`${SUPABASE_ANON_KEY}` -> `$${SUPABASE_ANON_KEY}`) so Compose does not resolve it at render time.

1. `infra/04-data/couchdb/docker-compose.yml`

- Fixed healthchecks to use the actual container env var (`$${COUCHDB_USER}`) instead of undefined `$${COUCHDB_USERNAME}`.
- Removed invalid keys accidentally nested under `secrets.couchdb_cookie` (`logging`, `deploy`) that break compose schema validation for standalone file checks.

1. Secret migration (`password/token` -> Docker secrets files)

- `infra/04-data/cassandra/docker-compose.yml`: `CASSANDRA_PASSWORD` -> `CASSANDRA_PASSWORD_FILE=/run/secrets/cassandra_password`
- `infra/04-data/minio/docker-compose.cluster.yaml`: root 계정/비밀번호를 `MINIO_ROOT_USER_FILE`, `MINIO_ROOT_PASSWORD_FILE`로 전환
- `infra/04-data/mongodb/docker-compose.yml`: root/mongo-express/exporter 관련 비밀번호를 secrets 기반으로 전환
- `infra/04-data/neo4j/docker-compose.yml`: `neo4j-entrypoint-with-secrets.sh` 추가, `NEO4J_AUTH`를 `neo4j_password` secret으로 주입
- `infra/04-data/opensearch/docker-compose.cluster.yml`: `ELASTIC_PASSWORD` 의존 제거, admin/dashboard/exporter 비밀번호를 secrets 주입 방식으로 전환
- `infra/07-workflow/airflow/docker-compose.yml`: Celery broker 비밀번호를 `airflow_valkey_password` secret으로 전환
- `infra/09-tooling/locust/docker-compose.yml`: InfluxDB token을 `influxdb_api_token` secret으로 주입
- `infra/09-tooling/syncthing/docker-compose.yml`: `FILE__PASSWORD` 직접 주입 제거, `FILE__PASSWORD_FILE` + `syncthing_password` secret 사용

1. `docker-compose.yml` (root secrets registry)

- 신규 secret registry 항목 추가:
  - `cassandra_password`
  - `mongodb_root_password`
  - `mongo_express_basicauth_password`
  - `neo4j_password`
  - `airflow_valkey_password`
  - `syncthing_password`

1. `.env.example`

- 전체 compose interpolation 변수 누락을 `0`으로 유지.
- secret 파일로 전환된 민감 변수(`*_PASSWORD`, token 등)는 `.env.example`에서 제거.
- 비민감 변수(포트/호스트/사용자명)만 템플릿에 유지.

1. Hardening & Observability Standardization

- **Local YAML Anchors**: `x-optimizations` 블록을 각 계층의 `docker-compose.yml`에 로컬로 정의하여 scoping 이슈를 방지하고 일관된 설정을 보장.
  - `security-baseline`: `no-new-privileges: true` 및 `cap_drop: ALL` 강제 적용.
  - `logging-loki`: 전역 Loki 로깅 드라이버 및 외부 레이블 통일.
  - `labels-base`: `hy-home.scope: infra` 및 `observability.logs: "true"` 메타데이터 자동 주입.
- **NGINX/Traefik Gateway Hardening**:
  - `security_opt`/`cap_drop` 템플릿 전환.
  - Traefik: `read_only: true` 및 `/tmp` tmpfs 마운트 적용.
- **Service Tier Refactoring**:
  - `01-gateway`: NGINX 및 Traefik 표준화 완료.
  - `02-auth`: Keycloak 보안 및 로깅 표준화 완료.
  - `04-data`: PostgreSQL, Valkey, RedisInsight 리소스 제한 및 보안 표준화 완료.
  - `06-observability`: LGTM Stack 전체(`infra-*` 계층) 로깅 및 보안 표준화 완료.

## Result Summary

- Missing active compose interpolation vars vs `.env.example`: `0`
- Root stack config render with template env: success
- YAML lint for compose files: success
- Infrastructure Hardening: All core services (`gateway`, `auth`, `data`, `observability`) utilize standardized security/logging anchors.
- Metadata Consistency: All containers emit `hy-home.tier` and `hy-home.scope` labels for unified log indexing.

## Notes

- Many infra compose files are designed to be included by root `docker-compose.yml` and therefore rely on root-defined networks/secrets (`infra_net`, secrets registry). Standalone `-f <service compose>` execution may still require additional top-level declarations by design.
- `infra/09-tooling/syncthing/docker-compose.yml` references `nt-sync`, `nt-webserver`, `nt-observability` networks without local declarations. This is valid only when those networks are pre-created by external orchestration.
- `scripts/preflight-compose.sh` now treats optional-stack-only secret files as `WARN` to avoid blocking core stack bootstrap.

## Repro Commands

```bash
# 1) Lint compose YAML files
yamllint docker-compose.yml infra/**/docker-compose*.yml infra/**/docker-compose*.yaml

# 2) Root render check
docker compose --env-file .env.example config > /tmp/root.compose.rendered.yaml

# 3) Active interpolation vars that are NOT in .env.example
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' .env.example | sort -u > /tmp/env_vars_u.txt
rg --files -g 'docker-compose*.yml' -g 'docker-compose*.yaml' \
  | sort \
  | while IFS= read -r f; do
      awk '!/^[[:space:]]*#/' "$f" \
      | perl -ne 'while(/(?<!\\$)\\$\\{([A-Za-z_][A-Za-z0-9_]*)[:}?-]?/g){print "$1\\n"}'
    done \
  | sort -u > /tmp/compose_vars_u.txt
comm -23 /tmp/compose_vars_u.txt /tmp/env_vars_u.txt
```
