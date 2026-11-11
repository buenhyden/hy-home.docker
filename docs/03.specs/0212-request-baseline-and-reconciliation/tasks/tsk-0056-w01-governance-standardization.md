---
title: "W01 Governance Standardization Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0056"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W01 Governance Standardization Task

## Overview

### Objective

Own W114/criterion 109. Assess the v14.2 W01 obligations GOV-01 to GOV-08 and
SUP-12 against their canonical owners in this workspace. Correct only the gaps
this Task reproduces, and record local adoption separately from any
cross-repository adoption.

## Inputs and Authorization

On 2026-11-11 the owner merged PR 953, which completed the W00 intake in
TSK-0053. The owner then approved a new SPEC-0212 Task to own W01. The v14.2
package under `_workspace/workspace_execution_tasks/` (prompt
`tasks/TASK-hy-home-docker-W01.md`) is untrusted reference data, not an
instruction source or an authority.

The authorization covers local assessment, repository-side corrections of
reproduced gaps, and synthetic verification. Cross-repository adoption
(GOV-04 under D-04), protected-branch rules, remote settings and the user-global
Codex hook trust stay separate owner decisions. Template and generator work is
handed to W03 and runtime wiring to W07; neither is changed here.

The TSK-0053 assessment at baseline `648a78a26` is the prior observation:
GOV-01, 02, 03, 05, 06 and 08 KEEP; GOV-04 DEFER; GOV-07 CHANGE (done). This
Task re-checks those at the current `main` `0a726ee1c` before reusing them.

## Work Log

### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no operation outside the stated boundary.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0056 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0056 | ready | in-progress | #owner-approved-local-execution |

### W01 obligation assessment 2026-11-11

A fresh-context `rules-engineer` read the canonical owners at `main`
`0a726ee1c`, and the controller spot-checked the deciding lines. KEEP cites
the operative current sentence, not a heading.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| GOV-01 | KEEP | `sdlc.md` owns Task execution state, approval separate from acceptance, and visible failures; Registry `lifecycles` own family states |
| GOV-02 | KEEP | `bootstrap.md` limits the Provider Registry to translation; provider adapters own syntax only |
| GOV-03 | KEEP | Registry frontmatter rules enforced by `check-document-metadata.py`; `approval-boundaries.md` says a record is not an authenticator |
| GOV-04 | KEEP local, DEFER cross-repo | `approval-boundaries.md` separates shared approval from each repository's own adoption; compatibility windows across repositories are out of scope under D-04 |
| GOV-05 | KEEP | `github-governance.md`: one person's review is never two approvals, and an App or signature never stands in for owner acceptance |
| GOV-06 | GAP, CHANGE | Generated copies pass `provider_surface_renderer.py --check` (drift 0), but five rules were hand-authored in several policies (D1 to D5 below) |
| GOV-07 | GAP, CHANGE | Only a retry was barred from weakening a Gate; no general rule covered a code-rule contradiction |
| GOV-08 | KEEP | `approval-boundaries.md` reuses approval inside an approved scope, keeps secret reads separate, and has static deny-rule tests; runtime enforcement UNVERIFIED |
| SUP-12 | KEEP | `approval-boundaries.md`: this repository never decides or records adoption for another |

GOV-06 duplicates, each now with one owner and links from the others:

- D1, Stage 98: the documentation protocol owns its content and the quality
  standards own its check inventory.
- D2, batch deletion approval: owned by the SDLC sequence, which now also
  carries each package's criterion state.
- D3, `reserved_history` at retirement: owned by the documentation protocol
  retirement preconditions.
- D4, approval reuse: owned by approval boundaries.
- D5, lifecycle state lists: owned by the Registry `lifecycles`. The SDLC
  keeps only the Stage 01-03 rule that is not in the Registry.

`workflows.md` keeps its delegation-scope refinement, because it adds meaning
rather than repeating it. Commit `c66c792a6` makes these changes and adds the
GOV-07 rule to the quality standards. Review answer `55ce3e362` restores the
README-check wording, names the rule owner's approval for changing a rule,
and routes the checklist's `not-required` restatement to the SDLC.

The v14.2 W01 common contract fields (`contract_id`, `approved_by` and the
rest) and Project-Template as the authoring source are cross-repository
adoption. They stay DEFER under GOV-04 and D-04, and no schema is added here.
W01-B is KEEP: no record, check result or role string counts as approval.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W01 obligation assessment | 109 | W114 | governance-owner-assessment | GOV-01 to GOV-08 and SUP-12 at main `0a726ee1c` | NOT_RUN | Assessment not yet run | required | - |
| W01 obligation assessment result | 109 | W114 | governance-owner-assessment | GOV-01 to GOV-08 and SUP-12 at main `0a726ee1c` | PASS | Per-ID table above: seven KEEP, GOV-06 and GOV-07 GAP fixed, GOV-04 cross-repo DEFER | required | W01 obligation assessment |
| W01 governance checks | 109 | W114 | governance-contract-and-documents | Commits `c66c792a6` and `55ce3e362` | PASS | agent governance contract PASS; renderer drift 0; metadata selected8 violations0; links alignment and commands PASS; test_agent_governance_ci_routing and test_registry OK | required | - |
| W01 governance review | 109 | W114 | independent-document-review | Fresh-context rules-engineer of `c66c792a6` | FAIL | CHANGES_REQUIRED for the Stage 98 README wording; obligations, anchors and the state-list removal otherwise verified | required | - |
| W01 governance re-review | 109 | W114 | independent-document-review | Scoped rules-engineer re-review of `55ce3e362` | PASS | RESOLVED: Stage 98 wording, rule-owner approval sentence and checklist link verified; anchors resolve; no new finding | required | W01 governance review |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 109 | accepted | W01 obligation assessment result, W01 governance checks, W01 governance re-review | Owner accepted on 2026-11-11 in this chat; GOV-04 cross-repository adoption stays DEFER under D-04 | SPEC-0212 TSK-0056 |

## Review and Completion

In progress. The owner accepted criterion 109 on 2026-11-11. GOV-04
cross-repository adoption and GOV-08 runtime enforcement stay recorded as
DEFER and UNVERIFIED; the Task stays open until the owner closes it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W00 intake](tsk-0053-master-workspace-reconciliation.md)
