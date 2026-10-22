---
title: "Subagent Model and Routing Text Task"
version: "0.3.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0217-TSK-0001"
parent_ids:
- "SPEC-0217-PLAN-0001"
created: "2026-10-08"
---

# Subagent Model and Routing Text Task

## Overview

### Objective

Move the generated Claude subagents to the current Claude generation and give
each generated subagent description the routing text its role already states.

## Inputs and Authorization

A prompt audit on 2026-10-08 reported that the Provider Registry pins the
previous Claude generation and that every generated subagent description is
boilerplate with no routing signal. On 2026-10-08 the owner approved both
fixes ("하위 에이전트가 쓰는 모델: 수정. 하위 에이전트 설명문(description 수정."), which
covers the protected `.agents/**`, `scripts/**`, `.claude/**` and `.codex/**`
edits below. Baseline: `main` `b0a72d2e5`. Registry issues SPEC-0217.

## Work Log

### Baseline

All 14 roles under `.agents/roles/` have exactly one `## Overview` paragraph
and one `### Use When` list. The renderer built every Claude and Codex
description from scope and agent ID alone, and its generated-Codex check
matched that boilerplate by regular expression. The Claude work profiles used
`claude-opus-5` (`adversarial-review`, `long-horizon-supervision`) and
`claude-sonnet-5` (`complex-implementation`, `evidence-research`). A search
found the earlier IDs only in the registry, the generated projections and
Stage 90 research.

### W1 Routing Descriptions

`test_claude_agent_descriptions_carry_role_routing_text` in
`test_validator_entrypoints.py`, the renderer's registered test, checks that
each generated Claude description contains the role's Overview paragraph and
`Use when:`. Against the earlier renderer it failed for all 14 roles (RED).
`_description` now joins the Overview paragraph and the Use When cases and
raises when a role lacks either section. The generated-Codex check requires a
non-empty description instead of the boilerplate; it still identifies a
generated file by the source marker in `developer_instructions`. After
`--write`, the test passes for all 14 roles (GREEN). Codex descriptions change
the same way, since both providers share `_description`.

### W2 Model Selections

The four Claude work profiles and their `models` entries now name
`claude-opus-5-5` and `claude-sonnet-5-5`. Effort values, the Haiku
`routine-validation` profile and every Codex selection are unchanged.
`--write` regenerated the `model:` line of the 13 affected Claude subagents
and nothing else.

### Review Round 1

An independent `code-reviewer` pass on PR #388 found no Critical issue and one
Important one: the Use When pattern stopped at the first line that was not a
`-` bullet, so a wrapped bullet would silently drop its continuation and every
later case, and the test checked only the `Use when:` literal. The renderer now
splits the whole Use When block on `-` bullets, collapses wrapped lines and
joins the cases with semicolons. The description test now checks every case in
both the Claude and Codex projections, and a synthetic role with a wrapped
bullet fails against the earlier renderer (RED) and passes after (GREEN).
Acceptance criterion 3 now excludes this package's own baseline narration,
which names the earlier models on purpose. The reviewer's other note, that a
hand-written Codex file carrying the generated marker is now treated as stale
generated output, is accepted: the marker is itself a claim of generation, and
`--write` quarantines rather than deletes.

### Current Contract Approval 2026-10-22

The user's current request on 2026-10-22 explicitly authorizes status and lifecycle
processing for implemented Specs, Plans and Tasks. The earlier audit was compared
with the current Spec and Plan, and this package's public implementation at
`bd4168e20` was confirmed unchanged since the audit input `d7bec9a9a`.
The current contracts and assignments remain valid, so the Spec and Plan are each
approved through `draft → approved`, with their first stable version `1.0.0`.
This present decision neither backdates approval of the original implementation
nor grants new operational authorization or risk acceptance.

### Current Readiness Review 2026-10-22

The currently approved parent Spec and Plan, assigned Work Units, existing
implementation, and this Task's Evidence and Criterion Acceptance were secured
as closure-review inputs. Preparation for the document closure requested today
is complete, so the Task transitions `draft → ready` today. No execution status
is inferred for the time of the historical source or runtime work.

### Current Closure Review 2026-10-22

The prepared document closure review was performed, transitioning the Task
`ready → in-progress`. The canonical package reader and the assignment, evidence
and acceptance rows confirm PASS for all 4 criterion/Work Unit pairs assigned
to this Task, accepted decisions for all criteria it owns, and no unresolved FAIL.
Existing checks and decisions are reused; observation and acceptance rows are unchanged.
Completion covers model selections and the description renderer in source. Registry entitlement/runtime_acceptance remains `needs_revalidation`, and the Sonnet effort sweep remains outstanding.

### Current Completion Decision 2026-10-22

Today's readiness and closure reviews, including assigned-pair PASS and existing
accepted decisions, are complete, so the Task transitions `in-progress → completed`.
Completion is limited to this Task's assigned scope. The lifecycle rows below
record the document transitions actually performed today; they do not replace
historical execution evidence. Archive readiness is derived by the canonical
reader, and this change performs no Stage 98 move.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0217 | draft | approved | #current-contract-approval-2026-10-22 |
| SPEC-0217-PLAN-0001 | draft | approved | #current-contract-approval-2026-10-22 |
| SPEC-0217-TSK-0001 | draft | ready | #current-readiness-review-2026-10-22 |
| SPEC-0217-TSK-0001 | ready | in-progress | #current-closure-review-2026-10-22 |
| SPEC-0217-TSK-0001 | in-progress | completed | #current-completion-decision-2026-10-22 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Description test | 1 | W1 | RED with the earlier renderer (14 failures), GREEN after | Working tree | PASS | W1 Routing Descriptions | - |
| Renderer parity and contract | 2 | W1 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | W1 Routing Descriptions | - |
| Renderer parity and contract (2) | 2 | W2 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | W2 Model Selections | - |
| Wrapped Use When bullet | 1 | W1 | Synthetic role test RED with the earlier renderer, GREEN after; every case checked in both projections | Working tree | PASS | Review Round 1 | - |
| Renderer parity after review | 2 | W1 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | Review Round 1 | - |
| Earlier model IDs | 3 | W2 | `git grep` for `claude-opus-5` and `claude-sonnet-5` outside Stage 90, Stage 98 and this package | Working tree | PASS | W2 Model Selections | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | accepted | Description test, Wrapped Use When bullet | Generation 5 row acceptance |
| 2 | accepted | Renderer parity and contract, Renderer parity and contract (2), Renderer parity after review | Generation 5 row acceptance |
| 3 | accepted | Earlier model IDs | Generation 5 row acceptance |

## Review and Completion

The current status is `completed`. Today's
[completion decision](#current-completion-decision-2026-10-22) owns the current
lifecycle; the existing completion, observation and limitation records below
are preserved as history for their dated inputs.

W1 and W2 are complete in source. Runtime acceptance of the new models
(entitlement and native subagent invocation) remains `needs_revalidation` in
the registry, and the effort values have not been re-swept for Sonnet 5.5.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
