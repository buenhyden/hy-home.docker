---
title: "12 Analytics"
version: "0.1.0"
type: "common/package-readme"
status: "review"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-10-01"
---

# 12 Analytics

## Overview

저장소를 사용하는 데이터 처리·변환·조회·품질 검증·BI 패키지입니다.
[04 Data](../04-data/README.md)의 공유 저장소와 기존 루트 Compose를 사용합니다.
폴더 분리는 새 Compose 프로젝트나 보안·장애 격리를 만들지 않습니다.

## Audience

데이터 엔지니어, 분석 사용자와 패키지 운영자를 위한 인덱스입니다.

## Scope

분석 작업의 실행 패키지를 소유합니다. 작업 스케줄과 재시도 조정은 Workflow,
이벤트 전달은 Messaging, 공유 데이터 저장은 Data가 소유합니다.

## Structure

| Package | 역할 | 분류·profile | 주요 의존성 |
| --- | --- | --- | --- |
| [flink](flink/) | 스트림·배치 SQL 처리 | OPTIONAL / `lakehouse` | SeaweedFS Iceberg catalog; Kafka 입력은 별도 선택 |
| [spark](spark/) | 배치·테이블 관리 작업 | OPTIONAL / `lakehouse` | SeaweedFS Iceberg catalog |
| [trino](trino/) | SQL 조회 | OPTIONAL / `lakehouse` | SeaweedFS Iceberg catalog |
| [great-expectations](great-expectations/) | 데이터 품질 검증 작업 | OPTIONAL / `lakehouse` | Trino |
| [superset](superset/) | 데이터 탐색·BI | OPTIONAL / `bi` | mng-pg 메타데이터, Keycloak, 설정된 Trino 데이터 소스 |
| [jupyterlab](jupyterlab/) | 대화형 데이터 분석 | OPTIONAL / `data-science` | 토큰 인증, 선택적 MLflow 연계 |
| [dbt](dbt/) | PostgreSQL SQL 변환 작업 | OPTIONAL / `analytics-engineering` | mng-pg와 기능 전용 역할·스키마 |

JupyterLab은 단일 사용자 코드 실행 환경이며 JupyterHub나 프로덕션 notebook
플랫폼을 제공하지 않습니다. 필수 서버 토큰과 기존 gateway/SSO를 유지합니다.
notebook은 `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`에 보관하며 실행 전
디렉터리 존재와 UID1000 소유권을 확인합니다. `data-science`는 AI tier의
MLflow도 선택하지만 폴더 번호가 기동 순서나 물리적 격리를 만들지는 않습니다.

## How to Work in This Area

- 저장소 루트에서 각 profile을 선택합니다. `analytics`라는 새 기동 profile은
  추가하지 않았고 HOME 선택도 바뀌지 않습니다.
- Flink checkpoint와 Superset 메타데이터는 영속 상태입니다. Analytics라는
  분류가 데이터 삭제나 백업 제외를 허용하지 않습니다.
- Spark·GX·dbt는 1회성 작업입니다. dbt는 PostgreSQL 어댑터를 유지하며 `run`과
  `build`는 대상 스키마에 씁니다. 기본 명령과 부작용은 패키지 README를 따릅니다.
- Trino·Flink의 loopback 경계와 기존 secret·volume·network 연결을 유지합니다.
- 공개 설정 점검: `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`.
  tier 정적 점검: `bash scripts/hardening/check-all-hardening.sh 12-analytics`.

## Related Documents

- [인프라 인덱스](../README.md)
- [문서 진입점](../../docs/README.md): Stage 05의 Lakehouse 0094, Superset 0097,
  dbt 0090 Guide·Policy·Runbook을 확인합니다.
