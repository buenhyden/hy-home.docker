# Data Tier Guides

> Comprehensive guides for databases, object storage, and persistence engines.

## Overview (KR)

이 디렉토리는 `04-data` 티어의 다양한 데이터 서비스(SQL, NoSQL, Vector, Storage 등)에 대한 설정, 최적화 및 사용 가이드를 포함합니다. 시스템의 영속성 계층을 견고하게 유지하고 어플리케이션과의 원활한 연동을 목표로 합니다.

## Guide Contents

| Document | Purpose |
| :--- | :--- |
| [01.core-dbs.md](./01.core-dbs.md) | Shared Postgres & Valkey Management |
| [02.ha-postgres.md](./02.ha-postgres.md) | Patroni-based High Availability Cluster |
| [03.storage.md](./03.storage.md) | S3-compatible Storage (MinIO, SeaweedFS) |
| [04.specialized-dbs.md](./04.specialized-dbs.md) | MongoDB, Cassandra, InfluxDB, Qdrant, etc. |
| [05.integrated-stacks.md](./05.integrated-stacks.md) | Supabase Stack Management |

## Navigation

- [Infrastructure Source](../../../infra/04-data/README.md)
- [Operational Policies](../../../docs/08.operations/04-data/README.md)
- [Troubleshooting Runbooks](../../../docs/09.runbooks/04-data/README.md)
