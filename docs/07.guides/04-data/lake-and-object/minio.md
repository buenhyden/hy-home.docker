# MinIO Object Storage Guide

> S3-compatible high-performance object storage server.

---

## Overview (KR)

이 문서는 MinIO 오브젝트 스토리지에 대한 기술 가이드를 제공한다. `hy-home.docker` 환경에서 MinIO를 연결하고 사용하는 방법, 버킷 관리 절차 및 아키텍처적 통합 방안을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator

## Purpose

이 가이드는 사용자가 MinIO 서비스를 이해하고, 애플리케이션 또는 다른 인프라 서비스와 통합하며, 기본적인 관리 작업을 수행할 수 있도록 돕는다.

## Prerequisites

- `infra/04-data/lake-and-object/minio` 서비스가 실행 중이어야 함.
- S3 SDK (AWS SDK 등) 또는 MinIO Client (`mc`)가 설치되어야 함.

## Step-by-step Instructions

### 1. 연결 정보 확인 (Connection Info)

- **Internal API**: `http://minio:9000`
- **Internal Console**: `http://minio:9001`
- **External API**: `https://minio.${DEFAULT_URL}`
- **External Console**: `https://minio-console.${DEFAULT_URL}`

### 2. 버킷 초기화 및 자동화 (Bucket Initialization)

MinIO 배포 시 `minio-create-buckets` 작업이 자동으로 실행되어 다음 버킷을 생성한다.
- `tempo-bucket`: Tempo 분산 추적 데이터 저장
- `loki-bucket`: Loki 로그 데이터 저장
- `cdn-bucket`: 공개 에셋 저장소 (Public/Anonymous Read 활성화)
- `doc-intel-assets`: 문서 지능화 작업을 위한 자산 저장소

### 3. MinIO Client (mc) 사용 (Using mc)

원격 관리를 위해 `mc`를 설정한다.
```bash
# 별칭 설정
mc alias set myminio https://minio.${DEFAULT_URL} [ACCESS_KEY] [SECRET_KEY]

# 버킷 리스트 확인
mc ls myminio

# 데이터 복사 예시
mc cp local-file.txt myminio/cdn-bucket/
```

### 4. 애플리케이션 연동 (App Integration)

애플리케이션에서 AWS SDK 등을 사용하여 연결할 때는 `path-style` 접근 방식을 활성화해야 한다.
```javascript
const s3 = new AWS.S3({
  endpoint: 'http://minio:9000',
  s3ForcePathStyle: true, // 필수 설정
  signatureVersion: 'v4'
});
```

## Common Pitfalls

- **Path-Style Access**: MinIO는 기본적으로 가상 호스트 기반 접근이 아닌 경로 기반 접근을 사용하므로 클라이언트 설정에서 반드시 활성화해야 한다.
- **Root Credentials**: `MINIO_ROOT_USER`와 `MINIO_ROOT_PASSWORD`는 서비스 배포용 비밀번호이므로, 애플리케이션 연동 시에는 별도의 IAM 사용자나 App Credentials를 사용하는 것을 권장한다.

## Related Documents

- **Spec**: [Data Persistence Spec](../../../../docs/04.specs/04-data/spec.md)
- **Operation**: [MinIO Operations Policy](../../../../docs/08.operations/04-data/lake-and-object/minio.md)
- **Runbook**: [MinIO Recovery Runbook](../../../../docs/09.runbooks/04-data/lake-and-object/minio.md)

