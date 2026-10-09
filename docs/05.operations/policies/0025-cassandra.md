---
title: "Cassandra Operations Policy"
version: "2.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0025"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Cassandra Operations Policy

## Overview

독립 Cassandra LAB의 단일 노드·데이터 보존·인증 경계를 정의한다. HOME 소비자와 공유하지 않는다.

## Scope

`labs/cassandra.yml`의 `cassandra-node1`, `cassandra-node1-volume`, `lab_cassandra_core_net`와 연결 문서에 적용한다. exporter와 Cassandra password secret은 현재 구현에 없다.

## Rules

- **Required:** 공식 Compose에 선언된 공식 Cassandra 이미지의 실제 `/var/lib/cassandra`를 새 LAB 전용 `${LAB_DATA_DIR}/cassandra/node1`에 영속한다. 기존 HOME/과거 anonymous volume은 자동 재사용·삭제하지 않는다.
- **Required:** `AllowAllAuthenticator`/`AllowAllAuthorizer` 기본 상태를 무인증으로 취급한다. 내부 네트워크만 사용하며 host port·gateway route와 실제 업무 소비자를 추가하지 않는다.
- **Required:** 실제 인증·권한이 필요하면 이미지 지원 설정과 무인증·오인증 거부를 격리 검증한 뒤 별도 승인된 소스 변경으로 적용한다.
- **Required:** 백업은 release/schema/keyspace/replication/topology와 snapshot tag 및 모든 SSTable을 묶는다. restore는 새 빈 격리 대상에서만 검증한다.
- **Required:** 용량·업그레이드·복구·보존 기간과 소비자 영향을 확인한 뒤 운영을 승인한다. volume 삭제와 secret 변경은 별도 범위다.
- **Allowed:** 정적 Compose 렌더와 승인된 read-only 건강 확인.
- **Disallowed:** 단일 노드를 HA로 주장하거나 `nodetool` 건강을 복구 증거로 사용하지 않는다.

### Accountable lifecycle boundary

@buenhyden이 LAB 기동·중단·복구·정리 승인과 기존 상태 소유권을 확인한다. [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)과 [POL-0021](0021-backup-and-restore.md)을 따른다.

## Exceptions

승인된 예외 없음.

### Verification

`LAB_DATA_DIR=/tmp/hy-home-lab-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra.yml --profile cassandra config --quiet`와 문서 링크 검사를 수행한다. 실제 CQL·복원은 `NOT_RUN`으로 기록한다.

### Review Cadence

이미지·profile·mount·접속·인증 계약 변경 시 검토한다.

### Traceability

- Declared parent: [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)
- Subject peers: [GDE-0025](../guides/0025-cassandra.md), [RUN-0025](../runbooks/0025-cassandra.md)

## Related Documents

- [LAB Compose](../../../labs/cassandra.yml)
- [LAB 설명](../../../labs/cassandra.md)
- [Cassandra backup](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
