---
title: "Cassandra Operations Policy"
version: "2.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0025"
parent_ids:
- "AD-0004"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Cassandra Operations Policy

## Purpose and Scope

### Objective

독립 Cassandra LAB의 단일 노드·데이터 보존·인증 경계를 정의한다. HOME 소비자와 공유하지 않는다.

#### Authority

- Declared parent: [AD-0004](../../../02.architecture/descriptions/0004-data-architecture.md)
- [LAB Compose](../../../../labs/cassandra/docker-compose.yml)

### Applies To

`labs/cassandra/docker-compose.yml`의 `cassandra-node1`, `cassandra-node1-data`, `lab_cassandra_core_net`와 연결 문서에 적용한다.

#### Exclusions

exporter와 Cassandra password secret은 현재 구현에 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0025-R1 | 항상 | 필수: 공식 Cassandra `/var/lib/cassandra`를 named volume `cassandra-node1-data`에 영속하고 기존 HOME/anonymous volume은 자동 재사용/삭제하지 않는다 | `docker compose ... --profile cassandra config --quiet` 정적 렌더 / 문서 링크 검사 | 정적 렌더 결과 |
| POL-0025-R2 | 항상 | 필수: `AllowAllAuthenticator`/`AllowAllAuthorizer` 기본을 무인증으로 취급하고 내부 네트워크만 사용하며 host port/gateway route/업무 소비자를 추가하지 않는다 | `docker compose ... --profile cassandra config --quiet` 정적 렌더 / 문서 링크 검사 | 정적 렌더 결과 |
| POL-0025-R3 | 실제 인증/권한이 필요할 때 | 필수: 이미지 지원 설정과 무인증/오인증 거부를 격리 검증한 뒤 별도 승인된 소스 변경으로 적용한다 | 수동 | none |
| POL-0025-R4 | 백업/복구 시 | 필수: 백업은 release/schema/keyspace/replication/topology, snapshot tag, 모든 SSTable을 묶고 restore는 새 빈 격리 대상에서만 검증한다 | 수동 | none |
| POL-0025-R5 | 운영 승인 시 | 필수: 용량/업그레이드/복구/보존 기간과 소비자 영향을 확인한 뒤 승인하며 volume 삭제와 secret 변경은 별도 범위다 | 수동 | none |
| POL-0025-R6 | 정적 확인 시 | 허용: 정적 Compose 렌더와 승인된 read-only 건강 확인 | `docker compose ... --profile cassandra config --quiet` 정적 렌더 / 문서 링크 검사 | 정적 렌더 결과 |
| POL-0025-R7 | 항상 | 금지: 단일 노드를 HA로 주장하거나 `nodetool` 건강을 복구 증거로 사용한다 | 수동 | none |

- **Required:** 공식 Compose에 선언된 공식 Cassandra 이미지의 실제 `/var/lib/cassandra`를 named volume `cassandra-node1-data`(bind 대상 `${LAB_DATA_DIR}/cassandra/node1`)에 영속한다. 기존 HOME/과거 anonymous volume은 자동 재사용·삭제하지 않는다.
- **Required:** `AllowAllAuthenticator`/`AllowAllAuthorizer` 기본 상태를 무인증으로 취급한다. 내부 네트워크만 사용하며 host port·gateway route와 실제 업무 소비자를 추가하지 않는다.
- **Required:** 실제 인증·권한이 필요하면 이미지 지원 설정과 무인증·오인증 거부를 격리 검증한 뒤 별도 승인된 소스 변경으로 적용한다.
- **Required:** 백업은 release/schema/keyspace/replication/topology와 snapshot tag 및 모든 SSTable을 묶는다. restore는 새 빈 격리 대상에서만 검증한다.
- **Required:** 용량·업그레이드·복구·보존 기간과 소비자 영향을 확인한 뒤 운영을 승인한다. volume 삭제와 secret 변경은 별도 범위다.
- **Allowed:** 정적 Compose 렌더와 승인된 read-only 건강 확인.
- **Disallowed:** 단일 노드를 HA로 주장하거나 `nodetool` 건강을 복구 증거로 사용하지 않는다.

#### Accountable lifecycle boundary

@buenhyden이 LAB 기동·중단·복구·정리 승인과 기존 상태 소유권을 확인한다. [POL-0006](../01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)과 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)을 따른다.

### Exceptions

#### Exception Conditions

승인된 예외 없음.

#### Approval and Review

이미지·profile·mount·접속·인증 계약 변경 시 검토한다.

## Enforcement

### Mechanisms

`LAB_DATA_DIR=/tmp/hy-home-lab-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra/docker-compose.yml --profile cassandra config --quiet`와 문서 링크 검사를 수행한다. 실제 CQL·복원은 `NOT_RUN`으로 기록한다.

### Limits

정적 Compose 렌더와 문서 링크 검사만 이름이 붙은 검사이며, 아래 항목은 기계적으로 강제되지 않는다.

- 실제 CQL과 복원은 `NOT_RUN`으로 기록되며 실행 증거가 없다.
- 무인증 상태 취급, 승인 후 운영, 백업 구성은 수동 검토에 의존한다.
- 인증·권한 적용은 별도 승인된 소스 변경과 격리 검증이 있어야 하며 현재 검사는 없다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- Subject peers: [GDE-0025](../../guides/15-labs/0025-cassandra.md), [RUN-0025](../../runbooks/15-labs/0025-cassandra.md)
- [LAB 설명](../../../../labs/cassandra/README.md)
- [Cassandra backup](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
