---
title: '[ARD-DATA-01] Data Platform Architecture'
status: 'Draft'
version: 'v0.1.0'
owner: 'Data Architect'
tags: ['ard', 'architecture', 'data', 'postgresql', 'ha']
---

# [ARD-DATA-01] Data Platform Architecture

## 1. Overview

This platform provides a highly available, self-healing PostgreSQL environment using the Zalando Spilo image (Patroni + PostgreSQL 17), backed by an etcd Distributed Configuration Store (DCS).

## 2. Component Diagram

```mermaid
graph TD
    Client[Client Apps] --> HAProxy[pg-router HAProxy]
    HAProxy -->|Port 15432: Write| Master[PG Primary]
    HAProxy -->|Port 15433: Read| Replica[PG Replicas]
    
    subgraph "DCS Quorum"
        etcd1[etcd-1] --- etcd2[etcd-2] --- etcd3[etcd-3]
    end
    
    subgraph "PostgreSQL HA Cluster"
        Master --- etcd1
        Replica --- etcd1
    end
```

## 3. Technology Choice: Patroni

- **Choice**: Patroni (Python-based cluster manager).
- **Rationale**: Automates failover, simplifies replication setup, and integrates natively with etcd/Kubernetes environments.

## 4. Availability & Reliability

- **Clustering**: 3-node PostgreSQL cluster with 1 Primary and 2 synchronous/asynchronous standbys.
- **Failover**: Automated master election via Patroni Leader Election in etcd.
- **Routing**: HAProxy dynamically updates backend list based on REST API health checks (`/primary`, `/standby`).

## 5. Persistence Strategy

- **Volumes**: Persistent volumes mounted to `/home/postgres/pgdata`.
- **Backups**: Standard WAL-G or pgBackRest integration patterns (TBD).
