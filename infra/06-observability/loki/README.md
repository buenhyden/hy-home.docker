# Loki

> High-availability log aggregation system inspired by Prometheus.

## Overview

Loki is the log storage engine for the hy-home.docker ecosystem. It is designed to be cost-effective by indexing only metadata (labels) and storing compressed log chunks in an S3-compatible backend (MinIO).

## Structure

```text
loki/
├── config/
│   └── loki-config.yaml # Master configuration file
├── Dockerfile          # Custom Loki image build
├── docker-entrypoint.sh # Entrypoint wrapper
└── README.md           # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Engine | hy/loki:3.6.6-custom | Log storage & query |
| Storage | MinIO (S3) | Chunk/Index persistence |
| Query | LogQL | Advanced log filtering |

## Configuration

- **Config File**: `config/loki-config.yaml`.
- **Backend**: Configured to use the `04-data` tier's MinIO service.
- **Retention**: 7 days (configured in YAML).
- **Secrets**: Uses `minio_app_user_password` for S3 authentication.

## Persistence

- **Chunks/Index**: Stored in MinIO buckets (`loki-bucket`).
- **Local Data**: Persistent volume `loki-data` (mounted to `/loki`) for WAL/temp files.

## Operational Status

> [!IMPORTANT]
> Ensure MinIO is healthy before starting Loki, as it depends on S3 availability for operation.

---

Copyright (c) 2026. Licensed under the MIT License.
