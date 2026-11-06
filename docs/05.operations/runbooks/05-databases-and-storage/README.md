---
title: "데이터베이스와 저장소 런북"
version: "0.1.7"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
---

# 데이터베이스와 저장소 런북

## Overview

데이터베이스와 저장소의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [OpenSearch Recovery Runbook](0019-opensearch.md) | `RUN-0019` | 정상 단일 OpenSearch(`opensearch` profile)의 준비 상태 점검과 별도 standalone LAB `opensearch-cluster`의 정적·운영 경계를 다룬다. |
| [SeaweedFS Stack Health and Recovery Runbook](0024-seaweedfs.md) | `RUN-0024` | SeaweedFS 스택의 정적 진단, 경보 대응, 최초 활성화, 백업·격리 복구 절차를 다룬다. |
| [Management Database Health and Recovery Runbook](0028-management-database.md) | `RUN-0028` | management database의 정적 진단, 계획된 백업·격리 복구, monitor 계정과 경보 대응 절차를 다룬다. |
| [04-Data Optimization Hardening Runbook](0030-data-optimization-hardening.md) | `RUN-0030` | data tier(`infra/04-data`)의 정적 hardening 점검 절차와 회귀 대응을 다룬다. 서비스 실행과 데이터 복구는 포함하지 않는다. |
| [PostgreSQL Logical Upgrade and Restore Rehearsal Runbook](0032-postgresql-logical-upgrade-restore-rehearsal.md) | `RUN-0032` | synthetic fixture를 PostgreSQL source major에서 logical backup으로 캡처해 target major isolated image에 복원·비교하는 로컬 rehearsal 절차다. |
| [Neo4j Health and Recovery Triage Runbook](0033-neo4j.md) | `RUN-0033` | 단일 Community `neo4j`의 health triage와 offline dump 격리 복원 rehearsal 계약을 다룬다. |
| [04-Data Storage Exhaustion Runbook](0035-storage-exhaustion.md) | `RUN-0035` | 디스크 부족 경보·쓰기 거부 시 데이터를 삭제하지 않고 원인 owner를 가려 조치를 정하는 triage 절차다. |
| [RedisInsight Recovery Runbook](0076-redisinsight.md) | `RUN-0076` | RedisInsight의 gateway 접근, 설정 보존, inspector 비밀 회전, 업그레이드와 복구 절차를 다룬다. |
| [SurrealDB Runbook](0080-surrealdb.md) | `RUN-0080` | `surrealdb`의 헬스 트리아지와 계획된 격리 export/import 리허설을 다룬다. |
| [Development Database Source Preflight Runbook](0100-development-database.md) | `RUN-0100` | `dev-db` source 변경의 정적 사전 검사와 DEV 지표 경보·중지 절차를 다룬다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
