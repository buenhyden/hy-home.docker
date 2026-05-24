---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/prometheus-recovery.md -->

# Prometheus Recovery Operations

## Procedure

### Prometheus TSDB Hub Recovery

**Symptoms**: Prometheus fails to start, logs show "TSDB block truncation error" or "corruption in segment".

#### 1. Diagnosis

Check the logs of the Prometheus container:

```bash
docker logs <prometheus_container_id>
```

#### 2. Immediate Action (Safe)

If the error is related to memory or locks:

1. Restart the container: `docker restart prometheus`.
2. Ensure the volume mount has correct permissions (`nobody:nogroup`).

#### 3. Advanced Recovery (Data Loss Risk)

If the TSDB index is corrupted:

Safety prerequisites:

- Confirm incident owner approval before running data-loss-risk recovery steps.
- Capture current container and volume state before modifying TSDB files.
- Verify backup evidence and available destination capacity before removing WAL data.

1. **Stop** Prometheus: `docker compose stop prometheus`.
2. **Snapshot** the data directory: `tar -czvf /tmp/prometheus_data_backup.tar.gz /var/lib/docker/volumes/prometheus_data`.
3. **Delete** the WAL (Write Ahead Log): `rm -rf /var/lib/docker/volumes/prometheus_data/_data/wal`.
4. **Restart** Prometheus.

#### 4. Verification

Check if the metrics are visible in Grafana. If not, verify that Alloy is successfully pushing metrics.

---
[Return to Observability Index](../../guides/06-observability/README.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/runbooks/06-observability/prometheus-recovery.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)

## Evidence

- Capture command output, timestamps, and operator/agent actions for any execution of this runbook.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Operations template](../../../99.templates/operation.template.md)
