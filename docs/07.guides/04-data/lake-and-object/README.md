# Lake and Object Storage Guides

> Guides for data lake and object storage systems.

## Overview

이 디렉토리는 `hy-home.docker`의 데이터 레이크 및 오브젝트 스토리지 관련 가이드를 포함한다. 대용량 비정형 데이터 저장 및 관리를 위한 MinIO와 SeaweedFS의 활용 방법을 안내한다.

## Audience

이 README의 주요 독자:

- Developers using S3 or Filer APIs
- Operators managing storage clusters
- AI Agents looking for storage integration metadata

## Structure

```text
lake-and-object/
├── README.md      # This file
├── minio.md       # MinIO Object Storage Guide
└── seaweedfs.md   # SeaweedFS Storage Guide
```

## Related References

- **Parent**: [04-data Guides](../README.md)
- **Implementation**: [lake-and-object Infrastructure](../../../../infra/04-data/lake-and-object/minio/README.md)
- **Operations**: [lake-and-object Operations](../../../08.operations/04-data/lake-and-object/README.md)
- **Runbooks**: [lake-and-object Runbooks](../../../09.runbooks/04-data/lake-and-object/README.md)

---

## Scope

### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

## How to Work in This Area

1. 관련 `infra/` 서비스 README와 같은 tier의 operation/runbook 문서를 함께 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
