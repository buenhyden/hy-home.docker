# Qdrant

## Overview

A Vector Database for AI applications, used here primarily for **RAG (Retrieval-Augmented Generation)** with Ollama.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `qdrant` | `qdrant/qdrant:v1.16.3` | Vector Database |

## Networking

Service runs on `infra_net` with a static IP.

| Service | Static IP | Internal Port | Host Port | Traefik Domain |
| :--- | :--- | :--- | :--- | :--- |
| `qdrant` | `172.19.0.41` | `${QDRANT_PORT}` | `${QDRANT_HOST_PORT}` | `qdrant.${DEFAULT_URL}` |

## Persistence

- **Data**: `qdrant-data` → `/qdrant/storage`

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `QDRANT__TELEMETRY_DISABLED` | Disable usage reporting | `false` |

## Traefik Integration

Services are exposed via Traefik with TLS enabled (`websecure`).

- **Dashboard**: `qdrant.${DEFAULT_URL}` (Web UI)

## Usage

1. **Dashboard**: Access `https://qdrant.${DEFAULT_URL}`.
2. **API (Internal)**: `http://qdrant:6333` (Used by Open WebUI).
3. **API (External)**: `localhost:${QDRANT_HOST_PORT}`.
