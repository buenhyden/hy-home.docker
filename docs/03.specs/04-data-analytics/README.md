# 04-data-analytics Specifications

> 데이터 분석 파이프라인 및 워크플로우 서비스 기술 사양

## Overview

`docs/03.specs/04-data-analytics`는 Airflow, ksqlDB, dbt 등 분석 파이프라인 서비스의 기술 사양을 포함합니다.

## Scope

### In Scope

- 분석 파이프라인 서비스 인터페이스 및 스케줄링 사양
- 스트리밍 SQL 및 배치 처리 경계 정의

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/04-data/` 담당)
- 기본 데이터 저장 사양 (`04-data/` 담당)

## Structure

```text
04-data-analytics/
├── spec.md      # Data analytics services technical specification
└── README.md    # This file
```

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/04-data/README.md](../../../infra/04-data/README.md)
- [docs/05.operations/guides/04-data/](../../05.operations/guides/04-data/)
