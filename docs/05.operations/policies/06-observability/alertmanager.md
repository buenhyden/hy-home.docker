---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/alertmanager.md -->

# Alertmanager Operations Policy

## Overview

이 정책은 Alertmanager notification routing, grouping, inhibition,
receiver, silence, secret boundary를 정의한다. 사용 흐름은 Alertmanager
guide가, 장애 대응 절차는 Alertmanager runbook이 담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/alertmanager` compose와
`config/config.yml`에 선언된 Alertmanager 운영 기준을 다룬다.

- **Systems**: compose service `alertmanager`, container `infra-alertmanager`, image `prom/alertmanager:v0.33.0`, config `infra/06-observability/alertmanager/config/config.yml`, volume `alertmanager-data`
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Alert grouping은 `alertname`, `job`, `domain`, `severity` label을
    기준으로 한다.
  - Default routing은 `group_wait: 30s`, `group_interval: 5m`,
    `repeat_interval: 4h`, receiver `team-notifications-slack`를 유지한다.
  - `severity="critical"` route는 receiver `critical-notifications`와
    `repeat_interval: 1h`를 유지한다.
  - Active receivers는 Slack channel `#notification`과 `#critical-alerts`를
    기준으로 한다.
  - SMTP placeholder와 `smtp_username`, `smtp_password` secret은 유지하되,
    `email_configs`가 commented state이면 email delivery를 active control로
    선언하지 않는다.
  - `smtp_username`, `smtp_password`, `slack_webhook` 값은 Docker Secret으로만
    주입하고, entrypoint에서 rendered `/tmp/config.yml`로 변환한다.
  - Inhibition은 critical이 같은 alert의 warning을 억제하고,
    `InstanceDown`이 app/datastore/messaging service-level alerts를 억제하는
    현재 규칙을 따른다.
  - Alertmanager route는
    `gateway-standard-chain@file,sso-errors@file,sso-auth@file` middleware
    chain을 유지한다.
  - Planned maintenance silence는 종료 시각과 사유를 포함해야 한다.
- **Allowed**:
  - Receiver, grouping, inhibition, silence policy 변경은 plan/task evidence와
    config diff를 함께 남긴다.
  - Email delivery를 활성화하려면 `email_configs`를 실제 receiver로
    전환하고 SMTP secret/rendering 검증을 같은 변경 단위에 포함한다.
- **Disallowed**:
  - Slack webhook, SMTP username/password, rendered config secret 값을 문서,
    로그, task evidence에 기록하는 행위
  - `email_configs`가 inactive인데 critical 알림의 email delivery가 보장된다고
    선언하는 행위
  - 승인 없이 route, receiver, inhibition, secret rendering, protected
    middleware, image version을 runtime에서 변경하는 행위
  - expiry 없는 무기한 silence를 생성하는 행위

## Exceptions

- 보안 사고 또는 대규모 장애 대응 중 임시 route/receiver 조정이 필요하면
  사용자 승인, runbook evidence, rollback evidence를 남긴다.
- Emergency notification noise suppression은 incident commander 또는 owning
  operator가 만료 시각을 지정한 경우에만 허용한다.

## Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-low|image: prom/alertmanager:v0.33.0|smtp_username|smtp_password|slack_webhook|alertmanager.middlewares|/-/ready' infra/06-observability/docker-compose.yml`
- Alert routing config:
  `rg -n 'group_by: \\[\"alertname\", \"job\", \"domain\", \"severity\"\\]|repeat_interval: 4h|receiver: \"team-notifications-slack\"|receiver: \"critical-notifications\"|severity=\"critical\"|email_configs:' infra/06-observability/alertmanager/config/config.yml`
- Repository contracts:
  `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Alertmanager image, route tree, receiver, inhibition rule, secret reference,
  middleware, healthcheck가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/alertmanager.md)
- [Recovery runbook](../../runbooks/06-observability/alertmanager.md)
