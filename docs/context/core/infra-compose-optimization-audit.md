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

2. `infra/04-data/couchdb/docker-compose.yml`
- Fixed healthchecks to use the actual container env var (`$${COUCHDB_USER}`) instead of undefined `$${COUCHDB_USERNAME}`.
- Removed invalid keys accidentally nested under `secrets.couchdb_cookie` (`logging`, `deploy`) that break compose schema validation for standalone file checks.

3. `.env.example`
- Added missing variables referenced by compose files so active interpolation coverage is complete across root + infra compose files.
- Added optional stack defaults/placeholders for:
  - Cassandra, CouchDB, MongoDB, Neo4j, SeaweedFS
  - Kafka controller host ports
  - OpenSearch cluster credentials/cluster name
  - MinIO optional password var
  - Airflow `_AIRFLOW_WWW_USER_USERNAME`
  - Locust and Syncthing ports/credentials
  - Optional directory roots (`DEFAULT_DATABASE_DIR`, `DEFAULT_STORAGE_DIR`, `DEFAULT_RESOURCES_DIR`, `DEFAULT_SYNCTHING_DIR`)

## Result Summary

- Missing active compose interpolation vars vs `.env.example`: `0`
- Root stack config render with template env: success
- YAML lint for compose files: success

## Notes

- Many infra compose files are designed to be included by root `docker-compose.yml` and therefore rely on root-defined networks/secrets (`infra_net`, secrets registry). Standalone `-f <service compose>` execution may still require additional top-level declarations by design.
- `infra/09-tooling/syncthing/docker-compose.yml` references `nt-sync`, `nt-webserver`, `nt-observability` networks without local declarations. This is valid only when those networks are pre-created by external orchestration.

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
