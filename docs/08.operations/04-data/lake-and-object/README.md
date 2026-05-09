# Lake and Object Storage Operations

> Operations policies for data lake and object storage systems.
> 데이터 레이크 및 오브젝트 스토리지 운영 정책.

---

## Overview

This directory contains operations policies for data lake and object storage systems, ensuring data persistence, security, and availability.

이 디렉토리는 데이터 지속성, 보안 및 가용성을 보장하기 위한 데이터 레이크 및 오브젝트 스토리지 운영 정책을 포함한다.

## Direct Documents

- [MinIO Object Storage Policy](minio.md)
- [SeaweedFS Distributed Storage Policy](seaweedfs.md)

## Related References

- [04-data Operations Index](../README.md)
- [Lake and Object Technical Guides](../../../07.guides/04-data/lake-and-object/README.md)
- [Lake and Object Recovery Runbooks](../../../09.runbooks/04-data/lake-and-object/README.md)

---

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 운영 정책과 controls
- 허용/금지/예외 기준
- 검증 방법과 review cadence

### Out of Scope

- 단계별 복구 절차
- 튜토리얼 문서
- incident timeline

## Structure

```text
docs/08.operations/04-data/lake-and-object/
├── minio.md  # 문서
├── README.md  # This file
└── seaweedfs.md  # 문서
```

## How to Work in This Area

1. 같은 서비스의 guide와 runbook을 확인해 정책과 실행 절차가 분리되어 있는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
