---
status: active
---

# Cassandra Runbook

## Cassandra Recovery Procedure

> Emergency recovery procedures for Apache Cassandra single-node instance.

---

### Overview (KR)

이 문서는 Cassandra 서비스 중단, 데이터 오염 또는 노드 장애 시 신속하게 서비스를 정상화하기 위한 긴급 대응 절차를 설명한다.

### Procedure Type

`disaster-recovery`

### Target Audience

- On-call Engineer
- SRE
- AI-Operator

### Purpose

Cassandra 서비스 장애 발생 시 다운타임을 최소화하고, 데이터 손실 없이 최단 시간 내에 서비스를 복구하는 것을 목표로 한다.

### Pre-remediation Checklist

- [ ] `docker ps`를 통해 컨테이너 상태 확인
- [ ] `docker logs cassandra-node1`에서 "Error" 키워드 검색
- [ ] `${DEFAULT_DATA_DIR}/cassandra` 볼륨 접근 가능 여부 확인
- [ ] 사용 가능한 최근 백업본(Snapshot) 존재 여부 확인

### Remediation Steps

#### Scenario 1: Service Down (Container Crash)

컨테이너가 비정상 종료된 경우 재시작을 시도한다.

1. 컨테이너 재시작:

   ```bash
   cd infra/04-data/nosql/cassandra
   docker-compose up -d
   ```

2. 시작 로그 확인 (Status 'Ready' 확인):

   ```bash
   docker logs -f cassandra-node1
   ```

#### Scenario 2: Data Corruption (Restore from Snapshot)

데이터 오염 시 스냅샷을 기반으로 복원한다.

1. 서비스 중지:

   ```bash
   docker-compose stop cassandra-node1
   ```

2. 기존 데이터 백업 (안전을 위해):

   ```bash
   mv ${DEFAULT_DATA_DIR}/cassandra/data ${DEFAULT_DATA_DIR}/cassandra/data_broken
   ```

3. 스냅샷 복사:
   (백업 스토리지에서 최근 스냅샷을 `${DEFAULT_DATA_DIR}/cassandra/data` 위치로 복구)
4. 권한 확인 및 시작:

   ```bash
   chown -R 999:999 ${DEFAULT_DATA_DIR}/cassandra/data
   docker-compose start cassandra-node1
   ```

### Verification Steps

1. 노드 상태 확인:

   ```bash
   docker exec -it cassandra-node1 nodetool status
   ```

   (상태가 `UN`이어야 함)
2. 데이터 샘플 쿼리:

   ```bash
   docker exec -it cassandra-node1 cqlsh -u ${CASSANDRA_USER} -p ${CASSANDRA_PASSWORD} -e "SELECT * FROM system.local;"
   ```

### Post-remediation Tasks

- 장애 원인 분석 (Post-mortem) 작성 및 공유
- 모니터링 임계값 조정 필요성 검토
- 백업 무결성 추가 점검

### Canonical References

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

### Procedure or Checklist

#### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

#### Procedure

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

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/nosql/cassandra.md)
- [Operations policy](../../../policies/04-data/nosql/cassandra.md)
- [Operations template](../../../../99.templates/operation.template.md)
