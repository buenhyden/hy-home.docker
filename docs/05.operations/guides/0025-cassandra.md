---
title: "Cassandra Usage Guide"
version: "1.0.5"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0025"
parent_ids:
- "POL-0025"
implementation_services:
  infra/04-data/cassandra/docker-compose.yml:
  - 'cassandra-exporter'
  - 'cassandra-node1'
created: "2026-05-10"
---

# Cassandra Usage Guide

## Usage

### Overview

이 문서는 [Cassandra Compose 구현](../../../infra/04-data/cassandra/docker-compose.yml)의 단일 `cassandra-node1`과 `cassandra-exporter`를 설명한다. 두 서비스는 모두 정확히 `cassandra` profile에 속하며 `lab_net`에서 동작한다. frozen service classification은 `LAB`이고, 한 호스트의 단일 데이터 노드이므로 quorum이나 host-level HA를 제공하지 않는다.

### Current implementation

| 항목 | 이 저장소의 구현 결정 |
| --- | --- |
| Consumer와 data 근거 | 확인된 HOME consumer는 없음; 쓰기량이 많은 workload와 keyspace를 위한 LAB wide-column 평가용. |
| Source·update 책임 | [Compose](../../../infra/04-data/cassandra/docker-compose.yml)가 image source를 소유한다. dependency 자동화가 변경을 제안할 수 있지만 upgrade는 운영자 검토가 소유한다. |
| 서비스·profile | `cassandra-node1`, `cassandra-exporter`; 정확한 profile은 `cassandra`. |
| 흐름·의존성 | CQL client는 `lab_net`의 node를 사용하며 exporter는 node health 확인 후 시작한다. |
| 노출·영속성 | opt-in `cassandra`, 공유 `lab_net`, host/public route 없음. `/bitnami/cassandra` bind는 실제 기본 `/var/lib/cassandra` 데이터를 보호하지 못한다. |
| 환경 설정·secret | `CASSANDRA_USERNAME`과 Compose가 소유한 tuning key; `cassandra_password`는 `/run/secrets`에 있다. |
| Health·자원 | `nodetool status`와 CQL health; node는 `template-stateful-high`, exporter는 `template-infra-low`. |
| 보안 | 구현 미준수: 선언된 공식 image는 Bitnami 인증 환경 변수를 처리하지 않으며 기본 AllowAll 인증/권한을 사용한다. Secret mount는 접근 통제가 아니다. |
| Backup·upgrade | tag를 붙인 SSTable snapshot과 schema/topology 목록을 함께 보존한다. version 변경이나 제거 전에 격리된 환경에서 호환되는 restore를 수행한다. |
| License·edition | Apache Cassandra source에는 Apache-2.0이 적용된다. 이 저장소는 source에 선언된 single-node 배포판을 실행하며 상용 기능을 제공한다고 주장하지 않는다. |

### Identity-specific behavior

공식 Cassandra image Dockerfile/entrypoint 와 tagged cassandra.yaml 은 Bitnami CASSANDRA_USER/PASSWORD_FILE 을 처리하지 않고 AllowAllAuthenticator/AllowAllAuthorizer 를 사용한다. image VOLUME 은 `/var/lib/cassandra`; 현재 `/bitnami/cassandra` bind 는 실제 기본 data 를 보호하지 않는다.2026-03-18 image-family switch 이후 남은 source 불일치이며 runtime data loss 나 public exposure 를 관측한 것이 아니다. 운영 활성화/재생성/복원은 중단하고 별도 구현 및 data ownership 검토가 필요하다. 선언된 exporter/server 조합의 호환성은 미확인이고 자체 healthcheck 도 없다. node heap 와 container 메모리 상한이 같아 off-heap 여유를 보장하지 않는다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `cassandra-exporter` | Cassandra JMX exporter; 별도 mount, 호환성 미확인 | 자체 healthcheck 없음; process와 해당 기능/metrics 별도 확인 | [선택·의존·접속·입력·mount](../../../infra/04-data/cassandra/docker-compose.yml) |
| `cassandra-node1` | LAB wide-column node; 공식 image auth/persistence 불일치로 활성화 중단 | nodetool 상태; 인증/지속성 증명 아님 | [선택·의존·접속·입력·mount](../../../infra/04-data/cassandra/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Cassandra를 wide-column 저장소로 사용할 때 현재 repository의 서비스명, secret mount, 볼륨 경계, 메트릭 exporter 경로를 오해하지 않도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../docker-compose.yml)는 Cassandra 파일을 include하며, 두 서비스의 정확한 profile은 `cassandra`다.
- `DEFAULT_DATA_DIR`, `CASSANDRA_USERNAME`, `cassandra_password` secret 파일이 로컬 환경에서 준비되어 있어야 한다.
- 인증·영속성 계약의 구현 수정과 격리 검증 전 운영 활성화를 중단한다. 실제 실행 상태는 확인하지 않았으며, secret 값을 문서나 로그에 남기지 않는다.

### Step-by-step Instructions

현재는 정적 profile/source 확인과 별도 승인된 상태 triage만 가능하다. Credential을 준 CQL 성공은 인증 증거가 아니며, 정상·오류·무인증 credential의 격리 검증이 구현 수정 뒤 필요하다. exporter 포트는 compose의 `${CASSANDRA_EXPORTER_PORT:-8080}` 및 `${CASSANDRA_EXPORTER_LISTEN_PORT:-8081}` 기준이다. 실행 가능한 명령 순서와 기대 결과는 [Cassandra runbook](../runbooks/0025-cassandra.md#steps)을 따른다.

### Common Pitfalls

- 현재 구현은 단일 노드다. image tag는 Compose declaration이 소유하며, 다중 노드 quorum, repair 자동화, zero-downtime node rotation을 구현된 기능처럼 문서화하지 않는다.
- 공식 image는 `/var/lib/cassandra`에 쓰고 image VOLUME을 선언한다. 현재 `/bitnami/cassandra` bind는 과거 Bitnami 설정이며, 실제 데이터 위치·anonymous volume 소유권을 별도 승인으로 확인하기 전 backup/recreate/removal을 진행하지 않는다.
- 평문 password 환경 변수를 전제로 한 명령을 사용하지 않는다. compose는 `/run/secrets/cassandra_password`를 사용한다.
- restore 전에 Cassandra release/schema, keyspace 목록, replication 설정, snapshot tag, token/topology를 기록한다. snapshot은 schema와 모든 table SSTable을 함께 보존하고 빈 격리 target에서만 검증한다.

## Common Checks

- `docker compose --profile cassandra config --quiet`
- `docker exec cassandra-node1 nodetool status`에서 `cassandra-node1` 상태가 `UN`인지 확인한다.
- `docker compose ps cassandra-node1 cassandra-exporter`에서 Cassandra가 healthy이고 exporter가 실행 중인지 확인한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Cassandra runbook](../runbooks/0025-cassandra.md)을 따른다.

## Traceability

- Declared parent: [Cassandra Operations Policy](../policies/0025-cassandra.md) (`POL-0025`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../policies/0025-cassandra.md) (`POL-0025`), [Runbook](../runbooks/0025-cassandra.md) (`RUN-0025`)

## Related Documents

- [Cassandra backup and restore](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
- [Cassandra security](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/security.html)
- [Apache Cassandra source and license](https://github.com/apache/cassandra)

- [Operations index](../README.md)
- [Operations policy](../policies/0025-cassandra.md)
- [Recovery runbook](../runbooks/0025-cassandra.md)
- [Infra README](../../../infra/04-data/cassandra/README.md)
- [Compose implementation: infra/04-data/cassandra/docker-compose.yml](../../../infra/04-data/cassandra/docker-compose.yml)
