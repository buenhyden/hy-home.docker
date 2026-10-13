---
title: "Task Lifecycle Generation 6 Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0231-TSK-0001"
parent_ids:
- "SPEC-0231-PLAN-0001"
created: "2026-10-13"
---

# Task Lifecycle Generation 6 Task

## Objective

Give execution state, acceptance and archive readiness one owner each, as
SPEC-0231 states, and move the active Stage 03 corpus to that contract.

## Inputs and Authorization

On 2026-10-13 the owner asked to proceed with the Task status structure
change (prompt v9 findings F03 and F06) and chose, when asked: Spec and Plan
keep authority statuses only; acceptance moves to a per-criterion table; the
multi-item Task mode is included now. The prompt v9 request authorizes
repository source, test, document and governance changes, logical commits,
the branch push, its pull request and per-Spec integration. Baseline `main`
`2a57d4122`. Archive approval is not part of this request.

## Work Log

### Starting State

Read on `2a57d4122`:

- `docs/99.templates/registry.json` sets `lifecycle_generation` 5. The `spec`
  and `plan` lifecycles include `in-progress`, `blocked` and `completed`, and
  `_validate_execution_states` in `spec_packages.py` makes them project Task
  execution.
- `_v5_evidence_contract` reads the eight-column Evidence table and treats a
  `PASS` and `accepted` row as closing its criterion and Work Unit pair. A
  `FAIL` row with `pending` acceptance blocks nothing.
- `_validate_completion_evidence` runs only for a `completed` Spec and
  requires a `completed` Plan; `archive.validate_active_stage_occupancy`
  lets a package wait in Stage 03 only with a `completed` Spec and Plan.
- Generation 4 already had per-row item status and a per-criterion review
  table; generation 5 folded both into the Evidence row.
- The generation migration proof and `_generation_normalizations` are
  written for generations 4 and 5 only.
- Corpus: 52 Tasks (draft 23, completed 16, in-progress 10, blocked 3), 44
  of them with the eight-column table; 8 completed Tasks are generation 4
  historical bodies. Spec and Plan: draft 18, completed 4, in-progress 3,
  blocked 1 each.

### W1 Contract

The Registry sets `lifecycle_generation` 6 and `contract_id`
`SDLC-COMMON-v5`, ends `evidence_columns` in `Resolves`, adds
`criterion_acceptance_section`, `criterion_acceptance_columns` and
`execution_items`, gives the `spec` and `plan` lifecycles the authority
statuses only, adds the Criterion Acceptance section to the Task profile,
declares the six Spec and Plan normalizations to `approved`, and lets an
`approved` Spec or Plan enter disposition. The profile schema and
`registry.py` check the generation 6 values exactly and keep the generation 5
values for generation 5 Registries, which are still validated at their own
revisions. `validate_registry` returns no finding. The Task template carries
the new Evidence header, the Criterion Acceptance table and author prompts
for both Task modes.

### W2 Reader

`spec_packages.py` gains `_validate_parent_authority`, `_execution_item_rows`,
`_v6_evidence_contract`, `PackageEvidence` and `archive_readiness_findings`.
The generation 5 historical admission moved unchanged into
`_v5_historical_admission`; `_v6_historical_admission` adds every terminal
Task whose bytes equal the generation 6 source and reads a generation 5 Task's
closed pairs from its own PASS and accepted rows. The repository transition
check accepts generation 6, reads its normalizations from the Registry, and a
generation 5 reconciliation receipt stays readable when its target was
normalized. Preserved packages still parse with the statuses generation 6
normalized away; current packages are held to the new lifecycle. The metadata
check stops requiring `status` for a Task with an Execution Items table and
reports one that is declared.

`tests/lib/document_governance/test_generation6.py` pins each rule with a
passing and a failing case (18 tests). They were written after the code, so
their RED state on `2a57d4122` is only that the functions do not exist; the
item-status rule below has a real RED.

### W3 Readiness

Under generation 6 a package leaves Stage 03 for the completed archive only
when `archive_readiness_findings` was empty on its base revision; each loaded
package carries the evidence the predicate reads. Stage 03 occupancy keeps its
consistency checks and needs no readiness. Stage 03 has no archive hold
source, so the Spec's hold clause was dropped.

### W4 Migration

A one-off helper outside the repository rewrote the 37 nonterminal Tasks:
`Acceptance` became `Resolves`; a later `PASS` on the same Work Unit with a
shared criterion resolved 32 earlier `FAIL` rows and 12 stayed unresolved;
12 duplicate Evidence names got a numeric suffix; each criterion's decision
went to the lowest-numbered Task carrying evidence for it: 79 `accepted`, 3
`rejected`, 49 `pending`. Eight Spec and Plan pairs moved to `approved` (4
`completed`, 3 `in-progress`, 1 `blocked`). The 16 terminal Tasks (8
generation 4 and 8 generation 5) are byte-identical and load as historical.
All 27 packages load; SPEC-0208, 0209, 0210 and 0212, the four formerly
`completed` packages, are ready for archive review and the others list what
is open.

Before merge the migration proof cannot find its integration merge, so the
repository checks run on a synthetic `--no-ff` merge of this branch into
`origin/main`, the shape `candidate-quality` checks out. There the metadata
check reports no violation.

A branch that still writes the generation 5 Evidence (the P01 branches edit
SPEC-0204 TSK-0006) must, after rebasing, rename the last Evidence header
cell to `Resolves`, write `-` or the resolved FAIL row names in it, and add
the Criterion Acceptance section.

### W5 Text and Review

SDLC states the generation 6 rules once; the documentation protocol,
checklist, templates and READMEs route to it. REQ-0026-FR-0009 and its
acceptance criterion and AD-0030 state the new waiting rule, and ADR-0048
(proposed) replaces ADR-0037 decisions 1 to 3 without editing that accepted
ADR. The empty and repeated `### Usage` headings in the Stage 01, 02 and 03
READMEs became `### Audience` and `### Authoring Flow`.

An independent read-only `rules-engineer` review returned four blocking and
ten other findings. Fixed: documentation protocol item 14 (B1); restated
readiness copies now link to SDLC (B2); hold clause (B3); REQ-0026, AD-0030
and ADR-0048 (B4); completion wording (N1); a running item hidden by a
blocked summary now fails parent approval, a test that failed before the fix
(N2); terminal-parent wording (N3); package-completion wording in SDLC, the
protocol's checklist sentence and the Stage 03 README (N4); `not-required`
closure (N6); restated acceptance in the templates README (N7) and status
list in the Stage 03 README (N8); template prompts (N9). Not changed: the
branch-integration receipt section's "atomic completion" wording (N4, its own
flow), promotion receipt placement (N5), and the handoff prompt's section
names (N10, unrelated).

### Test Suite

On the synthetic merge at the W3 commit the document governance suite ran
876 tests with 8 failures. Five were generation 5 fixtures and were moved:
two lifecycle tests and the generation 5 table test now read the generation 5
snapshot at `2a57d4122`, the fragmented-evidence fixture uses approved parents
and the generation 6 tables, and the identity fixture uses `in-review` to
`approved`. The three remaining failures,
`test_tombstone_identity_inherits_the_retired_artifact_id`, fail the same way
on unchanged `2a57d4122` and are not part of this change.

### W6 Gate

After rebasing onto `e931417be` the branch was merged with `--no-ff` into
`origin/main` as `d28b15c1c`. There the metadata check selected 68 documents
with no violation and no archive finding. The changed gate passed the active
and changed metadata checks, the candidate preflight, the corpus lifecycle
check (0 violations), archive recovery (0 violations) and the 15-, 15- and
148-test suites, then hit the local 3000 s limit inside the document
governance suite and was stopped (exit 124). That suite's local result is
`NOT_RUN`; the hosted `candidate-quality` run on the pull request decides
criterion 6.

Hosted `candidate-quality` on pull request #441 (head `f38fd2ea5`, base
`e931417be`, run 38359942268) passed: governance contract, provider renderer,
metadata check (68 documents, 0 violations), corpus lifecycle and archive
recovery (0 violations), workflow contract, every pre-commit hook and commit
validation. The hosted changed profile runs no unit suite, so the governance
suite on the rebased branch stays `NOT_RUN`; its last full run is the one in
Test Suite.

The owner merged pull request #441 with a merge commit, `ffd201182` (parents
`e931417be` and `f38fd2ea5`), the one first-parent integration the generation
6 proof requires.

### Contract Migration

| Date | Source revision | Evidence |
| --- | --- | --- |
| 2026-10-13 | 2a57d4122dc8dac954afca364b838e4bf97fd44a | #starting-state: generation 5 Registry and corpus read before the migration |


### Governance Suite

The full document governance suite (`python3 -m unittest discover -s
tests/lib/document_governance -t .`) ran with no time limit in a detached
scratch worktree on `b1a6976f4` on 2026-10-13: 894 tests in 1844 s, 893
passed and one failed. `test_registry_high_water_is_not_below_repository_history`
reported `registry high_water=232 observed=234`. That test reads every local
ref (`--all`), and the unmerged local branches for SPEC-0233 and SPEC-0234
already issue Spec numbers 233 and 234. That cause is likely but not yet
verified; the test is rerun once both branches merge.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract | 1 | W1 | `validate_registry`; Registry tests | Branch | PASS | W1 Contract | - |
| Reader | 1, 2 | W2 | `test_generation6` (18); item-status fixture RED then GREEN | Branch | PASS | W2 Reader | - |
| Readiness | 3 | W3 | Corpus readiness listing; preservation gate | Branch | PASS | W3 Readiness | - |
| Migration | 4 | W4 | Corpus load; terminal Task byte identity; metadata check on synthetic merge | Branch on `2a57d4122` | PASS | W4 Migration | - |
| Text | 5 | W5 | Independent rules review; metadata check | Branch | PASS | W5 Text and Review | - |
| Gate | 6 | W6 | Changed gate on synthetic merge; stopped at local 3000 s limit in the governance suite | `d28b15c1c` | NOT_RUN | W6 Gate | - |
| Candidate | 6 | W6 | Hosted `candidate-quality`, changed profile | PR #441 at `f38fd2ea5` | PASS | W6 Gate | - |
| Governance suite | 6 | W6 | Full document governance suite, 893 of 894 passed | `b1a6976f4` | FAIL | Governance Suite | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |
| 6 | pending | - | - |

## Review and Completion

No row is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
