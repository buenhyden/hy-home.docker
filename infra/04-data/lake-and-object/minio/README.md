<!-- [ID:04-data:minio] -->
# MinIO Object Storage

> S3-compatible high-performance object storage server.

---

## 1. Context & Objective (KR)

MinIO는 `hy-home.docker` 에코시스템의 기본 오브젝트 스토리지 계층이다. 인프라 워크로드(Loki 로그, Tempo 트레이스)의 영속성을 보장하고, 애플리케이션의 공개 에셋 저장소(CDN) 역할을 수행한다. S3 호환 API를 통해 높은 호환성과 성능을 제공하며, 내부 및 외부 데이터 가용성을 통합 관리한다.

## 2. Requirements & Constraints

- **Engine**: MinIO RELEASE.2025-09-07T16-13-09Z
- **Protocol**: Standard S3-compatible API
- **Deployment**: Docker Compose (Single-node or 4-node cluster)
- **Secrets**: `MINIO_ROOT_USER_FILE` 및 `MINIO_ROOT_PASSWORD_FILE` 필수 사용
- **Ports**: 9000 (API), 9001 (Console)

## 3. Setup & Installation

### 3.1. Single-node Deployment

```bash
# 기본(단일 노드) 서비스 시작
docker compose up -d
```

### 3.2. Cluster Deployment

```bash
# 4노드 클러스터 구성 시작
docker compose -f docker-compose.cluster.yaml up -d
```

## 4. Usage & Integration

### 4.1. Entrypoints

- **API (Internal)**: `http://minio:9000`
- **Dashboard (External)**: `https://minio-console.${DEFAULT_URL}`
- **API (External)**: `https://minio.${DEFAULT_URL}`

### 4.2. Initialized Buckets

배포 시 `minio-create-buckets` 서비스를 통해 다음 버킷이 자동 생성된다:

- `tempo-bucket`, `loki-bucket`: 관측성 데이터
- `cdn-bucket`: 공개 에셋 (Anonymous Read 활성화)
- `doc-intel-assets`: 문서 분석 데이터

## 5. Maintenance & Safety (Maintenance & Safety)

- **Secrets Management**: 루트 자격 증명은 `.env` 및 `.secrets/` 폴더를 통해 안전하게 관리해야 한다.
- **Monitoring**: Prometheus 엔드포인트(`:9000/minio/v2/metrics/cluster`)가 활성화되어 있으며 전역 Grafana 대시보드에서 지표를 확인한다.
- **Health Check**: `curl`을 사용하여 `/minio/health/live` 경로로 상태를 점검한다.

## 6. Known Issues & Troubleshooting

- **Path-Style Access**: 클라이언트가 가상 호스트 기반 접근을 시도할 경우 연결이 실패할 수 있으므로, 반드시 `path-style` 접근을 활성화해야 한다.
- **Quota Management**: 버킷 용량 제한이 설정되지 않았으므로 호스트 디스크 사용량을 주의 깊게 모니터링해야 한다.

## 7. Canonical References

- **Official MinIO Docs**: [https://docs.min.io/](https://docs.min.io/)
- **S3 API Compatibility**: [https://min.io/docs/minio/linux/index.html](https://min.io/docs/minio/linux/index.html)

## 8. Related Documents

- **Guide**: [Technical Guide](../../../../docs/05.operations/guides/04-data/lake-and-object/minio.md)
- **Operation**: [Operations Policy](../../../../docs/05.operations/guides/04-data/lake-and-object/minio.md)
- **Runbook**: [Recovery Runbook](../../../../docs/05.operations/guides/04-data/lake-and-object/minio.md)
- **Spec**: [Data Persistence Spec](../../../../docs/03.specs/04-data/spec.md)

---
Copyright (c) 2026. Licensed under the MIT License.

---

## Overview

`infra/04-data/lake-and-object/minio`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/04-data/lake-and-object/minio/
├── docker-compose.cluster.yaml  # Docker Compose 정의
├── docker-compose.yml  # Docker Compose 정의
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related References

- [infra/README.md](../../../README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
