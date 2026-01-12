# Qdrant

## Overview

Qdrant is a vector similarity search engine and vector database.

## Services

- **qdrant**: Qdrant server.
  - API Port: `${QDRANT_PORT}` (6333)
  - URL: `https://qdrant.${DEFAULT_URL}`

## Configuration

### Volumes

- `qdrant-data`: `/qdrant/storage`

## Networks

- `infra_net`
  - IP: `172.19.0.41`

## Traefik Routing

- **Domain**: `qdrant.${DEFAULT_URL}`
