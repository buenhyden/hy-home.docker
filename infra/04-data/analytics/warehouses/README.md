# StarRocks (OLAP Warehouse)

> High-performance analytical database for real-time analytics.

## Overview (KR)

`warehouses` 스택은 서브-세컨드 OLAP 쿼리 및 대규모 데이터 웨어하우징을 위해 StarRocks 클러스터 (FE 및 BE 노드)를 제공한다. `infra_net`과 통합되어 안전한 데이터 수집 및 쿼리를 지원한다.

## Audience

이 README의 주요 독자:

- **Data Engineers**: 데이터 수집 및 모델링 설계
- **Analytics Developers**: 대량 데이터 쿼리 최적화
- **AI Agents**: 인프라 탐색 및 웨어하우스 상태 분석

## Scope

### In Scope

- StarRocks Frontend (FE) 및 Backend (BE) 노드 구성
- 데이터 및 메타데이터를 위한 로컬 볼륨 영속성
- Prometheus Exporter를 통한 헬스 모니터링
- 클러스터 확장 및 기본 엔진 설정

### Out of Scope

- 외부 카탈로그 통합 (예: Iceberg, Hudi) (-> 시스템 가이드 참조)
- 루틴 데이터 수집 (ETL) 절차 수행
- 리소스 파티셔닝 및 멀티테넌시 세부 관리

## Structure

```text
warehouses/
├── fe/                 # Frontend metadata and configuration
├── be/                 # Backend storage and computation
├── docker-compose.yml  # Standard StarRocks stack
└── README.md           # This file
```

## How to Work in This Area

1. 아키텍처 컨텍스트는 [시스템 가이드](../../../../docs/07.guides/04-data/analytics/warehouses.md)를 참조한다.
2. 자원 거버넌스는 [운영 정책](../../../../docs/08.operations/04-data/analytics/warehouses.md)을 확인한다.
3. 유지보수 및 복구 절차는 [복구 런북](../../../../docs/09.runbooks/04-data/analytics/warehouses.md)을 사용한다.

## Related References

- **System Guide**: [docs/07.guides/04-data/analytics/warehouses.md](../../../../docs/07.guides/04-data/analytics/warehouses.md)
- **Operations**: [docs/08.operations/04-data/analytics/warehouses.md](../../../../docs/08.operations/04-data/analytics/warehouses.md)
- **Runbook**: [docs/09.runbooks/04-data/analytics/warehouses.md](../../../../docs/09.runbooks/04-data/analytics/warehouses.md)
- **Monitoring**: `starrocks-fe:8030/metrics`

## AI Agent Guidance

1. StarRocks 노드(FE/BE)를 수정하기 전에 메타데이터 저장 경로와 영속성 설정을 확인한다.
2. BE 노드 확장 시 FE 노드에서의 등록 절차를 런북에서 먼저 찾아본다.
3. 데이터 쿼리 효율성을 높이기 위해 스키마 변경을 제안하기 전 시스템 가이드의 최적화 파트를 읽는다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
