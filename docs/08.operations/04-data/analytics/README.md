# Analytics Operations (04-Data)

> Operational policies and governance for the analytical data tier.

## Overview (KR)

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 운영 정책을 관리한다. 자원 통제, 보안 규약, 백업 주기 및 보존 정책을 정의하여 시스템의 안정성과 규정 준수를 보장한다.

## Audience

이 README의 주요 독자:

- **Operators**: 시스템 자원 관리 및 백업/보안 정책 실행
- **Compliance Officers**: 데이터 보존 및 보안 규정 준수 확인
- **AI Agents**: 자원 최적화 및 정책 기반 자동화 수행

## Scope

### In Scope

- 데이터 엔진별 자원 할당 정책 (JVM, CPU, Memory)
- 데이터 백업 및 보존(Retention) 주기 정책
- 접근 제한 및 보안 통제 기준
- 운영 감사 및 규정 준수 확인 절차

### Out of Scope

- 실시간 장애 대응 절차 (-> `09.runbooks/` 담당)
- 시스템 이해 및 사용법 (-> `07.guides/` 담당)
- 인프라 배포 코드 관리 (-> `infra/` 담당)

## Structure

```text
analytics/
├── influxdb.md      # InfluxDB Operations Policy
├── ksqldb.md        # ksqlDB Operations Policy
├── opensearch.md    # OpenSearch Operations Policy
├── warehouses.md    # StarRocks Operations Policy
└── README.md        # This file
```

## How to Work in This Area

1. 정책 변경 시 반드시 **ARD-0012** 분석 아키텍처 원칙과 대조한다.
2. 모든 정책 문서는 `operation.template.md`를 기반으로 작성한다.
3. 정책 수정 후에는 반드시 관련 런북(`09.runbooks/`)의 실행 절차와의 일치 여부를 확인한다.
4. AI Agent는 정책 위반 사례 발견 시 즉시 사용자에게 보고하고 대응 시나리오를 제안한다.

## Related References

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Guides**: [docs/07.guides/04-data/analytics/](../../../07.guides/04-data/analytics/README.md)
- **Runbooks**: [docs/09.runbooks/04-data/analytics/](../../../09.runbooks/04-data/analytics/README.md)

## AI Agent Guidance

1. 운영 정책은 시스템의 제약 사항을 정의하므로, 인프라 변경 제안 시 이 폴더의 정책을 우선적으로 참조한다.
2. 정책 문서의 `Controls` 섹션을 분석하여 자동화된 가드레일을 구축한다.
3. 중복된 정책이 존재할 경우 SSoT로 통합하고 상호 참조 링크를 갱신한다.

---
Copyright (c) 2026. Analytics Tier Operations.
