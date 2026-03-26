<!-- Target: docs/08.operations/04-data/analytics/opensearch.md -->

# OpenSearch Operations Policy

> Policy and governance for OpenSearch clusters.

---

## Overview (KR)

이 문서는 OpenSearch 운영 정책을 정의한다. 리소스 할당(JVM Heap), 보안 통제(Secrets), 인덱스 관리 및 검증 방법을 규정한다.

## Policy Scope

OpenSearch 엔진, Dashboards, 그리고 수반되는 데이터 볼륨의 운영 거버넌스.

## Applies To

- **Systems**: `opensearch`, `opensearch-dashboards`
- **Agents**: Data Tier Managing Agents
- **Environments**: Production, Staging

## Controls

- **Required**:
  - `OPENSEARCH_JAVA_OPTS`를 통한 명시적 힙 메모리 할당 (최소 1GB 권장).
  - 모든 API 통신은 HTTPS를 강제하며, Docker Secrets를 통한 비밀번호 관리 필수.
- **Allowed**:
  - 개발 환경에서의 싱글 노드 구성.
- **Disallowed**:
  - `admin` 계정의 하드코딩된 비밀번호 사용 금지.
  - 보안 플러그인 비활성화 금지 (Production).

## Exceptions

- 로컬 테스트 환경에서는 Self-signed 인증서 사용이 허용된다.

## Verification

- `/_cluster/health` API를 통해 클러스터 상태가 `green` 또는 `yellow`인지 정기적으로 확인한다.
- `prometheus-exporter`를 통한 힙 사용률(JVM Memory) 모니터링.

## Review Cadence

- Quarterly (분기별 임계치 및 보안 설정 검토)

## Related Documents

- **ARD**: `[../../02.ard/04-data-tier.md]`
- **Runbook**: `[../../../09.runbooks/04-data/analytics/opensearch.md]`
- **Postmortem**: `[N/A]`
