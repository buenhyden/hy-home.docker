# Data Operations Policy (04-data)

> Governance for Persistence, Backup, and Security (04-data)

## 1. Context & Objective

This policy defines the operational standards and data protection requirements for the `hy-home.docker` data infrastructure layer (04-data). Our goal is to ensure maximum durability, availability, and security for all persistent workloads.

- **Primary Goal**: Zero data loss for core databases.
- **Availability Target**: 99.9% uptime for HA clusters.
- **Security Mandate**: End-to-end encryption and secret management.

## 2. Infrastructure Standards

### 2.1 Persistence Hierarchy

All persistent data must be stored within the standardized `${DEFAULT_DATA_DIR}` hierarchy, isolated by service name.

- **High-Performance (SSD)**: PostgreSQL, OpenSearch, and Qdrant must utilize direct host SSD mounts.
- **Distributed (HDD/Hybrid)**: SeaweedFS and Cassandra may utilize larger volume mounts.

### 2.2 Volume Isolation

Docker volumes must be named following the pattern `${SERVICE_NAME}-data` to ensure clear mapping during migration or backup.

## 3. Maintenance & Safety

### 3.1 Backup Strategy

- **SQL (PostgreSQL)**: Daily logical dumps (`pg_dump`) at 03:00 KST, complemented by weekly physical snapshots.
- **NoSQL & Object Storage**: Incremental snapshots or integrated replication jobs.
- **Retention**: Minimum 30-day retention period for all production database backups.

### 3.2 Secret Management

Database credentials must **NEVER** be exposed as plain-text environment variables. Use Docker secrets or Vault integration provided by the `03-security` tier.

## 4. Operational Procedures

### Health Monitoring

Infrastructure monitoring (Prometheus/Grafana) must track:

- **Disk Usage**: Alert at 80% capacity.
- **IOPS/Latency**: Detect storage bottlenecks early.
- **Replication Lag**: Monitor HA clusters for consistency synchronization.

### Scaling & Migration

Vertical scaling (Resource limits) should be performed during maintenance windows. Horizontal scaling (Clustering) is the preferred method for increasing throughput.

## 5. Security & Compliance

- **Encryption at Rest**: Mandatory for PII and sensitive application data.
- **TLS 1.3**: Required for all internal and external data traffic.
- **Audit Logging**: Enable access logs for administrative operations on core databases.

## 6. Related Documentation

- [Technical Guides](../../07.guides/04-data/README.md)
- [Recovery Runbooks](../../09.runbooks/04-data/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
