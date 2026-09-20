---
title: "Renovate Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
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

- [Renovate Compose](../../../../../infra/09-tooling/renovate/docker-compose.yml)
- [Self-host configuration](../../../../../infra/09-tooling/renovate/config/config.js)
- [Repository configuration](../../../../../renovate.json5)
- [Dependency-version policy](../../00-workspace/0086-dependency-version-management/policy.md) (`POL-0086`)

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

## Common Checks

- Strict repository and self-host configuration validation.
- `bash scripts/operations/sync-tech-stack-versions.sh --check`.
- For an authorized live job, reconcile sanitized results with every generated
  branch/PR and confirm that no merge was performed by this job authorization.

## Traceability

- Governing architecture: [AD-0009](../../../../02.architecture/descriptions/0009-tooling-architecture.md)
- Subject peers: [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Renovate self-hosted configuration](https://docs.renovatebot.com/self-hosted-configuration/)
- [Renovate configuration validation](https://docs.renovatebot.com/config-validation/)
- [Operations index](../../../README.md)
