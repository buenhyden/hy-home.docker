<!-- Target: docs/08.operations/04-data/analytics/opensearch.md -->

# OpenSearch Operations Policy

> Operational policy for search engines, log aggregation, and security.

---

## Overview (KR)

이 문서는 OpenSearch 운영 정책을 정의한다. 로그 데이터의 저장 기간, 샤드(Shard) 및 복제본(Replica) 관리 기준, 그리고 보안 인증 및 접근 통제 규약을 규정한다.

## Policy Scope

이 정책은 플랫폼 내 모든 OpenSearch 클러스터, 데이터 노드 및 Dashboards 시각화 인터페이스를 관리한다.

## Applies To

- **Systems**: OpenSearch, OpenSearch Dashboards, Index Shuffling Scripts
- **Agents**: Log Analysis Agents, Security Pattern Detectors
- **Environments**: Production (Cluster), Staging, Dev (Single Node)

## Controls

- **Required**:
  - 모든 인덱스는 최소 1개 이상의 복제본(Replica)을 가져야 함 (가용성 보장).
  - JVM Heap 크기는 가용한 물리 메모리의 50%를 초과하지 않도록 설정.
  - 외부 접근은 반드시 HTTPS를 경유해야 하며, IP 화이트리스트를 적용함.
- **Allowed**:
  - 특정 기간 이후 로그 데이터의 스냅샷(Snapshot) 생성 및 S3 이동.
  - 비즈니스 로직에 따른 커스텀 분석기(Analyzer) 추가.
- **Disallowed**:
  - `admin` 계정의 패스워드를 평문으로 인프라 코드에 하드코딩 금지.
  - 인증되지 않은 데이터 벌크(Bulk) 로드 제안 금지.

## Exceptions

- 테스트 환경에서 자원 절약을 위해 일시적으로 복제본(Replica)을 0으로 설정하는 것을 허용 (단, 72시간 이내 원복).

## Verification

- `_cluster/health` API를 통한 클러스터 상태(Green/Yellow) 주기적 점검.
- Curator 또는 ISM(Index State Management)을 통한 인덱스 생명주기 검증.

## Review Cadence

- Quarterly (분기별)

## AI Agent Policy Section

- **Log Cache Policy**: 빈번하게 사용되는 검색 결과 캐시는 10GB로 제한.
- **Eval Threshold**: 검색 쿼리 지연시간이 200ms를 초과할 경우 알림 및 인덱싱 성능 튜닝 수행.

## Related Documents

- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **Runbook**: [opensearch.md](../../../09.runbooks/04-data/analytics/opensearch.md)
