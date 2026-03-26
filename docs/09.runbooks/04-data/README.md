# Data Recovery Runbook (04-data)

> Incident Response & Emergency Restoration Procedures (04-data)

## Overview

이 디렉터리는 `hy-home.docker` 데이터 인프라 계층(04-data)에서 발생할 수 있는 긴급 장애에 대응하기 위한 단계별 실행 지침(Runbook)을 포함합니다. 서비스의 가동 시간을 극대화하고 데이터 손실을 최소화하는 것이 목적입니다.

## Audience

이 README의 주요 독자:

- 장애 대응을 수행하는 **Operators / SRE**
- 복구 절차를 검증하는 **QA Engineers**
- 실시간 장애 조치를 돕는 **AI Agents**

## Scope

### In Scope

- 데이터베이스 노드 및 클러스터 레벨 복구 절차
- 백업 데이터로부터의 완전 복구 프로세스
- 슬롯 수리 및 정족수(Quorum) 복구 지침

## Structure

```text
04-data/
├── storage-exhaustion.md
├── valkey-cluster.md     # Valkey Cluster 긴급 복구 런북
├── minio.md              # MinIO Object Storage 긴급 복구 런북
└── README.md
```

## How to Work in This Area

1. 장애 발생 시 가장 먼저 [Initial Triage](./README.md#setup--initial-triage) 절차를 확인합니다.
2. 특정 서비스 장애의 경우 해당 서비스의 개별 런북 문서를 즉시 실행합니다.
3. 복구 완료 후에는 반드시 `VERIFICATION` 단계를 거쳐야 합니다.

## Related References

- **Guides**: [Technical Guides](../../07.guides/04-data/README.md)
- **Operations**: [Operations Policy](../../08.operations/04-data/README.md)

---

## Setup & Initial Triage

장애 대응 시 다음 단계를 가장 먼저 수행합니다.

1. **서비스 상태 확인**: `docker compose ps`
2. **로그 리뷰**: `docker compose logs --tail=100 [service]`
3. **디스크 공간 확인**: `df -h`

---
Copyright (c) 2026. Licensed under the MIT License.
