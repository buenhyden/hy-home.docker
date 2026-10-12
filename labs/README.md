---
title: "독립 LAB source"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
created: "2026-10-12"
---

# 독립 LAB source

## Overview

이 디렉터리는 정상 root Compose와 분리된 LAB entrypoint, 공개 안내와
LAB 전용 build·bind source를 보관합니다. 운영 문서의 LAB 분류 위치는
`docs/05.operations/`의 유형별 `labs/`이며 이 runtime source family와 구분합니다.

## Audience

LAB source 관리자, 운영자와 정적 검토자입니다.

## Scope

source 경로와 공개 구성의 탐색입니다. 실제 기동, 이미지 업데이트, 비밀값 이관,
부하 생성, 데이터 삭제·복구를 문서 이동으로 승인하거나 완료로 처리하지 않습니다.

## Structure

| LAB | Entry point와 안내 | Source 자산 |
| --- | --- | --- |
| PostgreSQL HA | [Compose](postgresql-ha.yml), [안내](postgresql-ha.md) | [config·wrapper·초기화 SQL](postgresql-ha/README.md) |
| Valkey Cluster | [Compose](valkey-cluster.yml), [안내](valkey-cluster.md) | [config·scripts](valkey-cluster/README.md) |
| Locust | [Compose](locust.yml), [안내](locust.md) | [build source](locust/README.md) |
| Cassandra | [Compose](cassandra.yml), [안내](cassandra.md) | 독립 Compose source |
| CouchDB | [Compose](couchdb.yml), [안내](couchdb.md) | [initializer](couchdb-cluster-init.sh) |
| MongoDB | [Compose](mongodb.yml), [안내](mongodb.md) | 독립 Compose source |
| Kafka | [Compose](kafka-cluster.yml), [안내](kafka-cluster.md) | 독립 Compose source |
| OpenSearch | [Compose](opensearch-cluster.yml), [안내](opensearch-cluster.md) | [Dashboards 설정](opensearch-cluster-dashboards.config) |

[dashboards](dashboards/README.md)는 기존 LAB 관측 자산을 보관합니다.
[공개 환경 예시](.env.example)는 정적 구성 입력이며 실제 비밀값을 저장하지 않습니다.

## Configuration

데이터 LAB의 역할과 선택 경계는 다음과 같습니다. 각 flat Compose와 안내가
실제 profile·source·권한 계약을 소유합니다.

| LAB | 역할 | Profile·진입점 | 실행·상태 경계 |
| --- | --- | --- | --- |
| [PostgreSQL HA](postgresql-ha/README.md) | Patroni·etcd·HAProxy 토폴로지 | `postgres-ha` | HOME mng-pg와 별개 |
| [Valkey Cluster](valkey-cluster/README.md) | 6노드 캐시·KV 토폴로지 | `valkey-cluster` | HOME mng-valkey와 별개 |
| [Cassandra](cassandra.md) | wide-column 저장소 | `cassandra` | 독립 LAB |
| [CouchDB](couchdb.md) | 문서 동기화 저장소 | `couchdb` | 독립 LAB |
| [MongoDB](mongodb.md) | 문서 저장소·replica set | `mongodb` | 독립 LAB |
| [OpenSearch Cluster](opensearch-cluster.md) | 세 노드 검색 토폴로지 | `opensearch-cluster` | HOME 단일 노드와 별개 |
| [Locust](locust/README.md) | 독립 부하 검증 image source | `labs/locust.yml` | root include와 HOME 상태를 공유하지 않음 |

Locust 전용 공개 입력은 [.env.example](.env.example)의 `LAB_LOCUST_*`를
사용합니다. Locust source는 이 독립 entrypoint용이며 root profile에 추가하지
않습니다. 실제 부하 target·권한·종료 조건은 별도 수용 입력입니다.

## Usage

각 flat entrypoint는 기존 `scripts/operations/lab.py`의 exact LAB 이름으로
선택합니다. 실제 실행 전에는 목적·lease·대상·resource·권한·정리와 복구 경계를
별도로 확정해야 하며, source render는 native 성공의 증거가 아닙니다.
공유 `infra/common-optimizations.yml`의 재사용 외에 LAB 전용 build와 bind source는
이 family에 둡니다. 운영 데이터와 secret의 위치·값은 이번 source 이동으로 바꾸지 않습니다.

같은 호스트의 복제 노드는 호스트 장애를 격리하지 않습니다. HOME 단일 인스턴스와
LAB 클러스터를 구분하고 성능·HA를 측정 없이 보장하지 않습니다. Valkey LAB 복구에는
조율된 RDB checkpoint와 완전한 AOF set/manifest, 새로운 cluster identity가 필요합니다.
게시된 client/bus 포트의 노출 경계를 유지합니다. 이 source 정리는 복구 실행 증거가 아닙니다.

## Related Documents

- [문서 탐색](../docs/README.md)
- [운영 문서 탐색](../docs/05.operations/README.md)
