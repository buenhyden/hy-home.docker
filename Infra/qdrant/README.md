# Qdrant

## Overview

A Vector Database for AI applications, used here primarily for RAG (Retrieval-Augmented Generation) with Ollama.

## Service Details

- **Image**: `qdrant/qdrant:v1.16.3`
- **Port**: `${QDRANT_PORT}` (6333)
- **Volumes**: Data persisted in `qdrant-data`.

## Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `QDRANT__TELEMETRY_DISABLED` | Disable usage reporting | `false` |

## Network

Configured with a static IP on `infra_net`.

| Service | IP Address |
| :--- | :--- |
| `qdrant` | `172.19.0.41` |

## Traefik Configuration

- **Domain**: `qdrant.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS enabled)
- **Use**: Exposes the Qdrant Web UI (Dashboard).
