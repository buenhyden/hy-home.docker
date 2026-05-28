---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/nosql/mongodb.md -->

# MongoDB Runbook

## Overview (KR)

이 문서는 MongoDB 레플리카 셋의 Primary 부재, 과도한 데이터 지연(Lag), 또는 Arbiter 장애 발생 시의 신속한 복구 절차를 설명한다.

## MongoDB Recovery Procedure

> Emergency recovery procedures for MongoDB Replica Set and failover incidents.

---

### Procedure Type

`disaster-recovery`

### Target Audience

- On-call Engineer
- SRE
- DBA

### Purpose

레플리카 셋의 Primary를 재선출하고, Secondary 노드를 최신 상태로 재동기화하며, 클러스터의 정족수를 보호하여 쓰기 가용성을 확보한다.

### Pre-remediation Checklist

- [ ] `rs.status()` 명령으로 멤버 상태 확인 (`PRIMARY` 유무 확인)
- [ ] `docker logs`를 통해 Election 로그 분석
- [ ] 네트워크 분리(Split-brain) 가능성 검토
- [ ] Oplog window 내 최신 데이터 존재 여부 확인

### Remediation Steps

#### Scenario 1: No Primary Elected

정족수 부족으로 Primary가 선출되지 않는 경우.

1. 죽은 노드(Secondary 또는 Arbiter) 우선 복구:

   ```bash
   docker-compose restart mongodb-rep2
   ```

2. 최소 2개 노드가 살아나면 자동으로 Election이 시작됨.
3. 강제 선출 (긴급 상황):
   Primary로 만들고자 하는 노드에서 `rs.stepDown()` 또는 Priority 조정을 통해 선출 유도.

#### Scenario 2: Stale Secondary (Re-sync required)

Secondary 노드 데이터가 너무 오래되어 Oplog로 추적이 불가능한 경우.

1. Secondary 노드 중지 및 데이터 초기화:

   ```bash
   docker-compose stop mongodb-rep2
   rm -rf ${DEFAULT_DATA_DIR}/mongodb/data2/*
   ```

2. 컨테이너 시작:

   ```bash
   docker-compose start mongodb-rep2
   ```

3. Initial Sync 시작 확인:

   ```bash
   rs.status() # stateStr: 'STARTUP2' 확인
   ```

### Verification Steps

1. 클러스터 멤버십 확인:

   ```bash
   rs.conf()
   ```

2. 쓰기 테스트:

   ```bash
   db.test.insertOne({status: "recovered", date: new Date()})
   ```

### Post-remediation Tasks

- Oplog 사이즈 증설 필요성 검토
- Arbiter 배치 위치 물리적 격리 확인
- 펜싱(Fencing) 로직 및 타이머 값(ElectionTimeout) 조정 검토

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
- [Usage guide](../../../guides/04-data/nosql/mongodb.md)
- [Operations policy](../../../policies/04-data/nosql/mongodb.md)
- [Operations template](../../../../99.templates/operation.template.md)
