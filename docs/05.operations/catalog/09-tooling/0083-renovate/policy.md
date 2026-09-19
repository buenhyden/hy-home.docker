---
title: "Renovate Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0083"
parent_ids:
- "AD-0009"
created: "2026-09-19"
---

# Renovate Policy

## Overview

Renovate is an explicitly selected `dependency-update` job with remote repository
write capability. It is never part of HOME or ordinary tooling startup.

## Policy Scope

The policy covers `renovate`, its Docker Secret, configuration, cache, remote
changes, upgrades, and evidence. `POL-0086` remains the update-strategy authority.

## Controls

- Mount `renovate_token` only as the declared secret and grant the minimum
  repositories and permissions. Never print the token file or rendered secret.
- Preserve `allowScripts: false` and the explicit command allowlist. Expanding
  either requires security review and a bounded justification.
- Strictly validate repository and self-host configs before a run. Treat a
  validator PASS as syntax evidence only.
- Obtain authorization before any live job because it can write branches and
  pull requests. Merge, close, and token rotation are separately authorized
  actions.
- Keep the cache disposable. Do not treat it as repository truth or back it up as
  business state. Git and the remote hosting service own durable configuration
  and generated changes.
- Upgrade by immutable image declaration, official migration/release review,
  strict validation, dry-run/discovery, and one bounded canary repository.
- Record job time, config commit, intended repositories, image declaration,
  sanitized result, and generated PRs without secret values.

## Verification

```bash
renovate-config-validator --strict --no-global renovate.json5
renovate-config-validator --strict infra/09-tooling/renovate/config/config.js
bash scripts/operations/sync-tech-stack-versions.sh --check
```

## Exceptions

Any broader token permission, repository scope, allowed command, script
execution, or remote mutation requires a recorded owner, expiry, rollback, and
security review. Syntax validation is never an exception to live-run approval.

## Review Cadence

Review monthly and whenever the image, token scope, repository list, managers,
allowed commands, or `POL-0086` changes.

## Traceability

- Governing architecture: [AD-0009](../../../../02.architecture/descriptions/0009-tooling-architecture.md)
- Subject peers: [Guide](guide.md), [Runbook](runbook.md)

## Related Documents

- [Renovate Compose source](../../../../../infra/09-tooling/renovate/docker-compose.yml)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
- [Renovate security and permissions](https://docs.renovatebot.com/security-and-permissions/)
- [Operations index](../../../README.md)
