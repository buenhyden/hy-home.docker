---
title: "Data Tier (04-data)"
version: "1.2.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# 04 Data

## Overview

이 tier는 영속 엔진과 상태 저장이 필요한 플랫폼 의존성을 담습니다. 루트
Compose 프로젝트가 leaf 파일을 include하고 공유 네트워크, secret, `extends`를
소유합니다. leaf를 독립 프로젝트로 다루지 말고 저장소 루트에서 운영하십시오.

## Audience

이 패키지 맵의 독자는 저장소 데이터 tier의 operator와 maintainer입니다.

## Scope

루트 Compose 프로젝트가 선택하는 데이터 패키지 카테고리와 카테고리별로 문서화된 운영
경계를 다룹니다.

## Structure

### 카테고리 맵

| Category | Directory | Summary |
| --- | --- | --- |
| [operational/](operational/README.md) | 운영 데이터 | `mng-db`(HOME 공유 PostgreSQL/Valkey), `supabase`(OPTIONAL 별도 애플리케이션 플랫폼) |
| [cache-and-kv/](cache-and-kv/README.md) | 캐시/키-값 저장소 | `valkey-cluster`(LAB) |
| [lake-and-object/](lake-and-object/README.md) | Lake/오브젝트 저장소 | `seaweedfs`(HOME S3 스토어, Iceberg REST catalog 제공) |
| [analytics/](analytics/README.md) | 분석 | `influxdb`(OPTIONAL), `opensearch`(OPTIONAL/LAB), `superset`(OPTIONAL BI) |
| [lakehouse/](lakehouse/) | Lakehouse(README 없음, 폴더 자체를 확인) | `flink`, `great-expectations`, `spark`, `trino`(모두 OPTIONAL) |
| [nosql/](nosql/README.md) | NoSQL | `cassandra`, `couchdb`, `mongodb`(모두 LAB) |
| [relational/](relational/README.md) | 관계형 데이터베이스 | `postgresql-cluster`(LAB) |
| [specialized/](specialized/README.md) | 특화 데이터 서비스 | `qdrant`(HOME 벡터 스토어), `neo4j`(OPTIONAL 그래프) |

각 서비스의 정확한 profile, classification, 관계는 해당 카테고리 README와
서비스별 README가 소유합니다.

SurrealDB는 유일한 소비자인 [`11-laboratory/open-notebook`](../11-laboratory/open-notebook/surrealdb/README.md)로
이전되어 이 tier에는 없습니다.

## How to Work in This Area

### Operating contract

- 루트 프로젝트를 통해 맵에 있는 정확한 profile을 사용합니다. 예:
  `docker compose --env-file .env.example --profile mng config --quiet`.
- 렌더링된 secret이나 비공개 resolved host 경로를 증거에 출력하지 않습니다.
- 호스트 디렉터리로 백업되는 named volume은 영속 상태일 뿐 백업이 아닙니다.
  동일 호스트 replica는 호스트 손실을 막지 못합니다.
- 선택된 모든 엔진에는 named consumer, 용량/보존 경계, 엔진 지원 백업, 별도
  암호화된 목적지, 격리된 복구 절차가 필요합니다.
- 이미지, 토폴로지, credential, volume, migration, 정리 변경에는 소유
  Stage 05 guide/policy/runbook과 승인된 task가 필요합니다.

## Related Documents

[문서 진입점](../../docs/README.md)을 사용해 Stage 05 운영 인덱스
(`docs/05.operations/README.md`)를 찾으십시오. 특히 HOME state-owner
matrix를 다루는 POL-0021과 storage exhaustion을 다루는 RUN-0035를 참고하십시오.
