---
title: "Subagent Model and Routing Text Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0217-TSK-0001"
parent_ids:
- "SPEC-0217-PLAN-0001"
created: "2026-10-08"
---

# Subagent Model and Routing Text Task

## Objective

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Description test | 1 | W1 | RED with the earlier renderer (14 failures), GREEN after | Working tree | PASS | W1 Routing Descriptions | accepted |
| Renderer parity and contract | 2 | W1 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | W1 Routing Descriptions | accepted |
| Renderer parity and contract | 2 | W2 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | W2 Model Selections | accepted |
| Wrapped Use When bullet | 1 | W1 | Synthetic role test RED with the earlier renderer, GREEN after; every case checked in both projections | Working tree | PASS | Review Round 1 | accepted |
| Renderer parity after review | 2 | W1 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | Review Round 1 | accepted |
| Earlier model IDs | 3 | W2 | `git grep` for `claude-opus-5` and `claude-sonnet-5` outside Stage 90, Stage 98 and this package | Working tree | PASS | W2 Model Selections | accepted |

## Review and Completion

W1 and W2 are complete in source. Runtime acceptance of the new models
(entitlement and native subagent invocation) remains `needs_revalidation` in
the registry, and the effort values have not been re-swept for Sonnet 5.5.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
