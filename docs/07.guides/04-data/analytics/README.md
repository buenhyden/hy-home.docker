# Analytics Documentation (04-Data)

> Guides, operations, and runbooks for the analytical data tier.

## Overview (KR)

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 시스템 가이드, 운영 정책 및 복구 절차를 관리한다. 시스템 이해(Guide)와 실행 지침(Operation/Runbook)을 분리하여 관리함으로써 운영 효율성을 극대화한다.

## Audience

이 README의 주요 독자:

- **Architects**: 데이터 분석 파이프라인 설계 및 엔진 선택
- **Operators**: 분석 노드 상태 점검 및 장애 복구
- **Data Engineers**: 분석 스키마 및 쿼리 인터페이스 활용
- **AI Agents**: 분석 데이터 추출 및 시스템 최적화 제안

## Scope

### In Scope

- 분석 엔진 설정 가이드 및 기술 규약
- 엔진별 데이터 보존 정책 및 실시간 처리 규약
- 운영 업무 자동화를 위한 복구 절차
- 하위 엔진별 세부 가이드 파일 아카이브

### Out of Scope

- 핵심 트랜잭션 데이터베이스 관리 (-> `04-data/relational` 담당)
- 시각화 대시보드 UI 디자인 가이드
- 인프라 배포 코드 관리 (-> `infra/04-data/analytics/` 담당)

## Structure

```text
analytics/
├── influxdb.md      # InfluxDB (TSDB) Guide
├── ksqldb.md        # ksqlDB (Stream) Guide
├── opensearch.md    # OpenSearch (Logs) Guide
├── warehouses.md    # StarRocks (OLAP) Guide
└── README.md        # This file
```

## How to Work in This Area

1. 신규 기술 도입 시 반드시 **ADR-0015** 기술 선택 기록을 먼저 확인한다.
2. 모든 가이드 문서는 `guide.template.md`를 기반으로 작성한다.
3. 문서 수정 시 관련 운영 정책(`08.operations/`) 및 런북(`09.runbooks/`)과 상호 참조 무결성을 확인한다.
4. AI Agent는 문서 생성 시 한국어 요약(Overview KR)을 반드시 포함한다.

## Related References

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Implementation**: [infra/04-data/analytics/](../../../infra/04-data/analytics/)
- **Operations**: [docs/08.operations/04-data/analytics/](../../../08.operations/04-data/analytics/README.md)
- **Runbooks**: [docs/09.runbooks/04-data/analytics/](../../../09.runbooks/04-data/analytics/README.md)

## AI Agent Guidance

1. 문서 계층 구조를 유지하기 위해 상위 README와 하위 문서 간의 링크를 반드시 검증한다.
2. 기술적 용어는 명확하게 사용하되, 의사결정의 원천은 항상 ADR을 참조한다.
3. 중복된 정보를 생성하기보다 SSoT 문서를 확장하는 방식으로 작업한다.

---
Copyright (c) 2026. Analytics Tier Documentation.
