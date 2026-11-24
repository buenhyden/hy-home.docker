---
title: "Workspace Maintenance Follow-up Task"
version: "0.2.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-24"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0097"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-19"
---

# Workspace Maintenance Follow-up Task

## Scope

### Objective and Parent

Own criterion 153 and work unit W169 under the [Spec](../spec.md) and
[Plan](../plan.md): triage CodeQL, settle the test modules that failed in
TSK-0096's run, record the owner's acceptances, and add the workspace
environment and maintenance guides.

### Inputs and Authority

On 2026-11-19, after PR #1124 merged, the owner asked in this chat to check
and handle CodeQL and the nine failing test modules, to accept ADR-0063 and
criterion 152, to close criterion 144 and TSK-0088, to add `05.environment`
and `06.maintenance` and move the RUN-0021 workspace sections, then to commit,
push, open and merge a pull request and bring `dev` and `origin/dev` up to
date. Work is on branch `docs/workspace-maintenance-cutover` from `main` at
`eadd81adc`.

## Execution Log

### Work Performed

#### CodeQL

Eleven alerts were open on `main`. The six `py/redos` alerts (`hook_rules.py`
lines 284 and 285, `test_lab_isolation.py` 246, `test_compose_baseline_gates.py`
5827) were measured with the attack strings CodeQL reported: every pattern
matches in 0.0 s at 20 repetitions, because each repetition starts at a
whitespace boundary and consumes non-whitespace tokens, so no two repetitions
overlap. The five `py/clear-text-storage-sensitive-data` and
`py/weak-sensitive-data-hashing` alerts are test fixtures that write a
synthetic password to a 0600 temporary file or produce the Valkey ACL SHA-256
form the fixture must match. No code changed for them. Dismissing the eleven
alerts through the API was refused by this session's permission classifier,
so they stay open for the owner to dismiss.

#### Test modules

The nine modules that failed in TSK-0096's run imported `jsonschema` without
`referencing` from the system interpreter. `tests/README.md` already requires
the hash-locked venv; with `.venv/bin` first on `PATH` every module passes. No
test or code changed; the new onboarding guide states the requirement.

#### Acceptances

ADR-0063 is accepted, criterion 152 is accepted and TSK-0096 is completed, and
criterion 144 is accepted with TSK-0088 completed through PASS rows on the real
tree that resolve its rehearsal FAIL rows. TSK-0095's ledger follows.

#### Environment and maintenance

`docs/00.workspace/05.environment/onboarding.md` and
`docs/00.workspace/06.maintenance/harness-maintenance.md` use the governance
knowledge form through Registry `additional_paths`. The shared memory, session
capture, analysis, forecast, dispatch and observe sections of RUN-0021 moved to
the maintenance guide in English with unchanged commands and limits. Observe
names the guide as the owner of capture, analysis and dispatch failures, and
the session capture manifest consumer follows it. A new document starts at
`draft`, and the script manifest accepts only an active Operations Runbook as
the runtime authority of a mutating script, so RUN-0021 stays that authority
and names each script until the guide is active.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0097 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0097 | ready | in-progress | #codeql |

### Blockers and Decisions

- The CodeQL dismissals need the owner, or a permission rule that allows them.
- Moving the runtime authority of the workspace scripts to the maintenance
  guide waits for the guide to become active and for the script manifest
  contract to admit a workspace maintenance owner.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ReDoS measurement | 153 | W169 | Reported attack strings at 12, 16 and 20 repetitions against each flagged pattern | `main` at `eadd81adc` | PASS | 0.0 s for every case | required | - |
| Alert dismissal | 153 | W169 | `gh api` PATCH of alerts 46 to 51 and 53 to 57 | GitHub code scanning | NOT_RUN | Refused by the session permission classifier | required | - |
| ReDoS re-check | 153 | W169 | The flagged `hook_rules.py` and `test_lab_isolation.py` patterns against the reported repetitions written with a real 0x7f byte, at 8 to 24 repetitions, plus 3,000 random units at 20 repetitions | `main` at `1b7e76aad`, 2026-11-24 (P16) | PASS | At most 0.2 ms at 80 repetitions; no super-linear growth; 10 alerts open (46-48, 50, 51, 53-57); the earlier `test_compose_baseline_gates.py` alert is gone | required | - |
| Owner dismissal | 153 | W169 | `gh api` PATCH of alerts 46 to 51 and 53 to 57 | GitHub code scanning, run by the owner, 2026-11-24 04:23-04:24 UTC | PASS | Owner `buenhyden` dismissed 46-48, 50 and 51 as false positive and 53-57 as used in tests; 49 had been fixed on 2026-11-20; 0 alerts open | required | Alert dismissal |
| Venv test modules | 153 | W169 | `python3 -m unittest` per module over `tests/lib` and `tests/validation` with `.venv/bin` first on `PATH` | This branch | PASS | 210 of 210 modules after the in-progress records were completed | required | - |
| Document checks | 153 | W169 | links `--mode all` and `--mode alignment`, operations catalog, corpus lifecycle, script manifest, agent governance contract, renderer `--check` | This branch | PASS | All exit 0 | required | - |
| Fenced heading fix | 153 | W169 | `test_open_task_resolves_unnumbered_routes_only_in_evidence_rows` | `47df34c63` and its parent | PASS | FAIL without the fix, OK with it | required | - |

### Resolution Links

None.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 153 | pending | ReDoS measurement, Venv test modules, Document checks, Fenced heading fix | The owner decides; the alert dismissal is still open | @buenhyden |

### Remaining Conditions

The owner dismissed the ten CodeQL alerts on 2026-11-24 (Owner dismissal);
no alert is open. Criterion 153 has no open required row; the owner decides
its acceptance. The maintenance guide is active
(2.8.0); the runtime-authority move is a separate change.

## Handoff

### Promotion Receipt

None yet.

### Next Owner

The owner decides criterion 153.
