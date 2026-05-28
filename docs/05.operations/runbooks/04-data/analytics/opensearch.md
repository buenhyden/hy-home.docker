---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/analytics/opensearch.md -->

# OpenSearch Runbook

## Overview (KR)

이 런북은 OpenSearch 클러스터 장애, 샤드 불균형, 검색 지연 및 색인 실패 상황에 대한 대응 절차를 정의한다. 데이터 손실 없이 클러스터 상태(Yellow/Red)를 정상화하기 위한 단계를 제공한다.

## OpenSearch Recovery Procedure

> Scope: OpenSearch Cluster & Index Recovery

---

### Purpose

검색 서비스의 다운타임을 줄이고, 분산 환경에서의 데이터 무결성을 유지하며 클러스터를 정상 상태로 복구하는 것을 목적으로 한다.

### Canonical References

- [../../../../02.architecture/requirements/0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- [../../../guides/04-data/analytics/opensearch.md](../../../guides/04-data/analytics/opensearch.md)
- [../../../policies/04-data/analytics/opensearch.md](../../../policies/04-data/analytics/opensearch.md)

## When to Use

- 클러스터 상태가 `Red` (데이터 일부 소실 가능성) 또는 `Yellow` (복제본 불완전)일 때.
- 인덱싱 속도가 급격히 느려지거나 대량의 429(Too Many Requests) 에러 발생 시.
- 특정 데이터 노드가 응답하지 않을 때.

## Procedure

### Checklist

- [ ] 클러스터 헬스 API 호출 (`_cluster/health`)
- [ ] 미할당 샤드(Unassigned Shards) 목록 확인
- [ ] 각 노드의 디스크 잔여 용량 및 메모리(JVM) 상태 확인

### Steps

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

### Verification Steps

- [ ] 클러스터 상태가 `Green`으로 복구되었는지 확인.
- [ ] `_cat/shards` 명령어로 모든 샤드가 `STARTED` 상태인지 확인.

### Observability and Evidence Sources

- **Signals**: OpenSearch `cluster_status`, `indexing_latency`, `search_latency`.
- **Evidence to Capture**: `_cluster/state` 결과물, 노드 에러 로그.

### Safe Rollback or Recovery Procedure

- [ ] 데이터 소실 위험 시, 기존 인덱스의 스냅샷(Snapshot) 존재 여부 확인.
- [ ] 대규모 샤드 이동 작업 전 `cluster.routing.allocation.enable`을 `none`으로 설정하여 폭주 방지.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/opensearch.md)
- [Operations policy](../../../policies/04-data/analytics/opensearch.md)
- [Operations template](../../../../99.templates/operation.template.md)
