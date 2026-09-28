---
title: "Package Disposition Wait and Task Cancellation Execution"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0179-TSK-0001"
parent_ids:
- "SPEC-0179"
- "SPEC-0179-PLAN-0001"
created: "2026-09-17"
---

# Package Disposition Wait and Task Cancellation Execution

## Objective

Record the execution of SPEC-0179, from its review to its completion.

## Inputs

- Operator request of 2026-09-17 to converge the documentation standard, which
  this package takes as its first sub-project.
- Operator approvals of 2026-09-17: the structural disposition wait, the
  structured `cancellation` frontmatter, the design as a whole, one local
  proposal commit, and the Spec.
- Current authorization: on 2026-09-28 the operator superseded the earlier
  per-integration remote restriction and authorized commit, push, protected-main
  PR merge, and cleanup through the Authorized Delivery Route. Integration 1
  records the Spec review edge; three later PRs record approval, activation, and
  completion. Gate-specific authorization also permits Compose environment-based
  validation and ephemeral Conftest container execution and cleanup. Actual
  payload removal, production deployment or service mutation, protection changes,
  and history rewriting remain excluded.
- Historical route approval (2026-09-17): the operator approved a direct push of
  this package's commits to `main` and asked that it be recorded as a rule bypass.
  `.agents/governance/github-governance.md` requires agents to treat `main` as
  protected with no direct push, so this push is recorded as an
  operator-authorized bypass of that rule, not as the current delivery route.
  Before the push, `git fetch origin main` showed `origin/main` at `2edac5bd6`
  with no commit ahead of the local branch, so the push was a fast-forward.
- Position is read from Git: `git rev-parse HEAD` and
  `git log --oneline origin/main..HEAD`.

## Work Log

### W1: Registry scope narrowed and the review transition held (2026-09-17, local-executed)

The proposal commit `4429ced1e` drafted Behavior Contract 1 as reading every
terminal status from the Registry and removing `TERMINAL_DOCUMENT_STATUSES` and
`_TERMINAL_STATUSES`. Listing the Registry lifecycles showed the union of their
`terminal_statuses` holds `rejected`, `resolved`, `published`, `sealed`, and the
template lifecycle's `draft`, so replacing the per-document set would make a
resolved Incident, a published Postmortem, and a rejected ADR findings. The
`spec`, `plan`, and `task` lifecycles also list no `retired`, which
`_TERMINAL_STATUSES` uses in `spec_packages.py` at its package removal and
preservation checks. The Spec and `ADR-0037` now read the Registry only for
Stage 03 members and leave both sets unchanged and out of scope.

The occupancy fixtures write only `status` and no Registry, so the cancellation
judgment is one public pure function that package validation and occupancy both
call, rather than a step inside `_load_package` that occupancy could not reach.

This Plan and Task are added as drafts. Setting the Spec to `review` in the
same worktree failed `check-document-metadata.py --mode check-changed` with
`invalid-initial-status: new spec documents must start at draft` (exit 1),
because the check judges against `@{upstream}` at `2edac5bd6`, where the
package does not exist. The proposal commit `4429ced1e` is not pushed, so the
Spec stays `draft` and the review transition waits for the first integration.

Checks run on the worktree before the W1 commit are recorded under
Verification Evidence.

### Standard 3.0.0 adoption authorization — 2026-09-28

The repository owner explicitly approved accepting ADR-0037, the waiting and
cancellation transition, reassessment/history-only adoption, and proceeding to
complete Standard 3.0.0 adoption. This is the actual current-session approval;
it supersedes the earlier pending B1/B2 boundary recorded below. It grants no
specific payload-removal authorization, commit, push, merge, service operation
or secret access. Those actions are not performed.

The implementation extends this Spec/Plan and the existing proposed ADR-0037
before its first acceptance. ADR-0036 is preserved using the explicitly registered
one-unit legacy transition allowance, because no authorized commit can establish
its prepared superseded metadata as an exact source object in this session.
All other new captures use the exact generation. Source objects and existing
capture rows are retained; no fake approval or capture date is populated.

## Verification Evidence

W1 and W2 carry no acceptance criterion. Results before the proposal commit
`4429ced1e`, local, index snapshot: `check-document-corpus-lifecycle.py
--base-ref HEAD` exit 0 with zero violations; `check-document-metadata.py
--mode check-changed` over four documents exit 0 with zero violations. After
that commit, local, worktree equal to `4429ced1e`: `run-ci-gate.py --profile
changed` exit 0. Hosted CI: NOT_RUN, no push is authorized.

### Standard 3.0.0 Reconciliation (2026-09-28)

#### Pre-approval scope and observed baseline

Initial request before the later adoption approval: local non-destructive repairs and reviewable contract
reconciliation. No ADR acceptance, archive removal, commit, push, merge,
service operation or secret access. The existing draft lifecycle is retained;
this investigation is not a completion receipt for W3–W8.

Observed HEAD: `be949f338056ee05ca139ea72403576aa18f21d8`, branch
`docs/readme-navigation-language-contract`, non-shallow repository, with 17
pre-existing unstaged README edits. Locally configured origin resolves to
`github.com/buenhyden/hy-home.docker`; no credentials were output. Those edits are preserved. The supplied
`cb11af64194432d94739c47046ed707010634468` is unavailable locally (`git diff`
exit 128, bad object); no base comparison or full-history claim is made from
that SHA. No fetch or branch switch was performed.

Temporary inventory from `git ls-files`: 1,020 Markdown/LLM-entry documents,
186 READMEs, 964 classified, 56 outside registered profiles, zero ambiguous
matches; every `docs/**` document is classified. The 56 include native
provider outputs, skill-local references/assets, root shims, GitHub templates
and support/example files, not unregistered Stage documents. The temporary
inventory records metadata, profile/template bindings, role and parsed local
inline inbound/outbound counts. Those counts do not prove HTML/reference/wiki
coverage. Inventory and test-map scratch outputs are not a second Registry.

#### Pre-approval reconciliation decisions

| Item | Before / observation | This change / disposition | Owner and boundary |
| --- | --- | --- | --- |
| Frozen identity | Same-content payload and ancestor/member symlinks passed catalog identity; public scans followed linked roots | Shared descriptor snapshot for catalog and preservation/retirement/coverage/count paths; reject unsafe records | REQ-0026-FR-0012, `archive.py`, lifecycle recovery; existing contract repair |
| Catalog fixture | Package retirement test still wrote catalog rows in README | Fixture now writes `retention-catalog.md` and keeps the required index | Existing Registry catalog separation, not a new policy |
| Current/history list | Stage 03 already lists only four current packages; catalog already separate | Keep; no restoration of stale mixed index | SPEC-0184 and Stage 99 |
| Operations | Role layout exists; SPEC-0183 Task records owner follow-ups and merged implementation; ADR-0043 still proposed | Preserve layout and IDs; no retroactive acceptance | Existing SPEC-0183 owner must reconcile its lifecycle |
| Wait/cancellation | ADR-0037 proposed, this package draft; previous design/spec approval is recorded | Keep existing proposal; Plan addendum makes activation boundary explicit | W3–W7 and owner acceptance |
| Appraisal/history-only | No registered current assessment/availability contract | Proposed phased cutover in Plan, not active permission | REQ-0026, AD-0030, Registry; consequential decision required |
| Research | RES-0096 is the archive-domain research owner linked from RES-0002 | External source refresh remains in that existing owner | SPEC-0185 stays frozen |
| Commit Ledger | Existing execution revisions are provenance | Preserve all original ledger entries | Task evidence, not a duplicate recovery ledger |

#### Pre-approval common criteria binding

These are the pre-approval findings from the first pass, retained as execution
history. They are superseded by the post-approval implementation and verification
results below, not declarations of current standard conformance.
Responsibility for unresolved decisions remains with `@buenhyden`; re-review
when the named decision/contract is adopted, not when a document ages.

| Standard | Current binding | Result / reason / next condition |
| --- | --- | --- |
| S01 | documentation protocol, Registry, scripts | Existing ownership retained; no parallel authority |
| S02 | Registry lifecycles; ADR-0037 | Partial: target vocabulary and new transitions not adopted |
| S03 | Registry preserved profiles; Archive catalog | Existing six dispositions retained; unused resolved directory not created |
| S04 | SPEC-0179; package completion receipt | Partial: wait/cancellation require the existing decision, not a new fake status |
| S05 | Retention Catalog; proposed Plan B2 | Not implemented: assessment/availability need a registered contract |
| S06 | `validate_catalog_identity`, frozen transition fields | Legacy comparison repaired; exact-byte generation and checkout/index distinction pending |
| S07 | separate `retention-catalog.md` | Unit rows exist; post-removal rows not yet supported |
| S08 | `links.py` alignment | Current citation checks exist; appraisal priority and historical revision resolution pending |
| S09 | frontmatter schema with date FormatChecker | Existing conditional checks; cancellation and removal fields pending |
| S10 | Stage indexes, separate catalog, SPEC-0184 | Current/history separation already present; all-mode does not imply navigation/language coverage |
| S11 | REQ-0026, AD-0030, ADR-0037, this package | Owners preserved; acceptance not inferred from implementation |
| S12 | incident/postmortem profiles, operations check | Existing packet controls; no incident status changed |
| S13 | documentation language/profile rules, provider adapters | Existing native/frozen exceptions retained; broader language audit incomplete |
| S14 | registered CLI and gate runner | Actual scopes/results below; no skipped or zero-target pass invented |
| S15 | frozen payloads and catalog envelopes | No payload, legacy catalog path or original Task evidence edited |
| S16 | this dated Standard 3.0.0 evaluation | Proposal version recorded here; no runtime dependency on another repository |

#### Pre-approval verification scenario mapping

Each row is applicable. Related existing tests prove only their own cases;
a module pass is not a claim that every branch of the broader scenario is
covered. `NOT_RUN` means no mapped check was executed for that branch. Target
contracts that conflict with ADR-0036 remain pending rather than N/A.

| Scenario | Existing test binding | Scope / result limitation |
| --- | --- | --- |
| V01 | `DocumentRegistryTests.test_profile_lifecycles_encode_semantic_entry_and_terminal_states` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V02 | `ArchiveMinimizationTests.test_stage_03_occupancy_is_judged_per_package`; `SpecPackageTests.test_retained_package_keeps_non_terminal_execution_evidence` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V03 | `SpecPackageTests.test_completed_package_allows_cancelled_task_without_receipt` | Pending contract or missing coverage; target scenario NOT_RUN |
| V04 | `ArchiveMinimizationTests.test_active_stages_hold_no_terminal_document` | Pending contract or missing coverage; target scenario NOT_RUN |
| V05 | `RetentionCatalogTests.test_a_member_set_difference_is_reported`; `OperationsCatalogTopologyTests.test_incident_year_packet_and_roles_are_exact` | Mapped tests passed in the broad 643-test run; full scenario incomplete |
| V06 | `OperationsCatalogTopologyTests.test_incident_body_identity_year_and_date_relations_are_validated`; `DocumentRegistryTests.test_resolved_incident_requires_a_closure_date`; `DocumentRegistryTests.test_frontmatter_schema_enforces_date_formats` | Mapped tests passed in the broad 643-test run; full scenario incomplete |
| V07 | `RetentionCatalogTests.test_resolved_names_carry_the_incident_and_its_corrective_owner`; `DocumentRegistryTests.test_published_postmortem_requires_review_evidence` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V08 | `RetentionCatalogTests.test_a_mode_difference_is_reported`; `RetentionCatalogTests.test_source_must_be_one_commit_and_the_origin_path`; `RetentionCatalogTests.test_source_object_must_exist_with_the_unit_type` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V09 | `ArchiveMinimizationTests.test_archive_reads_reject_ancestor_symlink_special_file_and_swap`; `RetentionCatalogTests.test_a_line_ending_difference_is_reported`; `RetentionCatalogTests.test_catalog_identity_rejects_symlink_payload_and_ancestor`; `test_catalog_identity_rejects_symlink_package_member`; `test_catalog_rejects_symlink_package_root` | New symlink cases RED then GREEN; remaining generation/index branches incomplete |
| V10 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V11 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V12 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V13 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V14 | `SharedDocumentGovernanceTests.test_hidden_governance_links_are_checked_but_frozen_history_is_preserved`; `DocumentGraphTests.test_alignment_allows_only_the_archive_index_and_completed_bodies` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V15 | `DocumentGraphTests.test_alignment_validates_same_document_and_unselected_markdown_anchors` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V16 | `MigrationStateTests.test_tombstone_identity_inherits_the_retired_artifact_id` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V17 | `TemplateAndAuthoredResidueTests.test_incident_template_uses_registered_timestamp_placeholder`; `DocumentRegistryTests.test_conditional_frontmatter_contract_rejects_unknown_status_or_key` | Mapped tests passed in the broad 643-test run; full scenario incomplete |
| V18 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V19 | `CiGateRunnerContractTests.test_nonzero_fake_child_is_propagated_and_stops_plan` | PASS in 25-test gate suite; remaining zero-target/skip cases incomplete |
| V20 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V21 | `DocumentLinksCliTests.test_repository_modes_are_deterministic_and_non_mutating`; `FourDigitDocumentIdentityTests.test_metadata_validator_write_and_check_modes_are_explicit` | Mapped tests passed in the broad 643-test run; full scenario incomplete |
| V22 | `ArchitectureDocumentTests.test_supersession_edges_require_effective_successor_and_superseded_predecessor` | Mapped test passed in the broad 643-test run; full scenario incomplete |
| V23 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V24 | `MigrationStateTests.test_mutating_format_hooks_exclude_frozen_records_only`; `ArchiveMinimizationTests.test_every_frozen_migration_is_byte_identical` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V25 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V26 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V27 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V28 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V29 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V30 | `RetentionCatalogTests.test_a_catalog_left_in_the_stage_readme_is_not_read` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V31 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V32 | `LanguageModeTests.test_frozen_and_generated_readmes_are_not_judged` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V33 | `DocumentLinksCliTests.test_repository_modes_are_deterministic_and_non_mutating` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V34 | `ArchiveMinimizationTests.test_archive_enumeration_and_aggregate_byte_limits_fail_closed` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V35 | `ArchiveMinimizationTests.test_task10_recovery_references_all_resolve_to_regular_blobs`; `RetentionCatalogTests.test_source_commit_must_be_an_ancestor_of_head` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V36 | `DocumentGraphTests.test_retired_catalog_root_has_no_current_inputs` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V37 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V38 | `DocumentRegistryTests.test_active_corpus_uses_migrated_statuses_and_common_six` | Mapped tests PASS in 277-test run; full scenario incomplete |
| V39 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |
| V40 | No established test binding | NOT_RUN; explicit acceptance gap, not a skip or pass |

#### Commands observed in this session

All commands below are local and were run through `rtk proxy`; tool
sandbox initialization failed with `bwrap: loopback: Failed RTM_NEWADDR`, so
these same scoped commands used reviewed escalation. No rejection was
reported. Results from earlier Tasks are not counted here.

| Command / scope | Exit | Observed result |
| --- | --- | --- |
| `python3 scripts/validation/check-document-corpus-lifecycle.py --base-ref HEAD` before edits | 0 | lifecycle 0 violations; migrations 5, tombstones 140, preserved 239, decisions 286, recovery rows 374, recovery violations 0 |
| `python3 scripts/validation/check-document-links.py --mode all` before edits | 0 | 962 selected documents, 9,548 links, 0 failures; traceability/alignment/entrypoint/commands only |
| `python3 scripts/validation/check-operations-catalog.py` | 0 | PASS; current role-first topology |
| `python3 -m unittest tests.lib.document_governance.test_archive tests.lib.document_governance.test_spec_packages` baseline | 1 | 105 tests; one stale catalog-path fixture failed |
| New payload/ancestor/member symlink tests before production fix | 1 | 2 tests, 3 assertion failures; same-content symlinks incorrectly passed |
| `RetentionCatalogTests` plus corrected package-retirement test after repair | 0 | 32 tests, no failures |
| `python3 scripts/validation/run-ci-gate.py --profile changed --explain` | 0 | Selected routes inspected; explain is not execution |
| `python3 -m unittest tests.validation.lifecycle.test_equivalence` | 0 | 2 CLI-composition tests passed |
| `python3 -m unittest tests.validation.test_ci_gate_plan` | 0 | 25 selection/failure-propagation tests passed |
| `python3 scripts/validation/check-script-manifest.py` | 0 | Script manifest valid |
| `python3 scripts/validation/check-github-workflow-contract.py` | 0 | 5 workflows, 7 jobs, 8 action bindings validated; no hosted CI execution |
| `python3 -m ruff check` / `format --check` on the three Python files | 1 | UNAVAILABLE: Python environment has no ruff module; no dependency installed |

Both registered gate profiles select `check-conftest-policy.sh`, which runs
`docker compose run --rm conftest` and `down --remove-orphans`. The baseline
shell checks also consume the real `.env` when present. Those operations are
outside this request's no-service/no-secret boundary, so the full gate was not
executed or reported as a pass. The PostgreSQL leaf itself is registered with
`--check-config-only`; that leaf is not evidence of a live rehearsal. Full
profile `--explain` also exited 0 and is planning evidence only.
Hosted CI, deployment/runtime, actual removal, index/commit history-only
fixtures, and approval-dependent target semantics are NOT_RUN. No package
is marked completed. Follow-up verification and independent review are
recorded below.

#### Pre-approval full document regression and allocation repair

`python3 -m unittest discover -s tests/lib/document_governance -t .` exited 1:
643 tests in 628.924 seconds, one failure in
`IdentityHistoryTests.test_registry_high_water_is_not_below_repository_history`.
The full run overlapped final exception normalization, so it is broad
compatibility evidence, not a fixed final-tree receipt. The subsequently
added retirement error-path regression accounts for discovery now selecting
644 tests.

The failing check scans all local refs: `identity_spaces.spec.high_water`
was 184 while issued history contains 185. `git log --all` shows actual
SPEC-0185 issuance at `9f2432766` and preservation at `be3d244d6`, with review,
approval and activation commits between them. The current checkout lacks
that package; this is a ref/history discrepancy, not permission to recreate
it. Registry high-water is corrected to 185 and next-number to 186, reserving
an already-issued identity without issuing a new document, rewriting history
or importing another branch's content. The original 643-test failure is
retained here. After the correction, `python3 -m unittest
tests.lib.document_governance.test_identity_history
tests.lib.document_governance.test_registry` exited 0: 127 tests in 103.503
seconds. The full discovery suite was not rerun; this focused result does
not turn the earlier full-suite failure into a full-suite pass.

#### Follow-up results and remaining boundary

After relocating the new material under existing registered sections,
`check-document-metadata.py --mode check-changed --base-ref HEAD` with the
four explicit changed document paths exited 0: selected 4, violations 0.
The first attempt exited 1 with three documents introducing unregistered
H2 headings; only the heading placement was corrected, no gate relaxed.
`check-document-metadata.py --mode check-active --base-ref HEAD` then exited
0 over 445 selected current documents. `--mode check-contracts --base-ref
HEAD` exited 0 with zero repository contract violations.

The four-module run (`test_archive`, `test_spec_packages`, `test_registry`,
`test_links`) exited 0: 277 tests, 181.966 seconds. A later review regression
for invalid Git source arguments first failed twice and now has an explicit
`catalog-source-invalid` diagnostic; the final Archive module plus package-retirement fixture rerun exited 0:
74 tests, 66.903 seconds. Corpus revalidation exited 0 with the same 239 preserved documents
and zero violations. Link all-mode revalidation exited 0: 962 selected
documents, 9,548 links, zero failures. `git diff --check` exited 0.

`git diff --name-only HEAD` over the four frozen classes, tombstones,
migrations and retention catalog returned no paths, and the staged diff
was empty. This proves those tracked surfaces were not changed by this
working-tree diff; it does not prove all historical capture generations or
index-only attacks are implemented.

Independent security review found no blocker or important defect in the
scoped catalog snapshot fix. It also identified existing disposition-root
scans in preservation-boundary, retirement, coverage and recovery-count paths
that could enumerate a symlink target before catalog validation. The follow-up
reuses the same descriptor snapshot through `preserved_member_paths`, including
tombstone boundary reads and current-owner ancestor checks. Four isolated
regressions demonstrated RED then GREEN. The Archive and Spec Package
suites passed 113 tests in 101.863 seconds before final exception-message
normalization; the subsequent catalog suite passed 37 tests on that fix. A fresh post-freeze Archive/Spec run, including the final caller
repair, passed 114 tests in 101.094 seconds. Missing optional dispositions remain empty; unsafe trees produce
fixed diagnostics without host filenames. Final independent security review
reported no blocker or important finding. Its minor diagnostic observation
was reproduced by `test_unsafe_catalog_retirement_grants_no_exemption`
(exit 1, ValueError), then repaired at `_recorded_retirements`: unsafe input
grants no exemption while the Archive gate reports the failure. The complete
Spec Package module then passed 37 tests in 32.284 seconds. No secrets were
inspected.

After the allocation repair, final changed-document metadata validation
selected four documents with zero violations; Registry contract validation
also exited 0 with zero violations. Final corpus validation exited 0:
lifecycle violations 0; migrations 5, tombstones 140, preserved 239,
decisions 286, recovery rows 374, recovery violations 0. Independent code
review found no issue in the two-counter monotonic allocation repair.

At the end of the pre-approval pass, integration readiness was not complete. ADR acceptance,
new assessment/history-only/strict-generation contracts, unmapped
V scenarios, full gate and hosted CI remain open. Existing branch and index
are retained; no commit, push, merge, package disposition or branch removal
was performed.

### Post-approval Standard 3.0.0 implementation

This is the current result; the pre-approval observations above are historical.
ADR-0037 is accepted and ADR-0036 is preserved with its body unchanged under the
explicit bootstrap generation. The existing SPEC-0179 owns the expanded work.
At that local implementation checkpoint Spec/Plan/Task retained draft metadata.
The subsequent delivery approval and legal transitions are recorded in the
authorized delivery section below; no lifecycle edge is bypassed.

| Standard | Current binding and verification boundary |
| --- | --- |
| S01 | Existing policies, Registry, catalog and validators keep separate ownership; no parallel ledger |
| S02 | Profile lifecycles and separate disposition-entry mappings; no renamed or fabricated states |
| S03 | Existing six dispositions and complete units retained; no unused directory created |
| S04 | Registry-based package waiting, shared cancellation validation, unchanged PASS receipt duty |
| S05 | Optional current assessment table; absence unreviewed/retained; pinned scoped authorization |
| S06 | Explicit cutover and one bootstrap legacy unit; exact new blobs/modes/sets; separate Git views |
| S07 | Immutable capture rows and nondeletable assessment rows; DAG history and removal fixtures |
| S08 | Schema-pinned supported citation order; assessment before Incident exception; source-time links |
| S09 | Conditional cancellation/closure and explicit stdlib date/time assertions; no seeded approval |
| S10 | Current package routing includes calculated waiting; catalog remains separate from README |
| S11 | REQ-0026, AD-0030, expanded accepted ADR-0037 and existing package; no new artifact identity |
| S12 | Resolved Incident requires published Postmortem and real current corrective owner or reasoned none |
| S13 | Existing reader/profile language rules retained; edited REQ/AD/ADR conform; frozen text untouched |
| S14 | Existing public gates integrate archive changes; zero-test/missing-summary/required-skip cannot pass |
| S15 | Pre-existing frozen records and original Commit Ledgers unchanged; only current explanations updated |
| S16 | Registry standard_version 3.0.0 and this dated adoption evidence; no remote repository dependency |

The legacy generation is a bounded compatibility contract, not a claim that every
old source link can be recovered. Alignment explicitly reports 2,870 outbound
legacy links without capture provenance as unverified, and admits 55 historical
source documents only to alignment. That warning neither rewrites old records nor
makes them current authority. New exact captures must pass historical integrity.
The local tools cannot establish hosted CI, live service health or actual removal.

#### Post-approval scenario bindings

The following bindings supersede the first-pass NOT_RUN mappings. Test execution
results are recorded below; static/manual evidence is explicitly distinguished.

| Scenario | Concrete test or evidence |
| --- | --- |
| V01 | ArchiveDispositionRegistryTests; Registry duplicate-path and profile classification tests; altered occupancy Registry test |
| V02 | Stage03 occupancy matrix and retained execution-evidence package tests |
| V03 | task_cancellation_findings invalid-form matrix; withdrawn criterion still requires receipt PASS |
| V04 | completed-package occupancy matrix; malformed completion receipt and nonterminal member rejection |
| V05 | exact member-set mutations, package retirement atomicity, historical missing-unit assessment fixtures |
| V06 | conditional schema tests and resolved closure calendar/timezone/offset negatives; stdlib format assertion |
| V07 | resolved packet published Postmortem/current corrective owner or explicit reasoned-none fixtures |
| V08 | test_invalid_source_type_path_and_abbreviated_revision_fail; trusted capture_sources validation |
| V09 | exact body/newline/mode/member tests; no-follow link/special-file/race regressions; committed generation tampering |
| V10 | assessment snapshots remain separate from immutable capture and payload comparisons |
| V11 | scoped assess/remove approvals, hold, whole-unit absence, partial payload and resurrection fixtures |
| V12 | complete-history requirement and historical capture/payload loss tests, including DAG merges |
| V13 | test_assessment_blocks_incident_exemption_without_hiding_missing_target; package-directory bypass regression |
| V14 | source-revision target/anchor tests and unchanged sealed route last-authored context; public alignment selector |
| V15 | test_reference_html_wiki_and_footnote_links_share_normalization; all-link-forms boundary and encoded controls |
| V16 | existing tombstone inherited identity/quoted frontmatter and migration fixtures |
| V17 | rendered cancelled Task conditional schema, native envelopes and optional-empty checks |
| V18 | role-index exact member tests and navigation renderer/parser tests; current README manual review |
| V19 | run-unittest rejects zero/missing summaries and skips; nonzero child propagation gate tests |
| V20 | workflow contract checker and gate-plan path selection; hosted CI NOT_RUN (no remote authorization) |
| V21 | repository_modes_are_deterministic_and_non_mutating; provider renderer read-only and fixedpoint tests |
| V22 | effective successor/reciprocal chain architecture tests plus unique current assessment owner resolution |
| V23 | Manual evidence boundary: static checks are reported as static; runtime/deployment NOT_RUN |
| V24 | baseline frozen-byte comparison and formatter exclusion tests; no historical sweep |
| V25 | exact Task revision/action/unit/date/owner/visible quote; proposed/unrelated/future-branch approval negatives |
| V26 | independent index deletion/mode/bytes/catalog/assessment/Registry mutation tests with restored worktree |
| V27 | historical capture rows/payload union detects simultaneous deletion; public activation downgrade test |
| V28 | assessment row continuity, fresh decision/reason, rehabilitation, historical-edge chronology/ancestry fixtures |
| V29 | history-only blocks direct current hrefs while catalog survives; no real payload removed |
| V30 | navigation/catalog role distinction and existing current-only package index regressions |
| V31 | LanguageJudgeTests for prose versus code/identifiers/tables; existing frozen/native exemptions |
| V32 | native/frozen/generated/template body exemptions; no new preservation-authoring template |
| V33 | deterministic link checker and provider-renderer fixedpoint; no automatic dates/IDs/approvals |
| V34 | bounded entry/byte/history readers fail closed; no cleanup or auto-removal action exists |
| V35 | orphan/missing objects and incomplete history fail; sources require correct object type and ancestry |
| V36 | current role-first Operations, current package index and separate catalog regressions |
| V37 | supported CRLF versus raw object tests, bootstrap checkout representation, filter non-execution diagnostics |
| V38 | Incident template requires frontmatter-derived status or timestamped observation; schema date/time tests |
| V39 | original Task ledger/raw frozen bytes preserved; retained execution evidence tests |
| V40 | Manual current-owner review, current README routing and this actual-result record; no archived work reopened |

#### Post-approval execution results

- Link/Registry/catalog-contract rerun: 187 tests, 118.654 seconds, exit 0.
- Gate adapters and lifecycle CLI equivalence: 22 tests, 0.398 seconds, exit 0.
- Registry repository contracts and script manifest checks: exit 0.
- Existing active-document metadata check: 445 documents, zero violations.
- Intermediate corpus check: zero lifecycle/recovery violations; 240 preserved
  documents (the only new preservation is ADR-0036), 5 migrations, 140 tombstones,
  286 decisions and 374 recovery rows.
- Ruff, Black and coverage.py are unavailable in this environment. No dependency
  was installed and no unavailable check is represented as a pass.
- A mistyped test module path `tests.validation.test_ci_gate_adapters` produced
  an import error; the correct `tests.lib.gate.test_ci_gate_adapters` run above
  passed. The other selected modules continue to be recorded separately.

The first post-approval broad run selected 692 tests and exited 1 after
835.393 seconds: committed rehabilitation and committed resurrection exposed two
history defects. Both were fixed with targeted regressions before the final broad
rerun. This intermediate failure remains evidence, not a full-suite pass.

The gate-plan/Operations/Spec selection executed 155 real tests without
failure; its command exited 1 solely because the mistyped adapter module added an
import-error placeholder. The separate correct adapter run above passed. Provider
renderer verification passed 43 tests in 32.503 seconds.

Final CLI checks so far: changed metadata selected 31 documents with zero
violations; corpus lifecycle/recovery zero violations; link `--mode all` zero
failures, one explicit legacy warning, 961 current documents, 9,540 current links,
55 historical documents. All-mode now also invokes the existing navigation and
language handlers: their registered-route regression first failed (unsupported
modes), then passed together with the duplicate cancellation criterion fix
(10 tests, 0.897 seconds). The workflow contract check passed 5 workflows,
7 jobs and 8 pinned action bindings.

Python stdlib trace measured the new modules without installing coverage.py:
53 tests passed in 100.805 seconds; archive_assessments line coverage was 90%
and archive_snapshots 87%. This is focused line coverage, not repository-wide or
branch coverage, and preceded the final staged-Names/source-reachability additions.
The current full gate remains NOT_RUN because its service/secret-consuming leaves
are outside authorization; local static results do not imply hosted or runtime pass.

An intermediate broad rerun executed 721 tests in 828.260 seconds and exited 1
with 23 errors. Its already-imported three-argument `_names_are_valid` overlapped
with the new four-argument snapshot caller written while the process was running.
That mixed-version run is not a final receipt. The targeted archive/security
selection separately passed 177 tests in 156.848 seconds. A later trace selection
passed 56 tests in 122.851 seconds (assessment 90%, snapshot 87% line coverage).

Final review then found that selected-surface owner bytes were classified against
the worktree Registry. Assessment Current Owner and capture Names now receive
focused index-only Registry mutation regressions. Assessment tests passed 30
tests in 10.112 seconds; snapshot/catalog tests passed 65 tests in 34.187 seconds.
The completed/resolved Names regressions failed under the old classifier and
passed with selected-surface classification. The final frozen-source broad rerun is recorded below. No completed lifecycle or successful
full CI gate is claimed here.

Final frozen-source focused trace run: 61 tests passed in 426.709 seconds,
exit 0. `archive_assessments` line coverage was 91%; `archive_snapshots` was 87%.
The 60 implementation/test/Registry/schema input checksums remained unchanged
through this run. This supersedes the earlier focused coverage measurement only;
it is not branch coverage or repository-wide coverage. The final corpus check
again reported zero violations (240 preserved documents and 374 recovery rows),
and final active metadata selected 445 documents with zero violations.

Final complete document-governance regression:
`python3 -m unittest discover -s tests/lib/document_governance -t .` passed
730 tests in 805.113 seconds, exit 0, on the unchanged frozen implementation.
This is the final broad receipt and supersedes both earlier failed broad runs.
No tests were skipped in this run. Gate adapter/lifecycle CLI and provider
renderer results remain the separate successful runs recorded above.

Local implementation, fixture verification and independent review of the approved
adoption are complete. Integration is not complete: the index is unchanged,
no commit/push/merge occurred, and SPEC-0179 still needs its registered integration
edges and the changed-profile gate before a completion receipt/status is valid.
That gate includes service/secret-consuming leaves outside this request; it is
NOT_RUN, not waived or passed. No actual archive payload removal, service action,
secret-value access or hosted CI result is claimed. Existing frozen records are
unchanged; ADR-0036 is the sole new capture and its original body is identical.

The subsequent stop-hook request supplied no validator diagnostic. Read-only
`run-ci-gate.py --profile changed --explain` passed and exposed a real integration
gap: the explicit document-governance gate list omitted the three new archive
modules. A gate-membership regression failed first, then the existing
`.github/workflow-contract.yml` leaf registered all three modules. Workflow/plan
regressions passed 72 tests in 17.443 seconds; the workflow contract passed
5 workflows, 7 jobs and 8 action bindings. Provider surface drift also passed
(2 providers, zero drift). Archive implementation inputs remain unchanged.
The full selected plan still invokes Compose configuration (which may read real
`.env`) and Conftest `compose run`/`down`; the original request excludes those
operations. The executable full changed profile remains NOT_RUN pending explicit
approval of those specific operations; `--explain` is not a gate pass.

The owner subsequently explicitly allowed Compose environment-based validation
and Conftest container execution/cleanup for this changed-gate run only. The first
full command exited 1 before execution with `ci-gate-entrypoint-identity` because
modified entrypoints differed from the original index. A managed isolated
worktree at the same HEAD stages the reviewed changes while the original index
stays empty. Its first full run exited 2: 51 fixture tests passed, then the
unittest adapter attempted to parse uncaptured `stderr` and raised
`ci-gate-adapter-operation`. A real subprocess regression reproduced this failure.
The adapter now uses its existing bounded capture path and emits both streams
once; mock output remains isolated in tests. All 21 adapter tests passed in
0.234 seconds. The full isolated command is rerun with this fix; no commit or
remote operation is authorized by the gate-specific approval.

The next full isolated run passed the document-library gate (602 tests),
Operations/supply-chain fixtures (239 tests), and Compose validation (72 selections,
355 rendered services), then exited 1 at the baseline regression leaf: two file-mode
checks failed and 23 opt-in runtime tests were skipped. The managed checkout had
made the two OIDC scripts group-writable; their isolated modes were restored to
the original checkout's modes (Open WebUI 0755, Gatus 0555). All 19 OIDC tests then
passed; the original scripts were not changed.

Remaining-gate checks found two new Archive modules missing from the script
manifest, the existing language test module missing from the full-profile gate,
and three stale English assertions against existing Korean invocation warnings.
The manifest now records the modules' direct consumers/tests, the gate includes
`test_language`, and the warning assertions preserve the same Korean prohibitions.

The existing tests README explicitly exempts registered opt-in runtime integration
skips from CI failure. The same six full baseline modules remain selected; the
existing leaf now declares its five exact opt-in TestCase scopes through
`--optional-runtime-skips`. Every actual skip must have a unique verbose receipt,
match the summary count and a declared class; undeclared required skips still fail.
Each declaration must be observed, and a declared class that executes successfully
is accepted. This adds no runtime flags or environment admission. Full-profile
coverage uses the same adapter argument parser, retaining exact module coverage
and duplicate rejection. Independent review approved these bounded changes.

Focused workflow/model/manifest regression: 158 tests passed in 27.730 seconds.
Surface ownership/adapter/manifest regression: 89 tests passed in 10.863 seconds.
The registered tail from baseline regressions through the final Storybook contract
then exited 0: its test batches were 111 (23 explicitly registered opt-in skips),
18, 42, 24, 48, 30 and 157. These tail results do not substitute for a full changed
profile. The final whole command is rerun on this fixed staged snapshot.

Final whole changed-profile receipt (supersedes earlier NOT_RUN and failed-gate
observations): `python3 scripts/validation/run-ci-gate.py --profile changed`
exited 0 in the managed `archive-validation` worktree at baseline
`be949f338056ee05ca139ea72403576aa18f21d8`, with the complete reviewed result
staged. All 59 staged result paths matched the original worktree's bytes before
execution and remained unchanged through the run. The original index stayed empty.

The 16 unittest batches selected 1,635 tests: 1,612 executed successfully and
23 existing opt-in runtime tests were explicitly reported as skipped under the
five registered classes. No required test was silently skipped or waived.
The document-library gate passed 609 tests in 532.500 seconds. Compose validation
passed 72 selections and 355 rendered services; the complete command also passed
its registered policy, manifest, workflow and final Storybook checks. This is a
local changed-profile result, not hosted CI, opt-in rehearsal, deployment, formal
SPEC lifecycle completion or actual history-only removal evidence. It does not
claim that an unstaged checkout satisfies the entrypoint/index identity contract.

The only subsequent edits record this receipt in this Task and the Plan. Their
metadata/link/diff checks are rerun separately; no implementation or test input
is changed after this whole-gate receipt. Formal integration edges remain pending.

### Authorized delivery preparation — 2026-09-28

The operator explicitly requested: “완료되었으면, commit하고, push하고, merge하고,
개발 브랜치 및 워크트리를 정리한다.” This supersedes earlier commit and integration
restrictions for this task. The concrete target is `buenhyden/hy-home.docker`:
create/push the `codex/archive-standard3` PR branch, merge through protected
`main`, then delete the delivered task branch and archive its managed worktrees.
Recovery is Git history and an ordinary reviewed revert; no history rewrite,
protection change, payload removal or production deployment is included.

Authenticated before-state reads found no open PR, no repository rulesets,
required `validation-changed` with strict up-to-date checking, zero required
approving reviews and code-owner review disabled. CODEOWNERS still routes the
changed governance, scripts, docs/specs and docs/templates paths to `@buenhyden`.
No human approval review is claimed. After-state PR/check/merge evidence will be
recorded as observed.

Fetching the named baseline made `origin/main` at
`cb11af64194432d94739c47046ed707010634468` available. The original branch has 13
unmerged prior README/language commits plus pre-existing unstaged README edits.
They are preserved in the original checkout. Delivery uses an isolated managed
worktree at main; it ports only Archive adoption and necessary catalog extraction,
keeps main's frozen SPEC-0185 package and unchanged catalog row, and excludes the
unrelated README-language enforcement. The legacy capture cutoff and ADR-0036
source now use this ancestor of the delivery branch. Prior test receipts cover
the earlier snapshot only; delivery checks are recorded separately below.

Delivery preparation checks: changed metadata selected 18 documents with zero
violations; link mode all checked 960 documents and 9,841 links with zero failures
and one explicit legacy warning (2,870 uncaptured links). The upstream Renovate
change already uses CodeQL upload-sarif revision
`1c5b675653bb5c22dbe9b12b556ec555138e09fd`, but main's Action registry and code
baseline still named the prior revision. The official pinned manifest was fetched
and verified as `node24`; both existing registrations were synchronized without
weakening pin/runtime/consumer checks. The workflow-contract regression rerun
passed 48 tests in 12.175 seconds. Earlier port runs observed incomplete concurrent
Registry state and are not passing evidence; subsequent frozen runs supersede them.

The first full delivery gate stopped at the public lifecycle regressions (15 tests,
2 failures). The cutover revision still stored capture rows in Archive README,
so the new-generation reader incorrectly treated 25 existing captures as exact
new captures. A failing isolated extraction regression reproduced the defect;
the shared legacy reader now uses the existing bounded Git reader for README only
when the separate catalog is absent. Snapshot regressions passed 29 tests in
27.764 seconds, and the actual corpus/recovery command passed with zero violations
(migrations 5, tombstones 140, preserved 243, decisions 286, recovery rows 374).
No frozen payload was edited. The bounded delivery review found no blocker or
Important issue; the parent separately reviewed this final two-file correction.
The final whole changed gate is rerun after staging this corrected snapshot.

The next whole delivery gate passed the 15 public lifecycle regressions, then
stopped at one of 124 metadata regressions: main requires direct `spec.md` index
links, while the unrelated local navigation branch allowed package directories.
The three current rows now retain main's direct-link and Status-column contract;
`check-document-metadata.py --mode check-contracts` reports zero violations.
The earlier invalid `--mode contracts` invocation exited 2 and is not evidence.

Preflight also found main's existing Compose image updates absent from their
`infra/tech-stack.versions.json` projection. The existing `sync-tech-stack-versions.sh
--write` updated eight component tags only; `--check` then passed for 92
repositories (76 external, 16 local/custom). Compose declarations and runtime
state were unchanged. Script-manifest and workflow-contract checks passed.

### Final main-based delivery validation — 2026-09-28

The resumed whole gate first exited 1 after the 590-test document library passed:
six infrastructure assertions still named image pins predating main's Renovate
updates. The existing readiness, PostgreSQL rehearsal and supply-chain consumers,
their tests/negative fixtures, and sample-service documentation now match main's
unchanged Compose/Dockerfile selections. Seven official OCI index/amd64 manifest
identities were SHA-verified; no image selection or runtime service changed.
All 168 focused regressions passed; negative topology defects were retained.

The pinned cached Ruff 0.15.12 found a Python 3.11 f-string quoting incompatibility,
import/precedence style findings and formatting drift. These were corrected without
changing validation semantics. All 27 changed Python files pass Ruff check and
format check; changed Markdown (20 files), YAML and the three changed shell scripts
pass their configured linters. The staged Gitleaks scan found no leaks.

Final command `python3 scripts/validation/run-ci-gate.py --profile changed`,
local managed archive-delivery worktree, baseline
`cb11af64194432d94739c47046ed707010634468`, staged result snapshot: exit 0.
The 16 batches selected 1,611 tests; 1,588 executed successfully and the existing
23 opt-in runtime tests were explicitly skipped under their registered scopes.
The document library passed 590 tests and infrastructure passed 239. All 63
result-file hashes stayed unchanged during the observed frozen run. This receipt
supersedes the interrupted and failed main-based runs, not their historical record.

Independent final security/code review found no blocker or Important issue,
verified synchronized pin consumers and negative fixtures, and found no weakened
tests. The final policy review's five stale delivery statements were corrected,
and Plan criteria 11–14 now map to W8. Only these three Spec-package documents
and this evidence changed after the whole gate; focused metadata/link/diff checks
cover that documentation-only update. No hosted pass or lifecycle completion is
inferred from this local receipt. PR results are recorded in subsequent integrations.

## Review Evidence

At W1, no review had run.

For the 2026-09-28 repair, independent code review approved the scoped
catalog/fixture/documentation diff after correcting EOF whitespace and
missing final-test evidence wording. Independent security review approved
the catalog snapshot and public-root traversal hardening with no blocker or
important finding. Its diagnostic follow-up was addressed with a failing
then passing package-retirement regression. These are agent reviews of the
local diff. Owner acceptance was subsequently given explicitly in this session
and is recorded in the adoption authorization above.

The post-approval independent reconciliation review found and verified fixes for
selected-surface owner classification, public contract downgrade bypasses and
historical authorization. Its final bounded rereview found no remaining blocker
or Important issue. The security review passed 130 targeted tests before the last
owner-classification additions; that is not represented as a final full-suite run.
A required rules-engineer policy review found two wording contradictions: optional
Plan in ADR-0037 versus the required completed Plan contract, and physical retention
wording versus history-only availability. Both were corrected in the current
adoption diff. Its read-only rereview approved the policy with no remaining blocker
or Important issue. These reviews do not authorize commits or runtime actions.

## Commit Ledger

- `4429ced1e` docs(architecture): Propose ADR-0037 and draft SPEC-0179
- `055d94b78` docs(specs): Narrow the SPEC-0179 Registry scope and draft its plan
- The commit that records integration 1 in this Task is identified by
  `git log` rather than here, because a commit cannot name its own hash.
