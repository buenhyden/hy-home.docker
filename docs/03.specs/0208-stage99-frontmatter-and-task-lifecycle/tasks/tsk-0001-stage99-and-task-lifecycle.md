---
title: "Stage 99 and Task Lifecycle Task"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0208-TSK-0001"
parent_ids:
- "SPEC-0208"
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
and diff-check passed. These are focused QA receipts; final gate and review
remain unrecorded.

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
`blocked` event. Completed Tasks remain unchanged.

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

### Inventory

| Work unit | Owner | Surface or consumer | Disposition |
| --- | --- | --- | --- |
| W1 | Stage 99 Registry | `docs/99.templates/registry.json`; metadata and lifecycle validators consume profile and common contracts | Amend minimal common contract and SPEC allocation only. |
| W2 | Stage 99 profile schema and validator | `docs/99.templates/contracts/document-profile.schema.json`; `scripts/lib/document_governance/spec_packages.py` and focused tests consume the new common fields | Add optional typed fields, implement fail-closed consumer behavior and tests; leave the frontmatter schema unchanged. |
| W2 | Stage 99 templates | `templates/specs/{spec,plan,task}.template.md`; Stage 03 authors consume them | Align prompts and receipt/event tables. |
| W3 | Stage 03 navigation | `docs/03.specs/README.md`; human package discovery consumes it | Add SPEC-0208 route and describe derived summary semantics. |
| W3 | Current package records | SPEC-0182 and SPEC-0204 nonterminal Plan/Task prose; authors and reviewers consume it | Migrate recorded terminology only; do not reopen completed or terminal records. |
| W4 | Validation, review, and integration | Existing validator scripts, independent reviewer, and local Git | Run and record owner-selected checks and review; make the approved local commit only after receipts exist. |

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
`registry.py:2248`; profile classification reaches `metadata/profile.py:55`
and `metadata/profile.py:2140`; template-section enforcement reaches
`metadata/heading.py:735`; role-source and Markdown-template checks reach
`metadata/reference.py:1151-1176`; Spec receipt and lifecycle consumers reach
`spec_packages.py:1054-1152` and `metadata/reference.py`. These paths consume
contracts and do not become policy owners.

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
| 1 | W1 | in-progress | Draft inventory recorded; implementation and review evidence pending. | SPEC-0208 Task 0001 |
| 2 | W2 | in-progress | Contract fields and validator implementation are in place; focused and compatibility tests passed in v3. | Stage 99 Registry and profile schema |
| 3 | W2 | in-progress | Spec, Plan, and Task templates express the bounded authoring contract; focused and compatibility tests passed in v3. | Stage 99 templates |
| 4 | W2 | in-progress | Earlier RED is preserved above; v3 implementation and focused/compatibility tests passed. The same-package v4 contract amendment remains pending. | W2 validator owner |
| 5 | W3 | in-progress | Current nonterminal Task summaries, evidence rows, and Plan references migrated from recorded facts. | SPEC-0208 Task 0001 |
| 5 | W4 | draft | Checkpoint complete: final evidence commit and the same-package v4 amendment remain pending. | SPEC-0208 Task 0001 |

## Review Evidence

Rules-engineer policy review passed for the corrected contract at reviewed
digest `a5378c82...`. Code-reviewer re-review passed and approved the corrected
source at `5f84f235accacad65d3bbeb326763ff8954fa8dc3f5f8c97f3e3d7f194704d2d`.
Both are read-only and cannot approve, execute, or authenticate an operation.
The evidence commit and same-package v4 amendment remain pending.

## Commit Ledger

Prepared subject: `fix(governance): Normalize Task lifecycle evidence`.

No commit SHA exists. Local commit, push, PR, merge, and remote checks are not
recorded as performed.

## Rulings

The initial template and Task state contain no seeded approval or timestamp.
Approval-source authentication remains a manual, separate boundary from the
structural fields introduced by this package.

## Deferred Items

W2 owns validator implementation and tests under this package; this Task
records their evidence. Any future lifecycle enum or stored package state
requires a separate approved contract change.
