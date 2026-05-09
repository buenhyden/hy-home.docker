# Lake and Object Storage Recovery Runbooks

> Operational procedures for data lake and object storage systems.
> 데이터 레이크 및 오브젝트 스토리지 장애 대응 및 복구 절차.

---

## Overview

This directory contains recovery runbooks for data lake and object storage systems, providing step-by-step procedures for emergency response and service restoration.

이 디렉토리는 데이터 레이크 및 오브젝트 스토리지 시스템의 장애 대응을 위한 실행 절차(Runbook)를 포함하며, 긴급 상황 시 서비스 복구를 위한 수동 조치 단계를 제공한다.

## Direct Documents

- [MinIO Recovery Runbook](minio.md)
- [SeaweedFS Recovery Runbook](seaweedfs.md)

## Related References

- [04-data Runbooks Index](../README.md)
- [Lake and Object Technical Guides](../../../07.guides/04-data/lake-and-object/README.md)
- [Lake and Object Operations Policies](../../../08.operations/04-data/lake-and-object/README.md)

---

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

## Structure

```text
docs/09.runbooks/04-data/lake-and-object/
├── minio.md  # 문서
├── README.md  # This file
└── seaweedfs.md  # 문서
```

## How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
