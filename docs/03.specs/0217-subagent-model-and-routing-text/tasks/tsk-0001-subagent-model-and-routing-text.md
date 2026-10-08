---
title: "Subagent Model and Routing Text Task"
version: "0.1.0"
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Description test | 1 | W1 | RED with the earlier renderer (14 failures), GREEN after | Working tree | PASS | W1 Routing Descriptions | accepted |
| Renderer parity and contract | 2 | W1 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | W1 Routing Descriptions | accepted |
| Renderer parity and contract | 2 | W2 | `provider_surface_renderer.py --check`; `check-agent-governance-contract.py`; entrypoint test module | Working tree | PASS | W2 Model Selections | accepted |
| Earlier model IDs | 3 | W2 | `git grep` for `claude-opus-5` and `claude-sonnet-5` outside Stage 90 and Stage 98 | Working tree | PASS | W2 Model Selections | accepted |

## Review and Completion

W1 and W2 are complete in source. Runtime acceptance of the new models
(entitlement and native subagent invocation) remains `needs_revalidation` in
the registry, and the effort values have not been re-swept for Sonnet 5.5.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
