# MinIO Object Storage

> S3-compatible high-performance object storage server.

## Overview

MinIO serves as the primary object storage layer for the `hy-home.docker` ecosystem. It provides persistence for infrastructure workloads (Loki logs, Tempo traces) and serves as a public asset repository for applications.

## Audience

이 README의 주요 독자:

- 인프라를 배포하고 관리하는 **Operators**
- S3 저장소를 사용하는 **Developers**
- 시스템 상태를 점검하는 **AI Agents**

## Scope

### In Scope

- MinIO 단일 노드 및 클러스터 배포 구성
- `minio-init`을 통한 버킷 자동 초기화 (Loki, Tempo, CDN)
- S3 호환 API 및 Console 액세스 설정

### Out of Scope

- 개별 버킷 내 데이터의 애플리케이션 레벨 관리
- MinIO Client (`mc`)의 상세 사용법 (Technical Guide 참조)
- 세부 백업 및 복구 절차 (Operation/Runbook 참조)

## Structure

```text
minio/
├── README.md                  # This file
├── docker-compose.yml         # Single-node deployment
└── docker-compose.cluster.yaml # 4-node cluster deployment
```

## How to Work in This Area

1. 배포 전 `MINIO_ROOT_USER_FILE` 및 `MINIO_ROOT_PASSWORD_FILE` 비밀번호 파일이 준비되었는지 확인합니다.
2. 단일 노드 테스트 시 `docker compose up -d`를 사용합니다.
3. 운영 환경 클러스터 배포 시 `docker-compose.cluster.yaml` 설정을 검토합니다.
4. 버킷 정책 변경 시 `minio-create-buckets` 서비스의 로직을 수정합니다.

## Available Scripts

| Command                               | Description                     |
| ------------------------------------- | ------------------------------- |
| `docker compose up -d`                | 단일 노드 MinIO 서비스 시작     |
| `docker compose -f docker-compose.cluster.yaml up -d` | 4노드 클러스터 MinIO 시작 |
| `docker compose logs -f minio`        | MinIO 서버 로그 실시간 확인     |
| `docker compose ps`                   | 서비스 상태 및 헬스체크 확인    |

## Tech Stack

| Category   | Technology   | Notes                               |
| ---------- | ------------ | ----------------------------------- |
| Engine     | MinIO        | RELEASE.2025-09-07T16-13-09Z        |
| Protocol   | S3           | Standard S3-compatible API          |
| Deployment | Docker       | Compose-based deployment            |
| UI         | Console      | Port 9001 (Internal/External entry) |

## Related References

- **Guide**: [Technical Guide](../../../../docs/07.guides/04-data/lake-and-object/minio.md)
- **Operation**: [Operations Policy](../../../../docs/08.operations/04-data/lake-and-object/minio.md)
- **Runbook**: [Recovery Runbook](../../../../docs/09.runbooks/04-data/lake-and-object/minio.md)
- **Related Spec**: [Data Persistence Spec](../../../../docs/04.specs/04-data/spec.md)

---
Copyright (c) 2026. Licensed under the MIT License.
