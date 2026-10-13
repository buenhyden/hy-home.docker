---
title: "데이터베이스와 저장소 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 데이터베이스와 저장소 가이드

## Overview

데이터베이스와 저장소의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [OpenSearch Usage Guide](0019-opensearch.md) | `GDE-0019` | 정상 `opensearch`는 선택형 단일 노드다. 정상 root는 `infra/04-data/opensearch/docker-compose.yml`의 `opensearch`와 `opensearch-dashboards`만 include한다. 세 노드  |
| [SeaweedFS Usage Guide](0024-seaweedfs.md) | `GDE-0024` | SeaweedFS는 S3 object store이며 SPEC-0180 S07에서 MinIO를 대체했다. |
| [Management Database Usage Guide](0028-management-database.md) | `GDE-0028` | management database는 인증, 워크플로, 도구를 위한 6개 서비스(PG 엔진·init·monitor provision·exporter, Valkey 엔진·exporter)로 구성된 HOME 의존성이다. |
| [04-Data Optimization Hardening Usage Guide](0030-data-optimization-hardening.md) | `GDE-0030` | 이 subject는 data tier 전반의 static 제어를 검증한다: root profile 유효성, 명시적 persistence 소유권, secret, healthcheck, 리소스, 네트워크 경계, 복구 소유권. service 활성화, 데이터 |
| [Neo4j Usage Guide](0033-neo4j.md) | `GDE-0033` | 이 문서는 root compose에 active include된 [Neo4j Compose 구현](../../../../infra/04-data/neo4j/docker-compose.yml)을 설명한다. |
| [RedisInsight Usage Guide](0076-redisinsight.md) | `GDE-0076` | RedisInsight는 `admin`과 `admin-data` 하위의 OPTIONAL admin UI이다. |
| [SurrealDB Guide](0080-surrealdb.md) | `GDE-0080` | SurrealDB는 Open Notebook을 위한 `OPTIONAL` 데이터베이스로, 업스트림 호환성을 위해 운영 계약이 SurrealDB v2로 제한되어 있다. Compose 구현은 정확히 `surrealdb`와 `notebook` profile  |
| [Development Database Usage Guide](0100-development-database.md) | `GDE-0100` | `dev-db`는 미래 외부 프로젝트의 업무 데이터를 위한 선택형 개발 엔진이다. 관리 서비스 metadata·세션·관리 queue는 `mng-db`에 계속 남는다. `app_db`는 신규 프로젝트의 공용 DB가 아니며, 현재 source integr |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
