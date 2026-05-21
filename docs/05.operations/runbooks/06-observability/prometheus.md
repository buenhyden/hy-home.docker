---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/prometheus.md -->

# Prometheus Runbook

## Recovery Runbook: Prometheus

Recovery procedures for common Prometheus service disruptions and metrics collection failures.

### Incident Scenarios

#### 1. Prometheus Container Crash (OOM/Corruption)

**Symptoms**: Prometheus UI unreachable, Grafana metrics `NaN` or missing, alerts stop firing.
**Recovery**:

1. Check container logs:

   ```bash
   docker logs infra-prometheus
   ```

2. If OOM, increase memory limits in `infra/06-observability/docker-compose.yml`.
3. If corruption, check TSDB integrity and consider restarting without the corrupted WAL.
4. Final restart:

   ```bash
   docker compose restart prometheus
   ```

#### 2. Scrape Target Unavailable

**Symptoms**: Alert `PrometheusAllTargetsMissing` or specific service metrics missing.
**Recovery**:

1. Identify failing job in Prometheus UI (`/targets`).
2. Verify target reachability:

   ```bash
   docker exec -it infra-prometheus ping <target-service-name>
   ```

3. Ensure target service is healthy and exposing `/metrics`.
4. Validate `prometheus.yml` configuration (ports, job name).

#### 3. Alerting Rule Evaluation Failure

**Symptoms**: Alert `PrometheusRuleEvaluationFailures` is firing.
**Recovery**:

1. Check Prometheus logs for syntax or performance errors in rules.
2. Validate rule files using `promtool`:

   ```bash
   docker exec infra-prometheus promtool check rules /etc/prometheus/alert_rules/*.yml
   ```

3. Fix any syntax errors or simplify expensive PromQL expressions.

### Recovery Verification

1. Access the Prometheus UI: [http://prometheus.hy-home.local/-/healthy](http://prometheus.hy-home.local/-/healthy) (or internal port `9090`).
2. Verify all "critical" scrape targets are "UP" in the `/targets` page.
3. Confirm that Grafana dashboards are receiving new metrics data.

---
**AI Agent Note**: AI agents should use the `promtool` command to verify any proposed changes to Prometheus or Alerting configurations before applying them.

### Overview (KR)

이 런북은 `docs/05.operations/runbooks/06-observability/prometheus.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [Observability operations index](../../README.md)
- [Prometheus usage guide](../../guides/06-observability/prometheus.md)
- [Prometheus operations policy](../../policies/06-observability/prometheus.md)
- [Prometheus infra README](../../../../infra/06-observability/prometheus/README.md)

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

### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

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

- Capture command output, timestamps, and operator/agent actions for any execution of this runbook.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/prometheus.md)
- [Operations policy](../../policies/06-observability/prometheus.md)
- [Operations template](../../../99.templates/operation.template.md)
