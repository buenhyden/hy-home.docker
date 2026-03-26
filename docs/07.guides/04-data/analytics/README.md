# Analytics Documentation (04-Data)

> Guides, operations, and runbooks for the analytical data tier.

## Overview

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 시스템 가이드, 운영 정책 및 복구 절차를 관리한다. "Golden 5" 택소노미에 따라 시스템 이해(Guide)와 실행 지침(Operation/Runbook)을 분리하여 관리한다.

## Audience

- **Architects**: 데이터 분석 파이프라인 설계 및 엔진 선택 기준 이해
- **Operators**: 분석 노드 상태 점검 및 장애 복구 수행
- **Data Scientists**: 분석 스키마 및 쿼리 인터페이스 활용
- **AI Agents**: 분석 데이터 추출 및 최적화 제안

## Scope

### In Scope

- 인퍼런스 및 분석용 엔진 설정 가이드
- 각 엔진별 영구 데이터 관리 및 백업 절차
- 데이터 보존(Retention) 정책 및 실시간 처리 규약

### Out of Scope

- 핵심 트랜잭션 데이터베이스 관리 (-> `04-data/core` 담당)
- 시각화 대시보드 UI 디자인

## Structure

```text
analytics/
├── influxdb.md      # InfluxDB (TSDB) 가이드 및 운영
├── ksqldb.md        # ksqlDB (Stream) 가이드 및 운영
├── opensearch.md    # OpenSearch (Logs) 가이드 및 운영
├── warehouses.md    # StarRocks (OLAP) 가이드 및 운영
└── README.md        # This file
```

## How to Work in This Area

1. 신규 분석 엔진 추가 시 반드시 **ADR-0015** 기술 선택 기록을 먼저 확인한다.
2. 각 엔진 문서 수정 시 **Spec-04-data-analytics**의 기술 규약을 준수한다.
3. 운영 절차 변경 시 관련 런북(`docs/09.runbooks/04-data/analytics/`)을 함께 갱신한다.

## Related References

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operations**: [docs/08.operations/04-data/analytics/](../../../08.operations/04-data/analytics/)
- **Runbooks**: [docs/09.runbooks/04-data/analytics/](../../../09.runbooks/04-data/analytics/)

---
Copyright (c) 2026. Analytics Tier Documentation.
