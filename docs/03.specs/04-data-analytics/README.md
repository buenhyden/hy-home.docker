<!-- Target: docs/03.specs/04-data-analytics/README.md -->

# 04-data-analytics Specifications

> 데이터 분석 엔진 기술 사양

## Overview

`docs/03.specs/04-data-analytics`는 `infra/04-data/analytics`의 InfluxDB, ksqlDB, OpenSearch, StarRocks 엔진 계약을 포함합니다. 현재 구현은 InfluxDB 3.x Core를 primary compose로 사용하고 InfluxDB 2.x compose를 legacy Flux 호환 경로로 유지합니다. ksqlDB는 Kafka/Schema Registry/Connect dependency를 가진 optional analytics service이고, OpenSearch는 primary stack과 optional cluster variant를 분리하며, StarRocks는 standalone FE/BE compose로 관리합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- QA Engineers
- AI Agents

## Scope

### In Scope

- 시계열, 스트리밍 SQL, 로그 검색, OLAP 엔진 인터페이스 사양
- root-commented optional analytics compose의 integration and validation boundary
- current compose image/version family와 operations handoff

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/04-data/` 담당)
- 기본 데이터 저장 사양 (`04-data/` 담당)
- workflow orchestration 및 Airflow 스케줄링 사양 (`07-workflow/` 담당)

## Structure

```text
04-data-analytics/
├── spec.md      # Data analytics services technical specification
└── README.md    # This file
```

## How to Work in This Area

1. 구현 또는 검증 전 [spec.md](./spec.md)를 먼저 확인합니다.
2. 상위 요구사항과 아키텍처 맥락은 Related Documents의 PRD/ARD/ADR 링크에서 추적합니다.
3. 새 child contract가 필요하면 `docs/99.templates`의 대응 템플릿을 사용하고 이 폴더 README를 함께 갱신합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [Data analytics execution traceability plan](../../04.execution/plans/2026-05-22-data-analytics-execution-traceability.md)
- [Data analytics execution traceability task](../../04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md)
- [docs/03.specs/README.md](../README.md)
- [infra/04-data/README.md](../../../infra/04-data/README.md)
- [docs/05.operations/guides/04-data/](../../05.operations/guides/04-data/)
