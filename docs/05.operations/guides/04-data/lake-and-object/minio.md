---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/lake-and-object/minio.md -->

# MinIO Object Storage Usage Guide

> Use this guide to understand and verify the root-active MinIO object storage implementation.

---

## Usage

### Overview

MinIO는 `infra/04-data/lake-and-object/minio/docker-compose.yml`에 선언된 S3-compatible object storage다. 현재 root-active compose path는 단일 `minio` service와 bucket/bootstrap job `minio-create-buckets`를 실행하며, optional `docker-compose.cluster.yaml`은 root include에 포함되지 않은 별도 cluster variant다.

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- SRE
- AI Agent

### Purpose

이 가이드는 현재 MinIO service set, Traefik entrypoint, initialized buckets, secret boundary, 일반 확인 절차를 설명한다. 단일 compose와 optional cluster compose를 혼동하지 않도록 한다.

### Prerequisites

- Repository checkout at the project root.
- Docker Compose access on the local or approved infrastructure host.
- Docker Secret files for `minio_root_username`, `minio_root_password`, `minio_app_username`, and `minio_app_user_password`.
- Runtime data directory `${DEFAULT_DATA_DIR}/minio/data-1`.

### Step-by-step Instructions

1. 현재 root-active compose service set을 확인한다.

   ```bash
   docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage config --services
   ```

   Expected services: `minio`, `minio-create-buckets`.

2. 접근 경로를 확인한다.

   - Internal API: `http://minio:${MINIO_PORT:-9000}`
   - Internal console: `http://minio:${MINIO_CONSOLE_PORT:-9001}`
   - External API: `https://minio.${DEFAULT_URL}` through Traefik
   - External console: `https://minio-console.${DEFAULT_URL}` through Traefik

3. 자동 bucket bootstrap 범위를 확인한다.

   `minio-create-buckets` creates `tempo-bucket`, `loki-bucket`, `cdn-bucket`, and `doc-intel-assets`; it also sets anonymous public read only for `cdn-bucket`.

4. 일반 상태를 확인한다.

   ```bash
   docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage ps minio minio-create-buckets
   ```

### Common Pitfalls

- Treating `docker-compose.cluster.yaml` as root-active. It is an optional local compose variant and must be called out separately in evidence.
- Using root credentials for application integration. Use the app user created by `minio-create-buckets` and avoid recording secret values.
- Assuming host ports are published directly. The current root-active compose uses Traefik labels and does not declare direct host ports.
- Documenting secret values or command output that includes credentials.

## Common Checks

- `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage config`
- `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage ps`
- Search paired guide/policy/runbook and infra README for cluster-node assumptions, direct host-port assumptions, direct secret values, or old command forms.
- Expected result: compose renders, documented services match root-active compose, and optional cluster references are clearly marked optional.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](../../../runbooks/04-data/lake-and-object/minio.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/lake-and-object/minio.md)
- [Recovery runbook](../../../runbooks/04-data/lake-and-object/minio.md)
- [Infrastructure service README](../../../../../infra/04-data/lake-and-object/minio/README.md)
