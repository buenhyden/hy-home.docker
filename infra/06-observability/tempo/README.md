# Tempo

> High-volume, low-cost distributed tracing backend.

## Overview

Tempo is the distributed tracing backend for the hy-home.docker ecosystem. It is optimized for high-volume trace ingestion and cost-effective storage by utilizing an S3-compatible backend (MinIO).

## Structure

```text
tempo/
├── config/
│   └── tempo.yaml       # Master configuration file
├── Dockerfile          # Custom Tempo image build
├── docker-entrypoint.sh # Entrypoint wrapper
└── README.md           # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Engine | hy/tempo:2.10.1-custom | Trace storage & query |
| Storage | MinIO (S3) | Block/Index persistence |
| Ingestion | Alloy (OTLP) | Trace collection pipeline |

## Configuration

- **Config File**: `config/tempo.yaml`.
- **Backend**: Configured to use the `04-data` tier's MinIO service.
- **Retention**: 24h (configured via `compactor`).
- **Secrets**: Uses `minio_app_user_password` for S3 authentication.

## Persistence

- **Traces**: Stored in MinIO buckets (`tempo-bucket`).
- **Local Data**: Persistent volume `tempo-data` (mounted to `/var/tempo`) for WAL.

## Operational Status

> [!TIP]
> Use **Alloy** as the primary OTLP ingestion point. Applications should not target Tempo directly to allow for better batching and load balancing.

---

Copyright (c) 2026. Licensed under the MIT License.
