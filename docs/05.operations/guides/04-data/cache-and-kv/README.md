# Cache and KV Operations (04-data/cache-and-kv)

> Operations Policies for Distributed Caching and KV Stores / 분산 캐시 및 Key-Value 저장소 운영 정책

## Overview (KR)

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에 대한 운영 표준과 보안 정책을 포함한다. 데이터 영속성, 메모리 관리, 접근 제어를 규정한다.

This path contains operational standards and security policies for services in the cache and KV storage layer, such as Valkey and Redis. It regulates data persistence, memory management, and access control.

## Audience

이 README의 주요 독자:

- 운영 표준을 관리하는 **Operators**
- 보안 통제를 감사하는 **Security Engineers**
- 정책 준수 가이드를 읽는 **AI Agents**

## Scope

### In Scope

- Valkey Cluster 운영 및 보안 정책
- 캐시 메모리 할당 및 제거(Eviction) 기준
- 데이터 영속성(AOF/RDB) 설정 표준

### Out of Scope

- NoSQL 데이터베이스 정책 (nosql/ 참조)
- 백업 시스템 구현 세부 사항
- 개별 애플리케이션 권한 관리

## Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 운영 정책
└── README.md            # 이 파일
```

## How to Work in This Area

1. 전역 데이터 보안 정책은 [backup-policy.md](../../../policies/04-data/backup-policy.md)를 먼저 확인합니다.
2. 정책 위반 사항 발견 시 즉시 담당자에게 보고하고 [Procedure](./README.md)을 참조합니다.

## Available Policies

- [Valkey Cluster Operations Policy](./valkey-cluster.md): 백업, 보안, 리소스 관리 표준.

## Related References

- **Implementation**: [infra/04-data/cache-and-kv/README.md](../../../../../infra/04-data/cache-and-kv/README.md)
- **Usage**: [04-data Usages](./README.md)
- **Procedure**: [04-data Procedures](./README.md)

---

## Overview

`docs/05.operations/04-data/cache-and-kv`는 운영 정책, 통제 기준, 검증 방법을 정의하는 operation 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Usage

> Migrated from `docs/05.operations/04-data/cache-and-kv/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Cache and KV Usages (04-data/cache-and-kv)

> Distributed Caching and Fast Key-Value Storage Usage Usages / 분산 캐시 및 Key-Value 저장소 활용 가이드

#### Overview (KR)

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에 대한 사용자 가이드를 포함한다. 에코시스템 내에서 캐싱 레이어를 효과적으로 활용하기 위한 기술 정보를 제공한다.

This path contains user guides for services in the cache and KV storage layer, such as Valkey and Redis. It provides technical information for effectively utilizing the caching layer within the ecosystem.

#### Audience

이 README의 주요 독자:

- 시스템을 연동하는 **Developers**
- 캐시 상태를 점검하는 **Operators**
- 가이드 구조를 파악하는 **AI Agents**

#### Scope

##### In Scope

- Valkey Cluster 연동 가이드
- Redis 호환 클라이언트 설정 지침
- 캐싱 전략 및 모범 사례

##### Out of Scope

- 인프라 배포 스크립트 (infra/ 참조)
- 개별 애플리케이션의 비즈니스 로직
- 데이터베이스 쿼리 튜닝 (relational/ 참조)

#### Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 활용 가이드
└── README.md            # This file
```

#### How to Work in This Area

1. [valkey-cluster.md](./valkey-cluster.md)를 통해 클러스터 모드 연결 방법을 숙지합니다.
2. 새로운 가이드 추가 시 `docs/99.templates/operation.template.md`를 사용합니다.
3. 관련 운영 정책은 [05.operations/04-data/cache-and-kv/README.md](./README.md)를 확인합니다.

#### Available Usages

- [Valkey Cluster Usage](./valkey-cluster.md): 6노드 분산 클러스터 연결 및 사용법.

#### Related References

- **Implementation**: [infra/04-data/cache-and-kv/README.md](../../../../../infra/04-data/cache-and-kv/README.md)
- **Operation**: [04-data Operations](./README.md)
- **Procedure**: [04-data Procedures](./README.md)

---

#### Overview

`docs/05.operations/04-data/cache-and-kv`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Procedure

> Migrated from `docs/05.operations/04-data/cache-and-kv/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Cache and KV Procedures (04-data/cache-and-kv)

> Incident Response and Recovery for Caching Services / 분산 캐시 및 Key-Value 저장소 장애 복구 런북

#### Overview (KR)

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에서 발생할 수 있는 장애 상황에 대응하기 위한 실행 지침을 포함한다. 신속한 서비스 복구와 데이터 무결성 유지를 목적으로 한다.

This path contains operational instructions for responding to failure situations that may occur in services in the cache and KV storage layer, such as Valkey and Redis. It aims for rapid service recovery and maintenance of data integrity.

#### Audience

이 README의 주요 독자:

- 긴급 장애 조치를 수행하는 **Operators / SRE**
- 복구 절차를 학습하는 **AI Agents**
- 시스템 안정성을 검증하는 **QA Engineers**

#### Scope

##### In Scope

- Valkey Cluster 노드 장애 복구
- 클러스터 슬롯 불일치 해결 절차
- 네트워크 파티션 및 정족수 복구

##### Out of Scope

- 관계형 DB 복구 (relational/ 참조)
- 애플리케이션 코드 버그 수정
- 클라우드 인프라(AWS/GCP) 레벨 복구

#### Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 장애 복구 런북
└── README.md            # 이 파일
```

#### How to Work in This Area

1. 장애 발생 시 [valkey-cluster.md](./valkey-cluster.md)의 진단 단계를 즉시 수행합니다.
2. 모든 복구 작업은 수행 전후로 [Operations](./README.md) 정책을 준수하는지 확인합니다.

#### Available Procedures

- [Valkey Cluster Procedure](./valkey-cluster.md): 노드 장애, 슬롯 오류 복구 절차.

#### Related References

- **Implementation**: [infra/04-data/cache-and-kv/README.md](../../../../../infra/04-data/cache-and-kv/README.md)
- **Usage**: [04-data Usages](./README.md)
- **Operation**: [04-data Operations](./README.md)

---

#### Overview

`docs/05.operations/04-data/cache-and-kv`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.
