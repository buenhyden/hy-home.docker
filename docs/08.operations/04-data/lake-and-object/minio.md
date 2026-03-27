# MinIO Object Storage Operations Policy

> S3-compatible object storage operations and governance.
> S3 호환 오브젝트 스토리지 운영 및 거버넌스 정책.

---

## Overview

### English
This document defines the operational policies for MinIO Object Storage. It regulates backup strategies for data persistence, security control standards, system availability maintenance, and performance monitoring methods within the `hy-home.docker` environment.

### Korean
이 문서는 MinIO 오브젝트 스토리지의 운영 정책을 정의한다. `hy-home.docker` 환경 내에서 데이터 지속성 보장을 위한 백업 전략, 보안 통제 기준, 시스템 가용성 유지 및 성능 모니터링 방법을 규정한다.

## Policy ID

`OP-DATA-LAKE-MINIO-001`

## Scope

- MinIO Cluster and Single Node data volume protection.
- Global and application-level Access Control (IAM).
- Storage quota management and monitoring thresholds.
- Manual and automated bucket lifecycle management.

## Controls & Standards

- **Secret Management**: Must use `MINIO_ROOT_USER_FILE` and `MINIO_ROOT_PASSWORD_FILE`. Direct use of plaintext credentials in environment variables is prohibited in production.
- **Monitoring**: Prometheus endpoint must be enabled and integrated with the global monitoring system (Grafana/Prometheus).
- **Data Protection**: Critical data buckets must have periodic backups enabled using `mc mirror` or server-side replication.
- **Access Control**: Follow the Principle of Least Privilege (PoLP). Application-specific service accounts must be used instead of root credentials.

## Monitoring & Alerting

- **Health Check**: Monitor `/_minio/health/live` and `/_minio/health/ready` endpoints.
- **Metrics**: Track `minio_disk_storage_used_bytes` and `minio_disk_storage_free_bytes`. Alert if free space is less than 15%.
- **Uptime**: Alert if the MinIO service is unresponsive for more than 5 minutes.

## Backup & Lifecycle

- **Volume Backup**: Nightly backups of the `/data` volume using filesystem snapshots or `mc mirror` to an offsite location.
- **Version Control**: Enable Object Locking and Versioning for critical production buckets to prevent accidental deletion.
- **Retention**: Define lifecycle rules for temporary buckets (e.g., auto-delete after 24 hours for `tmp-` prefix).

## Compliance Requirements

- **Audit Logs**: Access logs must be retained for at least 90 days for compliance auditing.
- **Encryption**: Enable Server-Side Encryption (SSE) for sensitive data buckets.
- **Public Access**: Public access remains disabled by default. Exceptions for CDN/Public assets require explicit approval.

## Related Documents

- **Technical Guide**: [minio.md](../../../07.guides/04-data/lake-and-object/minio.md)
- **Recovery Runbook**: [minio.md](../../../09.runbooks/04-data/lake-and-object/minio.md)
- **Infrastructure**: [minio/README.md](../../../../infra/04-data/lake-and-object/minio/README.md)

