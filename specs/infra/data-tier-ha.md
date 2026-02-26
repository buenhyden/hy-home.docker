---
title: '[SPEC-DATA-01] Data Tier HA Technical Specification'
status: 'Draft'
version: 'v0.1.0'
owner: 'Data Engineer'
tags: ['spec', 'technical', 'data', 'postgresql', 'ha']
---

# [SPEC-DATA-01] Data Tier HA Technical Specification

## 1. Overview

This specification details the technical implementation of the Patroni-managed PostgreSQL cluster.

## 2. Cluster Configuration (Patroni)

- **DCS Type**: `etcd` (3-node quorum)
- **Node Names**: `pg-0`, `pg-1`, `pg-2`
- **REST API Port**: `8008` (Patroni monitoring)

## 3. Healthcheck Logic

| Endpoint | Method | Expected Status | Description |
| --- | --- | --- | --- |
| `/primary` | GET | 200 OK | Node is the current Primary |
| `/replica` | GET | 200 OK | Node is a healthy Replica |
| `/health` | GET | 200 OK | Patroni local agent is alive |

## 4. HAProxy Routing (pg-router)

- **Writer Backend (15432)**:
  - Check: `option httpchk GET /primary`
  - Mode: `tcp`
- **Reader Backend (15433)**:
  - Check: `option httpchk GET /replica`
  - Mode: `tcp`

## 5. Persistence & Recovery

- **Data Mount**: `/home/postgres/pgdata`
- **Init Script**: `scripts/spilo-entrypoint-with-secrets.sh`
- **Secret Integration**: PGPASSWORD and User credentials read from `/run/secrets/`.
