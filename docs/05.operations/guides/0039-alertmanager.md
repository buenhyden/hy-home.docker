---
title: "Alertmanager Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0039"
parent_ids:
- "POL-0039"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - alertmanager
created: "2026-05-10"
---

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
   rg -n 'service: template-stateful-low|image: prom/alertmanager:|container_name: infra-alertmanager|smtp_username|smtp_password|slack_webhook|alertmanager-data|/-/ready|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
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

### Source-backed operating contract

- **목적·분류·구현 소유권**: `alertmanager`는 `HOME` 알림 라우팅 서비스이며 `obs`/`alerting`으로 선택한다. [observability Compose](../../../infra/06-observability/docker-compose.yml), mount된 config template과 entrypoint가 구현을 소유한다.
- **흐름·의존성·보안**: Prometheus는 `obs_net`으로 alert를 보낸다. Alertmanager는 이를 grouping·inhibition하고, 승인되어 활성화된 Slack receiver로 라우팅한다(email_configs는 주석 처리되어 있다). Traefik이 UI를 보호한다. entrypoint는 `smtp_username`, `smtp_password`, `slack_webhook` Docker Secret의 credential을 임시 runtime config로 렌더링한다. 이 파일을 일반 evidence로 렌더링하거나 보관하지 않는다.
- **상태·자원**: `alertmanager-data:/alertmanager`는 silence와 notification log를 보존한다. 이 data를 잃어도 Prometheus alert가 삭제되지는 않지만 알림이 반복되거나 silence가 사라질 수 있다. Compose limit은 source 설정이며 측정된 여유 용량이 아니다.
- **정상 사용·수명 주기**: 저장소 root에서 `docker compose --profile obs config --quiet`를 실행하고, 렌더링된 secret을 출력하지 않은 채 source config를 검증한다. receiver test 이후에만 시작하거나 reload한다. 정지 상태의 data volume과 source template, secret 참조를 함께 backup한다. 고정된 image를 한 번에 하나씩 upgrade하고 grouping, inhibition, silence 보존과 통제된 알림 전송을 검증한다.
- **공식 문서·license**: 공식 [Alertmanager 설정 문서](https://prometheus.io/docs/alerting/latest/configuration/)를 따른다. Alertmanager에는 Apache-2.0 license가 적용된다.

### Renderer and delivery limitation

Compose 진입 스크립트는 SMTP/Slack 시크릿을 요구하지만 Slack 수신자만 활성화되어 있다. SMTP 치환자가 이메일 전송을 활성화하지 않는다. Raw `sed` 치환은 임의 시크릿의 구분자·앰퍼샌드·역슬래시·줄바꿈을 안전하게 인코딩하지 못한다. 이는 렌더러 결함이며 원격 셸 실행의 관찰 증거는 아니다. 시크릿이나 렌더링된 YAML을 출력하거나 자격 증명을 약화·변형하지 않는다. 비노출 방식으로 호환성을 확인할 수 없으면 시작·회전을 중단하고 @buenhyden에게 별도 렌더러 수정을 요청한다. Readiness는 통지·grouping/inhibition 성공을 증명하지 않으므로 승인된 시험 수신자와 제한된 알림으로 따로 검증한다.

## Common Checks

- `docker compose --profile obs ps alertmanager`
- `docker logs --tail=100 infra-alertmanager`
- `rg -n 'route:|receivers:|inhibit_rules:|__SLACK_WEBHOOK_URL__|email_configs:' infra/06-observability/alertmanager/config/config.yml`
- `rg -n 'alertmanagers:|targets: \\[\"alertmanager:9093\"\\]' infra/06-observability/prometheus/config/prometheus.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0039-alertmanager.md)을 따른다.

## Traceability

- Declared parent: [Alertmanager Operations Policy](../policies/0039-alertmanager.md) (`POL-0039`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0039-alertmanager.md) (`POL-0039`), [Runbook](../runbooks/0039-alertmanager.md) (`RUN-0039`)

## Related Documents

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0039-alertmanager.md)
- [Recovery runbook](../runbooks/0039-alertmanager.md)
