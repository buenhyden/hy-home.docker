---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/nosql/couchdb.md -->

# CouchDB Runbook

## Overview (KR)

이 문서는 CouchDB 클러스터 정족수 상실, 노드 간 복제 중단, 또는 데이터 정합성 이슈 발생 시의 복구 절차를 정의한다.

## CouchDB Recovery Procedure

> Emergency recovery procedures for CouchDB Cluster and node synchronization issues.

---

### Procedure Type

`incident-response`

### Target Audience

- On-call Engineer
- SRE
- AI-Agent

### Purpose

CouchDB 클러스터의 고가용성 상태를 복구하고, 노드 간 데이터 불일치를 해결하여 안정적인 문서 동기화 환경을 재구축한다.

### Pre-remediation Checklist

- [ ] `https://couchdb.${DEFAULT_URL}/_membership` 결과 분석
- [ ] 노드 간 HTTP 통신(Port 5984) 및 Cluster 통신(Port 4369, 5986) 확인
- [ ] `couchdb_secret`이 모든 노드에서 동일한지 확인

### Remediation Steps

#### Scenario 1: Node Out-of-Sync (Re-joining Cluster)

클러스터에서 이탈한 노드를 다시 조인시킨다.

1. 로그 확인: `docker logs couchdb-node1`
2. 노드 재시작:

   ```bash
   docker-compose restart couchdb-node1
   ```

3. 클러스터 수동 조인 (필요 시):
   (Setup API를 통해 이탈한 노드의 IP/Port를 다시 추가)

#### Scenario 2: High Fragmentation (Manual Compaction)

디스크 부족으로 인한 쓰기 거부 시 압축을 수행한다.

1. 모든 데이터베이스 목록 확인:

   ```bash
   curl -u ${USER}:${PASS} https://couchdb.${DEFAULT_URL}/_all_dbs
   ```

2. 특정 DB 압축 실행:

   ```bash
   curl -H "Content-Type: application/json" -X POST -u ${USER}:${PASS} \
        https://couchdb.${DEFAULT_URL}/<db_name>/_compact
   ```

### Verification Steps

1. 클러스터 동기화 지연 확인:

   ```bash
   curl -u ${USER}:${PASS} https://couchdb.${DEFAULT_URL}/_scheduler/docs
   ```

2. 특정 문서 리비전 일치 여부 확인 (각 노드별 직접 쿼리).

### Post-remediation Tasks

- `revs_limit` 정책 적정성 검토
- 디스크 자동 확장 트리거 점검
- 공유 시크릿(Secret) 관리 상태 재확인

### Canonical References

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Steps

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

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
- [Usage guide](../../../guides/04-data/nosql/couchdb.md)
- [Operations policy](../../../policies/04-data/nosql/couchdb.md)
