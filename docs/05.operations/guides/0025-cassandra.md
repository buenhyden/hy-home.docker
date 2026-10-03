---
title: "Cassandra Usage Guide"
version: "2.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "GDE-0025"
parent_ids:
- "POL-0025"
created: "2026-05-10"
---

# Cassandra Usage Guide

## Usage

독립 `labs/cassandra.yml`은 공식 `labs/cassandra.yml`에 선언된 공식 Cassandra 이미지의 단일 `cassandra-node1` 실습용 정의다. HOME root는 include하지 않으며 확인된 HOME 소비자는 없다. 이미지 선언 버전은 Compose가 소유한다. 현재 공식 이미지의 기본 `AllowAllAuthenticator`/`AllowAllAuthorizer`는 계정 인증을 제공하지 않는다. 이를 인증된 업무 저장소로 사용하지 않는다.

### Current implementation

| 항목 | 계약 |
| --- | --- |
| 서비스·선택 | `cassandra-node1`, 독립 Compose의 `cassandra` profile |
| 연결 | `lab_cassandra_core_net` 내부 CQL, host port·gateway route 없음 |
| 영속 | 새 `${LAB_DATA_DIR}/cassandra/node1` bind → `/var/lib/cassandra`; 기존 HOME 또는 과거 anonymous volume을 자동 연결하지 않음 |
| 입력 | `labs/.env.example`과 비공개 `labs/.env`의 `LAB_DATA_DIR`; 인증 secret·exporter 없음 |
| 건강·자원 | `nodetool status` health와 Compose 한도; 실제 CQL·디스크·복원은 미검증 |
| 백업 | schema/keyspace/topology·snapshot tag·SSTable 세트를 함께 보존하고 빈 격리 대상에 복원 검증 필요 |

### Identity-specific behavior

공식 이미지가 지원하지 않는 Bitnami 환경 변수와 `/bitnami/cassandra` mount는 제거했다. 추적된 설정에는 Cassandra 인증·권한 설정이 없다. 격리 네트워크는 동일 네트워크 peer의 CQL 접근을 인증하지 않는다. 기존 데이터가 없음을 추정하지 않으며, 이전 anonymous volume의 소유자·내용은 운영 검토 전까지 보존한다.

### Usage Type

`system-guide`

### Target Audience

Operator, Developer, AI Agent.

### Purpose

현재 LAB 서비스·데이터·인증 경계를 소스와 일치시킨다.

### Prerequisites

실행 전 Docker context, 독립 project, 새 디렉터리·volume, network, 포트, 자원, 정확한 정리 범위를 확인한다. 실제 기동·복구는 별도 승인 범위다.

### Step-by-step Instructions

정적 렌더만 수행한다. `LAB_DATA_DIR=/tmp/hy-home-lab-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra.yml --profile cassandra config --quiet`. 실제 건강·CQL 검증은 [런북](../runbooks/0025-cassandra.md)의 실행 경계를 따른다.

### Common Pitfalls

`nodetool`의 UN 상태는 인증, 영속 복구, 업무 CQL 성능의 증거가 아니다. 단일 노드는 HA가 아니다. 무인증 CQL을 외부 network나 실제 업무 데이터에 연결하지 않는다.

## Common Checks

정적 Compose 렌더와 root include 제외를 확인한다. 격리 실행은 `NOT_RUN`이다.

## Runbook Handoff

[RUN-0025](../runbooks/0025-cassandra.md)를 따른다.

## Traceability

- Declared parent: [POL-0025](../policies/0025-cassandra.md)
- Architecture: [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)

## Related Documents

- [LAB Compose](../../../labs/cassandra.yml)
- [LAB 설명](../../../labs/cassandra.md)
- [운영 정책](../policies/0025-cassandra.md)
