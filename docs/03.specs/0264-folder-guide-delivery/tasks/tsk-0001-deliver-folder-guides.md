---
title: "Folder Guide Delivery Task"
version: "0.3.0"
type: "sdlc/task"
status: "blocked"
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

Record the execution and evidence of work units W1 to W5 of the Plan.

## Inputs and Authorization

The owner requested the change on 2026-11-06 and chose one shared hook over
folder `CLAUDE.md` shims, then amended that choice the same day to a shim for
Claude and the hook for Codex (#owner-amendment). Spec approval is the
owner's, in the pull request.

## Work Log

### Implementation

W1 to W3 are implemented on `feat/folder-agents-guide-hook`:
`scripts/lib/hooks/folder_guides.py`, the dispatcher wiring, 8 tests, the
manifest entry, `.claude/provider.md` 1.6.0, `.codex/provider.md` 1.5.0 and the
audit of the 10 `AGENTS.md` files.

W5 is implemented in the working tree on top of `eef26df01`, not yet
committed. `scripts/operations/provider_surface_renderer.py` renders
`<folder>/CLAUDE.md` (marker comment, blank line, `@AGENTS.md`) beside each of
the 9 Git-tracked folder guides, reports a stale shim, and refuses to
overwrite a folder `CLAUDE.md` without its marker. The Stage 01, 02, 03, 05
and 90 loaders, the trusted Requirement snapshot, the navigation check and
`scripts/manifest.yaml` admit the shim. `documentation-protocol.md` 3.10.0,
`.claude/provider.md` 1.7.0, `.codex/provider.md` 1.6.0 and
`scripts/AGENTS.md` 0.2.2 describe it. The hook change that stops sending
guide content to Claude is made in parallel in `folder_guides.py`,
`agent-event-hook.sh` and `test_folder_guides.py` and is not recorded here.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0264 | draft | approved | #owner-approval |
| SPEC-0264-PLAN-0001 | draft | approved | #owner-approval |
| SPEC-0264-TSK-0001 | draft | ready | #owner-approval |
| SPEC-0264-TSK-0001 | ready | in-progress | #owner-approval |
| SPEC-0264 | approved | in-review | #owner-amendment |
| SPEC-0264-PLAN-0001 | approved | in-review | #owner-amendment |
| SPEC-0264-TSK-0001 | in-progress | blocked | #owner-amendment |

### Owner approval

On 2026-11-06 the owner approved the Spec, Plan and Task in the pull request
("SPEC-0264(Spec·Plan·Task 초안) 승인") and assigned the live observation to
the controller ("머지한 뒤 새 Claude 세션과 새 Codex 세션을 각각 repo root에서
시작은 니가 한다").

### Owner amendment

On 2026-11-06, after approving the hook-only design, the owner chose a folder
`CLAUDE.md` shim for Claude and the hook for Codex ("Claude는 shim, Codex는
hook"). The Spec and Plan return to `in-review` for that amendment, and this
Task stays `blocked` until the owner approves them again.

### Live observation (criterion 8)

After merge, the controller starts a new Claude session and a new Codex
session at the repository root. In Claude it reads a file under `infra/` and
records whether `infra/CLAUDE.md` loads with `infra/AGENTS.md`; in Codex it
edits a file under `infra/` and records whether the "Folder guide
`infra/AGENTS.md`" context appears once.

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
| E10 | 9 | W5 | renderer shim tests | `python -m unittest tests.validation.test_validator_entrypoints` on the W5 working tree | PASS | 8 tests OK, including shim create, drift, stale retirement and hand-written refusal | required | - |
| E11 | 9 | W5 | provider surfaces | `provider_surface_renderer.py --write`, then `--check`, on the W5 working tree | PASS | 9 shims written; drift=0 | required | - |
| E12 | 10 | W5 | document metadata | `check-document-metadata.py --mode check-active` and `--mode check-changed --base-ref origin/main` on the W5 working tree | PASS | violations=0 in both modes | required | - |
| E13 | 10 | W5 | links and contract | `check-document-links.py --mode alignment`, `check-agent-governance-contract.py --mode repository` on the W5 working tree | PASS | failures=0; failures=0 | required | - |
| E14 | 10 | W5 | script manifest | `check-script-manifest.py` on the W5 working tree | FAIL | `path-untracked scripts/CLAUDE.md`: the shims are not yet staged | required | - |
| E15 | 10 | W5 | script manifest | `check-script-manifest.py` with the 9 shims added to its tracked-path set in process | PASS | manifest valid | optional | - |
| E16 | 10 | W5 | suites | `tests.validation.test_agent_governance_ci_routing`, `tests.lib.document_governance.test_spec_packages` on the W5 working tree | FAIL | 172 tests, 1 failure: `test_static_checks_stop_descendants_after_parent_exit` (docker descendant survived), run beside other heavy checks | required | - |
| E17 | 1 | W5 | native shim load | Headless Claude Code 2.1.319 in a throwaway repository with root `CLAUDE.md`, `sub/CLAUDE.md` holding the marker comment then `@AGENTS.md`, and only `sub/data.txt` read | PASS | the `sub/AGENTS.md` codeword was answered; the trace shows one Read of `sub/data.txt` | optional | - |
| E18 | 10 | W5 | suites | `test_static_checks_stop_descendants_after_parent_exit` rerun alone on the W5 working tree | PASS | 1 test OK; the E16 failure is a timing failure unrelated to W5 | required | E16 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E1, E2, E6, E7, E8, E9, E17 | owner acceptance | @buenhyden |
| 2 | pending | E1, E6 | owner acceptance | @buenhyden |
| 3 | pending | E1, E6 | owner acceptance | @buenhyden |
| 4 | pending | E1, E2, E6, E7, E8 | owner acceptance | @buenhyden |
| 5 | pending | E1, E6, E8 | owner acceptance | @buenhyden |
| 6 | pending | E4 | owner acceptance | @buenhyden |
| 7 | pending | E5 | owner acceptance | @buenhyden |
| 8 | pending | - | live observation runs after merge (#live-observation-criterion-8) | @buenhyden |
| 9 | pending | E10, E11 | owner acceptance | @buenhyden |
| 10 | pending | E12, E13, E14, E15, E16, E18 | owner acceptance; E14 stays open until a PASS after the shims are staged | @buenhyden |

## Review and Completion

Open: the owner must approve the amended Spec and Plan before this Task
resumes. Criterion 8 needs the owner step, and E14 needs a PASS once the
shims are staged. A Codex shell read does not trigger delivery, and native
delivery in a live session of this repository is not yet observed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
