# Analytics Runbooks (04-Data)

> Step-by-step recovery and maintenance procedures for the analytical data tier.

## Overview (KR)

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 실행 런북을 관리한다. 장애 발생 시 즉각적으로 대응할 수 있는 단계별 절차와 일상적인 유지보수 작업 지침을 제공한다.

## Audience

이 README의 주요 독자:

- **Operators**: 장애 복구 및 유지보수 작업 수행
- **SREs**: 시스템 안정성 보장을 위한 런북 유지보수
- **AI Agents**: 장애 상황 감지 시 자동 대응 절차 실행

## Scope

### In Scope

- 분석 엔진 노드 복구 및 재시작 절차
- 데이터 손상 시 복구 및 동기화 작업
- 성능 저하 시 진단 및 튜닝 단계
- 인프라 리전 이동 또는 클러스터 마이그레이션

### Out of Scope

- 시스템 설계 및 기본 가이드 (-> `07.guides/` 담당)
- 운영 정책 정의 (-> `08.operations/` 담당)
- 일반 사용자 지원 업무

## Structure

```text
analytics/
├── influxdb.md      # InfluxDB Recovery Runbook
├── ksqldb.md        # ksqlDB Recovery Runbook
├── opensearch.md    # OpenSearch Recovery Runbook
├── warehouses.md    # StarRocks Recovery Runbook
└── README.md        # This file
```

## How to Work in This Area

1. 모든 런북은 즉시 실행 가능한 형태(Bash 명령어 등 포함)로 작성한다.
2. 모든 런북은 `runbook.template.md`를 기반으로 작성한다.
3. 런북 실행 전 반드시 관련 운영 정책(`08.operations/`)의 제약 사항을 확인한다.
4. AI Agent는 장애 탐지 시 관련 런북을 검색하여 대응 방안을 즉시 제시한다.

## Related References

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **Guides**: [docs/07.guides/04-data/analytics/](../../../07.guides/04-data/analytics/README.md)
- **Operations**: [docs/08.operations/04-data/analytics/](../../../08.operations/04-data/analytics/README.md)
- **Incidents**: [docs/10.incidents/](../../../10.incidents/README.md)

## AI Agent Guidance

1. 런북의 명령어는 시스템 상태에 따라 파라미터를 동적으로 조정해야 할 수 있으므로 실행 전 반드시 사용자 주의 문구를 포함한다.
2. 실행된 모든 단계와 결과는 `10.incidents/`에 기록하여 향후 Postmortem의 기반이 되도록 한다.
3. 복구가 완료된 후에는 `Verification Steps`를 통해 정상 작동 여부를 반드시 확인한다.

---
Copyright (c) 2026. Analytics Tier Runbooks.
