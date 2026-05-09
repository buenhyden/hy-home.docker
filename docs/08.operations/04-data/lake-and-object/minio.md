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

---

## Overview (KR)

이 문서는 `docs/08.operations/04-data/lake-and-object/minio.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
