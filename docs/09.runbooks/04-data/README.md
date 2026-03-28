# Data Recovery Runbook (04-data)

> Incident Response & Emergency Restoration Procedures (04-data)

## Overview

이 디렉터리는 `hy-home.docker` 데이터 인프라 계층(04-data)에서 발생할 수 있는 긴급 장애에 대응하기 위한 단계별 실행 지침(Runbook)을 포함합니다. 서비스의 가동 시간을 극대화하고 데이터 손실을 최소화하는 것이 목적입니다.

This directory contains step-by-step execution guidelines (Runbooks) for responding to emergency failures in the `hy-home.docker` data infrastructure tier (04-data). The objective is to maximize service uptime and minimize data loss.

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

### Out of Scope

- 하드웨어 및 인프라 프로비저닝 (Terraform/Ansible 범위)
- 애플리케이션 버그로 인한 데이터 보정

## Structure

```text
04-data/
├── cache-and-kv/         # 분산 캐시 및 KV 저장소 긴급 복구 런북
├── lake-and-object/       # 데이터 레이크 및 오브젝트 스토리지 긴급 복구 런북
├── nosql/                 # NoSQL 데이터베이스 복구 런북
├── optimization-hardening.md # 04-data 하드닝 회귀 복구 런북
├── operational/           # 운영 및 관리용 데이터베이스 복구 런북
├── storage-exhaustion.md   # 용량 부족 대응 공통 런북
├── relational/            # 관계형 데이터베이스(PostgreSQL) 복구 런북
├── relational.md          # Relational Database Recovery Runbook
└── README.md              # This file
```

## How to Work in This Area

1. 장애 발생 시 가장 먼저 [Initial Triage](./README.md#setup--initial-triage) 절차를 확인합니다.
2. 특정 서비스 장애의 경우 해당 서비스의 개별 런북 문서를 즉시 실행합니다.
3. 복구 완료 후에는 반드시 `VERIFICATION` 단계를 거쳐야 합니다.

## Documentation Standards

- 런북은 실시간 대응을 위한 가독성이 중요하며, 명령어 중심(KR/EN)이어야 합니다.
- 단계별 검증 기준(Verification)이 포함되어야 합니다.

## Related References

- **Guides**: [Technical Guides](../../07.guides/04-data/README.md)
- **Operations**: [Operations Policy](../../08.operations/04-data/README.md)
- **Hardening Runbook**: [04-data Optimization Hardening Runbook](./optimization-hardening.md)

---

## Setup & Initial Triage

장애 대응 시 다음 단계를 가장 먼저 수행합니다.

1. **서비스 상태 확인**: `docker compose ps`
2. **로그 리뷰**: `docker compose logs --tail=100 [service]`
3. **디스크 공간 확인**: `df -h`

---
Copyright (c) 2026. Licensed under the MIT License.
