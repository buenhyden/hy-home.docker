<!-- [ID:04-data:minio] -->
# MinIO Object Storage

> S3-compatible object storage for observability buckets and public asset storage.

## Overview

MinIO is the root-active object storage service for `hy-home.docker`. The active compose path is `infra/04-data/lake-and-object/minio/docker-compose.yml`, which runs a single `minio` service plus `minio-create-buckets` bootstrap job. The 4-node `docker-compose.cluster.yaml` remains an optional local variant and must not be described as part of the root include unless explicitly invoked.

## Audience

이 README의 주요 독자:

- Infrastructure Operators
- Application Developers using S3-compatible storage
- SREs
- AI Agents

## Scope

### In Scope

- Root-active MinIO service and bucket bootstrap behavior
- Docker Secret names and mount paths, without secret values
- Traefik API/console route surface
- Optional cluster variant identification

### Out of Scope

- Secret values, access keys, and private bucket contents
- Application-level object lifecycle design
- SeaweedFS configuration
- Treating `docker-compose.cluster.yaml` as root-active infrastructure

## Structure

```text
minio/
├── docker-compose.yml          # Root-active single-node service plus bootstrap job
├── docker-compose.cluster.yaml # Optional 4-node local cluster variant
├── Dockerfile                  # Optional image/build context
└── README.md                   # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | MinIO Object Storage service leaf in `04-data`; root-active services: `minio`, `minio-create-buckets`; optional local cluster variant: `docker-compose.cluster.yaml` |
| Config files | `docker-compose.yml`, `docker-compose.cluster.yaml`, `Dockerfile` |
| Config values | env keys: `MINIO_ROOT_USER_FILE`, `MINIO_ROOT_PASSWORD_FILE`, `MINIO_PROMETHEUS_AUTH_TYPE`, `MINIO_API_ROOT_ACCESS`; profiles: `storage`, `obs`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lake-and-object/minio/docker-compose.yml`; cluster variant is local only |
| Networks | `infra_net`; static IPs: `172.19.0.29` (`minio`), `172.19.0.39` (`minio-create-buckets`) |
| Volumes | `minio-data:/data:rw`; bind source `${DEFAULT_DATA_DIR}/minio/data-1` |
| Ports | Direct host `ports` not declared; Traefik routes API and console to `${MINIO_PORT:-9000}` and `${MINIO_CONSOLE_PORT:-9001}` |
| Labels | `hy-home.tier`, Traefik API route `minio.${DEFAULT_URL}`, Traefik console route `minio-console.${DEFAULT_URL}` |
| Secret refs | `minio_root_username`, `minio_root_password`, `minio_app_username`, `minio_app_user_password`; mounted under `/run/secrets/` |
| Healthcheck | Compose healthcheck declared for `minio`; not declared for `minio-create-buckets` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/lake-and-object/minio.md), [Policy](../../../../docs/05.operations/policies/04-data/lake-and-object/minio.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/lake-and-object/minio.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Review the linked operations guide, policy, and runbook before changing MinIO configuration.
2. Keep credentials in Docker Secrets and document only secret names or mounted paths.
3. Distinguish the root-active single-node compose path from the optional cluster variant when recording evidence.
4. After compose or bucket initialization changes, run the validation commands listed below.

## Runtime Surface

| Surface | Current Evidence |
| --- | --- |
| Image | `minio/minio:RELEASE.2025-09-07T16-13-09Z` |
| Root-active services | `minio`, `minio-create-buckets` |
| API route | `https://minio.${DEFAULT_URL}` |
| Console route | `https://minio-console.${DEFAULT_URL}` |
| Bootstrap buckets | `tempo-bucket`, `loki-bucket`, `cdn-bucket`, `doc-intel-assets` |
| Public bucket policy | `cdn-bucket` anonymous public read is set by `minio-create-buckets` |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Validate this service with `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage config`.
- Verify status with `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage ps minio minio-create-buckets`.

## Troubleshooting

- Start with compose render and service status before changing configuration or secrets.
- Check `minio` and `minio-create-buckets` logs without copying secret-bearing output.
- For credential errors, verify Docker Secret file presence and mounted paths; do not print secret values.
- For bucket access errors, confirm bootstrap job evidence and linked operations runbook before changing bucket policy.

## Related Documents

- **Guide**: [Technical Guide](../../../../docs/05.operations/guides/04-data/lake-and-object/minio.md)
- **Policy**: [Operations Policy](../../../../docs/05.operations/policies/04-data/lake-and-object/minio.md)
- **Runbook**: [Recovery Runbook](../../../../docs/05.operations/runbooks/04-data/lake-and-object/minio.md)
- **Spec**: [Data Persistence Spec](../../../../docs/03.specs/04-data/spec.md)

---
Copyright (c) 2026. Licensed under the MIT License.
