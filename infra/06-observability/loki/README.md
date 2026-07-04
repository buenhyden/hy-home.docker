# Loki Log Aggregation System

## Overview

`infra/06-observability/loki` contains the Loki implementation for the `06-observability` tier. Loki runs as compose service `loki`, container `infra-loki`, image `hy/loki:3.7.3-custom`, stores working data in `loki-data`, and uses MinIO S3 bucket `loki-bucket` for log chunks and indexes. The custom image keeps Loki's upstream binary and a small entrypoint that exports `MINIO_APP_USER_PASSWORD` from Docker Secret `minio_app_user_password` before starting Loki with `-config.expand-env=true`.

## Audience

- Developers debugging application and infrastructure logs
- SREs managing retention, storage, and query performance
- Operators maintaining Loki readiness and MinIO connectivity
- AI Agents collecting evidence without exposing secret values

## Scope

### In Scope

- Log ingestion from Grafana Alloy to `http://loki:3100/loki/api/v1/push`
- MinIO-backed Loki storage and bucket `loki-bucket`
- Retention and compactor settings in `config/loki-config.yaml`
- LogQL querying through Grafana datasource `Loki`
- Compose service, custom image, entrypoint, secret, route, and readiness boundaries

### Out of Scope

- Application-side logging SDK changes
- Long-term audit archiving beyond the active retention policy
- MinIO bucket lifecycle policy outside the Loki service boundary
- Runtime retention, resource, secret, or route changes without operations evidence

## Structure

```text
loki/
├── config/
│   └── loki-config.yaml   # Loki config with MinIO, retention, compactor, and ruler settings
├── docker-entrypoint.sh   # Exports MINIO_APP_USER_PASSWORD from Docker Secret
├── Dockerfile             # Builds hy/loki:3.7.3-custom from upstream Loki plus entrypoint
└── README.md              # This file
```

## Service Boundary

| Field | Evidence |
| --- | --- |
| Purpose | Log aggregation and LogQL query backend for the `06-observability` tier |
| Compose service | `loki` in `infra/06-observability/docker-compose.yml` |
| Compose linkage | Declared in `infra/06-observability/docker-compose.yml` and mirrored in `infra/06-observability/docker-compose.dev.yml` |
| Container | `infra-loki` |
| Image | `hy/loki:3.7.3-custom` |
| Runtime user | `10001:10001` |
| Config files | `config/loki-config.yaml`, `Dockerfile`, `docker-entrypoint.sh` |
| Config values | MinIO S3 endpoint `http://minio:9000`, bucket `loki-bucket`, retention `168h`, compactor interval `10m` |
| Config mount | `./loki/config/loki-config.yaml:/etc/loki/loki-config.yaml:ro` |
| Volumes | `loki-data:/loki:rw` |
| Secret refs | `minio_app_user_password` |
| Environment refs | `MINIO_APP_USERNAME` |
| Networks | `infra_net`, `k3d-hyhome` |
| Ports | `${LOKI_HOST_PORT:-3100}:${LOKI_PORT:-3100}` |
| Route | `https://loki.${DEFAULT_URL}` through `gateway-standard-chain@file,sso-errors@file,sso-auth@file` |
| Labels | `traefik.http.routers.loki.*`, `traefik.http.services.loki.loadbalancer.server.port` |
| Healthcheck | `http://127.0.0.1:${LOKI_PORT:-3100}/ready` |
| Operations | [Guide](../../../docs/05.operations/guides/06-observability/loki.md), [Policy](../../../docs/05.operations/policies/06-observability/loki.md), [Runbook](../../../docs/05.operations/runbooks/06-observability/loki.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh), [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with the linked runbook, compose config rendering, service logs, and redacted storage/ingestion evidence |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d loki` | Start Loki from the repository root |
| `docker compose -f infra/06-observability/docker-compose.yml --profile obs restart loki` | Restart Loki after approved config or secret-reference changes |
| `docker compose -f infra/06-observability/docker-compose.yml --profile obs logs -f loki` | Tail Loki logs from the repository root |

## Configuration

### Storage and Retention

- **Bucket**: `loki-bucket`
- **S3 endpoint**: `http://minio:9000`
- **Access key source**: environment reference `MINIO_APP_USERNAME`
- **Secret key source**: Docker Secret `minio_app_user_password`, exported as `MINIO_APP_USER_PASSWORD`
- **Retention**: `retention_enabled: true`, `retention_period: 168h`
- **Compactor**: `compaction_interval: 10m`, `retention_delete_delay: 2h`

### Ingestion and Querying

- Alloy sends logs through `loki.write.local_loki` to `http://loki:3100/loki/api/v1/push`.
- Grafana provisions datasource `Loki` with URL `http://loki:3100`.
- Query through Grafana Explore with low-cardinality labels such as `service_name`, `env`, and `stream`.

## How to Work in This Area

1. Follow the [Loki guide](../../../docs/05.operations/guides/06-observability/loki.md) for usage and query context.
2. Follow the [Loki runbook](../../../docs/05.operations/runbooks/06-observability/loki.md) for readiness, storage, ingestion, restart, and rollback steps.
3. Keep `MINIO_APP_USER_PASSWORD`, rendered environment values, and MinIO credentials out of docs, logs, task evidence, and commit messages.
4. Do not change retention, compactor, MinIO bucket, resource caps, secret references, label cardinality policy, or route middleware without plan/task evidence and rollback notes.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking infrastructure documentation ready.
- Verify readiness with `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps loki` and `docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready`.
- Verify storage and retention config with `rg -n 'bucketnames: loki-bucket|retention_enabled: true|retention_period: 168h|compaction_interval: 10m' infra/06-observability/loki/config/loki-config.yaml`.
- Verify ingestion wiring with `rg -n 'loki.source.docker|loki.write|http://loki:3100/loki/api/v1/push' infra/06-observability/alloy/config/config.alloy`.

## Troubleshooting

- Start with `docker compose -f infra/06-observability/docker-compose.yml --profile obs config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For missing logs, verify Alloy `loki.write` status and Grafana datasource `Loki`.
- For storage failures, inspect redacted Loki log symptoms for MinIO, bucket, retention, compactor, or credential errors.
- For query latency, review label cardinality and avoid promoting high-cardinality fields to labels.

## Related Documents

- [infra/README.md](../../README.md)
- [Operations index](../../../docs/05.operations/README.md)
- [Loki guide](../../../docs/05.operations/guides/06-observability/loki.md)
- [Loki policy](../../../docs/05.operations/policies/06-observability/loki.md)
- [Loki runbook](../../../docs/05.operations/runbooks/06-observability/loki.md)
