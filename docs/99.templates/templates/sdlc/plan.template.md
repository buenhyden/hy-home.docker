---
status: draft
artifact_id: <artifact-id>
artifact_type: plan
parent_ids: [<parent-artifact-id>]
---
<!-- Target: docs/04.execution/plans/YYYY-MM-DD-<feature>.md -->

# [Feature Name] Implementation Plan

> Use this template for `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.
>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.
> - When closing a copied plan, update `## Completion Criteria` and closure
>   evidence; preserve detailed execution recipe checkboxes only when the task
>   evidence records them as historical instructions rather than current open
>   work.
> - Write this document in English. Preserve code identifiers, command names,
>   service names, environment variables, and quoted upstream terms exactly.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.
> - Replace example links with real target-relative links, or delete unused examples before saving.
>
> Target-relative examples from `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`:
>
> - PRD: `../../01.requirements/NNN-feature-or-system.md`
> - ARD: `../../02.architecture/requirements/####-system-or-domain.md`
> - ADR: `../../02.architecture/decisions/####-short-title.md`
> - Spec: `../../03.specs/NNN-feature-id/spec.md`
> - Task: `../tasks/YYYY-MM-DD-feature-or-stream.md`
> - Operations: `../../05.operations/README.md`

---

## Overview

This document is the implementation plan for [feature or component name]. It
defines work breakdown, verification, rollout, risk control, and completion
criteria.

## Context

[Why this work exists.]

## Goals & In-Scope

- **Goals**:
- **In Scope**:

## Non-Goals & Out-of-Scope

- **Non-goals**:
- **Out of Scope**:

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | [Action] | `path/to/file` | REQ-001 | [Evidence] |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | [Check] | [Command] | [Pass] |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| [Risk] | High | [Mitigation] |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**:
- **Sandbox / Canary Rollout**:
- **Human Approval Gate**:
- **Rollback Trigger**:
- **Prompt / Model Promotion Criteria**:

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed
- [ ] Required docs updated

## Related Documents

- **PRD**: [NNN-<feature-or-system>](../../01.requirements/NNN-<feature-or-system>.md)
- **ARD**: [####-<system-or-domain>](../../02.architecture/requirements/####-<system-or-domain>.md)
- **Spec**: [<feature-id> spec](../../03.specs/NNN-<feature-id>/spec.md)
- **ADR**: [####-<short-title>](../../02.architecture/decisions/####-<short-title>.md)
- **Task**: [YYYY-MM-DD-<feature-or-stream> task](../tasks/YYYY-MM-DD-<feature-or-stream>.md)
- **Operations**: [Operations index](../../05.operations/README.md)
