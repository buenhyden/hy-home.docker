---
title: "Agent Guide Follow-ups Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0254-TSK-0001"
parent_ids:
- "SPEC-0254-PLAN-0001"
created: "2026-11-04"
---

# Agent Guide Follow-ups Task

## Overview

### Objective

Close the four follow-ups SPEC-0251 left open.

## Inputs and Authorization

On 2026-11-04 the user approved, verbatim: "entrypoint link findings (9) 처리,
CI selection gap 처리, ADR-0002 처리, governance/agent-guide type name 처리
승인". Earlier the user approved moving the folder guides from `draft` to
`active`. The workflow-contract edit touches a protected surface under that
approval. This Task pushes and merges nothing: the coordinator pushes the
branch and opens the pull request, and the user merges.

## Work Log

### Current contract decision

The user's approval authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0254 | draft | approved | #current-contract-decision |
| SPEC-0254-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0254-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0254-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Decisions

- **Entrypoint links:** a document outside `docs/` may link a stage README or
  directory but no individual stage document. Each of the nine links became
  its label followed by the repository path in inline code, so the reader can
  still find the record and no link resolves into a stage document.
- **CI selection:** changed-path rules are unioned, and a path no rule maps
  selects every suite. `scripts/AGENTS.md` and `tests/AGENTS.md` were unmapped
  and already selected every suite, so the new rule lists only the seven guides
  that did not select agent-governance; adding the other two would have
  narrowed them.
- **Type name:** the stage authoring matrix says the family names the
  authority that owns the document. A folder guide is routing text beside a
  README, so it joins the `common` family as `common/agent-guide`, and its
  template moves to `docs/99.templates/templates/common/`.
- **ADR-0002:** not changed. Its `AI Agent Guidance` subsection sits under
  `## Consequences` in the accepted decision body, and
  `docs/02.architecture/AGENTS.md` ("do not rewrite an accepted decision
  body") with `documentation-protocol.md` ("Do not change an existing accepted
  decision silently") forbids rewriting it. Moving the text needs a separately
  approved superseding ADR; this is reported for the owner's decision.
- **Activation:** the `living` lifecycle allows `draft` to `active`; the nine
  guides moved with a minor version bump.

### Changed

- Nine `infra` README lines: individual stage links replaced by plain-text
  identities with paths.
- `.github/workflow-contract.yml`: one `changed_path_rules` entry for the seven
  guides, selecting `agent-governance`.
- `tests/validation/test_agent_governance_ci_routing.py`: every
  `folder-agent-guide` profile path selects agent-governance.
- Registry `folder-agent-guide` type and template role, the moved template,
  the nine guides' `type` and `status`, the stage authoring matrix and the
  documentation protocol.

### Open issues

- ADR-0002's `AI Agent Guidance` subsection stays until the owner approves a
  superseding ADR or another route.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | links-entrypoint | `check-document-links.py --mode entrypoint` before the edit, main 4adeb3d37 | FAIL | 9 `stage-link-outside-docs` findings in six `infra` READMEs | required | - |
| E2 | 1 | W1 | links-entrypoint | after the plain-text change | PASS | zero findings | required | E1 |
| E3 | 2 | W2 | ci-routing | `test_a_folder_agent_guide_change_selects_agent_governance` with the new rule, and with the workflow contract restored to main | PASS | OK with the rule; 7 subtests fail without it | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. No independent review has run and hosted CI
is not observed here; no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
