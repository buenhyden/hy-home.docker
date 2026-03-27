# OpenSearch

> Distributed search and analytics engine with Dashboards.

## Overview (KR)

`opensearch` 스택은 로그 집계, 풀텍스트 검색 및 실시간 시각화를 위한 확장 가능한 검색 백엔드를 제공한다. 고가용성 관측성 및 분석 워크로드를 위해 설계되었다.

## Audience

이 README의 주요 독자:

- **Developers**: 검색 쿼리 및 데이터 인덱싱 설계
- **Operators**: 노드 상태 관리 및 보안 설정
- **AI Agents**: 인프라 탐색 및 검색 효율 분석

## Scope

### In Scope

- OpenSearch 2.18 및 Dashboards 3.4.0을 위한 Docker 인프라
- 자원 할당(JVM Heap) 및 볼륨 영속성 관리
- 보안 설정 (Docker Secrets, HTTPS 적용)
- 커스텀 빌드 이미지를 통한 플러그인 관리

### Out of Scope

- 상세 검색 쿼리 로직 개발 (-> 시스템 가이드 참조)
- 인덱스 보존 정책 설계 (-> 운영 정책 참조)
- 개별 노드 장애 복구 절차 (-> 런북 참조)

## Structure

```text
opensearch/
├── opensearch/             # Engine configuration
├── opensearch-dashboards/  # Visualization configuration
├── Dockerfile              # Custom build for security
├── docker-compose.yml      # Standard stack
└── README.md               # This file
```

## How to Work in This Area

1. 아키텍처 컨텍스트는 [시스템 가이드](../../../../docs/07.guides/04-data/analytics/opensearch.md)를 참조한다.
2. 자원 거버넌스는 [운영 정책](../../../../docs/08.operations/04-data/analytics/opensearch.md)을 확인한다.
3. 유지보수 및 복구 절차는 [복구 런북](../../../../docs/09.runbooks/04-data/analytics/opensearch.md)을 사용한다.

## Related References

- **System Guide**: [docs/07.guides/04-data/analytics/opensearch.md](../../../../docs/07.guides/04-data/analytics/opensearch.md)
- **Operations**: [docs/08.operations/04-data/analytics/opensearch.md](../../../../docs/08.operations/04-data/analytics/opensearch.md)
- **Runbook**: [docs/09.runbooks/04-data/analytics/opensearch.md](../../../../docs/09.runbooks/04-data/analytics/opensearch.md)
- **Monitoring**: `opensearch-exporter:9114/metrics`

## AI Agent Guidance

1. OpenSearch 설정 변경 시 JVM Heap 메모리 설정을 신중히 확인한다.
2. HTTPS 및 보안 플러그인 설정을 수정할 때 인증서 경로를 누락하지 않도록 주의한다.
3. 인덱스 생성 및 삭제 작업을 자동화하기 전에 운영 정책의 데이터 보존 주기를 먼저 읽는다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
