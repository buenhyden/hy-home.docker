# Lake and Object Storage Operations

> Operations policies for data lake and object storage systems.
> 데이터 레이크 및 오브젝트 스토리지 운영 정책.

---

## Overview

This directory contains operations policies for data lake and object storage systems, ensuring data persistence, security, and availability.

이 디렉토리는 데이터 지속성, 보안 및 가용성을 보장하기 위한 데이터 레이크 및 오브젝트 스토리지 운영 정책을 포함한다.

## Direct Documents

- [MinIO Object Storage Policy](./minio.md)
- [SeaweedFS Distributed Storage Policy](./seaweedfs.md)

## Related References

- [04-data Operations Index](../README.md)
- [Lake and Object Technical Usages](./README.md)
- [Lake and Object Recovery Procedures](./README.md)

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
docs/05.operations/04-data/lake-and-object/
├── minio.md  # 문서
├── README.md  # This file
└── seaweedfs.md  # 문서
```

## How to Work in This Area

1. 같은 서비스의 guide와 runbook을 확인해 정책과 실행 절차가 분리되어 있는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Usage

> Migrated from `docs/05.operations/04-data/lake-and-object/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Lake and Object Storage Usages

> Usages for data lake and object storage systems.

#### Overview

이 디렉토리는 `hy-home.docker`의 데이터 레이크 및 오브젝트 스토리지 관련 가이드를 포함한다. 대용량 비정형 데이터 저장 및 관리를 위한 MinIO와 SeaweedFS의 활용 방법을 안내한다.

#### Audience

이 README의 주요 독자:

- Developers using S3 or Filer APIs
- Operators managing storage clusters
- AI Agents looking for storage integration metadata

#### Structure

```text
lake-and-object/
├── README.md      # This file
├── minio.md       # MinIO Object Storage Usage
└── seaweedfs.md   # SeaweedFS Storage Usage
```

#### Related References

- **Parent**: [04-data Usages](../README.md)
- **Implementation**: [lake-and-object Infrastructure](../../../../../infra/04-data/lake-and-object/minio/README.md)
- **Operations**: [lake-and-object Operations](./README.md)
- **Procedures**: [lake-and-object Procedures](./README.md)

---

#### Scope

##### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

##### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

#### How to Work in This Area

1. 관련 `infra/` 서비스 README와 같은 tier의 operation/runbook 문서를 함께 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Procedure

> Migrated from `docs/05.operations/04-data/lake-and-object/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Lake and Object Storage Recovery Procedures

> Operational procedures for data lake and object storage systems.
> 데이터 레이크 및 오브젝트 스토리지 장애 대응 및 복구 절차.

---

#### Overview

This directory contains recovery runbooks for data lake and object storage systems, providing step-by-step procedures for emergency response and service restoration.

이 디렉토리는 데이터 레이크 및 오브젝트 스토리지 시스템의 장애 대응을 위한 실행 절차(Procedure)를 포함하며, 긴급 상황 시 서비스 복구를 위한 수동 조치 단계를 제공한다.

#### Direct Documents

- [MinIO Recovery Procedure](./minio.md)
- [SeaweedFS Recovery Procedure](./seaweedfs.md)

#### Related References

- [04-data Procedures Index](../README.md)
- [Lake and Object Technical Usages](./README.md)
- [Lake and Object Operations Policies](./README.md)

---

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

##### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

#### Structure

```text
docs/05.operations/04-data/lake-and-object/
├── minio.md  # 문서
├── README.md  # This file
└── seaweedfs.md  # 문서
```

#### How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
