---
title: "Folder Guide Delivery Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0264-TSK-0001"
parent_ids:
- "SPEC-0264-PLAN-0001"
created: "2026-11-06"
---

# Folder Guide Delivery Task

## Overview

### Objective

Record the execution and evidence of work units W1 to W4 of the Plan.

## Inputs and Authorization

The owner requested the change on 2026-11-06 and chose one shared hook over
folder `CLAUDE.md` shims. Spec approval is the owner's, in the pull request.

## Work Log

### Implementation

W1 to W3 are implemented on `feat/folder-agents-guide-hook`:
`scripts/lib/hooks/folder_guides.py`, the dispatcher wiring, 8 tests, the
manifest entry, `.claude/provider.md` 1.6.0, `.codex/provider.md` 1.5.0 and the
audit of the 10 `AGENTS.md` files.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0264 | draft | approved | #owner-approval |
| SPEC-0264-PLAN-0001 | draft | approved | #owner-approval |
| SPEC-0264-TSK-0001 | draft | ready | #owner-approval |
| SPEC-0264-TSK-0001 | ready | in-progress | #owner-approval |

### Owner approval

On 2026-11-06 the owner approved the Spec, Plan and Task in the pull request
("SPEC-0264(Spec·Plan·Task 초안) 승인") and assigned the live observation to
the controller ("머지한 뒤 새 Claude 세션과 새 Codex 세션을 각각 repo root에서
시작은 니가 한다").

### Live observation (criterion 8)

After merge, the controller starts a new Claude session and a new Codex
session at the repository root, reads or edits a file under `infra/` in each,
and records whether the "Folder guide `infra/AGENTS.md`" context appears once.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1, 2, 3, 4, 5 | W1 | folder guide tests | `python -m unittest tests.lib.hooks.test_folder_guides` | PASS | 8 tests OK | required | - |
| E2 | 1, 4 | W1 | hook suites | `test_folder_guides test_tool_payload test_agent_governance_ci_routing test_script_manifest test_validator_entrypoints` | PASS | 162 tests OK | required | - |
| E3 | 1 | W1 | script manifest | `check-script-manifest.py` | PASS | manifest valid | required | - |
| E4 | 6 | W2 | provider surfaces | `provider_surface_renderer.py --check` | PASS | drift=0 | required | - |
| E5 | 7 | W3 | agent governance | `check-agent-governance-contract.py --mode repository` | PASS | exit 0 | required | - |
| E6 | 1, 2, 3, 4, 5 | W1 | folder guide tests | `python -m unittest tests.lib.hooks.test_folder_guides` at `a3695644a`, after the security review fixes | PASS | 15 tests OK, including untracked, symlinked, unreadable, subagent and denied-then-allowed cases | required | - |
| E7 | 1, 4 | W1 | hook suites | `test_folder_guides test_tool_payload test_agent_governance_ci_routing test_script_manifest test_validator_entrypoints test_ci_gate_adapters` at `a3695644a` | PASS | 209 tests OK | required | - |
| E8 | 1, 4, 5 | W1 | security review | `security-auditor` review of the hook diff, then a scoped re-review of the fix commit `c1648d5fa` | PASS | round 1 CHANGES_REQUIRED (F1-F8); round 2 APPROVED; two Low follow-ups fixed in `a3695644a` | required | - |
| E9 | 1 | W1 | manifest, surfaces, contract | `check-script-manifest.py`, `provider_surface_renderer.py --check`, `check-agent-governance-contract.py --mode repository` at `a3695644a` | PASS | manifest valid; drift=0; failures=0 | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E1, E2, E6, E7, E8, E9 | owner acceptance | @buenhyden |
| 2 | pending | E1, E6 | owner acceptance | @buenhyden |
| 3 | pending | E1, E6 | owner acceptance | @buenhyden |
| 4 | pending | E1, E2, E6, E7, E8 | owner acceptance | @buenhyden |
| 5 | pending | E1, E6, E8 | owner acceptance | @buenhyden |
| 6 | pending | E4 | owner acceptance | @buenhyden |
| 7 | pending | E5 | owner acceptance | @buenhyden |
| 8 | pending | - | live observation runs after merge (#live-observation-criterion-8) | @buenhyden |

## Review and Completion

Open: criterion 8 needs the owner step. A Codex shell read does not trigger
delivery, and native delivery in a live session is not yet observed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
