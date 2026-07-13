---
status: draft
artifact_id: <artifact-id>
artifact_type: task
parent_ids: [<parent-artifact-id>]
---

<!-- Target: docs/04.execution/tasks/YYYY-MM-DD-<harness-stream>.md -->

# Harness Task Contract: [Task Name]

> Use this template for harness-surface work tracked under
> `docs/04.execution/tasks/YYYY-MM-DD-<harness-stream>.md`.
>
> Rules:
>
> - Harness work changes governance, scripts, validation, CI, templates, or the
>   PR contract; it must not touch protected surfaces without recorded approval.
> - Consult [Approval Boundaries](../../00.agent-governance/rules/approval-boundaries.md)
>   and the [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
>   before changing state.
> - Secret-related changes record only path, ID, registry, and redacted
>   evidence; never secret values.
> - Target-relative links in `## Related Documents` are calculated from the
>   copied target path, not from `docs/99.templates/`.

---

## Goal

- [What this harness change must achieve.]

## Non-goals

- [What this change explicitly does not do.]

## Affected Surfaces

- [Governance / Scripts / Validation / CI / Templates / PR / Operations.]

## Allowed Paths

- [Exact paths this task may modify.]

## Forbidden Paths

- `docker-compose.yml` root-active include
- `infra/**` port, volume, network, secret mount
- `secrets/**` values
- `.env` real values
- `.github/workflows/**` permission expansion

## Approval Required

- [Protected surfaces touched and the approval source, or "None".]

## Required Validation

```bash
bash scripts/validation/validate-harness.sh
```

## Secret Handling

- [Path / ID / registry / redacted evidence only. No secret values.]

## Compose Impact

- [Profile / secret / volume / network / port / backup impact, or "None".]

## Operations Impact

- [Linked backup, restore, rotation, or restart runbook, or "None".]

## Rollback Plan

- [How to revert. Additive doc/script changes are revertible by `git revert`.]

## Evidence Location

- [Where validation output and approval evidence are recorded.]

## Related Documents

- **Approval Boundaries**: [Approval boundaries](../../00.agent-governance/rules/approval-boundaries.md)
- **Harness Map**: [Harness implementation map](../../00.agent-governance/harness-implementation-map.md)
- **Operations**: [Operations guide](../../05.operations/guides/<topic>.md)
