---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/alertmanager.md -->

# Alertmanager Notification Recovery Runbook

## Alertmanager Notification Recovery Procedure

> Scope: Alertmanager readiness checks, Prometheus delivery evidence, secret-rendered config verification, notification path triage, restart, and config rollback.

### Overview

이 런북은 Alertmanager UI/readiness failure, Prometheus alert delivery gap, Slack notification failure, silence/inhibition drift, and config rendering regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-alertmanager` 상태를 확인하고 Prometheus `alertmanager:9093` delivery, route/receiver config, Docker Secret-rendered runtime boundary, protected UI route를 검증하며, Secret 노출이나 receiver 정책 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

### Canonical References

- **Policy**: [Alertmanager operations policy](../../policies/06-observability/alertmanager.md)
- **Guide**: [Alertmanager usage guide](../../guides/06-observability/alertmanager.md)
- **Infrastructure**: [Alertmanager infra README](../../../../infra/06-observability/alertmanager/README.md)

## When to Use

- Prometheus에서 firing alert가 있는데 Alertmanager UI나 Slack receiver에서 보이지 않을 때.
- Alertmanager UI `https://alertmanager.${DEFAULT_URL}` 또는 `/-/ready` endpoint가 실패할 때.
- `smtp_username`, `smtp_password`, `slack_webhook` Secret 누락 또는 config rendering error가 의심될 때.
- 잘못된 silence 또는 inhibition rule로 중요 알림이 차단된 것처럼 보일 때.
- `config.yml` 변경 후 route, receiver, template, notification delivery 상태 검증이 필요할 때.

## Procedure

### Checklist

- [ ] `alertmanager` service, `infra-alertmanager` container, `alertmanager-data` volume, and Docker Secret IDs 상태를 확인한다.
- [ ] 문제 유형을 readiness, Prometheus delivery, receiver delivery, silence/inhibition, secret rendering, config regression 중 하나로 분류한다.
- [ ] Secret value, rendered `/tmp/config.yml`, Slack webhook URL, SMTP credential 원문은 기록하지 않는다.
- [ ] Route/receiver/inhibition/secret rendering을 변경해야 해 보이면 중단하고 owning operator approval을 받는다.

### Steps

1. 현재 service 상태, 최근 로그, readiness를 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps alertmanager
   docker logs --tail=200 infra-alertmanager
   docker exec infra-alertmanager wget -q --spider http://localhost:9093/-/ready
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-low|image: prom/alertmanager:v0.33.0|container_name: infra-alertmanager|alertmanager-data|smtp_username|smtp_password|slack_webhook|ALERTMANAGER_PORT|/-/ready|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

3. Secret 값이 아닌 placeholder와 route/receiver config만 확인한다.

   ```bash
   rg -n 'route:|group_by: \\[\"alertname\", \"job\", \"domain\", \"severity\"\\]|repeat_interval: 4h|receiver: \"team-notifications-slack\"|receiver: \"critical-notifications\"|severity=\"critical\"|inhibit_rules:|__SMTP_USERNAME__|__SMTP_PASSWORD__|__SLACK_WEBHOOK_URL__|email_configs:' infra/06-observability/alertmanager/config/config.yml
   ```

4. Prometheus가 Alertmanager target을 사용하고 있는지 확인한다.

   ```bash
   rg -n 'alertmanagers:|targets: \\[\"alertmanager:9093\"\\]|job_name: \"alertmanager\"' infra/06-observability/prometheus/config/prometheus.yml
   ```

5. Grafana datasource가 같은 Alertmanager endpoint를 가리키는지 확인한다.

   ```bash
   rg -n 'name: Alertmanager|uid: alertmanager|url: http://alertmanager:9093|handleGrafanaManagedAlerts: false' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

6. Silence or inhibition drift가 의심되면 UI에서 matcher, creator, comment, expiry를 확인한다.

   - UI: `https://alertmanager.${DEFAULT_URL}`
   - Expiry 없는 silence가 있으면 삭제 또는 만료 시각 부여를 owning operator에게 요청한다.
   - Critical alert를 숨기는 broad matcher가 있으면 evidence만 기록하고 정책 변경은 승인 후 수행한다.

7. Config와 Secret ID 경계가 정책과 일치하지만 runtime state가 회복되지 않으면 Alertmanager를 재시작한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart alertmanager
   docker logs --tail=100 infra-alertmanager
   ```

8. `config.yml` 변경 후 장애가 발생했다면 Git-managed config diff를 되돌리고 readiness를 재확인한다.

   ```bash
   git diff -- infra/06-observability/alertmanager/config/config.yml
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart alertmanager
   docker exec infra-alertmanager wget -q --spider http://localhost:9093/-/ready
   ```

   이 런북은 Slack webhook rotation, SMTP credential rotation, receiver/channel change, inhibition policy change, protected middleware change를 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

### Verification Steps

- [ ] `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps alertmanager`에서 `alertmanager` service가 running이다.
- [ ] `/-/ready` endpoint가 성공한다.
- [ ] Prometheus config의 `alertmanagers` target이 `alertmanager:9093`를 유지한다.
- [ ] Alertmanager UI에서 firing alerts, silences, receivers를 확인할 수 있다.
- [ ] Slack notification failure가 있었으면 test alert 또는 다음 firing alert에서 expected receiver 도착 여부를 확인하고 timestamp를 기록한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-alertmanager`
- **Health**: Alertmanager `/-/ready`, UI `https://alertmanager.${DEFAULT_URL}`
- **Config**: `infra/06-observability/alertmanager/config/config.yml`, Prometheus `alertmanagers` target, Grafana datasource
- **Metrics**: `alertmanager_notifications_failed_total`, `prometheus_notifications_alertmanagers_discovered`
- **Evidence to Capture**: failing receiver, route matcher, relevant log excerpt with secrets redacted, restart timestamp, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed `config.yml`, Compose, or datasource/Prometheus endpoint change가 원인이면 직전 Git diff 단위로 되돌리고 Alertmanager를 재시작한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Secret rotation, Slack webhook replacement, SMTP credential replacement, receiver/channel change, or protected route middleware change는 이 런북의 안전 롤백 범위를 벗어난다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, rendered `/tmp/config.yml`, Slack webhook URL, SMTP credential 원문은 기록하지 않는다.
- Notification 장애는 affected receiver, matching route, alert labels, log excerpt, silence/inhibition state를 함께 기록한다.
- Receiver/channel/secret/middleware 변경 필요성이 보이면 approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config rollback만 사용한다. Secret rotation, receiver/channel policy, inhibition policy, protected middleware, or external Slack/SMTP resource 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, receiver/channel/secret/middleware 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/alertmanager.md)
- [Operations policy](../../policies/06-observability/alertmanager.md)
