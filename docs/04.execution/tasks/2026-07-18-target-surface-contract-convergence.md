---
status: active
artifact_id: task:2026-07-18-target-surface-contract-convergence
artifact_type: task
parent_ids:
  - plan:2026-07-18-target-surface-contract-convergence
---

# Task: Target Surface Contract Convergence

## Overview

This is the execution/evidence ledger for Spec 133 and its six-unit Plan. It
records RED/GREEN results, protected-surface approval, manifest reviews,
destructive dispositions, logical commits, independent reviews, controlled
all-files QA, deviations, and closure. `not_run` is replaced only after the
corresponding command executes.

Execution branch: `codex/target-surface-contract-convergence`.
Execution worktree: `.worktrees/target-surface-contract-convergence`.
Immutable baseline: `32c40e11747bc0bd03789c24861d2e5d60c0e999`.

## Inputs

- Spec: `docs/03.specs/133-target-surface-contract-convergence/spec.md`
- Plan:
  `docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md`
- Parent: Spec 131 and the promoted Foundation manifest
- Work units: `T-TSC-001` through `T-TSC-006`
- Target roots: `.github`, `archive`, `examples`, `infra`, `projects`,
  `scripts`, `secrets`, and `tests`
- Canonical Stage 99 metadata, README, archive, and corpus contracts
- Canonical July 5 research and audit packs
- Controlled QA: `scripts/validation/run-agent-precommit-all-files.sh`

## Goals and Non-goals

Goals:

- classify the complete target corpus before mutation;
- activate distinct content/SDLC archive and typed example/README rules;
- retire approved InfluxDB 2 source and active direct consumers;
- remove only consumer-proven duplicate and phantom surfaces;
- activate deterministic static QA/CI regressions; and
- close with reviews, generated freshness, logical commits, and controlled QA.

Non-goals:

- live data migration, service startup, deployment, release, or remote GitHub
  mutation;
- secret-value access or raw rendered/log evidence;
- bulk README normalization or historical wording deletion;
- push, PR, merge, or worktree deletion without later explicit authority.

## Scope and Change Boundaries

Allowed paths are the eight target roots, direct Stage 00/01/02/03/04/05/90/99
consumers named in the Plan, `.env.example`, `.pre-commit-config.yaml`, and
`.prettierignore`. Generated changes are limited to canonical owners.

Forbidden actions: user-global config; credentials/tokens/private keys/auth
files/shell history/raw logs; service startup; live queries/data movement;
deployment/release/remote mutation; unmanifested deletion; direct all-files
pre-commit; `--no-verify`; history rewriting; destructive Git cleanup.

Compose impact: source-only InfluxDB 2 removal and unused k6/Locust v2 wiring
removal. InfluxDB 3 remains. No service starts.

Security impact: contract, workflow, secret-metadata, and evidence hardening;
no secret value or runtime security resource changes.

Operations impact: current InfluxDB, k6, Locust, OpenSearch, and SeaweedFS
guidance aligns with static source; no procedure executes.

Runtime impact: approved tracked Compose source changes only; live acceptance
remains unverified.

## Approval Evidence

Approval source:

- The user approved destructive contract/governance remediation, protected
  local surfaces, external research, logical commits, and Subagent-Driven work.
- The user directed deprecated implementations to be removed and approved
  InfluxDB 2 server/direct-consumer removal.
- The user approved Spec 133 and continued execution.

Protected surfaces: Stage 99 contracts/templates, Stage 00 routing, Stage 01-05
truth, workflows, Compose source, validators, secret metadata, research/audit,
and generated indexes may change only as named in the Plan.

Approval boundary: local tracked changes, read-only discovery/research, static
validation, commits, and final controlled wrapper are authorized. Live runtime,
data, remote, push, PR, merge, and worktree deletion are excluded.

Rollback/recovery: revert logical commits in reverse order and regenerate only
owned output. The pinned Git objects preserve withdrawn/archive source.

Redaction boundary: record commands, exit states, safe paths, counts, Git
objects/commits, approved generated hashes, and verdicts only. Never record
values from `secrets/**`, expanded Compose values, or raw logs.

## Work Breakdown

| Work unit | Responsibility | State |
| --- | --- | --- |
| T-TSC-001 | Archive, metadata, wave, and manifest foundation | implementation_and_reviews_complete_wave_verdicts_pending |
| T-TSC-002 | README, typed example, and Storybook cleanup | implementation_complete_review_pending |
| T-TSC-003 | Root content archive provenance migration | not_run |
| T-TSC-004 | Deprecated runtime and duplicate disposition | not_run |
| T-TSC-005 | Validator, QA routing, and static CI enforcement | not_run |
| T-TSC-006 | Research, audit, generated evidence, and closure | not_run |

## Work Log

| Date | Work unit | Agent role | Result |
| --- | --- | --- | --- |
| 2026-07-18 | Planning | Controller | Converted approved Spec 133 into a six-unit Plan and this evidence ledger. |
| 2026-07-18 | Planning discovery | Three read-only subagents | Contract/profile, corpus/runtime, and QA/evidence file maps were source-corroborated. No target implementation changed. |
| 2026-07-18 | Planning review | Independent read-only reviewer | Initial review found one Critical ordering defect and four Important ambiguities: target tests were created after first use, Spec status lagged Plan status, workflow test ownership/artifact policy was conditional, schema v2 was underspecified, and 74 manual versus 75 automated README coverage was conflated. |
| 2026-07-18 | Planning remediation | Controller | Moved target regression creation to Task 2, fixed Task 5 to the existing workflow owner, retained the artifact-upload prohibition, activated Spec 133, defined schema v2/CLI behavior, and separated automated 75-file from manual 74-file evidence. Fresh re-review is required before implementation. |
| 2026-07-18 | Planning re-review | Fresh read-only reviewer | No Critical remained; four Important precision gaps remained in Task 4 test ownership, the Spec body status, workflow-owner wording, and wave-only manifest/summary path resolution. |
| 2026-07-18 | Planning re-review remediation | Controller | Added the Task 4 regression path, aligned both Spec status surfaces, removed the conditional workflow owner, and bound wave-only read checks to registry manifest/summary paths while retaining explicit-output writes. Fresh terminal planning review remains required. |
| 2026-07-18 | Terminal planning review | Fresh read-only reviewer | Spec/Plan/Task status, schema v2/CLI, README evidence boundary, protected constraints, and task order passed. Two Important findings remained: duplicate workflow-policy ownership and non-fail-closed absence scans. |
| 2026-07-18 | Terminal planning remediation | Controller | Kept artifact-upload prohibition solely in the existing repository-contract owner and replaced both plain/masked grep commands with explicit fail-closed absence assertions. Final zero-finding review remains required before implementation. |
| 2026-07-18 | Zero-review follow-up | Fresh read-only reviewer | Workflow ownership passed. One Important shell edge remained because grep exit codes above 1 were treated like the expected no-match code 1. |
| 2026-07-18 | Zero-review remediation | Controller | Both absence scans now capture the false-branch status, accept only no-match code 1, and propagate every execution error. Final confirmation remains required. |
| 2026-07-18 | Planning terminal confirmation | Independent read-only reviewer | PASS and READY with C0/I0/M0. Both absence scans fail on matches, pass only on no-match code 1, propagate execution errors, and remain correct under `set -e`; workflow policy has one canonical owner. |
| 2026-07-18 | Linked-worktree baseline repair | Controller | After planning commit `5c4e1d55`, the new Plan became a tracked consumer of the promoted frontmatter contract and exposed one stale Foundation consumer row plus three generated-owner freshness gaps that pre-commit index state had hidden. Added only the exact Plan consumer and regenerated the Foundation summary, LLM Wiki index/coverage, and metadata inventory before any implementation task. |
| 2026-07-18 | SDD handoff compatibility | Controller | Renamed only the six Plan task headings to `Task N: T-TSC-NNN` so the required Superpowers `task-brief` extractor can produce bounded handoff files. Repository-specific ignored brief/report/progress artifacts use `_workspace/repo-support/`; no implementation contract changed. |
| 2026-07-18 | T-TSC-001 implementation | Documentation Specialist | Added path-selected content/SDLC archive profiles and templates, schema-v2 wave and manifest contracts, binary-safe root/direct selection, wave-resolved read checks, and the pending advisory 483-row target manifest plus generated summary. No target migration, destructive disposition, review promotion, runtime, secret-value, or remote action occurred. Independent specification and quality reviews remain not run. |
| 2026-07-18 | T-TSC-001 specification review | Independent specification reviewer | CHANGES REQUIRED, C0/I2/M1. Schema-v2 validation bypassed common result-state and safety gates; the Task omitted exact commit/command evidence; and the human contract described one contradictory universal entry shape. Quality review did not run. |
| 2026-07-18 | T-TSC-001 specification remediation | Fresh bounded fix implementer | Added binary-safe v2 result-state, transition, replacement, immutable rollback, partition-Plan, and confidentiality gates plus mutation regressions; separated v1/v2 human field contracts; and recorded exact value-safe evidence. Independent specification re-review and quality review remain pending. |
| 2026-07-18 | T-TSC-001 specification re-review | Independent specification reviewer | CHANGES REQUIRED, C0/I2/M0. Wave-focused archive checking selected rows before validating the registry-resolved candidate manifest, and v2 partition approval did not apply the canonical metadata identity and parent-relation contract. Quality review did not run. |
| 2026-07-18 | T-TSC-001 exceptional retry approval | User | After retry-limit escalation, explicitly approved one exceptional third bounded remediation and re-review for only the two remaining Important findings. |
| 2026-07-18 | T-TSC-001 exceptional specification remediation | QA Engineer | Made wave-focused archive checking validate candidate semantics and canonical bytes before row selection, and made v2 partition Plan approval reuse canonical metadata identity and parent-relation validation. Independent specification re-review and separate quality review remain pending; no verdict was promoted. |
| 2026-07-18 | T-TSC-001 exceptional specification re-review | Independent specification reviewer | CHANGES REQUIRED, C0/I1/M1. The exceptional validator findings were accepted as closed, but the human archive contract still stated one universal field shape instead of the registry's separate content/SDLC required, optional, forbidden, and conditional semantics. Quality review did not run and no verdict was promoted. |
| 2026-07-18 | T-TSC-001 additional exception approval | User | After review C0/I1/M1, explicitly approved one additional bounded remediation for the archive human contract plus canonical and ignored evidence synchronization only. |
| 2026-07-18 | T-TSC-001 archive-contract remediation | Documentation Specialist | Replaced the universal archive field statement with exact `content-archive` and `sdlc-archive` required/optional/forbidden sets, qualified replacement and snapshot conditions to the SDLC profile, and bound the human owner to the machine registry with a focused regression. Independent specification re-review and separate quality review remain pending. |
| 2026-07-18 | T-TSC-001 final specification review | Independent specification reviewer | CHANGES REQUIRED, C0/I1/M0. The production and contract findings were accepted as closed, but the 11-test `FinalReviewRemediationTests` fixture suite retained four failures across three methods because isolated `check-impacted` roots inherited the repository target wave and emitted `promoted-manifest-missing`. Quality review did not run and no verdict was promoted. |
| 2026-07-18 | T-TSC-001 fixture-remediation approval | User | Explicitly approved a test-only in-process helper that patches only the contract and metadata-profile loaders while invoking the real `lifecycle.main`; production, contracts, profiles, and manifests were excluded from mutation. |
| 2026-07-18 | T-TSC-001 fixture remediation | QA Engineer | Replaced serialized copied-contract CLI fixtures with the approved in-process loader boundary for isolated `check-impacted` roots. The exact affected three methods passed 3/3, the expanded focused lifecycle selection passed 56/56, and focused metadata passed 76/76. Full lifecycle passed 101/103; two separate base-existing/non-gate table-shape subcases remain outside this review gate. Independent specification re-review and separate quality review remain pending. |
| 2026-07-18 | T-TSC-001 CLI-shape remediation approval | User | From the latest C0/I1/M0 review state, explicitly approved only the two remaining stale table-driven CLI shape subcases; production, contracts, manifests, and other tests remained excluded. |
| 2026-07-18 | T-TSC-001 CLI-shape remediation | QA Engineer | Replaced only the `check-promoted` and `check-archive` broken-case arguments from admitted `--wave` to forbidden `--base-ref`. RED was exactly 101/103 at those two subcases; GREEN was lifecycle 103/103, targeted table 1/1, exact fixtures 3/3, expanded lifecycle 56/56, and metadata 76/76. Re-reviews remain pending. |
| 2026-07-18 | T-TSC-001 terminal independent reviews | Independent specification and quality reviewers | Exact reviewed range `e5d3d8c47da144e233bf45f1a6ada45b673136ff..1de1fefca8bbd743fa57ce1c5a4889b03a0de3d8`: specification PASS C0/I0/M0 (`spec_complete: YES`) and quality APPROVED C0/I0/M0 (`QUALITY_COMPLETE: YES`). Implementation and reviews are complete; the advisory manifest retains all row verdicts as pending, including the Windows provenance work owned by T-TSC-003. |
| 2026-07-18 | T-TSC-002 implementation | Documentation Specialist | Added the bounded target-surface regressions, instantiated the sample-specific Service contract, and removed the five live Storybook MCP phantom exceptions after confirming the tracked Storybook tree contains no mode `160000` entry. Seven matching manifest rows are `migrate`; all 483 review verdict pairs remain pending. Independent specification and quality reviews have not run. |
| 2026-07-18 | T-TSC-002 README inspection reconstruction | Documentation Specialist | The original 74-path manual checklist was not retained. Baseline Git tree evidence proves exactly 75 regular target READMEs, and the dated README profile inventory singles out `examples/sample-web-service/README.md` as the only unresolved example-profile finding. That file was manually inspected: its sample-specific inventory, setup, readiness, validation, troubleshooting, and links remain truthful; disposition is narrow in-scope contract normalization. Automated exact-one validation covers all 75. |

## Verification Evidence

| Work unit | RED evidence | GREEN/aggregate evidence | Result |
| --- | --- | --- | --- |
| T-TSC-001 | Metadata RED: 76 tests, 7 failures/5 errors; lifecycle RED: 38 tests, 11 failures/4 errors; first specification-fix mutation RED: 4/4 expected failures plus one human-contract test with four expected assertion failures; exceptional validator RED: two tests produced five expected subcase failures; archive-contract RED: one focused human-owner test exited 1 because the two exact profile sections were absent; final-review fixture RED: 11 tests with four failures across three methods, all caused by the isolated target root resolving the repository target wave and emitting `promoted-manifest-missing`; CLI-shape RED: full lifecycle 101/103 with exactly the `check-promoted` and `check-archive` table subcases failing because admitted `--wave` was used as the broken argument. All RED preceded the corresponding production, contract, or test-boundary change. | Metadata 76/76; lifecycle 45/45; first specification-fix mutations 4/4 and human contract 1/1; exceptional mutations 2/2; archive-contract metadata schema 26/26 and lifecycle human contract 11/11; targeted CLI shape 1/1; exact affected fixture methods 3/3; expanded focused lifecycle 56/56; full lifecycle 103/103; exact manifest 483=422+61, sorted/unique/exact union, all pending and byte-unchanged; contract, manifest, summary, promoted, explicit-base metadata, compile, Ruff, and diff gates exit 0. Terminal independent reviews over `e5d3d8c47da144e233bf45f1a6ada45b673136ff..1de1fefca8bbd743fa57ce1c5a4889b03a0de3d8`: specification PASS C0/I0/M0 (`spec_complete: YES`) and quality APPROVED C0/I0/M0 (`QUALITY_COMPLETE: YES`). | implementation_and_reviews_complete_wave_verdicts_pending |
| T-TSC-002 | New target suite RED: 8 tests ran with eight expected failure records across stale Service metadata/sections/instruction text and the five active phantom-reference subtests. Existing README profiles passed 4/4; exact-one/native, historical-evidence, and no-gitlink characterization cases were already green. | Existing README profiles 4/4 and new target suite 8/8; 75 target READMEs exact-one; Service metadata/order/required sections and no-placeholder checks pass; shell syntax, no-mode-160000, fail-closed active absence, wave manifest/summary, explicit-base metadata, links/alignment, Ruff, compile, and diff hygiene pass. Seven matching rows are `migrate`, 476 remain `preserve`, and all 483 specification/quality verdict pairs remain pending. | implementation_complete_review_pending |
| T-TSC-003 | not_run | not_run | not_run |
| T-TSC-004 | not_run | not_run | not_run |
| T-TSC-005 | not_run | not_run | not_run |
| T-TSC-006 | not_run | not_run | not_run |

Prospective commands and expected results live in the Plan. Record actual exit
state, bounded result, and skip rationale here without raw logs or secret data.

### T-TSC-001 Exact Command Evidence

Initial implementation RED preceded production changes:

```bash
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.ArtifactInferenceTests tests.validation.test_document_metadata.MetadataValidationTests tests.validation.test_document_metadata.ReadmeProfileTests -v
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.PublicContractTests tests.validation.test_document_corpus_lifecycle.HumanContractRoutingTests tests.validation.test_document_corpus_lifecycle.ManifestValidationTests tests.validation.test_document_corpus_lifecycle.ArchiveProvenanceTests -v
```

Results: metadata exit 1 with 76 tests, 7 expected failures, and 5 expected
errors; lifecycle exit 1 with 38 tests, 11 expected failures, and 4 expected
errors. Initial GREEN at implementation commit
`6e87a97977c2de48c1c89a278b159f956825fdd1` used the same commands and passed
76/76 metadata and 38/38 lifecycle tests.

Specification-remediation RED commands preceded the follow-up production and
human-contract fixes:

```bash
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.ManifestValidationTests.test_v2_delete_rejects_a_source_that_remains_in_the_result tests.validation.test_document_corpus_lifecycle.ManifestValidationTests.test_v2_rejects_invalid_transition_rollback_and_replacement tests.validation.test_document_corpus_lifecycle.ManifestValidationTests.test_v2_rejects_sensitive_evidence_without_echoing_the_value tests.validation.test_document_corpus_lifecycle.ManifestValidationTests.test_v2_partition_plan_must_resolve_to_a_tracked_canonical_plan -v
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.HumanContractRoutingTests.test_human_contract_separates_v1_and_v2_entry_fields_and_domains -v
```

Results: the first command exited 1 with 4/4 expected failures because v2 did
not emit the required result-state, transition/rollback/replacement,
confidentiality, or partition finding codes. The second exited 1 with one test
and four expected assertion failures because the v1/v2 field/domain wording was
absent and the universal v1-only entry sentence remained. GREEN used the exact
same commands and passed 4/4 and 1/1. All finding messages remained value-free;
the sensitive sentinel was absent from rendered findings.

Final follow-up GREEN and repository gates:

```bash
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.ArtifactInferenceTests tests.validation.test_document_metadata.MetadataValidationTests tests.validation.test_document_metadata.ReadmeProfileTests
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.PublicContractTests tests.validation.test_document_corpus_lifecycle.HumanContractRoutingTests tests.validation.test_document_corpus_lifecycle.ManifestValidationTests tests.validation.test_document_corpus_lifecycle.ArchiveProvenanceTests
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-manifest --wave target-surface-convergence
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-summary --wave target-surface-convergence
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted --wave target-surface-convergence
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 32c40e11747bc0bd03789c24861d2e5d60c0e999
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m py_compile scripts/validation/check-document-metadata.py scripts/validation/check-document-corpus-lifecycle.py tests/validation/test_document_metadata.py tests/validation/test_document_corpus_lifecycle.py
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH ruff check scripts/validation/check-document-metadata.py scripts/validation/check-document-corpus-lifecycle.py tests/validation/test_document_metadata.py tests/validation/test_document_corpus_lifecycle.py
git diff --check
```

Results: exit 0 throughout; metadata 76/76, lifecycle 45/45, contract and
promoted violations 0, explicit-base metadata selected 25 with violations 0,
compile and lint passed, and diff hygiene passed. The canonical target manifest
remains exactly 483 sorted unique rows with all verdicts pending; its manifest
and summary bytes are unchanged by this follow-up.

Exceptional retry-limit remediation RED commands preceded the final bounded
production fix:

```bash
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.CandidateManifestCliTests.test_wave_archive_check_validates_candidate_before_archive_selection tests.validation.test_document_corpus_lifecycle.FinalReviewRemediationTests.test_v2_partition_plan_requires_canonical_identity_and_parent_relations -v
```

Result: exit 1; two tests produced five expected subcase failures. Wave-focused
`check-archive` returned exit 0 for removed and altered archive selectors and
noncanonical manifest bytes, while the v2 partition helper returned no finding
for a Plan missing canonical identity or using an unresolved parent. GREEN used
the exact same command and passed 2/2. Diagnostics assert stable value-safe
finding codes and do not echo candidate bodies.

Final exceptional-remediation verification repeated the focused metadata and
lifecycle commands above and passed 76/76 and 45/45. `check-contract`,
wave-resolved `check-manifest`, `check-summary`, and `check-promoted`, explicit-
base metadata selected 25 with zero violations, compile, Ruff, and diff hygiene
all exited 0. The target manifest SHA-256 remained
`d7b5289b9af8037fb9423060390b7a6f0119d205f83ebbc3a0b900f248889da8`
and its Git diff remained empty. Focused `check-archive --wave
target-surface-convergence` now exits 1 with only the planned value-safe Windows
commit/preservation provenance findings; T-TSC-003 owns that migration.

An expanded non-prescribed FinalReview selection passed 55/59 and exposed four
temporary-repository `check-impacted` fixture failures because the copied
contract resolves a target-wave manifest absent from those isolated roots. The
same three test methods reproduced the identical four failures and the same
value-safe `promoted-manifest-missing` code from an exact exported
`6766ca25f7300b6f712f6ece6f7458fb3c7fe7dc` tree. They are therefore not caused
by this remediation and were not broadened into this two-finding scope.

The exceptional validator remediation is commit
`90c803d6f48a9afeed1b7d95bf52ebe376b8d2b3`. Its specification re-review
returned C0/I1/M1: the validator findings were closed, but the human archive
owner still published a universal field shape that contradicted the separate
machine profiles. The user explicitly approved one additional bounded
exception for that contract defect and evidence synchronization.

Archive-contract RED preceded the human-owner change:

```bash
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests.test_archive_retention_human_owner_matches_machine_contract -v
```

Result: exit 1; one focused test errored at the missing exact
`content-archive`/`sdlc-archive` section boundary. GREEN at commit
`8f012c2bb57d19046f1c8c42cd54aae5868a542d` used these exact commands:

```bash
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests -v
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.HumanContractRoutingTests -v
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-manifest --wave target-surface-convergence
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-summary --wave target-surface-convergence
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 90c803d6f48a9afeed1b7d95bf52ebe376b8d2b3
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH ruff check tests/validation/test_document_metadata.py
git diff --check
```

Results: exit 0 throughout; metadata schema 26/26 and lifecycle human contract
11/11 passed; contract violations were 0; the registry-resolved manifest and
summary were current; explicit-base metadata selected 1 with zero violations,
legacy exceptions, or transition overrides; Ruff and diff hygiene passed. No
registry, template, validator, manifest, runtime, service, secret-value,
remote, or all-files pre-commit change occurred. Independent specification
re-review and separate quality review remain pending, and no passing verdict is
promoted.

The final specification review returned C0/I1/M0. Its only finding was the
previously observed fixture boundary: `FinalReviewRemediationTests` ran 11
tests with four failures across
`test_corpus_modes_reject_final_and_intermediate_markdown_symlinks_without_leakage`,
`test_impacted_cli_snapshots_safe_untracked_records_and_blocks_150th_leaf`, and
`test_cli_diagnostics_never_emit_metadata_payloads_across_modes`. Each failure
was the same value-safe `promoted-manifest-missing` result caused by an isolated
temporary repository resolving the real repository's promoted target manifest.
The user explicitly approved a test-only in-process helper boundary that
patches only `load_migration_contract` and `metadata.load_profiles` while still
invoking the real `lifecycle.main` entry point.

The exact affected methods then passed 3/3. The expanded focused lifecycle
selection, consisting of the prior 45-test focus plus all 11
`FinalReviewRemediationTests`, passed 56/56, and the focused metadata selection
passed 76/76. The full lifecycle module passed 101/103; its two remaining
failures are separate base-existing/non-gate table-shape subcases and are not
part of the accepted final-review fixture finding. The test-only remediation is
commit `a994bac09dc0c24b573a7ea204559eb5b7897671`. Production validators,
contracts, metadata profiles, target manifest, and generated summary remained
unchanged. Independent specification re-review and separate quality review
remain pending, and no passing verdict is promoted.

The user then explicitly approved only the remaining table-driven CLI-shape
correction from this latest C0/I1/M0 review state. The existing full lifecycle
RED was 101/103, and the current targeted reproduction failed exactly the
`check-promoted` and `check-archive` subcases because their broken-case input
still used admitted `--wave`. Commit
`c2a8d82832930e9bcde749b58da6843733c4f4b8` changes only those two inputs to
forbidden `--base-ref` arguments. The targeted test passed 1/1, full lifecycle
passed 103/103, exact fixture methods passed 3/3, expanded lifecycle passed
56/56, focused metadata passed 76/76, and `git diff --check` passed. Production,
contracts, profiles, manifests, and other tests remained unchanged; fresh
specification re-review and separate quality review remain pending.

CLI-shape RED/GREEN commands:

```bash
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.ReviewRemediationTests.test_all_sixteen_modes_have_table_driven_shape_contracts -v
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.FinalReviewRemediationTests.test_corpus_modes_reject_final_and_intermediate_markdown_symlinks_without_leakage tests.validation.test_document_corpus_lifecycle.FinalReviewRemediationTests.test_impacted_cli_snapshots_safe_untracked_records_and_blocks_150th_leaf tests.validation.test_document_corpus_lifecycle.FinalReviewRemediationTests.test_cli_diagnostics_never_emit_metadata_payloads_across_modes -v
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_corpus_lifecycle.PublicContractTests tests.validation.test_document_corpus_lifecycle.HumanContractRoutingTests tests.validation.test_document_corpus_lifecycle.ManifestValidationTests tests.validation.test_document_corpus_lifecycle.ArchiveProvenanceTests tests.validation.test_document_corpus_lifecycle.FinalReviewRemediationTests
PATH=/tmp/hy-home-docker-validation-venv/bin:$PATH python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.ArtifactInferenceTests tests.validation.test_document_metadata.MetadataValidationTests tests.validation.test_document_metadata.ReadmeProfileTests
git diff --check
```

The first command exited 1 before the edit with one test and exactly two failed
subcases, then passed 1/1 after the edit. The remaining commands exited 0 with
103/103, 3/3, 56/56, and 76/76 tests respectively; diff hygiene also exited 0.

### T-TSC-002 Exact Command Evidence

The focused RED preceded every sample, Storybook, script, ignore, manifest, and
summary change:

```bash
python3 -m unittest tests.validation.test_document_metadata.ReadmeProfileTests -v
python3 -m unittest discover -s tests/validation -p 'test_target_surface_contracts.py' -v
```

Results: the existing README profile suite passed 4/4. The new suite ran eight
tests and emitted eight expected failure records: three Service contract
methods failed for incomplete metadata, stale headings, and copied instruction
text, while the active-absence method failed once for each of the five live
phantom exceptions. Its all-75 exact-one/native exclusions, historical
Stage 03/04 evidence, and no-mode-`160000` characterization cases passed.

GREEN used the same commands and passed 4/4 and 8/8. The bounded static gates
were:

```bash
bash -n scripts/hooks/agent-event-hook.sh scripts/knowledge/report-graphify-health.sh
git ls-files --stage -- projects/storybook
git grep -n -F 'projects/storybook/mcp' -- .prettierignore projects/storybook scripts
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref f037630ddeef4e7cc738dd9489b9218c452510ae
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-manifest --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-summary --wave target-surface-convergence
bash scripts/validation/check-doc-implementation-alignment.sh
python3 -m py_compile tests/validation/test_target_surface_contracts.py
ruff check tests/validation/test_target_surface_contracts.py
git diff --check
```

Results: shell syntax passed; the Storybook index contained no mode `160000`;
the fail-closed active scan returned the expected no-match status 1 and no
execution error; explicit-base metadata reported zero violations; manifest and
generated summary were current; link/alignment checked 656 documents and 5,251
repository-local Markdown links with zero failures; compile, Ruff, and diff
hygiene passed. No all-files pre-commit, runtime, service, secret-value, remote,
or deployment action ran.

## Controlled Agent Pre-commit Evidence

- Command: not_run; Task 6 only.
- Allowed prefixes: not_finalized; must equal actual changed surfaces.
- Hook exit: not_run.
- Snapshot result: not_run.
- Observation boundary: Git-visible, non-ignored repository status only; the
  wrapper does not observe ignored or outside-worktree writes.
- Before/after/changed/unexpected path sets: not_run.
- Disposition: not_run.

## Review Evidence

| Work unit | Self-review | Specification review | Quality review | Findings/disposition |
| --- | --- | --- | --- | --- |
| T-TSC-001 | recorded | PASS; C0/I0/M0; `spec_complete: YES` | APPROVED; C0/I0/M0; `QUALITY_COMPLETE: YES` | Terminal independent reviews covered `e5d3d8c47da144e233bf45f1a6ada45b673136ff..1de1fefca8bbd743fa57ce1c5a4889b03a0de3d8`. All implementation-review findings are closed. This completes only the Task 1 implementation/review evidence: the advisory manifest remains 483 pending rows, and the expected Windows provenance gap remains owned by T-TSC-003; no wave verdict is promoted. |
| T-TSC-002 | recorded | pending | pending | Self-review found no scope expansion: exactly seven baseline rows changed to `migrate`, the generated summary is deterministic, all 483 row verdict pairs remain pending, the typed example keeps a `typed-example` manifest classification while carrying copyable Service metadata, and historical Stage 03/04 evidence remains truthful. Fresh independent specification and quality reviews are required. |
| T-TSC-003 | not_run | not_run | not_run | not_run |
| T-TSC-004 | not_run | not_run | not_run | not_run |
| T-TSC-005 | not_run | not_run | not_run | not_run |
| T-TSC-006 | not_run | not_run | not_run | not_run |
| Whole branch | N/A | not_run | not_run | exact final range pending |

Reviewers are separate fresh agents. A destructive row cannot pass until both
independent verdicts and all finding dispositions are recorded.

## Commit Ledger

| Work unit | Intended logical commit | Identity | Validation |
| --- | --- | --- | --- |
| Planning | `docs(plan): define target surface convergence execution` | `5c4e1d55` | metadata 10/0; traceability 46/0; alignment 656/5,251/141/0; aggregate 0 before the tracked-consumer baseline recheck |
| Planning repair | `docs(plan): repair tracked planning consumers` | `f7563631` | promoted manifest 0; generated index 1,290; coverage 1,289; inventory 913/2,145; worktree aggregate failures 0 |
| SDD compatibility | `docs(plan): align SDD task extraction` | `e5d3d8c4` | task-brief extraction and diff hygiene passed. |
| T-TSC-001 | `feat(docs): establish target corpus migration contracts` | `6e87a97977c2de48c1c89a278b159f956825fdd1` | Focused metadata 76/76; focused lifecycle 38/38; exact manifest and prescribed Task 1 gates passed. |
| T-TSC-001 review fix | `fix(docs): enforce target wave safety gates` | `6766ca25f7300b6f712f6ece6f7458fb3c7fe7dc` | Mutation RED/GREEN, focused suites, wave gates, explicit-base metadata, compile, lint, and diff hygiene; independent re-reviews remain pending. |
| T-TSC-001 exceptional review fix | `fix(docs): close target lifecycle validation gaps` | `90c803d6f48a9afeed1b7d95bf52ebe376b8d2b3` | Exceptional mutations 2/2, focused metadata 76/76, focused lifecycle 45/45, wave gates, explicit-base metadata, compile, Ruff, manifest-byte, and diff hygiene checks; its specification re-review returned C0/I1/M1 and quality review remains not run. |
| T-TSC-001 archive contract fix | `fix(docs): align archive retention profiles` | `8f012c2bb57d19046f1c8c42cd54aae5868a542d` | Focused archive human-owner RED/GREEN; metadata schema 26/26; lifecycle human contract 11/11; contract, manifest, summary, explicit-base metadata, Ruff, and diff checks passed; re-reviews remain pending. |
| T-TSC-001 fixture fix | `test(docs): isolate target wave lifecycle fixtures` | `a994bac09dc0c24b573a7ea204559eb5b7897671` | FinalReview RED 11 tests with four failures across three methods; exact affected GREEN 3/3; expanded focused lifecycle 56/56; full lifecycle 101/103 with two separate non-gate table-shape subcases; focused metadata 76/76. Production and manifest surfaces remained unchanged; re-reviews remain pending. |
| T-TSC-001 CLI shape fix | `test(docs): align lifecycle CLI shape expectations` | `c2a8d82832930e9bcde749b58da6843733c4f4b8` | Existing full RED 101/103 and targeted RED exactly two subcases; targeted GREEN 1/1, full lifecycle 103/103, exact fixtures 3/3, expanded lifecycle 56/56, metadata 76/76, and diff hygiene passed. Production and contract surfaces remained unchanged; re-reviews remain pending. |
| T-TSC-002 | `docs(examples): align sample and storybook contracts` | pending creation; immutable identity recorded in the ignored implementer report | RED/GREEN, README 75/75, shell syntax, no gitlink, fail-closed absence, manifest/summary, explicit-base metadata, links/alignment, compile, Ruff, and diff hygiene passed; independent reviews remain pending. |
| T-TSC-003 | `docs(archive): preserve Windows network note provenance` | pending | not_run |
| T-TSC-004a | `refactor(infra): retire InfluxDB 2 compatibility` | pending | not_run |
| T-TSC-004b | `chore(infra): remove unconsumed duplicate scaffolds` | pending | not_run |
| T-TSC-005 | `feat(qa): enforce target surface contracts` | pending | not_run |
| T-TSC-006 | `docs(execution): close target surface convergence` | pending | not_run |

Material review fixes and generated-only fallout receive additional rows.
The evidence-only `docs(task): record task one review remediation` commit is
ledger synchronization, not material implementation, and intentionally has no
commit-ledger row of its own.

## Deferred and Blocked Items

- Live InfluxDB data/query migration, service acceptance, deployment, release,
  remote enforcement, secrets, and runtime security remain deferred.
- SeaweedFS security scaffold activation remains a separate approved runtime
  and security chain.
- Any executable InfluxDB 2 data/query consumer blocks T-TSC-004 and routes to
  a new runtime/data Spec and Plan.
- Remote/local CI differences remain `needs_revalidation` unless dated
  read-only evidence is actually collected; no remote repair occurs.

Deferral destination: a new Stage 03 Spec and Stage 04 Plan/Task chain for the
specific runtime, data, security, deployment, or remote surface.

## Related Documents

- [Spec 133](../../03.specs/133-target-surface-contract-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-18-target-surface-contract-convergence.md)
- [Spec 131](../../03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
