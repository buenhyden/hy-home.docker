---
title: "데이터베이스와 저장소 정책"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 데이터베이스와 저장소 정책

## Overview

데이터베이스와 저장소의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [OpenSearch Operations Policy](0019-opensearch.md) | `POL-0019` | 이 문서는 정상 root의 단일 OpenSearch와 별도 standalone LAB 클러스터의 운영 경계를 정의합니다. 정상 구성은 `infra/04-data/opensearch/docker-compose.yml`의 선언된 OpenSearch cus |
| [SeaweedFS Operations Policy](0024-seaweedfs.md) | `POL-0024` | 이 정책은 현재 소스 구성을 데이터 보호, 보안, 리소스, 생명주기와 독립적으로 검증 가능한 운영 통제에 묶는다. |
| [Management Database Operations Policy](0028-management-database.md) | `POL-0028` | 이 정책은 현재 소스 구성을 데이터 보호, 보안, 리소스, 생명주기와 독립적으로 검증 가능한 운영 통제에 묶는다. |
| [04-Data Optimization Hardening Operations Policy](0030-data-optimization-hardening.md) | `POL-0030` | 이 정책은 현재 소스 구성을 데이터 보호, 보안, 리소스, 생명주기와 독립적으로 검증 가능한 운영 통제에 묶는다. |
| [Neo4j Operations Policy](0033-neo4j.md) | `POL-0033` | 이 정책은 root-active `OPTIONAL` Neo4j 운영 기준을 정의한다. |
| [RedisInsight Operations Policy](0076-redisinsight.md) | `POL-0076` | RedisInsight는 OPTIONAL 자격 증명 보유 관리자 클라이언트다. Gateway 접근은 각 대상 데이터베이스에 대한 최소 권한 부여를 대체하지 않는다. |
| [SurrealDB Policy](0080-surrealdb.md) | `POL-0080` | 이 정책은 `08-ai` 티어 내에서 Open Notebook이 사용하는 `OPTIONAL` 단일 서비스 SurrealDB 배포를 다룬다. |
| [Development Database Operations Policy](0100-development-database.md) | `POL-0100` | 현재 source 인계 소유자는 SPEC-0204이며, SPEC-0202의 합성 검증은 보관된 역사적 근거이다. 이 정책은 source-only `dev-pg`와 `dev-valkey`의 관리 데이터 분리, 최소 권한 provision, 그리고 승인  |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
