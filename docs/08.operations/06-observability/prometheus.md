# [OPERATIONAL-POLICY] 06-observability: prometheus

Standardized procedures for maintaining Prometheus metrics collection and alerting integrity.

## Procedures

### 1. Scrape Target Registration

To add a new service for monitoring:

1. Ensure the target service exposes metrics (usually on port `9090` or `8080`).
2. Update `infra/06-observability/prometheus/config/prometheus.yml`:

   ```yaml
   - job_name: 'new-service'
     static_configs:
       - targets: ['new-service:port']
   ```

3. Validate configuration:

   ```bash
   docker exec infra-prometheus promtool check config /etc/prometheus/prometheus.yml
   ```

4. Reload Prometheus (send `SIGHUP` or use API `-X POST /-/reload`).

### 2. Alerting Rule Management

- **Definition**: Rules must be added to the appropriate file in `config/alert_rules/`.
- **Naming**: Use camelCase for alert names (e.g., `PostgresInstanceDown`).
- **Standard Labels**:
  - `severity`: `critical` (immediate action), `warning` (investigation), `info` (notification only).
- **Testing**:

  ```bash
  promtool test rules config/alert_rules/tests/*.yml
  ```

### 3. Performance Monitoring

- **Cardinality Audit**: Periodically review high-cardinality metrics (e.g., `container_...` from cAdvisor).
- **Rule Evaluation**: Monitor `prometheus_rule_evaluation_duration_seconds` to ensure evaluations complete within the `15s` window.
- **TSDB Integrity**: Check for compaction failures in Prometheus logs.

## Constraints

- **Scrape Intervals**: Never set below `10s` without architectural approval.
- **Retention**: Default is `15d`; any changes require volume resizing.
- **Rule Format**: Use `expr`, `for`, `labels`, and `annotations` (Summary/Description).

---
**AI Agent Note**: AI agents must verify that every new infrastructure component includes a corresponding scrape configuration and basic "up" alert.

## Related Documents

- **Runbook**: [prometheus.md](../../09.runbooks/06-observability/prometheus.md)
- **Plan**: [2026-03-26-06-observability-standardization.md](../../05.plans/2026-03-26-06-observability-standardization.md)

---

## Overview (KR)

이 문서는 `docs/08.operations/06-observability/prometheus.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
