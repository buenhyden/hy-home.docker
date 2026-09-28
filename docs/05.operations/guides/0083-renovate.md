---
title: "Renovate Guide"
version: "0.2.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0083"
parent_ids:
- "POL-0083"
implementation_services:
  infra/09-tooling/renovate/docker-compose.yml:
  - renovate
created: "2026-09-19"
---

# Renovate Guide

## Usage

Renovate는 `dependency-update`에서만 선택하는 **DEV** one-shot repository
유지보수 작업이다. HOME과 일반 `tooling` 시작에서는 제외된다. root Compose
project는 `renovate.json5`, self-host 설정, `renovate_token` Docker Secret,
cache volume을 제공한다. live run은 원격 repository를 읽고 branch와 pull
request를 생성하거나 갱신할 수 있다.

### Implementation Sources

- [Renovate Compose](../../../infra/09-tooling/renovate/docker-compose.yml)
- [Self-host configuration](../../../infra/09-tooling/renovate/config/config.js)
- [Repository configuration](../../../renovate.json5)
- [Dependency-version policy](../policies/0086-dependency-version-management.md) (`POL-0086`)

`POL-0086`은 manager, release age, security update, automerge, updater
overlap을 관장한다. 이 package는 job 경계를 관장한다. `allowScripts: false`와
좁은 global command allowlist가 실행을 제한한다. cache는 다시 만들 수 있으며 Git
policy, 원격 repository 상태, token owner가 authoritative하다.

### Normal Use

1. token이나 원격 변경 없이 repository와 global 설정을 확인한다.

   ```bash
   renovate-config-validator --strict --no-global renovate.json5
   renovate-config-validator --strict infra/09-tooling/renovate/config/config.js
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

2. token repository scope, branch protection, dry-run 출력, 대상 repository를
   검토한다. validation은 token 권한을 증명하지 않는다.
3. live run은 외부 write 행위이므로
   [Renovate runbook](../runbooks/0083-renovate.md#procedure)에 있는 승인된
   절차로만 실행한다.

### Recovery and Upgrade

live job이 사용하지 않는지 확인한 후에만 cache를 삭제/재생성한다. policy를
Git에서 복원하고, 잘못된 원격 branch/PR을 개별적으로 검토하거나 닫으며,
노출이 의심될 때만 secret owner를 통해 token을 회전한다. 이미지 upgrade
전에는 Renovate release note와 migration을 검토하고 두 설정 모두를
validation한 뒤, 제한된 repository 집합에 대해 dry-run/discovery를 실행하고
단일 승인된 canary repository를 실행한다.

### Scheduled Operation via systemd

repository는 `infra/09-tooling/renovate/`에 systemd unit 파일 두 개를
제공한다.

| File | Purpose |
|---|---|
| [`hyhome-renovate.service`](../../../infra/09-tooling/renovate/systemd/hyhome-renovate.service) | oneshot service — Renovate Compose job을 실행 |
| [`hyhome-renovate.timer`](../../../infra/09-tooling/renovate/systemd/hyhome-renovate.timer) | weekly timer — service unit을 트리거 |

#### How the timer works

- **Schedule**: 월요일 00:00 KST에 최대 60분의 random jitter
  (`RandomizedDelaySec=3600`)를 둔다. 이 값은 `renovate.json5`의 schedule window
  (`Asia/Seoul` timezone의 `"* 0-5 * * 1"`)와 일치해서 host trigger와 in-app
  schedule guard가 같은 maintenance window를 쓰게 된다.
- **Missed fires**: `Persistent=true` 덕분에 월요일 trigger 시각에 host가
  오프라인이었다면 다음 boot 때 timer가 실행된다. 그 catch-up run은
  `renovate.json5` window를 벗어날 수 있다. 그 경우 Renovate는 Dependency
  Dashboard는 갱신하지만 window가 될 때까지 새 branch를 열지 않는다.
- **Start dependency**: timer는 service에 `Requires=`를 선언하지 않고
  service에는 `[Install]` section이 없으므로, timer를 enable하거나
  start하거나 reboot해도 그 자체로 즉시 run이 시작되지는 않는다.
- **Timezone**: `OnCalendar`는 `Asia/Seoul` suffix를 사용한다(systemd ≥ 242,
  이 host는 255를 실행 중).

#### Service flow

```text
Timer fires
  └─ ExecStartPre (1): assert renovate_token secret non-empty
  └─ ExecStartPre (2): docker compose pull --quiet renovate
  └─ ExecStart:        docker compose --profile dependency-update run --rm --no-deps renovate
```

run 이후에는 prune을 실행하지 않는다. `docker image prune`은 host 전역이다.
대체된 Renovate image tag는 정확한 reference로 수동 제거한다.

pre-flight check가 하나라도 실패하면 container를 만들기 전에 run이
중단된다. service는 자동 재시작하지 않으며(`Restart=no`), 실패한 run은 다음
시도 전에 사람이 log를 검토해야 한다.

#### Installation

host unit을 설치하거나 교체하는 것은 별도 승인이 필요한 host 변경이다.
symlink 대신 검토된 파일을 복사해 checkout이나 branch 전환, pull이 systemd가
실행하는 내용을 조용히 바꾸지 못하게 한다. 2026-09-21에 확인한 설치된
복사본은 이 repository보다 오래된 revision이었다.

```bash
# 1. Compare, then copy the reviewed revision (approved host change only)
diff /etc/systemd/system/hyhome-renovate.service infra/09-tooling/renovate/systemd/hyhome-renovate.service
sudo install -m 0644 infra/09-tooling/renovate/systemd/hyhome-renovate.service /etc/systemd/system/
sudo install -m 0644 infra/09-tooling/renovate/systemd/hyhome-renovate.timer /etc/systemd/system/

# 2. Reload and enable only the timer
sudo systemctl daemon-reload
sudo systemctl enable hyhome-renovate.timer
sudo systemctl start hyhome-renovate.timer
```

#### Operational checks

```bash
# Timer status and next trigger time
systemctl status hyhome-renovate.timer
systemctl list-timers hyhome-renovate.timer

# Last run log (full output)
journalctl -u hyhome-renovate.service --no-pager

# Trigger manually (bypass timer, authorized runs only)
sudo systemctl start hyhome-renovate.service

# Stop and disable scheduled runs without removing the unit
sudo systemctl disable --now hyhome-renovate.timer
# Stop a run in progress (the container is removed by --rm)
sudo systemctl stop hyhome-renovate.service
```

> policy와 runbook의 모든 live-run 승인과 evidence 규칙은 timer가 트리거한
> run과 수동으로 트리거한 run에 똑같이 적용된다.

## Common Checks

- repository와 self-host 설정에 대한 strict validation.
- `bash scripts/operations/sync-tech-stack-versions.sh --check`.
- 승인된 live job의 경우, sanitized 결과를 생성된 모든 branch/PR과 대조하고
  이 job 승인으로는 merge가 일어나지 않았는지 확인한다.

## Traceability

- Governing architecture: [AD-0009](../../02.architecture/descriptions/0009-tooling-architecture.md)
- Subject peers: [Policy](../policies/0083-renovate.md), [Runbook](../runbooks/0083-renovate.md)

## Related Documents

- [hyhome-renovate.service](../../../infra/09-tooling/renovate/systemd/hyhome-renovate.service)
- [hyhome-renovate.timer](../../../infra/09-tooling/renovate/systemd/hyhome-renovate.timer)
- [Renovate self-hosted configuration](https://docs.renovatebot.com/self-hosted-configuration/)
- [Renovate configuration validation](https://docs.renovatebot.com/config-validation/)
- [systemd.timer(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)
- [systemd.time(7) — OnCalendar](https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html)
- [Operations index](../README.md)
