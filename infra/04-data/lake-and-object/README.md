# Lake & Object Storage (04-data/lake-and-object)

> 데이터 레이크 및 오브젝트 스토리지 서비스 / Data Lake and Object Storage Services

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 데이터 레이크 및 오브젝트 스토리지 서비스를 위한 구성을 포함합니다. 비정형 데이터, 파일, 백업 아카이브를 위한 대용량 스토리지 계층입니다.

## Audience

이 README의 주요 독자:

- 인프라를 배포하고 관리하는 **Operators**
- 스토리지 서비스를 연동하는 **Developers**
- 자동화된 운영 작업을 수행하는 **AI Agents**

## Scope

### In Scope

- MinIO S3 호환 오브젝트 스토리지 구성
- SeaweedFS 분산 파일 시스템 구성
- 버킷 정책, 접근 제어, 시크릿 마운트

### Out of Scope

- 애플리케이션 레벨 데이터 모델링
- 백업 정책 정의 (`docs/05.operations/policies/04-data/` 담당)

## Structure

```text
lake-and-object/
├── minio/        # MinIO S3-compatible object storage
├── seaweedfs/    # SeaweedFS distributed file system
└── README.md     # This file
```

## Related Documents

- [infra/04-data/README.md](../README.md)
- [docs/03.specs/04-data/README.md](../../../docs/03.specs/04-data/README.md)
- [docs/05.operations/guides/04-data/](../../../docs/05.operations/guides/04-data/)
- [secrets/storage/](../../../secrets/storage/)
