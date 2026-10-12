---
title: "데이터 계층 (04-data)"
version: "1.3.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
created: "2025-11-12"
---

# 04 데이터

## Overview

데이터 저장·접근 기반 패키지를 서비스 이름으로 바로 배치합니다. 처리·변환·품질
검증·BI는 [12 Analytics](../12-analytics/README.md)가 담당합니다. 루트 Compose는 정상 HOME 패키지만 include합니다.

## Audience

공유 데이터와 선택형 데이터베이스의 operator·maintainer를 위한 인덱스입니다.

## Scope

HOME 공유 상태와 개발 DB, 오브젝트·벡터 저장소, OPTIONAL 데이터 플랫폼을
다룹니다. 애플리케이션 업무 로직과 분석 처리의 소유권은 포함하지 않습니다.

## Structure

| Package | 역할 | 분류 | 선택·소비 경계 |
| --- | --- | --- | --- |
| [mng-db](mng-db/) | 공유 PostgreSQL·Valkey | HOME | 관리 metadata·세션·큐; 패키지의 profile 참조 |
| [dev-db](dev-db/) | 개발 PostgreSQL·Valkey | OPTIONAL | `dev-data`; 프로젝트별 업무 데이터 provision |
| [supabase](supabase/) | 별도 데이터 플랫폼 | OPTIONAL | `supabase`; 공유 mng-db와 스키마·볼륨을 합치지 않음 |
| [seaweedfs](seaweedfs/) | 공유 S3·Iceberg REST catalog | HOME | `storage`; 관측·AI·Analytics가 함께 사용 |
| [opensearch](opensearch/) | 단일 검색·인덱스 저장소 | OPTIONAL | `opensearch` |
| [neo4j](neo4j/) | 그래프 저장소 | OPTIONAL | `graph` |
| [redisinsight](redisinsight/) | Redis/Valkey 관리 UI | OPTIONAL | `admin`, `admin-data`; 대상 데이터는 각 엔진 소유 |
| [qdrant](qdrant/) | 벡터 저장소 | HOME | `ai`, `ai-llm`, `qdrant` |

SurrealDB는 단일 소비자인 [Open Notebook](../08-ai/open-notebook/) 패키지에
속합니다. Data가 플랫폼의 모든 영속 상태를 소유하는 것은 아닙니다.

RedisInsight `/data`는 민감한 연결·설정 메타데이터를 보관합니다. 현재 추적된
`RI_ENCRYPTION_KEY`는 없으며 대상 데이터 백업과 별도로 복구합니다. Gateway·
admin CIDR·SSO 경계를 유지하고 내부 네트워크 접근도 별도로 검토합니다.

## Tech Stack

PostgreSQL·Valkey·SeaweedFS·Qdrant와 선택형 데이터 엔진의 버전은 각 패키지 Compose 및 Dockerfile이 소유합니다.

## Configuration

[루트 Compose](../../docker-compose.yml)의 include와 각 패키지의 profile·network·secret 선언을 함께 확인합니다.

## Validation

`python3 scripts/validation/run-ci-gate.py --profile changed`는 변경 경로에 맞는 검증을 선택합니다. 실행 여부와 종료 코드는 해당 Task에 기록합니다.

## Usage

- 저장소 루트에서 정확한 profile을 선택합니다. `core`나 디렉터리 이름만으로
  데이터 의존성 전체가 기동되지는 않습니다.
- 모든 상태 소유자는 named consumer, 용량·보존 경계, 엔진 지원 백업, 별도 암호화
  목적지와 격리된 복구 절차가 필요합니다. named volume 자체는 백업이 아닙니다.
- SeaweedFS는 소비자별 bucket identity를 사용합니다. 이전 MinIO 데이터는 기존
  복구 절차에 따라 보존하며 폴더 정리 때문에 제거하지 않습니다.
- runtime 버전은 각 Compose/Dockerfile 선언을 따릅니다. 서비스별 설정·secret
  참조·운영 문서는 정상 패키지 README에서 찾습니다.

## Related Documents

- [독립 LAB 인덱스](../../labs/README.md)

- [인프라 인덱스](../README.md)
- [문서 진입점](../../docs/README.md): Stage 05의 서비스 Guide·Policy·Runbook,
  백업 POL-0021 및 저장 공간 RUN-0035를 확인합니다.
