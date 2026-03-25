# Data Operations (04-data)

> Operational policies for persistence, backup, and high availability.

## Overview

This document defines the governance for all data services within `hy-home.docker`, ensuring data integrity, residency, and recovery readiness.

## Core Policies

### 1. Data Residency

- All persistence volumes MUST be mounted under `${DEFAULT_DATA_DIR}`.
- Management-specific databases MUST reside under `${DEFAULT_MANAGEMENT_DIR}`.

### 2. High Availability (HA) Standards

- Core SQL databases (Postgres) MUST utilize Patroni for consensus and automated failover.
- Search engines (OpenSearch) and NoSQL (MongoDB) MUST utilize replica sets with a minimum of 3 nodes.

### 3. Backup & Retention

- **Frequency**: Daily snapshots for core databases.
- **Retention**: 30 days for production data, 7 days for development/staging.
- **Verification**: Restoration tests MUST be performed monthly.

## Roles & Responsibilities

- **DevOps**: Responsible for infrastructure uptime and backup automation.
- **Developers**: Responsible for schema migrations and data model sanity.

---

## Navigation

- [Infrastructure Source](../../../infra/04-data/README.md)
- [Guides](../../../docs/07.guides/04-data/README.md)
- [Emergency Runbook](../../../docs/09.runbooks/04-data/README.md)
