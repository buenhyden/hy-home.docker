---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/alertmanager.md -->

# Alertmanager Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Alertmanager 사용 맥락과 설정 확인 방법을 설명한다. Alertmanager는 Prometheus가 전달한 alerts를 grouping, deduplication, inhibition, silence, receiver routing으로 처리하고 Slack receiver로 전달한다. Compose는 `infra/06-observability/alertmanager/config/config.yml`을 `/etc/alertmanager/config.yml.template`로 마운트한 뒤 Docker Secret 값을 런타임 `/tmp/config.yml`에 렌더링한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- Alertmanager compose service, route tree, receiver, inhibition, silence, and secret-rendered config boundary를 빠르게 파악한다.
- Prometheus alert delivery, Grafana datasource, protected route, and notification receiver 관계를 확인한다.
- 장애 대응, restart, config rollback, notification failure triage는 runbook으로 넘긴다.

### Prerequisites

- `infra/06-observability/alertmanager/config/config.yml` route/receiver 구조를 읽을 수 있는 권한.
- Docker Secret IDs `smtp_username`, `smtp_password`, `slack_webhook`가 준비되어 있어야 한다. Secret 값은 문서, 로그, task evidence에 기록하지 않는다.
- Prometheus `alertmanagers` target `alertmanager:9093`와 Grafana Alertmanager datasource가 현재 compose network에서 접근 가능해야 한다.
- Alertmanager UI `https://alertmanager.${DEFAULT_URL}` 접근 권한.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-stateful-low|image: prom/alertmanager:v0.33.0|container_name: infra-alertmanager|smtp_username|smtp_password|slack_webhook|alertmanager-data|/-/ready|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

2. Alertmanager config template boundary를 확인한다.

   ```bash
   rg -n 'group_by: \\[\"alertname\", \"job\", \"domain\", \"severity\"\\]|repeat_interval: 4h|receiver: \"team-notifications-slack\"|receiver: \"critical-notifications\"|severity=\"critical\"|__SMTP_USERNAME__|__SMTP_PASSWORD__|__SLACK_WEBHOOK_URL__|email_configs:' infra/06-observability/alertmanager/config/config.yml
   ```

3. 현재 routing model을 이해한다.

   - **Default route**: `group_by`는 `alertname`, `job`, `domain`, `severity` 기준이고 `repeat_interval`은 `4h`이다.
   - **Critical route**: `severity="critical"` alerts는 `critical-notifications` receiver로 전달되고 `repeat_interval`은 `1h`이다.
   - **Slack receivers**: 기본 receiver는 `#notification`, critical receiver는 `#critical-alerts` 채널을 사용한다.
   - **Email receiver**: SMTP placeholders는 유지하지만 `email_configs`가 commented state이면 email delivery를 활성 기능으로 간주하지 않는다.
   - **Inhibition**: critical alert가 같은 warning alert를 억제하고, `InstanceDown`은 같은 instance의 app/datastore/messaging service-level alerts를 억제한다.

4. Prometheus와 Grafana 연결을 확인한다.

   ```bash
   rg -n 'alertmanagers:|targets: \\[\"alertmanager:9093\"\\]|job_name: \"alertmanager\"' infra/06-observability/prometheus/config/prometheus.yml
   rg -n 'name: Alertmanager|uid: alertmanager|url: http://alertmanager:9093|handleGrafanaManagedAlerts: false' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

5. Planned maintenance silence는 Alertmanager UI에서 만료 시각과 사유를 포함해 생성한다.

   - UI: `https://alertmanager.${DEFAULT_URL}`
   - Silence는 expiry 없이 생성하지 않는다.
   - Secret, webhook, SMTP credential 값은 silence comment나 evidence에 남기지 않는다.

### Common Pitfalls

- **Secret rendering assumption**: Git-managed `config.yml`에는 placeholders가 있고, runtime `/tmp/config.yml`에는 Secret 값이 렌더링된다. `/tmp/config.yml` 원문을 evidence로 남기지 않는다.
- **Email assumption**: SMTP placeholders가 있어도 `email_configs`가 commented state이면 email notification을 보장한다고 쓰지 않는다.
- **Silence drift**: 만료 없는 silence나 너무 넓은 matcher는 critical alert를 숨길 수 있다.
- **Route drift**: `group_by`, `repeat_interval`, receiver name을 바꾸면 policy와 runbook evidence도 함께 갱신해야 한다.
- **Direct access assumption**: 외부 UI 접근은 Traefik protected route와 SSO middleware를 통한다. 내부 compose network에서는 `alertmanager:9093`를 사용한다.

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps alertmanager`
- `docker logs --tail=100 infra-alertmanager`
- `rg -n 'route:|receivers:|inhibit_rules:|__SLACK_WEBHOOK_URL__|email_configs:' infra/06-observability/alertmanager/config/config.yml`
- `rg -n 'alertmanagers:|targets: \\[\"alertmanager:9093\"\\]' infra/06-observability/prometheus/config/prometheus.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/alertmanager.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/alertmanager.md)
- [Recovery runbook](../../runbooks/06-observability/alertmanager.md)
