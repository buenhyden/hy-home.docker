---
status: draft
artifact_id: <artifact-id>
artifact_type: task
parent_ids: [<parent-artifact-id>]
---
<!-- Target: docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md -->

# Task: [Task Name]

> Use this template for `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`.
>
> Rules:
>
> - Task documents are traceability-first.
> - Core behavior should default to TDD.
> - Agent work must include eval tasks where applicable.
> - This is the canonical execution-tracking location; feature-local task notes under `03.specs/` are secondary.
> - Write this document in English. Preserve code identifiers, command names,
>   service names, environment variables, and quoted upstream terms exactly.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.
> - Replace example links with real target-relative links, or delete unused examples before saving.
>
> Target-relative examples from `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`:
>
> - Parent Spec: `../../03.specs/NNN-feature-id/spec.md`
> - Parent Plan: `../plans/YYYY-MM-DD-feature.md`
> - Operations direct target: `../../05.operations/guides/topic.md`
> - Operations domain target: `../../05.operations/guides/domain/topic.md`
> - Reference target: `../../90.references/{audits,data,research,learning}/category/item.md`

---

## Overview

This document tracks implementation and verification work for [feature or work
stream name]. It records tasks derived from the parent Spec and Plan in an
auditable form.

## Inputs

- **Parent Spec**: [Feature spec](../../03.specs/NNN-<feature-id>/spec.md)
- **Parent Plan**: [Execution plan](../plans/YYYY-MM-DD-<feature>.md)

## Working Rules

- Write failing tests first for core behavior.
- Every task must define evidence.
- Documentation-only work still needs validation evidence.
- If a feature-local `tasks.md` exists under `03.specs/`, this document remains the execution-tracking source of truth.

## Approved Surface Evidence

Use this section when the task touches high-risk approved surfaces such as
policy, runtime, CI, templates, secrets, remote GitHub, model policy, or provider
adapters. Delete the section when no such surface is in scope.

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| [surface] | [approval] | [target] | [evidence] | [evidence] | [rollback] | [redaction] |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | [Action] | impl | SPC-001 / §2 | Phase 1 | `pytest ...` | [Name] | Todo |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [ ] T-001 [Description]

### Phase 2

- [ ] T-002 [Description]

## Verification Summary

- **Test Commands**:
- **Eval Commands**:
- **Logs / Evidence Location**:

## Controlled Agent Pre-commit Evidence (If Applicable)

Use only for an approved final QA all-files gate. Direct `pre-commit run` is
prohibited for agents; invoke
`scripts/validation/run-agent-precommit-all-files.sh` from an initially clean
linked worktree. The wrapper never writes this evidence automatically. Delete
this section when the gate is not applicable.

| Command | Allowed Prefixes | Exit Status | Modified Paths | Review Disposition | Skipped Rationale |
| --- | --- | ---: | --- | --- | --- |
| [exact wrapper command] | [repo-relative prefixes] | [exit code] | [before/after/new/unexpected paths] | [accepted, separate commit, scope escalation, or blocked] | [reason, or N/A when executed] |

## Related Documents

- **Parent Spec**: [Feature spec](../../03.specs/NNN-<feature-id>/spec.md)
- **Parent Plan**: [Execution plan](../plans/YYYY-MM-DD-<feature>.md)
- **Operations / References**: [Operations guide](../../05.operations/guides/<topic>.md)
- **Reference**: [Reference item](../../90.references/{audits,data,research,learning}/<category>/<item>.md)
