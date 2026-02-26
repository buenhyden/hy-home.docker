---
title: '[ADR-0012] Database High Availability Strategy'
status: 'Approved'
date: '2026-02-26'
deciders: ['Platform Architect', 'Data Architect']
---

# [ADR-0012] Database High Availability Strategy

## Status

Approved

## Context

Standard master-slave replication without automated failover creates high RTO and manual operational overhead. We need a self-healing database tier for production-parity experimentation.

## Decision

We will standardize on **Patroni** (using the Zalando Spilo image) with an **etcd** DCS for PostgreSQL clusters.

## Rationale

- **Automated Failover**: Patroni handles master election and promotion automatically.
- **Self-Healing**: Nodes automatically rejoin and resync based on cluster state in etcd.
- **Dynamic Routing**: Integration with HAProxy ensures clients always connect to the current primary.
- **Modern Support**: Native integration with Kubernetes, though we utilize it here in Docker Compose.

## Consequences

- **Positive**: Near-zero RTO for database failover; reduced manual recovery scripts.
- **Negative**: Increased complexity (requires etcd cluster and HAProxy sidecars).
- **Security**: Requires strict DCS access control.
