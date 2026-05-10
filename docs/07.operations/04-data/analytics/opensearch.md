<!-- Target: docs/07.operations/04-data/analytics/opensearch.md -->

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
- **Procedure**: [opensearch.md](../../../07.operations/04-data/analytics/opensearch.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/04-data/analytics/opensearch.md` during the 2026-05-10 operations taxonomy consolidation.

### OpenSearch System Usage

> Distributed search and analytics engine with Dashboards.

---

#### Overview (KR)

이 문서는 OpenSearch 시스템에 대한 가이드다. 검색 엔진의 구조, API 사용법, Dashboards를 통한 시각화 및 문제 해결 방법을 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agents

#### Purpose

OpenSearch 클러스터의 아키텍처를 이해하고, 검색 API 및 시각화 도구를 효과적으로 활용하는 것을 돕는다.

#### Prerequisites

- `hy-home.docker` 인프라 네트워크 (`infra_net`) 지식.
- Docker Secrets 및 기본 HTTPS 통신 이해.
- `opensearch-admin_password` 시크릿 접근 권한.

#### Step-by-step Instructions

##### 1. API Access (REST)

OpenSearch는 `9200` 포트를 통해 검색 API를 제공한다.

```bash
### 클러스터 헬스 체크
read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
curl -X GET "https://opensearch:9200/_cluster/health" -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" --insecure
unset OPENSEARCH_ADMIN_PASSWORD
```

##### 2. Dashboards Usage

데이터 시각화 및 매니지먼트를 위해 Dashboards UI에 접속한다.

- URL: `https://opensearch-dashboard.${DEFAULT_URL}`
- 기본 계정: `admin`

##### 3. Index Management

매핑 설정 및 인덱스 생성을 수행한다.

```bash
read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
curl -X PUT "https://opensearch:9200/my-index" -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" --insecure -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 3,
      "number_of_replicas": 2
    }
  }
}'
unset OPENSEARCH_ADMIN_PASSWORD
```

#### Common Pitfalls

- **Memory Lock Fail**: `bootstrap.memory_lock=true` 설정에도 불구하고 호스트 시스템의 `ulimit` 제한으로 인해 메모리 락이 실패할 수 있다.
- **Certificate Mismatch**: 커스텀 인증서 적용 시 도메인 이름 불일치로 인한 통신 오류가 발생할 수 있다.

#### Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [opensearch.md](../../../07.operations/04-data/analytics/opensearch.md)
- **Procedure**: [opensearch.md](../../../07.operations/04-data/analytics/opensearch.md)

## Procedure

> Migrated from `docs/07.operations/04-data/analytics/opensearch.md` during the 2026-05-10 operations taxonomy consolidation.

### OpenSearch Recovery Procedure

: OpenSearch Cluster & Index Recovery

---

#### Overview (KR)

이 런북은 OpenSearch 클러스터 장애, 샤드 불균형, 검색 지연 및 색인 실패 상황에 대한 대응 절차를 정의한다. 데이터 손실 없이 클러스터 상태(Yellow/Red)를 정상화하기 위한 단계를 제공한다.

#### Purpose

검색 서비스의 다운타임을 줄이고, 분산 환경에서의 데이터 무결성을 유지하며 클러스터를 정상 상태로 복구하는 것을 목적으로 한다.

#### Canonical References

- `[../../02.ard/0012-data-analytics-architecture.md]`
- `[../../07.operations/04-data/analytics/opensearch.md]`
- `[../../07.operations/04-data/analytics/opensearch.md]`

#### When to Use

- 클러스터 상태가 `Red` (데이터 일부 소실 가능성) 또는 `Yellow` (복제본 불완전)일 때.
- 인덱싱 속도가 급격히 느려지거나 대량의 429(Too Many Requests) 에러 발생 시.
- 특정 데이터 노드가 응답하지 않을 때.

#### Procedure or Checklist

##### Checklist

- [ ] 클러스터 헬스 API 호출 (`_cluster/health`)
- [ ] 미할당 샤드(Unassigned Shards) 목록 확인
- [ ] 각 노드의 디스크 잔여 용량 및 메모리(JVM) 상태 확인

##### Procedure

1. **클러스터 상태 진단**:

   ```bash
   read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
   curl -X GET "https://opensearch:9200/_cluster/health?pretty" --insecure -u "admin:${OPENSEARCH_ADMIN_PASSWORD}"
   unset OPENSEARCH_ADMIN_PASSWORD
   ```

2. **미할당 샤드 원인 파악**:

   ```bash
   read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
   curl -X GET "https://opensearch:9200/_cluster/allocation/explain?pretty" --insecure -u "admin:${OPENSEARCH_ADMIN_PASSWORD}"
   unset OPENSEARCH_ADMIN_PASSWORD
   ```

3. **노드 강제 동기화**:
   중단된 노드를 재시작하고 샤드 재배치를 기다린다.

   ```bash
   docker compose restart opensearch
   ```

4. **샤드 수동 재배치 (필요 시)**:
   특정 노드에 샤드가 몰린 경우 수동으로 이동 명령을 수행한다.

#### Verification Steps

- [ ] 클러스터 상태가 `Green`으로 복구되었는지 확인.
- [ ] `_cat/shards` 명령어로 모든 샤드가 `STARTED` 상태인지 확인.

#### Observability and Evidence Sources

- **Signals**: OpenSearch `cluster_status`, `indexing_latency`, `search_latency`.
- **Evidence to Capture**: `_cluster/state` 결과물, 노드 에러 로그.

#### Safe Rollback or Recovery Procedure

- [ ] 데이터 소실 위험 시, 기존 인덱스의 스냅샷(Snapshot) 존재 여부 확인.
- [ ] 대규모 샤드 이동 작업 전 `cluster.routing.allocation.enable`을 `none`으로 설정하여 폭주 방지.

#### Related Operational Documents

- **Operations**: [docs/07.operations/04-data/analytics/opensearch.md](../../../07.operations/04-data/analytics/opensearch.md)

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
