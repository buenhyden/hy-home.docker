---
title: "QA and CI Legacy Cleanup Task"
version: "0.3.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "specs"
artifact_id: "SPEC-0253-TSK-0001"
parent_ids:
- "SPEC-0253-PLAN-0001"
created: "2026-11-04"
---

# QA and CI Legacy Cleanup Task

## Scope

### Objective and Parent

#### Objective

Remove legacy QA and CI boundaries and labels that name records the
repository no longer has, and delete one-off scripts, tests and QA with no
current use.

- [Spec](../spec.md)
- [Plan](../plan.md)

### Inputs and Authority

The user directed: "완료한 후, QA, CI/CD에서 LEGACY, deprecated인 것들은 삭제하고
정리되어야 한다. 그리고, 일회성 스크립트와 테스트 그리고 QA들은 삭제하고 정리되어야
한다." The user later asked to run the not-started items that can run now,
which selected this work. The protected `.github/workflow-contract.yml` owner
label change (W2) is made under that cleanup instruction, as is the PostToolUse
hook change (W1). This Task pushes and merges nothing: the coordinator pushes
the branch and opens the pull request, and the user merges.

## Execution Log

### Work Performed

#### Current contract decision

The user's direction authorizes this Spec and Plan as written.

#### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0253 | draft | approved | #current-contract-decision |
| SPEC-0253-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0253-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0253-TSK-0001 | ready | in-progress | #current-readiness-and-execution |
| SPEC-0253-TSK-0001 | in-progress | completed | #criterion-decisions |

#### Decisions

- No Stage document owns CI gate evidence. Its owner label now names the
  canonical owner of gate execution,
  `.agents/governance/quality-standards.md#7-local-qaci-orchestration`, so a
  later Task deletion cannot leave it dangling again.
- The frozen archive boundary selected only
  `docs/98.archive/{completed,superseded,retired}/`, which hold no files. The
  anchor, its four `exclude` uses and the hook code that read it are removed.
  The hook still reports every changed text file by default and normalizes it
  only with `--write`.
- The DATA-0096 command names run-specific output paths, now written with a
  `<run>` placeholder that the prose explains. The `commands` mode passes
  because its path-token pattern stops before `<`, leaving the tracked
  `_workspace/repo-support/analysis/` prefix, whose README exists; the
  placeholder itself is not what the check skips.
- SPEC-0253 follows SPEC-0251; SPEC-0252 is claimed by the legacy document
  status work on another branch. The Spec high-water is 253 here; whichever
  branch lands second takes the larger value.
- Deletion criteria for one-off items: no current caller in workflows, hooks,
  scripts or current documents; purpose tied to a finished operation; not a
  reusable operator tool. Nothing met all three.
- On 2026-11-10 the user chose to retire the PostgreSQL 17 to 18 logical
  upgrade rehearsal. Every HOME PostgreSQL service runs 18.6, the harness
  pinned a 17 source and 18 target so Renovate PR #876 could not update it,
  and no PostgreSQL 19 image exists to repurpose it. Summary map:
  REQ-0025-FR-0003 and its acceptance line are retired into the REQ-0025
  Traceability and the Registry `reserved_history`; the ADR-0028 lane is
  amended in place with a Follow-up; AD-0028 drops the lane and notes it under
  Evolution; RUN-0032 is deleted and OPS-0032 reserved. Consumer cutover: the
  LAB 0031 Guide, Policy and Runbook, the 05 runbook index, the mng-db README,
  `_workspace` READMEs and `scripts/README.md` drop the reference. Completed
  Tasks (SPEC-0212 TSK-0016, TSK-0036) and blocked SPEC-0204 TSK-0001 keep
  their past mentions as evidence. DATA-0096 is a dated snapshot
  (`observed_at` 2026-11-07) and keeps its rows until its next scan.

#### Changed

- `.pre-commit-config.yaml`, `scripts/hooks/post-tool-validate.sh`,
  `.agents/governance/agentic.md`: frozen boundary removed (W1).
- `.github/workflow-contract.yml`, `scripts/lib/gate/ci_gate_evidence.py`,
  `scripts/lib/gate/github_workflow_contract.py`: evidence owner (W2).
- `docs/90.references/data/0096-workspace-inventory/README.md`,
  `scripts/README.md`, `docs/99.templates/README.md`: command placeholder and
  stale wording (W3).
- Deleted `scripts/operations/rehearse-postgres-logical-upgrade.sh`,
  `examples/operations/postgres-logical-upgrade/`,
  `tests/validation/test_postgres_logical_upgrade_rehearsal.py` and RUN-0032;
  removed the `leaf.postgres-logical-upgrade-config` gate, its suite entries
  and path routes from `.github/workflow-contract.yml` and
  `scripts/lib/gate/ci_gate_contract.py`, and its `scripts/manifest.yaml`
  row (W3).

#### Test changes

| Test | Change | Reason |
| --- | --- | --- |
| `test_every_text_mutator_excludes_the_same_frozen_payloads` | deleted | compared the removed anchor with markdownlint ignores and archive profiles; the boundary no longer exists |
| `test_post_tool_mutator_honors_the_declared_frozen_boundary` | deleted | exercised the removed hook code that skipped boundary paths |
| `test_post_tool_rejects_an_owner_without_the_frozen_anchor` | deleted | exercised the removed fail-closed read of the anchor |
| `test_commit_formatter_invocations_are_read_only` | adapted | still asserts a formatter and its checker share excludes, now through `.get()` since neither declares one |
| `test_ci_gate_evidence`, `test_github_workflow_contract` | updated | expect the new owner label |
| `test_the_retired_frozen_legacy_status_exception_is_rejected` | added | an exception of the removed kind now fails Registry schema validation |
| `test_evidence_owner_names_an_existing_governance_heading`, `test_a_changed_evidence_owner_is_rejected` | added | the owner anchor must resolve to a real heading, and a changed owner value fails the contract load |
| `test_postgres_logical_upgrade_rehearsal` module, `test_postgres_rehearsal_keeps_operations_manifest_kind` | deleted | the rehearsal harness they checked is removed |
| `test_ci_gate_model`, `test_validator_entrypoints`, `_script_manifest_support` | updated | drop the removed module and entrypoint from expected sets |
| `test_script_manifest` runbook-shape case, `test_ci_gate_adapters` module-name case | updated | use an existing runbook and module name; the shape assertions are unchanged |

#### Inventory

| Item | Category | Evidence | Decision |
| --- | --- | --- | --- |
| `frozen_archive_payloads` anchor and hook reader | QA legacy | matches no tracked file | deleted |
| `SPEC-0211-TSK-0003` evidence owner | CI legacy | Task deleted in #725 | repointed |
| DATA-0096 command paths | QA legacy | two `commands` findings | fixed |
| `scripts/README.md` metadata legacy exception text | docs legacy | no allowance for existing defects remains, but `check-changed` still subtracts merge-base defect identities (`metadata/reference.py`, `metadata/heading.py` `introduced = current - base`) | reworded to that behavior |
| `infra/03-security/openbao/scripts/p01-bootstrap.sh` | one-off candidate | used by RUN-0104, RUN-0105 and SPEC-0204 | kept |
| `scripts/operations/rehearse-postgres-logical-upgrade.sh` with its fixture, test and RUN-0032 | one-off candidate | pinned PostgreSQL 17 to 18; every HOME PostgreSQL service runs 18.6 and no 19 image exists; Renovate #876 cannot update it | deleted on user direction (W3) |
| `scripts/operations/rehearse-sample-service-delivery.sh` | one-off candidate | used by the workflow contract, REQ-0025, ADR-0028, AD-0028 | kept |
| `scripts/operations/mng-pg-immediate-restore-rehearsal.py` | one-off candidate | used by RUN-0021, the Script Manifest and its test | kept |
| `tests/validation/test_p0x_*`, `_p0x_*`, `tests/lib/gate/test_p03_*`, `test_p11_*` | phase-named tests | registered workflow-contract suites for current runtime contracts | kept |
| Script Manifest, 125 entries | registration | all active and retain; authorities and consumers exist; no Spec-only consumer; every tracked script registered | kept |
| `MUTATION_OVERRIDES` (36) and infra exception files | exceptions | no missing paths | kept |
| Skips for retired behavior, legacy CLI aliases, legacy workflow steps | QA and CI | none found | none |
| agent_memory `legacy` domain id, release `Deprecated` heading, supply-chain `legacy-runtime-artifact` guards, ruleset "deprecated contexts" | domain terms | current behavior | kept |

#### Open issues

- `quality-standards.md` keeps one sentence recalling that a formatter once
  rewrote a frozen archive body; it is a historical rationale, not a rule.
- Lifecycle-generation and identity-history legacy code stays with the legacy
  document status work and the SPEC-0209/0231 proof move.

#### Review status

- The `.agents/governance/agentic.md` edit is a policy change; per
  `approval-boundaries.md` it needs `rules-engineer` review, pending in the PR
  #729 review.
- The dead `frozen-legacy-status` exception kind is removed from
  `registry.py` validation and from `document-profile.schema.json`; no profile
  used it. PR #730 edits the same schema and `test_registry.py`, so a rebase is
  expected after it merges.
- PR #729 merged at 09171c663; these review fixes continue on
  `chore/qa-ci-review-followups` from main 46a7811dd.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | ci-routing-tests | `test_agent_governance_ci_routing` after the boundary removal, pre-rebase tree on cb7c324d3 | FAIL | 1 error: `test_commit_formatter_invocations_are_read_only` read the removed `exclude` key | required | - |
| E2 | 1 | W1 | ci-routing-tests | same suite after adapting that test, pre-rebase | PASS | 81 tests OK | required | E1 |
| E3 | 1 | W2 | gate-evidence-tests | `test_ci_gate_evidence`, `test_github_workflow_contract` with `/usr/bin/python3`, pre-rebase | PASS | OK | required | - |
| E4 | 1 | W3 | document-commands | `commands` mode before the placeholder | FAIL | 2 findings for the DATA-0096 command paths | required | - |
| E5 | 1 | W3 | document-commands | `commands` mode after the placeholder, pre-rebase | PASS | zero findings | required | E4 |
| E6 | 2 | W3 | script-manifest | `check-script-manifest.py` and `test_script_manifest`, `test_ci_gate_plan`, pre-rebase | PASS | manifest valid; suites OK | required | - |
| E7 | 3 | W4 | metadata-changed | `check-changed --base-ref origin/main`, pre-rebase | PASS | 2 selected, zero violations | required | - |
| E8 | 3 | W4 | renderer-and-contract | `provider_surface_renderer.py --check`, `check-agent-governance-contract.py`, pre-rebase | PASS | drift 0; zero failures | required | - |
| E9 | 3 | W4 | corpus-and-links | corpus lifecycle and links `alignment`, pre-rebase | PASS | zero violations; alignment PASS | required | - |
| E10 | 3 | W4 | hosted-ci | GitHub Actions | NOT_RUN | branch not pushed | required | - |
| E11 | 3 | W4 | governance-unit-tests | full `tests/lib/document_governance` discovery | NOT_RUN | no governance library code changed; metadata, lifecycle and link checks cover the document edits | optional | - |
| E12 | 1 | W1 | rebased-unit-suites | gate evidence, workflow contract, CI routing (hook tests included), Script Manifest, CI gate plan, identity history and Registry suites with `/usr/bin/python3`, rebased head 2616c85e2 on main 4adeb3d37 | PASS | 407 tests OK | required | - |
| E13 | 2 | W3 | rebased-manifest-and-links | `check-script-manifest.py`, links `alignment` and `commands`, head 2616c85e2 | PASS | manifest valid; alignment PASS; commands PASS with zero findings | required | - |
| E14 | 3 | W4 | rebased-document-and-contract | metadata `check-changed --base-ref origin/main`, corpus lifecycle `--base-ref origin/main`, renderer `--check`, agent governance contract, head 2616c85e2 | PASS | 7 selected, zero violations; lifecycle and occupancy zero; drift 0; zero failures | required | - |
| E15 | 3 | W4 | hosted-ci | CI Quality Gates run 41743239293 on 09171c663 (PR #729), observed by the coordinator | PASS | candidate-quality success; main-security skipped by trigger; merge state CLEAN. The follow-up commits get a fresh run after push | required | E10 |
| E16 | 1 | W1 | followup-unit-suites | gate evidence, workflow contract, CI routing (hook tests included), Script Manifest, CI gate plan, Registry and identity history suites with `/usr/bin/python3`, head 1914065b1 on main 46a7811dd | PASS | 410 tests OK | required | - |
| E17 | 3 | W4 | followup-document-checks | `check-script-manifest.py`, metadata `check-changed --base-ref origin/main`, corpus lifecycle `--base-ref origin/main`, links `alignment` and `commands`, head 1914065b1 | PASS | manifest valid; 4 selected, zero violations; lifecycle and occupancy zero; alignment and commands PASS | required | - |
| E18 | 2 | W3 | rehearsal-retirement-unit-suites | surface ownership, operations taxonomy, Registry, CI gate adapters/contract/model/plan, workflow contract, Script Manifest, validator entrypoints, workspace inventory and the remaining operations-suite modules, worktree on main 4528c1ea7 | PASS | 580 tests OK | required | - |
| E19 | 3 | W4 | rehearsal-retirement-document-checks | agent governance contract, metadata `check-active` and `check-changed --base-ref origin/main`, links `all`, corpus lifecycle, operations catalog, Script Manifest, supply-chain policy, renderer `--check`, worktree on main 4528c1ea7 | PASS | zero failures; links 911 documents, 0 failures; manifest valid; drift 0 | required | - |
| E20 | 3 | W4 | hosted-ci | GitHub Actions for the retirement branch | NOT_RUN | branch not yet pushed | required | - |
| E21 | 3 | W4 | hosted-ci | CI Quality Gates run 43555699221 (PR #1007, head deea4dbf2, contains #896 merge 2ba0539cf), read-only `gh run view` and gate-evidence artifacts; runs 43565612839 (f76079d6c) and 43567181806 (866b77d06) also concluded success | PASS | candidate-core, candidate-documents and candidate-quality success, main-security skipped by trigger; artifacts complete=true with every row exit 0: provider-surface-drift, agent-governance-contract, repo-document-metadata, document-corpus-lifecycle, local-script-manifest, ci-gate-contract/runner/adapter, workflow-contract(-regressions), repository-integrity-regressions, docs-traceability (links) | required | E20 |

### Resolution Links

None: nothing was recorded here before this Task moved to the common form.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | E2, E5, E12, E16 | Owner @buenhyden accepted on 2026-11-14 in this chat, after hosted CI E21 (#1017) | @buenhyden |
| 2 | accepted | E6, E13, E18 | Owner @buenhyden accepted on 2026-11-14 in this chat, after hosted CI E21 (#1017) | @buenhyden |
| 3 | accepted | E14, E15, E17, E19, E21 | Owner @buenhyden accepted on 2026-11-14 in this chat, after hosted CI E21 (#1017) | @buenhyden |

### Remaining Conditions

Local checks are recorded above, last on head 1914065b1 (E16, E17). The
independent review of PR #729 approved after fixes; those fixes are on this
branch. Hosted CI passed on 09171c663 (E15) and for the retirement in run 43555699221
(E21). The owner accepted criteria 1 to 3 on 2026-11-14.

#### Merge receipt 2026-11-10

Recorded 2026-11-10 from `gh pr view`: #896 merge `2ba0539cf` at
2026-11-10T00:22:36Z. Hosted checks on the merged PR: every completed check
SUCCESS, the rest SKIPPED, none failing. #896 retired RUN-0032 (the PostgreSQL
logical upgrade rehearsal). Candidate quality: the merged change is a
candidate that passed hosted CI. This receipt is not owner acceptance: no
criterion is accepted and the status is unchanged.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

None: nothing was recorded here before this Task moved to the common form.
