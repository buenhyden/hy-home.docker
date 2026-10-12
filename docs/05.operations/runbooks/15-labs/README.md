---
title: "독립 LAB 문서 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 독립 LAB 문서 런북

## Overview

독립 LAB 문서의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Valkey Cluster Health Runbook](0022-valkey-cluster.md) | `RUN-0022` | LAB 전용 Valkey Cluster(`labs/valkey-cluster.yml`)의 정적 점검, 백업 계획, 격리 복원 절차를 다룬다. |
| [Cassandra Health and Recovery Triage Runbook](0025-cassandra.md) | `RUN-0025` | 독립 Cassandra 단일 노드 LAB의 정적 점검과 승인 후 read-only triage 순서다. 이번 변경에서 실제 서비스·데이터를 실행하지 않았다. |
| [CouchDB Cluster Triage Runbook](0026-couchdb.md) | `RUN-0026` | 범위: LAB 전용 CouchDB 3노드 cluster의 상태, cluster-init 결과, membership, 격리 network의 route 한계를 점검한다. 이 런북은 현재 compose에 맞는 점검 순서와, 별도 승인 후 수행할 fresh  |
| [MongoDB Replica Set Triage Runbook](0027-mongodb.md) | `RUN-0027` | 범위: LAB 전용 MongoDB replica set의 상태, init job 결과, Mongo Express 접속을 파괴적 데이터 작업 없이 점검한다. 이 런북은 현재 compose에 맞는 점검 순서와, 별도 승인 후 수행할 oplog-consis |
| [Supabase Stack Health Runbook](0029-supabase.md) | `RUN-0029` | 이 런북은 health triage와 별도 승인 후 수행할 coherent Supabase backup의 격리 복원 rehearsal 계약을 제공한다. 정상 root와 분리된 `labs/supabase.yml` LAB의 controller prefli |
| [PostgreSQL Cluster Health and Recovery Triage Runbook](0031-postgresql-cluster.md) | `RUN-0031` | 범위: LAB 전용 PostgreSQL HA cluster의 상태, etcd quorum 증상, HAProxy routing, Patroni leadership, init job 상태, exporter readiness를 파괴적 데이터 작업 없이 점검 |
| [Locust Recovery Runbook](0062-locust.md) | `RUN-0062` | Locust LAB 실행 중 target 상태가 나빠지거나 worker 연결이 끊길 때 부하를 멈추고 진단하는 절차다. 시나리오 파일 복구와 승인된 upgrade canary도 다룬다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

이동 대상은 LAB 관련 운영 문서다. 서비스 소스는 저장소 루트 `labs/`가 소유한다.
문서 이동은 LAB 서비스 기동, 배포, 비밀번호 변경, 데이터 이동·삭제 또는 복구 실행을 뜻하지 않는다.

## Related Documents

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
