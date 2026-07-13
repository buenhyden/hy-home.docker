---
status: active
artifact_id: task:2026-07-13-document-contract-canonicalization
artifact_type: task
parent_ids:
  - plan:2026-07-13-document-contract-canonicalization
---
<!-- Target: docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md -->

# Task: Document Contract Canonicalization

## Overview

This ledger tracks the six dependency-ordered implementation and review tasks
for Spec 129. It is the durable evidence source for registry, template,
contract, research, audit, repository/CI, generated-output, and controlled QA
work. Corpus migration and remote enforcement remain later sub-projects.

## Inputs

- **Parent Spec**:
  [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- **Parent Plan**:
  [Implementation plan](../plans/2026-07-13-document-contract-canonicalization.md)
- **Canonical Audit**:
  [Implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Canonical Research**:
  [Research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Registry**:
  [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)

## Working Rules

- Execute one task at a time with a fresh implementer and separate reviewer.
- Use RED/GREEN for code, validator, parser, template, and repository-gate
  behavior.
- Mark a task Done only after Spec PASS and Quality APPROVED with Critical 0
  and Important 0.
- Keep ignored briefs, review packages, and transient handoffs under ignored
  repo-support scratch; promote only durable evidence here.
- Preserve historical payloads and keep the 892-record corpus advisory.
- Never read secret values, raw logs, auth files, tokens, credentials, private
  keys, or shell history.
- Do not mutate runtime, Compose, infrastructure, deployment, provider-global,
  model-policy, ruleset, environment, or remote branch-protection state.
- Never run direct all-files pre-commit. Reserve the controlled wrapper for
  T-DCC-006 from an initially clean linked worktree.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 99 contracts and templates | User approval of Spec 129 and this staged foundation design | Registry, support contracts, typed templates, Release routing | Spec 129 baseline and `d900eabd` generated inventory | Per-task diffs, tests, and reviews | Revert the exact logical task commit | No copied secret values, raw logs, auth, tokens, credentials, or shell history |
| Stage 00 authoring governance | User approval permitting governance/contract changes | Documentation protocol and authoring matrix | Current Stage 00 routes at branch base `e2954cc3` | Linked registry/family/profile duties and review verdict | Revert Task 2 or Task 4 commit | No provider-global or user config mutation |
| Canonical Stage 90 research/audit | User approval to consolidate related documents into canonical packs | 2026-07-05 research and current implementation audit only | 892-record inventory; 11 reports/161 rows | Source-backed research and current evidence wording | Revert logical commit; regenerate owner outputs | Preserve historical commands, dates, counts, verdicts, and results |
| Validation and tracked CI | User approval of non-runtime harness improvement | Metadata parser/tests, repository contracts, existing read-only CI route | Existing changed/new metadata and `repo-contracts` job | RED/GREEN evidence and `failures=0` | Revert Task 1/5 commit | No remote run or protection claim |
| `_workspace` evidence | User-approved repo-support distinction and existing contract | Two tracked READMEs and independent repository enforcement | Existing allowlist and ignored repo-support scratch | Audit coverage only; no docs metadata inclusion | Revert audit wording | Do not inspect diagnostics, logs, auth, tokens, secret values, or shell history |
| Controlled pre-commit | User-approved wrapper design | Final clean linked-worktree QA gate | Clean Git status and wrapper contract | Command/path evidence in this ledger | Stop on unexpected paths; do not clean/hide output | Git-visible, non-ignored repository paths only |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-DCC-001 | Extend registry/parser with families, key order, README profiles, and parent serialization. | impl/test | Registry Model; VAL-129-001/004/005 | Task 1 | RED/GREEN metadata tests and independent review | Documentation Metadata Engineer | Done |
| T-DCC-002 | Complete typed Markdown templates and Release routing. | impl/test/doc | Template/Release Contracts; VAL-129-002/003 | Task 2 | Instantiation fixtures, route checks, review | Documentation Template Engineer | Done |
| T-DCC-003 | Align human contracts and canonical external research. | doc/research | Canonical Ownership; External Source Basis | Task 3 | Source verification, ownership scan, review | Documentation Specialist | Review Pending |
| T-DCC-004 | Align Stage 00 authoring and canonical audit truth, including `_workspace`. | doc/eval | Guardrails; VAL-129-002/005/006 | Task 4 | 11/161, semantic freshness, review | Agentic Workflow Specialist | Todo |
| T-DCC-005 | Integrate fail-closed repository and CI enforcement. | impl/test/ci | Validator Interfaces; VAL-129-007 | Task 5 | Adversarial tests, repo contracts, workflow security, review | QA / CI Engineer | Todo |
| T-DCC-006 | Regenerate evidence, run full QA/wrapper, review the branch, and close. | test/doc/eval | Verification; VAL-129-007/008 | Task 6 | Full bundle, wrapper, final review | QA / Documentation Lead | Todo |

## Phase View

### Phase 1 — Executable Foundation

- [x] T-DCC-001 Registry, parser, README profiles, and parent serialization
- [x] T-DCC-002 Typed templates and Release routing

### Phase 2 — Human and Evidence Alignment

- [ ] T-DCC-003 Human contracts and canonical external research — implementation complete; independent review pending
- [ ] T-DCC-004 Stage 00 authoring and canonical audit reconciliation

### Phase 3 — Enforcement and Closure

- [ ] T-DCC-005 Repository and CI contract enforcement
- [ ] T-DCC-006 Generated evidence, full QA, reviews, and closure

## Review Ledger

### T-DCC-001 Implementation Evidence

- **RED**:
  `python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.MetadataValidationTests tests.validation.test_document_metadata.ReadmeProfileTests -v`
  failed as expected before implementation because the three registry members,
  deterministic-order findings, and README classifier/consumer APIs were absent
  (`FAILED`; two assertion failures plus expected missing-schema/API errors).
- **GREEN**: the same focused command passed `31/31`; the full
  `tests.validation.test_document_metadata` module passed with `91` discovered
  tests and exit `0`.
- **Compatibility**:
  `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e2954cc3`
  retained the interface and passed with `selected=10 violations=0`.
  `--mode check-active` retained its interface and reported the preserved
  advisory migration debt (`selected=364 violations=1290`) without triggering
  corpus rewrites. `git diff --check` and Python compilation passed.
- **README boundary**: all `228` tracked `README.md` paths classify to exactly
  one declared profile; the fixture verifies byte-for-byte that classification
  performs no writes. No README or historical corpus document was modified.
- **Graphify**: `graphify update .` rebuilt `22860` nodes and `23825` edges.
  Health remained advisory only for two cross-root inferred edges; tracked
  source, Stage 00, Spec 129, and the Stage 04 plan were used as authoritative
  corroboration. Generated Graphify collateral was excluded from this task.
- **Protected surface**: changes are limited to the registry, metadata checker,
  focused validation tests, and this Task 1 ledger. Task 2+ templates, human
  contracts, audit/research packs, repository/CI gates, runtime, secrets,
  provider-global state, and remote GitHub state remain untouched.
- **Implementer self-review**: Spec mapping PASS and code-quality review PASS
  with Critical `0`, Important `0`, Minor `0`. This is implementer evidence,
  not the required independent approval.
- **Independent task review**: the combined reviewer read brief, report, and
  exact diff package for `237aa5d7..39eb562e`, returned Spec PASS and Task
  Quality Approved with Critical `0`, Important `0`, and Minor `0`, and
  confirmed exact registry keys/order, fail-closed README classification,
  declared-consumer semantics, parent serialization, test coverage, scope, and
  CLI compatibility.

### T-DCC-002 Implementation Evidence

- **RED**:
  `python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests -v`
  executed the new complete-mapping, instantiation, and Release-route fixtures
  and failed for the intended gaps: the five Markdown Spec-child templates and
  harness task template were absent from `template_sources`, while the Release
  template, Stage 05 index, and coordinated routing were missing. The RED
  fixture checkpoint is `3591fcd5`.
- **GREEN**: the same focused command passed `5/5`. It validates all `20`
  registered copyable typed Markdown sources, instantiates each target through
  `validate_record()` with a valid parent manifest, checks the Release route
  across Stage 00/05/99 catalogs, and confirms no Release event leaf exists.
  The full `tests.validation.test_document_metadata` module passed `93/93`.
- **Compatibility**:
  `bash scripts/validation/check-doc-traceability.sh` passed with
  `catalog_pairs_total=46` and `failures=0`;
  `bash scripts/validation/check-repo-contracts.sh` passed all sections;
  `git diff --check` passed.
- **Template boundary**: exactly the five Markdown Spec-child templates now
  declare `artifact_type: spec`; the harness task contract declares
  `artifact_type: task`; Release declares `artifact_type: release`. The YAML,
  GraphQL, and Protobuf templates remain unchanged and have no Markdown
  frontmatter. Existing template-specific body contracts were preserved.
- **Release boundary**: routing is
  `docs/05.operations/releases/YYYY-MM-DD-release-name.md`; the new Stage 05
  index requires real event evidence and distinguishes changelog/readiness
  inputs from execution. No Release event record was created. Deployment
  runtime remains owned by Spec 127 or a later approved runtime chain.
- **Graphify**: `graphify update .` completed with `22889` nodes and `23854`
  edges. Its generated tracked collateral was restored because Task 2 does not
  own generated evidence; tracked sources, Stage 00, Spec 129, and this Stage
  04 ledger remain authoritative.
- **Protected surface**: changes are limited to approved Stage 00 authoring
  routing, Stage 04 evidence, Stage 05 Release indexing, Stage 99 templates and
  catalogs, and metadata tests. Runtime, Compose, infrastructure, secrets,
  workflows, provider-global state, deployment execution, and remote GitHub
  state were not changed.
- **Implementer self-review**: Spec mapping PASS and code/document quality PASS
  with Critical `0`, Important `0`, Minor `0`.
- **Independent task review**: the reviewer checked the exact two-commit range
  `0ae9fe81..0445f336`, returned Spec PASS and Task Quality Approved with
  Critical `0`, Important `0`, and Minor `0`, and confirmed all twenty typed
  Markdown instantiations, coordinated Release routing with no event leaf,
  Spec 127 deployment separation, machine-readable template exclusion, unique
  spec-child bodies, and preserved harness approval/evidence sections.

### T-DCC-003 Implementation Evidence

- **Source verification**: on `2026-07-13`, re-opened the official YAML 1.2.2,
  GitHub YAML frontmatter/content practices, CommonMark 0.31.2, GFM, GitHub
  ruleset/protected-branch/required-check, deployment-environment, and
  deployment-history sources. `diataxis.fr` returned HTTP 429 from the task
  environment, so the four-type model was corroborated from the official
  `evildmp/diataxis-documentation-framework` source repository whose homepage
  points to the cited site. Normative external claims use direct primary URLs.
- **Ownership separation**: added separate SDLC, common/repository, and README
  human contracts. They route exact keys, profiles, transitions, path globs,
  heading arrays, parent ordering, and validator behavior to the registry and
  checker rather than copying executable semantics into prose or catalog
  READMEs.
- **Canonical research**: updated only the 2026-07-05 pack README and five
  named leaves in place. The earlier `2026-07-04`, `2026-07-10`, and
  `2026-07-11` source/count/verdict records remain visible, including 27
  workspace categories, 6 workflows/21 jobs, 15 quality jobs, 23 hook IDs,
  12 executed local gates plus one advisory recommendation, the historical 12
  remote contexts, and provider-model 145/142 routing. No duplicate pack or
  dated audit snapshot was created or rewritten.
- **Validation**: official-source ownership scan passed; the new-contract
  placeholder scan returned zero matches; traceability passed with
  `catalog_pairs_total=46 failures=0`; implementation alignment passed with
  `stage_docs_total=644`, `repo_local_markdown_links_checked=5093`, and
  `failures=0`; explicit-base metadata passed with
  `selected=16 violations=0`; `git diff --check` passed.
- **Generated boundary**: the broader repository-contract run reached only
  expected stale generated outputs for the LLM Wiki index/coverage and
  frontmatter semantic inventory after adding/changing tracked docs. Task 6
  owns generated refresh, so this task did not edit those outputs. Graphify was
  not refreshed because this task changes documentation only and generated
  collateral remains outside its scope.
- **Protected surface**: the registry, validator, tests, copyable templates,
  Task 4 audit pack, dated audit snapshots, generated outputs, runtime, Compose,
  infrastructure, secrets, provider/model policy, workflows, deployment, and
  remote GitHub settings remain unchanged.
- **Initial implementer self-review**: Spec mapping PASS and documentation/source
  quality PASS with Critical `0`, Important `0`, Minor `0`. Independent review
  remains pending and no approval verdict is claimed.
- **Independent review round 1**: Spec Issues / Needs fixes with Critical `0`,
  Important `1`, Minor `0`. I-01 found that `lifecycle-status.md` still copied
  the complete transition graph, terminal semantics, override-manifest fields,
  checker CLI flag, and enforcement behavior despite the registry's sole-owner
  boundary.
- **I-01 remediation**: replaced the duplicate executable policy with concise
  human evidence review, rejection handling, and ambiguity escalation guidance;
  exact transition, exception, and enforcement semantics now route directly to
  `document-metadata-profiles.yaml` and `check-document-metadata.py`.
- **Remediation validation**: ownership/duplicate scan passed with zero matches;
  placeholder scan passed with zero matches; explicit-base metadata passed with
  `selected=17 violations=0 legacy_exceptions=0 transition_overrides=0`;
  traceability passed with `catalog_pairs_total=46 failures=0`; implementation
  alignment passed with `stage_docs_total=644`,
  `repo_local_markdown_links_checked=5093`, and `failures=0`; `git diff --check`
  passed. Remediation self-review is C0/I0/M0; independent re-review remains
  pending.

| Task | Implementation Commit(s) | Spec Compliance | Quality | Findings / Resolution | Reviewer Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-DCC-001 | `39eb562e` | PASS | Approved | C0/I0/M0; no remediation required | `review-237aa5d7..39eb562e.diff`; combined reviewer verdict | Done |
| T-DCC-002 | `3591fcd5`, `0445f336` | PASS | Approved | C0/I0/M0; no remediation required | `review-0ae9fe81..0445f336.diff`; combined reviewer verdict | Done |
| T-DCC-003 | Pending Task 3 handoff commit | Round 1 Issues; re-review pending | Review Pending | Round 1 C0/I1/M0; I-01 remediated; remediation self-review C0/I0/M0 | `.superpowers/sdd/task-3-report.md`; promote re-review verdict after approval | Review Pending |
| T-DCC-004 | Pending | Pending | Pending | Pending | Ignored SDD report promoted here after approval | Pending |
| T-DCC-005 | Pending | Pending | Pending | Pending | Ignored SDD report promoted here after approval | Pending |
| T-DCC-006 | Pending | Pending | Pending | Pending | Whole-branch review evidence promoted here | Pending |

## Verification Summary

- **Focused Test Commands**: T-DCC-001 focused registry/metadata/README tests
  pass `31/31`; T-DCC-002 template tests pass `5/5`; T-DCC-003 ownership,
  placeholder, traceability, alignment, explicit-base metadata, and diff gates
  pass; T-DCC-004 and T-DCC-005 remain pending.
- **Full Test Commands**: the metadata validation module passes `93/93` after
  T-DCC-002; the final cross-suite bundle remains reserved for T-DCC-006.
- **Generated Freshness**: Pending T-DCC-006.
- **Graphify**: Required after code changes when available; advisory result and
  corroboration will be recorded per applicable task.
- **Logs / Evidence Location**: Durable concise results live in this task;
  ignored briefs/review packages live under repo-support scratch. Raw logs,
  secret-bearing output, and shell history are not evidence artifacts.

## Controlled Agent Pre-commit Evidence

Evidence covers only Git-visible, non-ignored repository paths. It does not
claim that the wrapper observes ignored/outside-repository writes or provides a
process/filesystem sandbox.

| Command | Allowed Prefixes | Exit Status | Modified Paths | Review Disposition | Skipped Rationale |
| --- | --- | ---: | --- | --- | --- |
| `bash scripts/validation/run-agent-precommit-all-files.sh --task docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md --allow-prefix docs/ --allow-prefix scripts/validation/ --allow-prefix tests/validation/ --allow-prefix .github/ --allow-prefix .pre-commit-config.yaml` | `docs/`, `scripts/validation/`, `tests/validation/`, `.github/`, `.pre-commit-config.yaml` | Pending | Pending | Pending | N/A; reserved for T-DCC-006 from an initially clean worktree |

## Deviation Notes

- **2026-07-13 preflight resolution**: The user approved resolving the conflict
  between the original one-commit-per-task wording and Task 6's clean-wrapper
  plus post-review closure requirements. Tasks 1-5 use at least one logical
  commit each. Task 6 uses a generated/pre-closure commit, pre-closure review,
  lifecycle-closure commit, and fresh post-closure whole-branch review. Review
  fixes remain separate logical commits. This changes commit/review sequencing
  only; scope, validation, rollback, and protected-surface boundaries remain
  unchanged.

## Program Follow-up Boundary

Completion of this task authorizes no automatic continuation. Later sub-project
Specs must independently own README/instruction migration, SDLC definition
chain, execution evidence, operations/release documents, reference/archive and
remaining corpus migration, corpus-wide blocking, and classic GitHub
branch-protection synchronization. Docker Compose services and deployment
runtime remain separate approval-gated work.

## Related Documents

- **Parent Spec**:
  [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- **Parent Plan**:
  [Implementation plan](../plans/2026-07-13-document-contract-canonicalization.md)
- **Stage 00 Governance**:
  [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage 99 Support**:
  [Template support](../../99.templates/support/README.md)
- **Canonical Audit**:
  [Implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Canonical Research**:
  [Research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Workspace Contract**:
  [`_workspace` contract](../../../_workspace/README.md)
