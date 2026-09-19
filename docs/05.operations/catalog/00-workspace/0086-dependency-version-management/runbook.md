---
title: "Dependency Version Management Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "RUN-0086"
parent_ids:
- "POL-0086"
created: "2026-09-19"
---

# Dependency Version Management Runbook

## When to Use

Use when source images, update policy or the curated version projection change.
Work from the repository root, with a cleanly identified diff and no private values
in output. This procedure does not run the networked Renovate update job.

## Procedure

1. Identify changed Compose/Dockerfile pins, build arguments and manager ownership.
2. Preview and validate the curated projection without writes:

```bash
bash scripts/operations/sync-tech-stack-versions.sh --dry-run
bash scripts/operations/sync-tech-stack-versions.sh --check
```

1. If source changes are intentional, run the same script without an option to
   update only the registry, then inspect that diff and repeat `--check`.
2. Run the official `renovate-config-validator --strict --no-global renovate.json5`
   and `renovate-config-validator --strict infra/09-tooling/renovate/config/config.js`
   using the supported Renovate Node runtime or approved tooling container.
3. Validate selected Compose profiles and related build changes. Test ambiguous,
   missing and digest sources through the existing synchronization test suite.
4. For any actual update job or deployment, obtain approval for that named action
   and record migration/backup prerequisites before executing it.

## Evidence

Record command, exit status, source commit, parser/validator runtime and limitations.
Unsupported Node or missing native validation dependencies must be explicit; no
local syntax result proves a remote bot run or a restored application database.

## Rollback or Recovery

Revert source and registry changes together. Config rollback does not downgrade
existing database files. Keep the last compatible image and protected backup;
restore data only through the service-owned isolated recovery procedure.

## Escalation

Stop on ambiguous sources, new unknown managers, registry-only pin changes,
credential errors, unsupported migration paths or unavailable recovery evidence.
Refer to @buenhyden for the exact decision; never bypass gates or force push.

## Traceability

- [Home/Dev architecture](../../../../02.architecture/descriptions/0031-home-development-host.md) (`AD-0031`)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Runtime version projection](../../../../../infra/tech-stack.versions.json)
- [Repository Renovate policy](../../../../../renovate.json5)
- [Dependabot scope](../../../../../.github/dependabot.yml)
