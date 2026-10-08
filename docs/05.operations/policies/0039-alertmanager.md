---
title: "Alertmanager Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "operations"
artifact_id: "POL-0039"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Alertmanager Operations Policy

## Overview

### Overview

이 정책은 Alertmanager notification routing, grouping, inhibition,
receiver, silence, secret boundary를 정의한다. 사용 흐름은 Alertmanager
guide가, 장애 대응 절차는 Alertmanager runbook이 담당한다.

## Scope

### Policy Scope

이 정책은 current `infra/06-observability/alertmanager` compose와
`config/config.yml`에 선언된 Alertmanager 운영 기준을 다룬다.

- **Systems**: compose service `alertmanager`, container `alertmanager`, image [prom/alertmanager image declaration](../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/alertmanager/config/config.yml`, volume `alertmanager-data`
- **Environments**: 로컬·개발·홈랩 운영

### Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0039-alertmanager.md) (`GDE-0039`), [Runbook](../runbooks/0039-alertmanager.md) (`RUN-0039`)

## Rules

### Controls

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

### Lifecycle and data controls

- Alertmanager를 HOME으로 유지하며 gateway 인증, secret-file 렌더링, 최소 수신자 권한과 증거 비식별화를 요구한다.
- Upgrade 전에 템플릿·matching secret과 정지된 `alertmanager-data`의 일관 copy/snapshot을 보존한다. 통지 상태를 live-copy하지 않는다.
- 격리 storage와 시험 수신자로 설정·silence·inhibition/grouping·notification log와 시험 전달을 검증한다.
- 제거에는 Prometheus routing 이전, 수신자 폐기, silence 증거 보존과 데이터 삭제 승인이 필요하다.

### Renderer and delivery limitation

Compose 진입 스크립트는 SMTP/Slack 시크릿을 요구하지만 Slack 수신자만 활성화되어 있다. SMTP 치환자가 이메일 전송을 활성화하지 않는다. Raw `sed` 치환은 임의 시크릿의 구분자·앰퍼샌드·역슬래시·줄바꿈을 안전하게 인코딩하지 못한다. 이는 렌더러 결함이며 원격 셸 실행의 관찰 증거는 아니다. 시크릿이나 렌더링된 YAML을 출력하거나 자격 증명을 약화·변형하지 않는다. 비노출 방식으로 호환성을 확인할 수 없으면 시작·회전을 중단하고 @buenhyden에게 별도 렌더러 수정을 요청한다. Readiness는 통지·grouping/inhibition 성공을 증명하지 않으므로 승인된 시험 수신자와 제한된 알림으로 따로 검증한다.

### Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-low|image: prom/alertmanager:|smtp_username|smtp_password|slack_webhook|alertmanager.middlewares|/-/ready' infra/06-observability/docker-compose.yml`
- Alert routing config:
  `rg -n 'group_by: \\[\"alertname\", \"job\", \"domain\", \"severity\"\\]|repeat_interval: 4h|receiver: \"team-notifications-slack\"|receiver: \"critical-notifications\"|severity=\"critical\"|email_configs:' infra/06-observability/alertmanager/config/config.yml`
- Repository contracts:
  원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- Alertmanager image, route tree, receiver, inhibition rule, secret reference,
  middleware, healthcheck가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Exceptions

### Exceptions

- 보안 사고 또는 대규모 장애 대응 중 임시 route/receiver 조정이 필요하면
  사용자 승인, runbook evidence, rollback evidence를 남긴다.
- Emergency notification noise suppression은 incident commander 또는 owning
  operator가 만료 시각을 지정한 경우에만 허용한다.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0039-alertmanager.md)
- [Recovery runbook](../runbooks/0039-alertmanager.md)
