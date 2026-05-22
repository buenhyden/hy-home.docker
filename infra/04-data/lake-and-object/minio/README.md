<!-- [ID:04-data:minio] -->
# MinIO Object Storage

> S3-compatible high-performance object storage server.

---

## Overview

MinIO는 `hy-home.docker` 에코시스템의 기본 오브젝트 스토리지 계층이다. 인프라 워크로드(Loki 로그, Tempo 트레이스)의 영속성을 보장하고, 애플리케이션의 공개 에셋 저장소(CDN) 역할을 수행한다. S3 호환 API를 통해 높은 호환성과 성능을 제공하며, 내부 및 외부 데이터 가용성을 통합 관리한다.

## Audience

이 README의 주요 독자:

- Infrastructure Operators
- Application Developers using S3-compatible storage
- AI Agents

## Scope

### In Scope

- MinIO single-node and cluster compose entrypoints
- Non-secret runtime settings, exposed API/console ports, and bucket initialization behavior
- Links to canonical guide, policy, runbook, and data spec

### Out of Scope

- Secret values, root credentials, access keys, and private bucket contents
- Application-level object lifecycle design
- SeaweedFS configuration

## Structure

```text
minio/
├── docker-compose.yml          # Single-node MinIO service definition
├── docker-compose.cluster.yaml # Optional cluster variant
├── Dockerfile                  # Custom image/build context when used
└── README.md                   # This file
```

## How to Work in This Area

1. Review the linked operations guide, policy, and runbook before changing MinIO configuration.
2. Keep credentials in Docker Secrets and document only secret names or mounted paths.
3. Distinguish the root-active single-node compose path from the optional cluster variant when recording evidence.
4. After compose or bucket initialization changes, run the validation commands listed below.

## Requirements & Constraints

- **Engine**: MinIO RELEASE.2025-09-07T16-13-09Z
- **Protocol**: Standard S3-compatible API
- **Deployment**: Docker Compose (Single-node or 4-node cluster)
- **Secrets**: `MINIO_ROOT_USER_FILE` 및 `MINIO_ROOT_PASSWORD_FILE` 필수 사용
- **Ports**: 9000 (API), 9001 (Console)

## Setup & Installation

### Single-node Deployment

```bash
# 기본(단일 노드) 서비스 시작
docker compose up -d
```

### Cluster Deployment

```bash
# 4노드 클러스터 구성 시작
docker compose -f docker-compose.cluster.yaml up -d
```

## Usage & Integration

### Entrypoints

- **API (Internal)**: `http://minio:9000`
- **Dashboard (External)**: `https://minio-console.${DEFAULT_URL}`
- **API (External)**: `https://minio.${DEFAULT_URL}`

### Initialized Buckets

배포 시 `minio-create-buckets` 서비스를 통해 다음 버킷이 자동 생성된다:

- `tempo-bucket`, `loki-bucket`: 관측성 데이터
- `cdn-bucket`: 공개 에셋 (Anonymous Read 활성화)
- `doc-intel-assets`: 문서 분석 데이터

## Maintenance & Safety

- **Secrets Management**: 루트 자격 증명은 `.env` 키와 Docker Secrets 파일 참조를 통해 안전하게 관리해야 하며, secret 값 원문은 문서화하지 않는다.
- **Monitoring**: Prometheus 엔드포인트(`:9000/minio/v2/metrics/cluster`)가 활성화되어 있으며 전역 Grafana 대시보드에서 지표를 확인한다.
- **Health Check**: `curl`을 사용하여 `/minio/health/live` 경로로 상태를 점검한다.

## Known Issues & Troubleshooting

- **Path-Style Access**: 클라이언트가 가상 호스트 기반 접근을 시도할 경우 연결이 실패할 수 있으므로, 반드시 `path-style` 접근을 활성화해야 한다.
- **Quota Management**: 버킷 용량 제한이 설정되지 않았으므로 호스트 디스크 사용량을 주의 깊게 모니터링해야 한다.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify bucket access by checking `docker logs minio | grep -i 'error\|warn'` and confirming the MinIO console is reachable.
- Confirm S3 API health by running a test upload/download against the MinIO endpoint.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For credential errors: verify `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` secrets are correctly injected and match the client configuration.
- For bucket access errors: confirm bucket policies and IAM permissions are correctly configured in the MinIO console.
- For storage issues: confirm the MinIO data volume is mounted and has sufficient disk space.

## Canonical References

- **Official MinIO Docs**: [https://docs.min.io/](https://docs.min.io/)
- **S3 API Compatibility**: [https://min.io/docs/minio/linux/index.html](https://min.io/docs/minio/linux/index.html)

## Related Documents

- **Guide**: [Technical Guide](../../../../docs/05.operations/guides/04-data/lake-and-object/minio.md)
- **Operation**: [Operations Policy](../../../../docs/05.operations/policies/04-data/lake-and-object/minio.md)
- **Runbook**: [Recovery Runbook](../../../../docs/05.operations/runbooks/04-data/lake-and-object/minio.md)
- **Spec**: [Data Persistence Spec](../../../../docs/03.specs/04-data/spec.md)

---
Copyright (c) 2026. Licensed under the MIT License.
