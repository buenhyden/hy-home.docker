---
title: "Stage 99 and Task Lifecycle Task"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0208-TSK-0001"
parent_ids:
- "SPEC-0208-PLAN-0001"
created: "2026-10-04"
---

# Stage 99 and Task Lifecycle Task

## Objective

Record the bounded Stage 99 lifecycle-contract work, its actual validation, and
the resulting current-document migration.

## Inputs

- SPEC-0208, its Plan, REQ-0024, REQ-0026, AD-0027, AD-0030, and ADR-0037.
- `docs/99.templates/registry.json`,
  `docs/99.templates/contracts/document-profile.schema.json`, and the Stage 03
  Spec, Plan, and Task templates.
- Current nonterminal SPEC-0182 and SPEC-0204 records; SPEC-0182 Task 0001 is
  already completed with review pending and is not reopened.
- Execution ceilings are two implementation writers and one read-only review
  seat, with at most two implementation attempts (one narrower retry). Token,
  time, money, and remaining allocation ceilings are unknown; no fixed repeat
  or full-gate loop is assumed. Rules-engineer reviews policy boundaries and
  code-reviewer reviews the final code/document diff.

## Work Log

Draft package created after observing `SPEC-0207` as the registry high-water
and `SPEC-0208` as the next allocation. The Registry allocation now records
`SPEC-0208` high-water and `SPEC-0209` next number. This initial-draft
observation predates the recorded approval, readiness, execution-start, and
W2 RED entries below.

### Contract Review

Root draft review found and this draft resolves three scope defects: it now
includes the approved local commit, names W2 validator implementation and tests
as package work with a separate source owner, and covers the whole joint package
rather than only this documentation slice. This is a draft review observation,
not independent review or PASS evidence.

### Approved P02 Scope

The current native user request authorizes the exact local P02 scope. It does
not assert a GitHub identity or authorize future publication.

### Preflight and Readiness

The controller completed the recorded bootstrap, allocation, and readiness
preflight for this package on 2026-10-04.

### Execution Start

The controller dispatched implementation under the approved P02 scope on
2026-10-04. This records the start of local work, not validation or completion.

W2 witnessed RED: two focused tests ran. The blocked-row aggregation test did
not reject a frontmatter `in-progress` summary (`SpecPackageError` was not
raised); its positive case only passed because five-column rows were ignored.
The lifecycle-chain test errored because the validated-details API is absent.
These failures are implementation evidence, not acceptance PASS.

Focused GREEN then ran eight tests in 9.361 seconds with `OK`; the metadata
caller-wiring test ran one test with `OK`. Current corpus loading against
`2bba11...` reported four packages, zero findings, and five actual records.
Scoped Ruff check passed, format-check reported six files already formatted,
and diff-check passed. These are focused QA receipts; at that point, final-gate
and independent-review outcomes remained unrecorded.

The read-only policy review found that the default Task template must retain
its four-column receipt, with the five-column form shown only as an opt-in
author prompt; it also clarified the source distinction between four-column
frontmatter status and multi-item Status cells. This bounded retry corrected
the template, SDLC, and Spec wording without a final review claim.

Before that narrow correction, staged checks covered 24 files (digest
`7147d4...`): classifier selected 15 Markdown, 7 Python, 2 JSON, and no
generated files; `changed --explain` selected 13 validators; markdownlint-cli2
0.23.3 reported 15 Markdown files and zero issues; gitleaks scanned 69.96 KB
with no leaks; metadata `check-changed --base-ref main` selected 15 with zero
violations, legacy findings, or overrides against `2bba11baa...`; and corpus
lifecycle reported zero violations (5 migrations, 140 tombstones, 348
preserved records, 286 decisions, 374 rows). These checks do not cover the
narrow correction, hosted/native behavior, or live state; final recheck and
review remain pending.

W3 reconciled the two current nonterminal Tasks from their recorded evidence.
SPEC-0182-TSK-0003 is blocked by the current recovery and R2-custody inputs;
SPEC-0204-TSK-0001 is blocked by exact-image, egress, Agent-renewal, and
operational-approval inputs. Each records only its present `in-progress` to
`blocked` event. At the v3 checkpoint, completed Tasks remained unchanged. The
v4 migration permits only `parent_ids` and actual `updated` metadata
normalization; their bodies, Commit Ledgers, and status facts remain immutable.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0208 | draft | review | #contract-review |
| SPEC-0208 | review | approved | #approved-p02-scope |
| SPEC-0208 | approved | active | #execution-start |
| SPEC-0208-PLAN-0001 | draft | approved | #approved-p02-scope |
| SPEC-0208-PLAN-0001 | approved | active | #execution-start |
| SPEC-0208-TSK-0001 | draft | ready | #preflight-and-readiness |
| SPEC-0208-TSK-0001 | ready | in-progress | #execution-start |
| SPEC-0208 | in-progress | completed | #v4-local-completion |
| SPEC-0208-PLAN-0001 | in-progress | completed | #v4-local-completion |
| SPEC-0208-TSK-0001 | in-progress | completed | #v4-local-completion |

### Contract Migration

#### V4 Contract Migration

| Date | Source revision | Evidence |
| --- | --- | --- |
| 2026-10-05 | 0d1874bb3571e92d5ff5128b4fdfeb3409f92338 | #v4-contract-migration: approved v4 lifecycle-contract migration starts from the successful v3 checkpoint. |

A native temporary-path `apply_patch` attempt was denied before execution with
an invalid-payload error; it created no file and no path exception or bypass was
used. Narrow metadata after the receipt correction selected one document with
zero violations, legacy findings, or overrides.

### V4 Pre-correction Receipts

The frozen v4 source digest was `02deccfd...` across 171 staged files. Focused
QA first reported 17 tests `OK`, then four tests `OK`. Its full current-class
run reported 60 tests with 16 failures and five errors before targeted fixture
correction; it was not rerun at that point. Renderer check reported two
providers with zero drift; scoped Ruff check and format checks passed for ten
files. The bounded policy review passed.

The unstaged gate preflight failed at entrypoint identity with no selected roots;
its log is `/tmp/hy-home-p02-v4-changed-gate-20261005.log`. After the controller
explicitly staged all 171 files, the public changed-stage gate exited 1 at the
agent-governance root: 53 tests ran and two knowledge/prompt-index expectations
failed. Downstream roots were not run. Independent code review at `02deccfd...`
was blocked by three Important findings: overbroad endpoint normalization, a
default four-column result/review/coverage gap, and unreachable pre-execution
or terminal states. One narrower QA correction is in progress; no v4 gate,
independent code-review approval, acceptance, native result, hosted result, or
live result was recorded at that point.

The public changed-gate retry logged at
`/tmp/hy-home-p02-v4-changed-gate-retry-20261005.log` exited 1 because the
document-links root could not resolve `#v4-contract-migration` in this Task.
The historical 2870 warning is separate. Downstream roots and implementation
results were not run; this is not a final PASS.

### V4 Corrected-Gate Receipts

The earlier final changed gate at
`/tmp/hy-home-p02-v4-changed-gate-final-20261005.log` exited 1 in metadata
implementation: 131 tests ran with 10 failures. Downstream roots were not run.
The Audience contract correction and six affected fixture methods then passed
in 102.168 seconds.

The corrected public changed gate at
`/tmp/hy-home-p02-v4-corrected-gate-20261005.log` reached a partial pass:
metadata implementation ran 131 tests with `OK` in 368.100 seconds. Its
library root then ran 656 tests and failed with 11 failures and 7 errors in
622.716 seconds; downstream roots were not run. This is an actual failure,
not a final gate PASS. At that failed-gate point, full-source fixture
corrections remained with QA.

The staged source at `c9c0e49...` was independently reviewed as a bounded
PASS conditional on AC5's final public-gate and local-commit evidence; it is
not acceptance or closure. The staged set classified 175 paths: 156 Markdown,
14 Python, 2 JSON, and 3 generated files. `markdownlint-cli2` 0.23.3 linted
159 Markdown files with zero issues
(`/tmp/hy-home-p02-v4-markdownlint-20261005.log`); the repository's 0.22.1
pin difference is an observed tool-version fact, not native-hook evidence.
Staged-patch gitleaks scanned 432,528 bytes with no leaks. `core.hooksPath`
was observed as `/home/hyunyoun/.codex/git-hooks`; its contents and execution
remain unobserved. Numeric budget, native writer authentication, hosted
checks, and live behavior remain unknown or unobserved.

### V4 Verified-Gate Receipts

The supported verified changed gate at
`/tmp/hy-home-p02-v4-verified-gate-20261005.log` exited 0 against reviewed
digest `7049e560...`. Metadata implementation ran 131 tests with `OK` in
368.810 seconds; the library root ran 656 with `OK` in 627.221 seconds;
supply-chain ran 239 with `OK` in 78.927 seconds; and the final root ran 176
with `OK` in 48.527 seconds. Metadata active reported 479 documents and zero
violations; document links reported 10,939 links across 1,097 documents with
zero errors and one separate historical 2870 warning; lifecycle and archive
checks reported zero findings. Static Compose validation ran; no live service
operation occurred.

`changed --explain` selected the supported 13 validators. The final metadata
command, `rtk proxy /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python
scripts/validation/check-document-metadata.py --mode check-changed --base-ref
main`, exited 0 with 132 selected documents, zero violations, zero legacy
findings, and zero overrides against merge-base
`2bba11baa1009e673a763a727b0a9e3d7e0bb5a7`; its log is
`/tmp/hy-home-p02-v4-metadata-final-20261005.log`.

The independent code review at `7049e560...` passed source, specification,
quality, and security review. At that pre-source-commit point, together with
the verified gate, this accepted AC1--AC4 evidence only and left AC5 pending
the actual v4 source commit. The final staged source classifies 176 paths: 156
authored Markdown files, 15 Python files (six consumer sources and nine test
modules), two JSON files, and three generated files. No native writer
authentication, hosted result, live result, hook execution, or numeric budget
result is observed.

### V4 Local Completion

The observed v4 source commit
`a36f83a1255ff22fbd80c91e27ee90b58480e3e4` was created on 2026-10-05 by
`rtk proxy git commit -m 'fix(governance): Align v4 lifecycle contracts and consumers'`
with exit 0. It contains 176 files, 3,675 insertions, and 1,226 deletions; the
worktree was clean after the commit. The pre-commit Task-only metadata check
selected one document with zero violations, legacy findings, or overrides;
Task-only markdownlint reported one file with zero issues; staged gitleaks
scanned 445,937 bytes with no leaks; and Commitizen's 75-character message
check succeeded. No installed-hook execution output was observed.

This local source-commit receipt, the verified gate, and independent review
complete W4 and AC5. It does not prove native writer authentication, hosted
checks, or live behavior; those remain unknown or unobserved.

Closure-candidate digest
`d11d5c6e571b7e7946e9410674c62d8e7de8ab6e5a3fe75e77f157a4eb705851`
received independent Specification, quality, and security review reported as
PASS; review is not authorization. Its narrow metadata command with
`--mode check-changed --base-ref main --changed-path` for the Spec, Plan, and
Task exited 0 with three selected documents and zero violations, legacy
findings, or overrides. Corpus lifecycle against `main` exited 0 with zero
violations; archive recovery reported 5 migrations, 140 tombstones, 348
preserved records, 286 decisions, and 374 rows with zero violations. Links
alignment exited 0 for 1,097 documents and 10,940 links with zero failures and
one separate historical 2870 warning. Package-record lint reported three files with
zero issues; staged gitleaks scanned 11,306 bytes with no leaks; and the
75-character Commitizen receipt-message check succeeded. These are
closure-candidate facts only: the ensuing Task-only narrow check and any finite
receipt commit are not claimed here, and no future receipt SHA is recorded.

### Inventory

| Work unit | Owner | Surface or consumer | Disposition |
| --- | --- | --- | --- |
| W1 | Stage 99 Registry | `docs/99.templates/registry.json`; metadata and lifecycle validators consume profile and common contracts | Amend minimal common contract and SPEC allocation only. |
| W2 | Stage 99 profile schema and validator | `docs/99.templates/contracts/document-profile.schema.json`; `scripts/lib/document_governance/spec_packages.py` and focused tests consume the new common fields | Add optional typed fields, implement fail-closed consumer behavior and tests; leave the frontmatter schema unchanged. |
| W2 | Stage 99 templates | `templates/specs/{spec,plan,task}.template.md`; Stage 03 authors consume them | Align prompts and receipt/event tables. |
| W3 | Stage 03 navigation | `docs/03.specs/README.md`; human package discovery consumes it | Add SPEC-0208 route and describe derived summary semantics. |
| W3 | Current package records | SPEC-0182 and SPEC-0204 nonterminal Plan/Task prose; authors and reviewers consume it | Migrate recorded terminology only; do not reopen completed or terminal records. |
| W3 | Lifecycle families and navigation | Requirements, AD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Postmortem, Research, Audit, Data, current archive catalog, and pure-navigation README profiles; Registry and profile consumers consume them | Apply the approved named lifecycle map, direct Plan/Task parents, common/readme navigation shape, and active navigation state. Retain roles, providers, knowledge, prompts, runtime projections, contracts, and unsupported/frozen profiles unless separately named or pure navigation. |
| W4 | Validation, review, and integration | Existing validator scripts, independent reviewer, and local Git | Recorded owner-selected checks, review, and the approved local source commit. |

The observed Registry has 50 profiles, 39 template roles, and 40 files under
`docs/99.templates/templates/`. The complete profile inventory is:
`requirements-package`, `architecture-description`, `adr`, `spec`,
`data-model-contract`, `openapi-contract`, `graphql-contract`,
`proto-contract`, `plan`, `task`, `guide`, `policy`, `runbook`, `incident`,
`postmortem`, `reference-category-readme`, `research`, `audit`, `data`,
`research-member`, `audit-member`, `migration`, `tombstone`,
`archive-retention-catalog`, `documentation-readme`, `repository-readme`,
`package-readme`, `runtime-governance-readme`, `readme`,
`incident-year-readme`, `governance-policy`, `governance-hook-policy`,
`governance-role`, `governance-skill`, `governance-provider`,
`governance-provider-index`, `governance-sdlc`, `governance-knowledge`,
`governance-knowledge-index`, `governance-prompt`, `governance-prompt-index`,
`runtime-projection-claude`, `runtime-projection-codex`, `template-source`,
`generated`, `unsupported`, `archive-record-completed`,
`archive-record-superseded`, `archive-record-retired`, and
`archive-record-resolved`.

The complete template-role inventory is: `archive/migration`,
`archive/tombstone`, `common/documentation-readme`, `common/package-readme`,
`common/readme`, `common/repository-readme`, `common/runtime-governance-readme`,
`governance/claude-agent`, `governance/codex-agent`,
`governance/hook-policy`, `governance/knowledge`, `governance/policy`,
`governance/prompt`, `governance/provider`, `governance/role`,
`governance/sdlc`, `governance/skill`, `operation/guide`,
`operation/incident`, `operation/policy`, `operation/postmortem`,
`operation/runbook`, `reference/audit`, `reference/audit-pack`,
`reference/category-readme`, `reference/data`, `reference/data-pack`,
`reference/research`, `reference/research-pack`, `sdlc/architecture-decision`,
`sdlc/architecture-description`, `sdlc/data-model`, `sdlc/graphql`,
`sdlc/openapi`, `sdlc/plan`, `sdlc/proto`, `sdlc/requirement`, `sdlc/spec`, and
`sdlc/task`. Each role maps to its existing source in `registry.json`; its
source is checked by `metadata/reference.py`. The fortieth file is the
template README, classified as `readme`, rather than an unregistered template.

The Registry, profile schema, and frontmatter schema are machine inputs loaded
by `registry.py`; `metadata/profile.py`, `metadata/heading.py`,
`metadata/reference.py`, `spec_packages.py`, links, references, operations,
archive, and runtime projection validation consume the Registry as applicable.
The frontmatter schema remains unchanged because no value grammar changes.
Non-Markdown OpenAPI, GraphQL, and Proto template sources, both JSON schemas,
and the Registry classify as `None` where classification is inapplicable; they
are registered machine inputs, not missing profiles. `archive-retention-catalog`,
`incident-year-readme`, `governance-provider-index`,
`governance-knowledge-index`, `governance-prompt-index`, `template-source`,
and fallback/archive-record profiles intentionally have no dedicated template.
No dedicated profile is created for a lifecycle event, completion item, role,
or machine input because these are capacity within existing contracts.

For the v4 scope, `requirements-package` maps to Requirement;
`architecture-description` to AD; `adr` to ADR; `spec`, `plan`, and `task` to
the Stage 03 family; `guide`, `policy`, and `runbook` to operational living
documents; `postmortem` to publication; and `research`, `audit`, `data`, and
their pack members to reference publication. `migration` and `tombstone` are
route records. `documentation-readme`, `repository-readme`, `package-readme`,
`runtime-governance-readme`, `readme`, and `incident-year-readme` retain their
path-specific profile IDs while using `common/readme` only when they are pure
navigation. Governance policies, hook policies, SDLC, and skills use the
operational living lifecycle; roles, providers, knowledge, prompts, runtime
projections, contracts, template sources, generated records, and unsupported
or frozen profiles retain their existing mappings.

All Stage 99 source files observed are `README.md`, `registry.json`,
`contracts/document-frontmatter.schema.json`,
`contracts/document-profile.schema.json`, `templates/README.md`, and the 39
role sources: `architecture/{decision,description}.template.md`,
`archive/{migration,tombstone}.template.md`, `common/readme-{category,documentation,package,repository,runtime-governance,stage}.template.md`,
`governance/{contract,control,knowledge,prompt,provider,role,rule,skill}.template.md`,
`operations/{guide,incident,policy,postmortem,runbook}.template.md`,
`references/{audit-pack,audit,data-pack,data,research-pack,research}.template.md`,
`requirements/requirement-package.template.md`,
`runtime/{claude-agent.template.md,codex-agent.template.toml}`, and
`specs/{plan,spec,task}.template.md` plus
`specs/contracts/{data-model.template.md,openapi.template.yaml,schema.template.graphql,service.template.proto}`.
The Registry owner reaches consumers through `registry.py:27-32` and
current loader/classifier and validator functions in
`scripts/lib/document_governance/registry.py`
(`load_registry`, `validate_registry`, `classify_path`),
`metadata/lifecycle.py` (`validate_record`), `metadata/reference.py`
(`validate_repository_contracts`), `spec_packages.py`
(`validate_spec_package_lifecycle` and
`validate_repository_spec_package_lifecycle_details`), and `taxonomy.py`
(`classify_path` and `validate_stable_identity`).
`scripts/operations/provider_surface_renderer.py` (`render_all`) consumes the
navigation surface. These verified file/function relationships identify
consumers, not policy owners; earlier line positions are v3 baseline facts,
not current anchors. `git show --name-status
a36f83a1255ff22fbd80c91e27ee90b58480e3e4` is the complete 176-path manifest:
156 authored Markdown migrations, two Registry/profile JSON contracts, three
generated outputs, six consumer sources (`metadata/lifecycle.py`,
`metadata/reference.py`, `registry.py`, `spec_packages.py`, `taxonomy.py`, and
`operations/provider_surface_renderer.py`), and nine test modules.

## Verification Evidence

### Focused QA

| Command | Result | Scope and limit |
| --- | --- | --- |
| `rtk /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_multi_item_task_status_is_derived_from_registered_rows tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_package_lifecycle_events_validate_the_actual_transition_chain` | RED: 2 tests; the event API raised `AttributeError`. | Initial missing aggregation/event API evidence. |
| `rtk /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_multi_item_task_status_is_derived_from_registered_rows` | RED: 1 test failed because `SpecPackageError` was not raised. | Initial blocked-summary mismatch evidence. |
| `rtk /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_multi_item_task_status_is_derived_from_registered_rows tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_multi_item_rows_reject_invalid_status_result_and_cancellation tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_completed_spec_counts_only_completed_pass_item_rows tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_old_registry_and_preserved_load_do_not_require_new_tables tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_package_lifecycle_events_validate_the_actual_transition_chain tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_package_lifecycle_events_reject_unbound_or_broken_chains tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_current_receipt_carrier_accepts_blocked_but_not_ready tests.lib.document_governance.test_registry.ActualTaskLifecycleTransitionTests` | GREEN: 8 tests, `OK`, 9.361 s. | Item summary, cancellation/PASS guards, historical compatibility, events, and receipt carrier. |
| `rtk /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_changed_mode_retains_repository_contract_findings` | GREEN: 1 test, `OK`. | Metadata caller wiring. |
| Current `load_spec_packages` and lifecycle details against `2bba11baa1009e673a763a727b0a9e3d7e0bb5a7` | GREEN: 4 packages, 0 findings, 5 validated transitions. | Current corpus only; no hosted, native, or live result. |

Scoped Ruff/diff results are recorded in Work Log. Exact scoped command strings
for those checks were not supplied, so this Task records their tool, scope, and
result only.

### V3 Retry Checkpoint

The narrow generic-error correction first reproduced one RED, then two focused
GREEN checks in 4.648 seconds; the two scoped static checks passed. The final
focused retry ran four tests in 2.673 seconds with exit 0, the full
`SpecPackageTests` compatibility run passed 54 tests in 56.126 seconds with
exit 0, and the current-repository load passed one test in 0.486 seconds with
exit 0. The base-aware helper against
`2bba11baa1009e673a763a727b0a9e3d7e0bb5a7` reported four packages, zero
findings, and five validated transitions; eight Python static checks passed.

The public supported changed-profile retry exited 0; its log is
`/tmp/hy-home-p02-changed-gate-retry-20261005.log`. It ran after the source
corrections represented by reviewed digest
`5f84f235accacad65d3bbeb326763ff8954fa8dc3f5f8c97f3e3d7f194704d2d`.
These are local repository receipts only: native writer-payload authentication,
hosted checks, and live behavior remain unobserved.

The first changed-gate attempt exited 1 at the document-links root because the
migrated SPEC-0204 criterion 4/W5 owner link named a non-existent POL-0079
filename. The verified owner is `0079-application-auth-integration.md`; that
attempt did not execute downstream roots. The later supported changed-profile
retry passed as recorded above. The separate historical 2870 archive warning
remains a baseline limitation, not this failure.

Code review at digest `a5378c82...` reproduced a four-column/multi-item
bypass and identified the POL-0079 link defect. At that review point both were
pending. The narrow validator and link corrections are now implemented and
reviewed at `5f84f235accacad65d3bbeb326763ff8954fa8dc3f5f8c97f3e3d7f194704d2d`.
The supported runner has only `changed`, `full`, and `explain` profiles; the
supported changed retry passed without a custom filtered wrapper.

| Acceptance criterion | Plan work unit | Status | Task result | Durable owner |
| --- | --- | --- | --- | --- |
| 1 | W1 | completed | PASS | [V4 verified-gate receipts](#v4-verified-gate-receipts) |
| 2 | W2 | completed | PASS | [V4 verified-gate receipts](#v4-verified-gate-receipts) |
| 3 | W2 | completed | PASS | [V4 verified-gate receipts](#v4-verified-gate-receipts) |
| 4 | W2 | completed | PASS | [V4 verified-gate receipts](#v4-verified-gate-receipts) |
| 5 | W3 | completed | PASS | [V4 verified-gate receipts](#v4-verified-gate-receipts) |
| 5 | W4 | completed | PASS | [V4 local completion](#v4-local-completion) |

## Review Evidence

| Acceptance criterion | Acceptance | Evidence |
| --- | --- | --- |
| 1 | accepted | Source review and the verified changed gate at `7049e560...`. |
| 2 | accepted | Focused corrections, source review, and the verified changed gate at `7049e560...`. |
| 3 | accepted | Source review and the verified changed gate at `7049e560...`. |
| 4 | accepted | Independent source/specification/quality/security review and the verified changed gate at `7049e560...`. |
| 5 | accepted | [V4 local completion](#v4-local-completion), verified gate, and independent review. |

Rules-engineer policy review passed for the corrected contract at reviewed
digest `a5378c82...`. Earlier code-review receipts at `5f84f235...` and
`c9c0e49...` remain dated evidence; the current independent review at
`7049e560...` passed source, specification, quality, and security. These
read-only reviews do not execute or authenticate an operation. The evidence
commit and same-package v4 amendment are recorded below. The v3 checkpoint
`0d1874...` is actual local history; P01 at `68e0bfd...` remains a separate
local, completed, unmerged branch and is not imported here.

## Commit Ledger

Prepared v4 subject: `fix(governance): Align v4 lifecycle contracts and consumers`.

The prior v3 checkpoint commit is
`0d1874bb3571e92d5ff5128b4fdfeb3409f92338`, created by
`rtk proxy git commit -m 'fix(governance): Normalize Task lifecycle evidence'`
with exit 0 for 24 files. No installed-hook execution output was observed.

The v4 source commit is
`a36f83a1255ff22fbd80c91e27ee90b58480e3e4`, created by
`rtk proxy git commit -m 'fix(governance): Align v4 lifecycle contracts and consumers'`
with exit 0 for 176 files (3,675 insertions and 1,226 deletions). Its worktree
was clean. Push, PR, merge, remote checks, installed-hook execution, native
writer authentication, hosted checks, and live behavior are not recorded as
performed. Any later finite receipt-commit OID belongs in the external final
report; this Task does not claim its own future SHA. Rollback reverses the
source and any receipt commits with `git revert`, never reset or history
rewriting.

## Rulings

The initial template and Task state contain no seeded approval or timestamp.
Approval-source authentication remains a manual, separate boundary from the
structural fields introduced by this package.

## Deferred Items

W2 owns validator implementation and tests under this package; this Task
records their evidence. The approved v4 amendment now owns the current
lifecycle-family, direct-parent, result, review, and generation contract;
later value-grammar changes still require their own approved contract.
