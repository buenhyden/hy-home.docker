---
title: "Alertmanager Notification Recovery Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0039"
parent_ids:
- "GDE-0039"
created: "2026-05-17"
---

# Alertmanager Notification Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

> Scope: Alertmanager 준비 상태, Prometheus 전달 증거, secret으로 렌더링한 설정, 알림 경로 진단, 재시작과 설정 rollback.

이 런북은 Alertmanager UI/readiness failure, Prometheus alert delivery gap, Slack notification failure, silence/inhibition drift, and config rendering regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `alertmanager` 상태를 확인하고 Prometheus `alertmanager:9093` delivery, route/receiver config, Docker Secret-rendered runtime boundary, protected UI route를 검증하며, Secret 노출이나 receiver 정책 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

### When to Use

- Prometheus에서 firing alert가 있는데 Alertmanager UI나 Slack receiver에서 보이지 않을 때.
- Alertmanager UI `https://alertmanager.${DEFAULT_URL}` 또는 `/-/ready` endpoint가 실패할 때.
- `smtp_username`, `smtp_password`, `slack_webhook` Secret 누락 또는 config rendering error가 의심될 때.
- 잘못된 silence 또는 inhibition rule로 중요 알림이 차단된 것처럼 보일 때.
- `config.yml` 변경 후 route, receiver, template, notification delivery 상태 검증이 필요할 때.

## Procedure

### Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`alertmanager`를 처음 기동하면 건강한 `prometheus`·`grafana` 의존성을 요구한다. 알림 대상은 현재 Slack이며 SMTP secret도 renderer 입력으로 필요하다. 상태 점검 뒤 별도 승인한 합성 알림의 실제 도착을 확인한다. 정지 전 silence·notification 상태를 보존하고 운영 알림의 중단 영향을 승인받는다.

### Checklist

- [ ] `alertmanager` service, `alertmanager` container, `alertmanager-data` volume, and Docker Secret IDs 상태를 확인한다.
- [ ] 문제 유형을 readiness, Prometheus delivery, receiver delivery, silence/inhibition, secret rendering, config regression 중 하나로 분류한다.
- [ ] Secret value, rendered `/tmp/config.yml`, Slack webhook URL, SMTP credential 원문은 기록하지 않는다.
- [ ] Route/receiver/inhibition/secret rendering을 변경해야 해 보이면 중단하고 repository owner @buenhyden approval을 받는다.

### Renderer and delivery limitation

Compose 진입 스크립트는 SMTP/Slack 시크릿을 요구하지만 Slack 수신자만 활성화되어 있다. SMTP 치환자가 이메일 전송을 활성화하지 않는다. Raw `sed` 치환은 임의 시크릿의 구분자·앰퍼샌드·역슬래시·줄바꿈을 안전하게 인코딩하지 못한다. 이는 렌더러 결함이며 원격 셸 실행의 관찰 증거는 아니다. 시크릿이나 렌더링된 YAML을 출력하거나 자격 증명을 약화·변형하지 않는다. 비노출 방식으로 호환성을 확인할 수 없으면 시작·회전을 중단하고 @buenhyden에게 별도 렌더러 수정을 요청한다. Readiness는 통지·grouping/inhibition 성공을 증명하지 않으므로 승인된 시험 수신자와 제한된 알림으로 따로 검증한다.

### Steps

1. 현재 service 상태, 최근 로그, readiness를 캡처한다.

   ```bash
   docker compose --profile obs ps alertmanager
   docker logs --tail=200 alertmanager
   docker exec alertmanager wget -q --spider http://localhost:9093/-/ready
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-low|image: prom/alertmanager:|container_name: alertmanager|alertmanager-data|smtp_username|smtp_password|slack_webhook|ALERTMANAGER_PORT|/-/ready|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
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
   - Expiry 없는 silence가 있으면 삭제 또는 만료 시각 부여를 repository owner @buenhyden에게 요청한다.
   - Critical alert를 숨기는 broad matcher가 있으면 evidence만 기록하고 정책 변경은 승인 후 수행한다.

7. Config와 Secret ID 경계가 정책과 일치하지만 runtime state가 회복되지 않으면 Alertmanager를 재시작한다.

   ```bash
   docker compose --profile obs restart alertmanager
   docker logs --tail=100 alertmanager
   ```

8. `config.yml`의 bind-mounted 내용만 바뀌었으면 아래 `git diff`로 후보를 확인하고 승인된 정상 revision의 해당 파일만 복원한다. `git diff`는 복원 명령이 아니다. 기존 컨테이너가 같은 bind의 복원 내용을 읽는지 확인한 경우에만 아래 restart를 사용한다. Compose의 config 선택·환경변수·mount·image나 secret bind 또는 파일 inode가 바뀌면 이 분기를 중단하고 [RUN-0086](0086-dependency-version-management.md)의 이전 image/선언 복원과 승인된 recreate 계획으로 넘긴다. Secret 유지보수는 [RUN-0085](0085-openbao.md)를 따른다.

   ```bash
   git diff -- infra/06-observability/alertmanager/config/config.yml
   docker compose --profile obs restart alertmanager
   docker exec alertmanager wget -q --spider http://localhost:9093/-/ready
   ```

   이 런북은 Slack webhook rotation, SMTP credential rotation, receiver/channel change, inhibition policy change, protected middleware change를 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

### Verification Steps

- [ ] `docker compose --profile obs ps alertmanager`에서 `alertmanager` service가 running이다.
- [ ] `/-/ready` endpoint가 성공한다.
- [ ] Prometheus config의 `alertmanagers` target이 `alertmanager:9093`를 유지한다.
- [ ] Alertmanager UI에서 firing alerts, silences, receivers를 확인할 수 있다.
- [ ] Slack notification failure가 있었으면 test alert 또는 다음 firing alert에서 expected receiver 도착 여부를 확인하고 timestamp를 기록한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 alertmanager`
- **Health**: Alertmanager `/-/ready`, UI `https://alertmanager.${DEFAULT_URL}`
- **Config**: `infra/06-observability/alertmanager/config/config.yml`, Prometheus `alertmanagers` target과 Grafana datasource
- **Metrics**: `alertmanager_notifications_failed_total`, `prometheus_notifications_alertmanagers_discovered`
- **Evidence to Capture**: 실패한 receiver·route matcher, secret을 제거한 관련 로그, 재시작 시각, 최종 복구 또는 보고 상태

### Safe Rollback or Recovery Procedure

- Git-managed `config.yml`, Compose, or datasource/Prometheus endpoint change가 원인이면 직전 Git diff 단위로 되돌리고 Alertmanager를 재시작한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Secret rotation, Slack webhook replacement, SMTP credential replacement, receiver/channel change, or protected route middleware change는 이 런북의 안전 롤백 범위를 벗어난다.

### Planned isolated restore rehearsal

**project 이름만 바꾸어서는 실행할 수 없다.** rehearsal 전에 고정된 container-name,
host port, bind-path, external-network와 route의 충돌을 제거하고 운영 환경으로의
알림 전송과 workflow egress를 차단하는 별도 Compose 정의와 storage 구성을 승인받는다.
이 격리 구성과 해당 subject의 backup 계약을 검토하기 전까지 계획은 NOT_RUN으로
유지한다. 임시 project에 운영 volume을 연결하거나 credential을 복사하지 않는다.

상태: **계획됨, 미실행**. Alertmanager 상태 복구에 성공했다고 주장하지 않는다.

1. 알림 전송을 비활성화하거나 test receiver로 돌린다. image/config digest와 silence 목록을 기록하고 Alertmanager를 중지한 뒤, 일관된 상태의 `alertmanager-data` snapshot을 생성한다. template과 secret 참조도 보존한다.
2. test 전용 credential을 사용하고 운영 route가 없는 별도 project/network에 복구한다. config 검증 후 Alertmanager를 시작한다.
3. secret 값을 노출하지 않고 readiness, source alert 수신, silence 보존, inhibition/grouping, notification-log 동작과 통제된 test 알림 전송 1회를 검증한다.
4. 불일치가 있으면 격리된 project를 중지하고 log/checksum을 보존한다. 수정하지 않은 backup으로 돌아간다. 운영 route/state 교체는 별도로 승인받는다.

## Verification

### Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, rendered `/tmp/config.yml`, Slack webhook URL, SMTP credential 원문은 기록하지 않는다.
- Notification 장애는 affected receiver, matching route, alert labels, log excerpt, silence/inhibition state를 함께 기록한다.
- Receiver/channel/secret/middleware 변경 필요성이 보이면 approval state를 기록한다.

## Rollback and Escalation

### Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config rollback만 사용한다. Secret rotation, receiver/channel policy, inhibition policy, protected middleware, or external Slack/SMTP resource 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

### Escalation

verification이 실패하거나, secret exposure risk가 보이거나, receiver/channel/secret/middleware 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

### Traceability

- Declared parent: [Alertmanager Usage Guide](../guides/0039-alertmanager.md) (`GDE-0039`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0039-alertmanager.md) (`GDE-0039`), [Policy](../policies/0039-alertmanager.md) (`POL-0039`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0039-alertmanager.md)
- [Operations policy](../policies/0039-alertmanager.md)
