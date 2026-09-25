---
title: "Renovate Guide"
version: "0.2.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
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

Renovate is a **DEV** one-shot repository maintenance job selected only by
`dependency-update`. It is excluded from HOME and ordinary `tooling` startup.
The root Compose project supplies `renovate.json5`, the self-host configuration,
the `renovate_token` Docker Secret, and a cache volume. A live run reads remote
repositories and may create or update branches and pull requests.

### Implementation Sources

- [Renovate Compose](../../../infra/09-tooling/renovate/docker-compose.yml)
- [Self-host configuration](../../../infra/09-tooling/renovate/config/config.js)
- [Repository configuration](../../../renovate.json5)
- [Dependency-version policy](../policies/0086-dependency-version-management.md) (`POL-0086`)

`POL-0086` owns managers, release age, security updates, automerge, and updater
overlap. This package owns the job boundary. `allowScripts: false` and the narrow
global command allowlist limit execution. The cache is rebuildable; Git policy,
remote repository state, and the token owner are authoritative.

### Normal Use

1. Check repository and global configuration without a token or remote mutation:

   ```bash
   renovate-config-validator --strict --no-global renovate.json5
   renovate-config-validator --strict infra/09-tooling/renovate/config/config.js
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

2. Review token repository scope, branch protection, dry-run output, and the
   intended repositories. Validation does not prove token permission.
3. A live run is an external write action. Execute only after authorization and
   name the single job:

   ```bash
   docker compose --profile dependency-update run --rm renovate
   ```

4. Review every generated branch/PR and sanitized job summary. A successful job
   does not authorize merging.

### Recovery and Upgrade

Delete/recreate only the cache after confirming no live job uses it. Restore
policy from Git, review or close erroneous remote branches/PRs individually, and
rotate the token only through its secret owner when exposure is suspected.
Before an image upgrade, review Renovate release notes and migrations, validate
both configs, run dry-run/discovery against a bounded repository set, then run a
single authorized canary repository.

### Scheduled Operation via systemd

The repository ships two systemd unit files under
`infra/09-tooling/renovate/`:

| File | Purpose |
|---|---|
| [`hyhome-renovate.service`](../../../infra/09-tooling/renovate/systemd/hyhome-renovate.service) | oneshot service — runs the Renovate Compose job |
| [`hyhome-renovate.timer`](../../../infra/09-tooling/renovate/systemd/hyhome-renovate.timer) | weekly timer — triggers the service unit |

#### How the timer works

- **Schedule**: Monday 00:00 KST with up to 60 minutes of random jitter
  (`RandomizedDelaySec=3600`). This matches the `renovate.json5` schedule
  window (`"* 0-5 * * 1"` in `Asia/Seoul` timezone) so the host trigger
  and the in-app schedule guard use the same maintenance window.
- **Missed fires**: `Persistent=true` causes the timer to fire on the next
  boot if the host was offline when the Monday trigger was due. That catch-up
  run can fall outside the `renovate.json5` window; Renovate then updates the
  Dependency Dashboard but does not open new branches until the window.
- **Start dependency**: the timer declares no `Requires=` on the service and the
  service has no `[Install]` section, so enabling or starting the timer, or a
  reboot, never starts an immediate run by itself.
- **Timezone**: `OnCalendar` uses the `Asia/Seoul` suffix (systemd ≥ 242,
  this host runs 255).

#### Service flow

```text
Timer fires
  └─ ExecStartPre (1): assert renovate_token secret non-empty
  └─ ExecStartPre (2): docker compose pull --quiet renovate
  └─ ExecStart:        docker compose --profile dependency-update run --rm --no-deps renovate
```

No post-run prune runs: `docker image prune` is host-wide. Remove superseded
Renovate image tags manually by exact reference.

If any pre-flight check fails the run aborts before the container is
created. The service does **not** auto-restart (`Restart=no`); a failed
run requires human log review before the next attempt.

#### Installation

Installing or replacing host units is a host change that needs its own
approval. Copy reviewed files instead of symlinking them, so a checkout,
branch switch or pull cannot silently change what systemd runs. The installed
copies checked on 2026-09-21 were an older revision than this repository.

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

> All live-run authorization and evidence rules in the policy and runbook
> apply equally to timer-triggered and manually triggered runs.

## Common Checks

- Strict repository and self-host configuration validation.
- `bash scripts/operations/sync-tech-stack-versions.sh --check`.
- For an authorized live job, reconcile sanitized results with every generated
  branch/PR and confirm that no merge was performed by this job authorization.

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
