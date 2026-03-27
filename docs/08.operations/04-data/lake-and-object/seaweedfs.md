# SeaweedFS Operations Policy

> Governance and operational standards for SeaweedFS distributed storage.
> SeaweedFS 분산 스토리지 거버넌스 및 운영 표준.

---

## Overview

### English
This document defines the operational policies and guidelines to ensure the stability of SeaweedFS. It covers data integrity protection, performance monitoring, backup, and security governance, providing core operational standards for SeaweedFS in the `hy-home.docker` data layer.

### Korean
이 문서는 SeaweedFS의 안정성을 보장하기 위한 운영 정책과 가이드라인을 정의한다. 데이터 무결성 보호, 성능 모니터링, 백업 및 보안 거버넌스를 아우르며, `hy-home.docker` 데이터 레이어의 핵심 운영 기준을 제시한다.

## Policy ID

`OP-DATA-LAKE-SWFS-001`

## Scope

- Management of Master, Volume, Filer, S3, and Mount services.
- Data lifecycle management for the Data Lake assets.
- Governance of `/mnt/seaweedfs` mount points and FUSE interactions.

## Controls & Standards

- **Metadata Integrity**: Filer metadata persistence must be ensured through regular backups (LevelDB/PostgreSQL).
- **Volume Replication**: Minimum replication level of `001` (2 copies in the same DC) is mandatory for production data.
- **Concurrency Control**: Monitor `GOMAXPROCS` and memory usage of the Filer during heavy I/O to prevent bottlenecks.
- **Network Security**: S3 port exposure is restricted to the internal `infra_net`. Remote access requires `security.toml` JWT authentication.

## Monitoring & Alerting

- **Master Status**: Track cluster health via `http://seaweedfs-master:9333/cluster/status`. Alert if free space falls below 20%.
- **Latency**: Alert if individual volume server response time exceeds 500ms.
- **Mount Health**: Monitor FUSE mount container CPU/Memory. Restart container if the mount point becomes stale.

## Backup & Lifecycle

- **Volume Export**: Use `weed export` for periodic archival of volume data to cold storage.
- **Filer Snapshot**: Daily snapshots of the Filer database and metadata volume (`seaweedfs-master-data`).
- **TTL Policies**: Use SeaweedFS TTL features to manage the expiration of log files and temporary artifacts.

## Compliance Requirements

- **Access Audit**: Retain Filer and S3 access logs for at least 90 days.
- **Encryption**: Use SSL/TLS for all S3 interface traffic in staging and production.

## Related Documents

- **Technical Guide**: [seaweedfs.md](../../07.guides/04-data/lake-and-object/seaweedfs.md)
- **Recovery Runbook**: [seaweedfs.md](../../09.runbooks/04-data/lake-and-object/seaweedfs.md)
- **Infrastructure**: [seaweedfs/README.md](../../../infra/04-data/lake-and-object/seaweedfs/README.md)

