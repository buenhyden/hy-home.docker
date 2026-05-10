# Data Operations Policy (04-data)

> Persistence, Backup, and Security (04-data) 운영 정책

## Overview

이 디렉터리는 `hy-home.docker` 데이터 인프라 계층(04-data)의 운영 표준 및 데이터 보호 요구 사항을 정의합니다. 모든 서비스의 지속성, 가용성 및 보안을 보장하는 것이 목적입니다.

This directory defines the operational standards and data protection requirements for the `hy-home.docker` data infrastructure tier (04-data). The objective is to ensure the persistence, availability, and security of all services.

## Audience

이 README의 주요 독자:

- 운영 정책을 수립하는 **Operators**
- 보안 통제를 적용하는 **Security Engineers**
- 정책 준수 여부를 확인하는 **AI Agents**

## Scope

### In Scope

- 데이터 저장 표준 및 볼륨 격리 정책
- 백업 전략 및 보관 기간
- 보안 및 규정 준수 통제

### Out of Scope

- 애플리케이션 레벨의 데이터 암호화 로직
- 클라우드 벤더사(AWS/GCP) 특화 보안 정책

## Structure

```text
04-data/
├── cache-and-kv/         # 분산 캐시 및 KV 저장소 운영 정책
├── lake-and-object/       # 데이터 레이크 및 오브젝트 스토리지 운영 정책
├── nosql/                 # NoSQL 데이터베이스 운영 정책
├── optimization-hardening.md # 04-data 최적화/하드닝 운영 정책
├── operational/           # 운영 및 관리용 데이터베이스 운영 정책
├── backup-policy.md       # 공통 백업 표준
├── relational/            # 관계형 데이터베이스 운영 정책
├── relational.md          # Relational Database Operations Policy
└── README.md              # This file
```

## How to Work in This Area

1. 전역 시스템 운영 원칙은 [Operations](../../README.md) 메인 페이지를 참조합니다.
2. 각 데이터 서비스별 개별 정책은 이 디렉터리의 개별 문서를 따릅니다.
3. 정책 변경 시 아키텍처 팀의 승인이 필요합니다.

## Documentation Standards

- 모든 정책은 명확한 Control 및 적용 범위를 포함해야 합니다.
- 한국어 Overview 및 영어 본문을 기본으로 합니다.

## Traceability Rules

- 모든 운영 정책은 ARD(Architecture Requirements Document)와 연결되어야 합니다.
- 대응되는 Procedure이 존재해야 합니다.

## Related References

- **Usages**: [Technical Usages](./README.md)
- **Procedures**: [Recovery Procedures](./README.md)
- **Hardening Policy**: [04-data Optimization Hardening Policy](../../policies/04-data/optimization-hardening.md)

---
Copyright (c) 2026. Licensed under the MIT License.

## Usage

> Migrated from `docs/05.operations/04-data/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Data Tier Usages (04-data)

> Persistence, Caching, and Storage Services 가이드

#### Overview

이 디렉터리는 `hy-home.docker` 데이터 인프라 계층(04-data)을 위한 기술 가이드를 포함합니다. 각 가이드는 데이터베이스 유형별로 정리되어 효율적인 시스템 이해와 운영을 돕습니다.

This directory contains technical guides for the `hy-home.docker` data infrastructure tier (04-data). Each guide is organized by database type to facilitate efficient system understanding and operation.

#### Audience

이 README의 주요 독자:

- 시스템을 사용하는 **Developers**
- 인프라를 관리하는 **Operators**
- 문서 구조를 학습하는 **AI Agents**

#### Scope

##### In Scope

- 관계형 데이터베이스(PostgreSQL) 사용 가이드
- 캐시 및 Key-Value 저장소(Valkey) 사용 가이드
- NoSQL 및 오브젝트 스토리지 가이드

##### Out of Scope

- 개별 비즈니스 로직에 특화된 쿼리 최적화 가이드
- 인프라 외부의 클라우드 매니지드 DB 가이드

#### Structure

```text
04-data/
├── cache-and-kv/         # 분산 캐시 및 KV 저장소 가이드 (Valkey Cluster)
├── lake-and-object/       # 데이터 레이크 및 오브젝트 스토리지 가이드
├── nosql/                 # NoSQL 데이터베이스 가이드
├── optimization-hardening.md # 04-data 최적화/하드닝 가이드
├── operational/           # 운영 및 관리용 데이터베이스 가이드
├── relational/            # 관계형 데이터베이스(PostgreSQL) 가이드
├── relational.md          # Relational Database Overview Usage
└── README.md              # This file
```

#### How to Work in This Area

1. 전반적인 데이터 아키텍처는 [Architecture](../../../02.architecture/requirements/0004-data-architecture.md) 문서를 먼저 확인합니다.
2. 특정 엔진의 구현 세부 사항은 `infra/04-data/` 경로의 소스 코드를 참조합니다.
3. 새로운 가이드 추가 시 `docs/99.templates/operation.template.md`를 사용합니다.

#### Traceability Rules

이 영역의 모든 문서는 다음 항목 중 하나 이상과 연결되어야 합니다.

- Architecture Requirements Document (ARD)
- Operations Policy
- Procedure

#### Related References

- **Operations**: [Data Operations Policy](./README.md)
- **Procedures**: [Data Recovery Procedures](./README.md)
- **Hardening Usage**: [04-data Optimization Hardening Usage](../../policies/04-data/optimization-hardening.md)
- **Source**: [Infrastructure Source](../../../../infra/04-data/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.

## Procedure

> Migrated from `docs/05.operations/04-data/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Data Recovery Procedure (04-data)

> Incident Response & Emergency Restoration Procedures (04-data)

#### Overview

이 디렉터리는 `hy-home.docker` 데이터 인프라 계층(04-data)에서 발생할 수 있는 긴급 장애에 대응하기 위한 단계별 실행 지침(Procedure)을 포함합니다. 서비스의 가동 시간을 극대화하고 데이터 손실을 최소화하는 것이 목적입니다.

This directory contains step-by-step execution guidelines (Procedures) for responding to emergency failures in the `hy-home.docker` data infrastructure tier (04-data). The objective is to maximize service uptime and minimize data loss.

#### Audience

이 README의 주요 독자:

- 장애 대응을 수행하는 **Operators / SRE**
- 복구 절차를 검증하는 **QA Engineers**
- 실시간 장애 조치를 돕는 **AI Agents**

#### Scope

##### In Scope

- 데이터베이스 노드 및 클러스터 레벨 복구 절차
- 백업 데이터로부터의 완전 복구 프로세스
- 슬롯 수리 및 정족수(Quorum) 복구 지침

##### Out of Scope

- 하드웨어 및 인프라 프로비저닝 (Terraform/Ansible 범위)
- 애플리케이션 버그로 인한 데이터 보정

#### Structure

```text
04-data/
├── cache-and-kv/         # 분산 캐시 및 KV 저장소 긴급 복구 런북
├── lake-and-object/       # 데이터 레이크 및 오브젝트 스토리지 긴급 복구 런북
├── nosql/                 # NoSQL 데이터베이스 복구 런북
├── optimization-hardening.md # 04-data 하드닝 회귀 복구 런북
├── operational/           # 운영 및 관리용 데이터베이스 복구 런북
├── storage-exhaustion.md   # 용량 부족 대응 공통 런북
├── relational/            # 관계형 데이터베이스(PostgreSQL) 복구 런북
├── relational.md          # Relational Database Recovery Procedure
└── README.md              # This file
```

#### How to Work in This Area

1. 장애 발생 시 가장 먼저 [Initial Triage](./README.md#setup--initial-triage) 절차를 확인합니다.
2. 특정 서비스 장애의 경우 해당 서비스의 개별 런북 문서를 즉시 실행합니다.
3. 복구 완료 후에는 반드시 `VERIFICATION` 단계를 거쳐야 합니다.

#### Documentation Standards

- 런북은 실시간 대응을 위한 가독성이 중요하며, 명령어 중심(KR/EN)이어야 합니다.
- 단계별 검증 기준(Verification)이 포함되어야 합니다.

#### Related References

- **Usages**: [Technical Usages](./README.md)
- **Operations**: [Operations Policy](./README.md)
- **Hardening Procedure**: [04-data Optimization Hardening Procedure](../../policies/04-data/optimization-hardening.md)

---

#### Setup & Initial Triage

장애 대응 시 다음 단계를 가장 먼저 수행합니다.

1. **서비스 상태 확인**: `docker compose ps`
2. **로그 리뷰**: `docker compose logs --tail=100 [service]`
3. **디스크 공간 확인**: `df -h`

---
Copyright (c) 2026. Licensed under the MIT License.
