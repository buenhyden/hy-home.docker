---
title: "독립 LAB 문서 가이드"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 독립 LAB 문서 가이드

## Overview

독립 LAB 문서의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Valkey Cluster Usage Guide](0022-valkey-cluster.md) | `GDE-0022` | 이 가이드는 선택적 six-node Valkey Cluster 실습을 설명한다. 모든 node가 Docker host 하나를 공유하므로 M0021은 모든 service를 **LAB**으로 분류한다. 이 cluster는 HOME workflow brok |
| [Cassandra Usage Guide](0025-cassandra.md) | `GDE-0025` | 독립 `labs/cassandra.yml`은 공식 `labs/cassandra.yml`에 선언된 공식 Cassandra 이미지의 단일 `cassandra-node1` 실습용 정의다. HOME root는 include하지 않으며 확인된 HOME 소비자는 |
| [CouchDB Usage Guide](0026-couchdb.md) | `GDE-0026` | 이 문서는 CouchDB Compose 구현의 3노드 클러스터 사용 기준을 설명한다. `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`는 정확히 `couchdb` profile과 선언된 ne |
| [MongoDB Usage Guide](0027-mongodb.md) | `GDE-0027` | 이 문서는 MongoDB Compose 구현의 replica set 사용 기준을 설명한다. 일곱 서비스는 모두 정확히 `mongodb` profile과 선언된 network에서 동작한다. frozen classification은 `LAB`이고 두 da |
| [Supabase Usage Guide](0029-supabase.md) | `GDE-0029` | `supabase`는 정상 root에서 분리된 LAB Compose의 exact `supabase` profile 기반 통합 백엔드 실험 환경이다. 13개 서비스가 PostgreSQL, Kong, Auth, REST, Realtime, Storage, |
| [PostgreSQL Cluster Usage Guide](0031-postgresql-cluster.md) | `GDE-0031` | 이 문서는 PostgreSQL cluster Compose 구현의 etcd/Patroni/HAProxy stack을 설명한다. 열한 서비스는 모두 exact `postgres-ha` profile에서 동작한다. frozen classification은 |
| [Locust Usage Guide](0062-locust.md) | `GDE-0062` | Locust는 `labs/locust.yml`의 `lab-locust-master`와 `lab-locust-worker`로 구성된 독립 LAB 분산 부하 생성기다. HOME root Compose와 `testing` profile에는 포함되지 않는다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

이동 대상은 LAB 관련 운영 문서다. 서비스 소스는 저장소 루트 `labs/`가 소유한다.
문서 이동은 LAB 서비스 기동, 배포, 비밀번호 변경, 데이터 이동·삭제 또는 복구 실행을 뜻하지 않는다.

## Related Documents

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
