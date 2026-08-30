---
profile_id: task
status: draft
artifact_id: task-0154-0002
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Role and Skill Canonicalization

## Objective

Narrow the Stage 99 `governance-role` profile to the agent-role genre and rename the two skills whose identifiers collide with globally installed provider skills. Plan Task 2.

## Inputs

- Task 1 result: `roles/` holds only agent roles.
- `docs/99.templates/registry.json` `profiles[governance-role]`.
- `docs/00.agent-governance/skills/{code-reviewer,test-automator}.md` and the two roles that reference them.

## Work Log

Not started. Record each plan step with the command run, the observed result,
the rollback path, and any skipped check with its rationale.

## Verification Evidence

Not started. Record the before and after output of every validator the plan
step names, with exit codes.

## Review Evidence

Not started. Record the independent review verdict, its findings by severity,
and the re-review result after any material finding.

## Commit Ledger

Not started. Record one row per logical commit with its subject and the paths it
touched.

## Rulings

Plan rulings 1 to 4 apply. Record any additional ruling made during execution
with the evidence that supported it.

## Deferred Items

None recorded yet.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
