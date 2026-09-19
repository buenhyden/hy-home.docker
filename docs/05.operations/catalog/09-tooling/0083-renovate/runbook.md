---
title: "Renovate Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0083"
parent_ids:
- "POL-0083"
created: "2026-09-19"
---

# Renovate Runbook

## When to Use

Use this for static readiness, a specifically authorized live job, or recovery
from incorrect Renovate changes. Work from the repository root.

## Procedure

1. Validate without accessing remote repositories:

   ```bash
   renovate-config-validator --strict --no-global renovate.json5
   renovate-config-validator --strict infra/09-tooling/renovate/config/config.js
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

2. Review dry-run/discovery output, repository scope, token owner, branch
   protection, and authorization. Do not infer remote readiness from step 1.
3. When the remote write is authorized, run only the job:

   ```bash
   docker compose --profile dependency-update run --rm renovate
   ```

4. Record sanitized exit status and enumerate generated remote changes. Review
   each branch/PR; do not merge or close it under this run authorization.

## Evidence

Record authorization, config commit, image declaration, intended repositories,
exit status, sanitized job summary, and every generated branch/PR. Do not record
the token, raw environment, or repository credentials.

## Rollback or Recovery

1. Stop the specific container if an active run is creating unwanted changes.
2. Restore erroneous local policy from Git and repeat strict validation.
3. Review remote branches/PRs individually. Close or revert only with explicit
   authorization and preserve the audit trail.
4. If the token may be exposed, disable the job and ask the secret owner to
   rotate/revoke it. Do not copy or display the current token.
5. Cache corruption is recovered by recreating the disposable cache while no job
   is running. Remote repository state is never restored from that cache.

### Verification and Status

Recovery is complete when no Renovate job is running, configs validate, remote
changes are accounted for, and token disposition is known. These recovery steps
were documented but not executed during the 2026-09-20 correction; no remote
repository mutation or token validation is claimed.

## Escalation

Escalate on unknown remote writes, excessive token permission, suspected token
exposure, an unrecognized allowed command, or remote state that cannot be safely
reconciled one change at a time.

## Traceability

- Governing architecture: [AD-0009](../../../../02.architecture/descriptions/0009-tooling-architecture.md)
- Subject peers: [Guide](guide.md), [Policy](policy.md)

## Related Documents

- [Renovate Compose source](../../../../../infra/09-tooling/renovate/docker-compose.yml)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
- [Renovate self-hosted configuration](https://docs.renovatebot.com/self-hosted-configuration/)
- [Operations index](../../../README.md)
