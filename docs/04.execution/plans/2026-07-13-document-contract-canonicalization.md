---
status: completed
artifact_id: plan:2026-07-13-document-contract-canonicalization
artifact_type: plan
parent_ids:
  - spec:129-document-contract-canonicalization
---
<!-- Target: docs/04.execution/plans/2026-07-13-document-contract-canonicalization.md -->

# Document Contract Canonicalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish one tested document-contract foundation for typed
frontmatter, README profiles, complete Markdown template coverage, Release
routing, and current audit truth before any broad corpus migration.

**Architecture:** Extend the existing metadata profile registry instead of
creating a parallel schema; make the current metadata checker and repository
contract gate its executable consumers; align copyable templates, Stage 00
routing, Stage 99 human contracts, the canonical research pack, and the sole
current implementation audit around that registry. Keep the 892-record corpus
advisory and defer corpus-wide blocking and remote enforcement to later waves.

**Tech Stack:** YAML 1.2-compatible metadata, Python 3.12, PyYAML, `unittest`,
Bash, Markdown/CommonMark with GitHub Flavored Markdown conventions, repository
generators, GitHub Actions, and Git.

## Global Constraints

- Spec 129 owns the contract-canonicalization foundation only. Do not bulk
  migrate README files or the historical document corpus.
- `docs/99.templates/support/document-metadata-profiles.yaml` remains the only
  machine-readable document-type registry. Do not add a parallel schema.
- Use the exact extension keys `frontmatter_order`, `document_families`, and
  `readme_profiles`.
- Canonical frontmatter presentation order is `status`, `artifact_id`,
  `artifact_type`, `parent_ids`, `supersedes`, `reviewed_at`, `review_cycle`,
  `generated_by`, `archived_from`, `archived_on`, `archive_reason`,
  `current_replacement`.
- Treat `parent_ids` as a semantic set serialized by
  `allowed_parent_types` precedence and then lexicographic `artifact_id`; list
  position never assigns semantic priority.
- Every copyable Markdown typed template must declare a valid target profile.
  The five Markdown spec-child templates use `spec`; the harness task contract
  uses `task`; Release receives a profile-aligned template and routing but no
  fictional release record.
- README frontmatter is absent by default. Allow `status`, `layer`, or
  `generated_by` only for a declared consumer or generated owner. Do not add or
  remove metadata from the 37 status-bearing README baseline in this wave.
- Separate SDLC documentation guidance from common/repository documentation
  guidance while defining shared metadata semantics only once.
- Preserve historical commands, counts, verdicts, dates, decisions, and
  execution results. Normalize only current contracts, routing, metadata
  envelopes, and links owned by this task.
- `_workspace` stays outside docs metadata inference and is independently
  enforced as exactly two tracked contract READMEs plus ignored non-secret
  repo-support scratch. Never inspect diagnostics, raw logs, auth files,
  tokens, credentials, secret values, private keys, or shell history.
- The canonical 2026-07-05 research pack is updated in place. Do not create a
  duplicate research pack or rewrite historical snapshot packs.
- The canonical 2026-07-05 implementation audit reports evidence and gaps; it
  never becomes policy. Keep exactly eleven criterion reports and 161 unique
  criterion rows.
- Keep metadata corpus mode advisory. Do not activate corpus-wide blocking,
  deployment runtime, Docker Compose runtime, repository rulesets, GitHub
  environments, or classic branch-protection mutation.
- Existing metadata command interfaces remain compatible. Add a focused mode
  only if a RED test proves the existing interface cannot expose the contract.
- Use TDD for parser, validator, template, and repository-gate behavior. Use
  `apply_patch` for authored edits and owner scripts for generated outputs.
- Execute tasks serially with a fresh implementation subagent and separate
  task reviewer. A task closes only after Spec PASS and Quality APPROVED with
  all Critical and Important findings resolved.
- Use at least one logical Conventional Commit per task. Task 6 separates the
  generated/pre-closure commit from the lifecycle-closure commit, and review
  fixes remain separate logical commits. Do not run implementation agents in
  parallel.
- Never invoke `pre-commit run --all-files` directly. Reserve
  `scripts/validation/run-agent-precommit-all-files.sh` for the final clean
  linked-worktree gate and record its Git-visible evidence in the task ledger.
- After code changes, run `graphify update .` when available. Treat Graphify as
  advisory and corroborate its report against tracked source, Stage 00, and
  stage documents; exclude unrelated generated collateral from task commits.

---

## Overview

This plan turns Spec 129 into six dependency-ordered implementation and review
units. Tasks 1 and 2 establish the executable registry and copyable artifact
coverage. Tasks 3 and 4 align human contracts, external-source rationale,
Stage 00 routing, and current audit truth. Task 5 makes the foundation
fail-closed in the existing repository/CI gate. Task 6 regenerates evidence,
runs the complete QA boundary, and closes the reviewed branch.

## Context

The existing registry already defines typed SDLC profiles and changed/new
metadata enforcement, but it does not define canonical key order, document
families, or explicit README families. Release has a profile and path inference
but no copyable template or complete routing. Five Markdown spec-child
templates and the harness task template are not mapped to their target types.
The canonical audit also overstates parent-list semantics, omits the already
implemented `_workspace` contract, and describes parts of Release and README
coverage as if no typed foundation existed.

The refreshed inventory after Spec 129 contained 892 records; tracking this
Plan/Task pair moves the planning baseline to 894. It remains an advisory
migration baseline with 546 records carrying findings, including 1,893
missing-required-key findings, seven replacement-free supersessions, and 125
stale-active findings. This plan must not turn those historical deficits into
an unbounded rewrite.

## Goals & In-Scope

- Extend and validate the single registry with frontmatter order, document
  families, README profiles, deterministic parent serialization, and complete
  Markdown template mappings.
- Add a Release template and complete its Stage 00, Stage 05, Stage 99, and
  validator routing without adding a Release record.
- Add distinct human-readable SDLC, common documentation, and README profile
  contracts that link back to shared metadata semantics.
- Revalidate the canonical research pack against official YAML, GitHub Docs,
  Diataxis, CommonMark/GFM, and GitHub enforcement documentation.
- Correct current canonical audit wording for metadata, templates, README
  profiles, parent ordering, Release, and `_workspace`.
- Integrate contract checks into the existing repository contract path already
  executed by the `repo-contracts` CI job.
- Regenerate metadata and Wiki evidence and close with full QA and independent
  task/branch reviews.

## Non-Goals & Out-of-Scope

- No broad README, Stage 01-05, reference, archive, infra, project, example, or
  root/provider document normalization.
- No deletion, archive move, supersession rewrite, or legacy-key cleanup in the
  target corpus.
- No `DESIGN.md`; active design stays under the numbered SDLC stages.
- No new PRD, ARD, ADR, incident, postmortem, release, deployment target, or
  environment invented to satisfy a template.
- No runtime Compose, infrastructure, secret, credential, provider-global,
  model-policy, remote GitHub, ruleset, environment, or branch-protection
  mutation.
- No corpus-wide metadata enforcement and no claim that tracked workflow
  definitions prove remote runs.

## File Responsibility Map

| Surface | Responsibility in this plan |
| --- | --- |
| `docs/99.templates/support/document-metadata-profiles.yaml` | Sole machine-readable schema, type, relation, order, template-source, and README-profile owner. |
| `scripts/validation/check-document-metadata.py` | Parse and validate the registry and typed target semantics. |
| `tests/validation/test_document_metadata.py` | RED/GREEN schema, ordering, profile, and template-instantiation fixtures. |
| `docs/99.templates/templates/**` | Copyable profile-aligned forms; Release and missing typed mappings close here. |
| `docs/99.templates/support/*.md` | Human SDLC/common/README contracts, selection, governance, lifecycle, and source rationale. |
| `docs/00.agent-governance/rules/*.md` | Agent authoring and stage-routing duties only. |
| `docs/05.operations/releases/README.md` | Release-document role and routing; no event record. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` | Canonical external-source analysis updated in place. |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/` | Current implementation/gap evidence and generated metadata inventory. |
| `scripts/validation/check-repo-contracts.sh` | Integrated local fail-closed contract gate. |
| `.github/workflows/ci-quality.yml` | Existing `repo-contracts` consumer; change only if a RED integration test proves named routing is missing. |
| `docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md` | Durable approvals, per-task evidence, review verdicts, deviations, and wrapper result. |

## Work Breakdown

| Task | Description | Target acceptance | Primary validation |
| --- | --- | --- | --- |
| T-DCC-001 | Extend the registry/parser with document families, canonical order, README profiles, and parent serialization. | VAL-129-001/004/005 | Focused schema and metadata tests. |
| T-DCC-002 | Complete typed Markdown templates and Release routing. | VAL-129-002/003 | Template instantiation and Release route tests. |
| T-DCC-003 | Align human contracts and canonical external research. | VAL-129-001/004 | Contract ownership and official-source review. |
| T-DCC-004 | Align Stage 00 authoring and the canonical current audit, including `_workspace`. | VAL-129-002/005/006 | 11/161 audit contract and precise source corroboration. |
| T-DCC-005 | Integrate fail-closed repository and CI enforcement for the new foundation. | VAL-129-001/003/004/007 | RED/GREEN repository contract tests and CI parse. |
| T-DCC-006 | Regenerate evidence, run full QA/wrapper, obtain whole-branch review, and close. | VAL-129-007/008 | Full suite, freshness, wrapper, clean diff, reviews. |

## Task 1: Registry, Parser, README Profiles, and Parent Serialization

**Files:**

- Modify `docs/99.templates/support/document-metadata-profiles.yaml`.
- Modify `scripts/validation/check-document-metadata.py`.
- Modify `tests/validation/test_document_metadata.py`.
- Update `docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md`.

**Interfaces:** Preserve `--mode report`, `--mode check-changed`, and
`--mode check-active`. `load_profiles()` must reject malformed new registry
members. Record validation must emit a dedicated finding when frontmatter keys
or `parent_ids` are not deterministically serialized. README path
classification must return exactly one declared profile or a deterministic
unclassified/ambiguous error; it must not rewrite README files.

- [x] **Step 1: Add failing schema and behavior fixtures**

Add focused tests covering:

```text
ProfileSchemaTests.test_frontmatter_order_requires_exact_unique_typed_keys
ProfileSchemaTests.test_document_families_require_known_unique_profiles
ProfileSchemaTests.test_readme_profiles_reject_overlap_and_unknown_members
MetadataValidationTests.test_frontmatter_presentation_order_is_enforced
MetadataValidationTests.test_parent_serialization_uses_type_precedence_then_id
MetadataValidationTests.test_parent_order_has_no_semantic_priority
ReadmeProfileTests.test_every_tracked_readme_has_exactly_one_profile
ReadmeProfileTests.test_status_bearing_readme_requires_declared_consumer
```

Use temporary registries for malformed cases. For README coverage, enumerate
tracked `README.md` files with `git ls-files -z`, assert one profile match per
path, and assert that the fixture neither modifies files nor infers a consumer
from `status` alone.

- [x] **Step 2: Run RED**

```bash
python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.MetadataValidationTests tests.validation.test_document_metadata.ReadmeProfileTests -v
```

Expected: failure because the three registry keys and their parser/validation
semantics do not yet exist.

- [x] **Step 3: Extend the registry exactly once**

Under `common`, add the exact twelve-key `frontmatter_order`. Add top-level
`document_families` with the Spec 129 `sdlc` and `common` members. Add
`readme_profiles` for root/workspace, stage index, governance catalog, provider
runtime, infrastructure root/tier/service, project root/leaf, scripts, tests,
secrets, examples, archive, template catalog, `_workspace` root, and
`_workspace/repo-support`.

Each README profile must declare non-overlapping `path_globs`, frontmatter
consumer behavior, required/optional/forbidden headings, allowed local-content
role, and canonical shared-rule owner. Use a more-specific-path-wins rule only
when it is encoded and tested; otherwise reject overlapping globs.

- [x] **Step 4: Implement fail-closed parser and validation behavior**

Validate types, non-empty strings, unique members, known profile references,
exact frontmatter-order membership, safe repository-relative patterns, and
README-profile uniqueness. Enforce key presentation order only for typed
targets. Sort parent IDs by the profile's `allowed_parent_types` order and then
lexicographically within a type; unknown/unresolved parents retain existing
findings and cannot be used to manufacture order.

Do not reinterpret YAML mapping order as semantic priority and do not change
the report/check command exit contracts.

- [x] **Step 5: Run GREEN and compatibility checks**

```bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e2954cc3
python3 scripts/validation/check-document-metadata.py --mode check-active
git diff --check
```

Expected: focused module passes; changed/active modes retain their existing
interfaces; no target README or historical corpus file is rewritten.

- [x] **Step 6: Review and commit**

Run Graphify because Python code changed, restore unrelated graph collateral,
complete the Task 1 implementer self-review, obtain Spec PASS and Quality
APPROVED, then commit:

```bash
git add docs/99.templates/support/document-metadata-profiles.yaml scripts/validation/check-document-metadata.py tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md
git commit -m "feat(docs): canonicalize document metadata registry"
```

## Task 2: Typed Templates and Release Routing

**Files:**

- Add `docs/99.templates/templates/operations/release.template.md`.
- Modify the five Markdown files under
  `docs/99.templates/templates/spec-contracts/`.
- Modify
  `docs/99.templates/templates/governance/harness-task-contract.template.md`.
- Modify `docs/99.templates/support/document-metadata-profiles.yaml`.
- Modify `docs/99.templates/support/template-selection.md`.
- Modify `docs/99.templates/templates/operations/README.md` and
  `docs/99.templates/templates/spec-contracts/README.md`.
- Modify `docs/99.templates/templates/governance/README.md`,
  `docs/99.templates/templates/README.md`, and `docs/99.templates/README.md`.
- Modify `docs/00.agent-governance/rules/stage-authoring-matrix.md`.
- Add `docs/05.operations/releases/README.md` and update
  `docs/05.operations/README.md`.
- Modify `tests/validation/test_document_metadata.py`.
- Update the Stage 04 task ledger.

**Interfaces:** All copyable Markdown typed templates instantiate a valid
target after registered placeholders are replaced. Release routes to
`docs/05.operations/releases/YYYY-MM-DD-release-name.md`, uses profile `release`,
and requires real event evidence; this task creates no release leaf.

- [x] **Step 1: Add failing complete-template fixtures**

Extend `TemplateMetadataTests` so the expected mapping includes the five
Markdown spec-child templates as `spec`, the harness task template as `task`,
and the new Release template as `release`. Add an instantiation test that
replaces registered placeholders, supplies a valid parent manifest, and passes
`validate_record()` for every copyable typed Markdown template.

Add route assertions for template selection, Stage 00 authoring matrix, Stage
05 releases index, and operations/template catalogs.

- [x] **Step 2: Run RED**

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests -v
```

Expected: failure for the six unmapped existing Markdown templates and the
missing Release template/routing.

- [x] **Step 3: Type existing Markdown templates**

For `agent-design.template.md`, `api-spec.template.md`,
`data-model.template.md`, `service.template.md`, and `tests.template.md`, add
typed `spec` placeholders in canonical key order and preserve their unique
contract sections. Type `harness-task-contract.template.md` as `task`, retain
its harness-specific approval/evidence sections, and remove template-source
instructions that conflict with target validation.

- [x] **Step 4: Add Release as one coordinated contract surface**

Create the Release template with unique sections for identity/scope, included
changes, artifacts, validation, approvals, rollout/rollback, outcome, known
issues, and related documents. Add its registry source mapping, template
selection row, operations template catalog route, Stage 00 authoring row,
Stage 05 releases index, and operations index link in the same task.

The releases index must state that changelog/release-readiness evidence is not
an executed release record and that deployment runtime remains owned by Spec
127 or a later approved runtime chain.

- [x] **Step 5: Run GREEN and template contract checks**

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests -v
python3 -m unittest tests.validation.test_document_metadata -v
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: every typed Markdown leaf has exactly one target mapping; no
machine-readable YAML/GraphQL/Proto template receives Markdown frontmatter; no
Release record is created.

- [x] **Step 6: Review and commit**

Obtain separate Spec and quality approval, then commit the coordinated surface:

```bash
git add docs/99.templates/templates docs/99.templates/support/document-metadata-profiles.yaml docs/99.templates/support/template-selection.md docs/00.agent-governance/rules/stage-authoring-matrix.md docs/05.operations/README.md docs/05.operations/releases/README.md tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md
git commit -m "feat(docs): complete typed template and release routing"
```

## Task 3: Human Contracts and Canonical External Research

**Files:**

- Add `docs/99.templates/support/sdlc-document-contract.md`.
- Add `docs/99.templates/support/common-document-contract.md`.
- Add `docs/99.templates/support/readme-profile-contract.md`.
- Modify `docs/99.templates/support/README.md`.
- Modify `docs/99.templates/support/frontmatter-contract.md`.
- Modify `docs/99.templates/support/template-contract.md`.
- Modify `docs/99.templates/support/template-governance.md`.
- Modify `docs/99.templates/support/template-selection.md`.
- Modify `docs/99.templates/support/lifecycle-contract.md` and
  `docs/99.templates/support/external-source-rationale.md` when present.
- Modify only the relevant canonical research files:
  `document-metadata-lifecycle.md`, `sdlc-document-roles.md`,
  `workspace-baseline.md`, `quality-ci-formatting.md`, and
  `automation-pipeline-workflow.md` under the 2026-07-05 research pack.
- Update the research pack README and Stage 04 task ledger.

**Interfaces:** The registry owns machine semantics. The three new human
contracts explain family-specific authoring and README profile selection
without copying the registry or hiding policy in catalog READMEs.

- [x] **Step 1: Capture source and preservation baseline**

Record the current reviewed dates, source links, and any dated counts or
verdicts in the four research files. Re-open and verify the official YAML
1.2.2, GitHub YAML frontmatter, GitHub Docs best-practices, Diataxis,
CommonMark/GFM, GitHub required-check/ruleset, and deployment-environment
sources. Use primary sources only for normative claims.

- [x] **Step 2: Write the three ownership-separated contracts**

The SDLC contract defines roles and lifecycle for PRD, ARD, ADR, Spec and
children, Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, and
Release. The common contract defines Reference, Audit, Archive, governance,
generated output, template source, repo-support, and unsupported/native
platform surfaces. The README contract defines profile selection, heading
envelopes, default-absent frontmatter, declared consumers, unique local
content, and shared-rule links.

Each document links to the registry as the sole machine owner and avoids
duplicating complete key arrays or validator logic.

- [x] **Step 3: Reconcile existing support documents**

Remove contradictory or duplicate-purpose prose, correct parent serialization
language, add Release coverage, and route family/README guidance to the new
canonical owners. Keep template governance about authoring/review and template
contract about shape/instantiation. Keep support README as catalog routing.

- [x] **Step 4: Update the canonical research pack in place**

Add source-backed analysis of typed, consumer-specific metadata; deterministic
serialization versus semantic meaning; content-type separation; README as
routing/local context; Release versus deployment evidence; and staged
migration/enforcement. Preserve unrelated provider/model and runtime research,
dated findings, commands, and historical evidence. Do not create a 2026-07-13
duplicate pack.

- [x] **Step 5: Validate ownership and preservation**

```bash
rg -n 'https://yaml.org/spec/1.2.2/|docs.github.com/.+yaml-frontmatter|diataxis.fr|spec.commonmark.org|github.github.com/gfm' docs/99.templates/support docs/90.references/research/2026-07-05-agentic-research-pack-refresh
rg -n 'T''BD|T''ODO|\[Feature|\[What|unresolved artifact placeholder|unresolved parent placeholder' docs/99.templates/support/sdlc-document-contract.md docs/99.templates/support/common-document-contract.md docs/99.templates/support/readme-profile-contract.md
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

Expected: official sources are present; placeholder scan is empty; historical
payload is preserved; no support/catalog README becomes a duplicate policy
owner.

- [x] **Step 6: Review and commit**

Obtain independent documentation/spec review, then commit:

```bash
git add docs/99.templates/support docs/90.references/research/2026-07-05-agentic-research-pack-refresh docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md
git commit -m "docs(contracts): align document governance and research"
```

## Task 4: Stage 00 Authoring and Canonical Audit Reconciliation

**Files:**

- Modify `docs/00.agent-governance/rules/documentation-protocol.md`.
- Modify `docs/00.agent-governance/rules/stage-authoring-matrix.md` only for
  ownership/routing not completed in Task 2.
- Modify the canonical audit pack README, implementation overview,
  `frontmatter-template-readme-implementation.md`,
  `sdlc-document-contracts-implementation.md`,
  `sdlc-quality-formatting-implementation.md`, and
  `workspace-rules-environment-implementation.md`.
- Modify `automation-candidates.md` and `security-framework-maturity.md` for
  the already captured 2026-07-12 read-only GitHub enforcement evidence.
- Modify criterion leaves only where the new implementation changes their
  evidence-backed state or recommendation.
- Update the Stage 04 task ledger.

**Interfaces:** Stage 00 tells agents how to select and validate canonical
contracts; it does not copy Stage 99 schemas. The audit reports current
implementation and gaps; it does not own rules. The 11-report/161-row contract
and all unrelated criterion states remain stable.

- [x] **Step 1: Reproduce the exact pre-change audit baseline**

```bash
python3 scripts/validation/audit_criterion_contract.py
bash scripts/validation/report-audit-pack-coverage.sh --check
rg -n 'parent_ids|Release|README profile|_workspace|template' docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/{README.md,implementation-overview.md,frontmatter-template-readme-implementation.md,sdlc-document-contracts-implementation.md,sdlc-quality-formatting-implementation.md,workspace-rules-environment-implementation.md}
```

Expected: 11 reports, 161 rows, and the stale/partial wording identified in
Spec 129 without changing historical snapshot packs.

- [x] **Step 2: Make Stage 00 a precise consumer**

Update the documentation protocol to require registry-driven profile
selection, template instantiation, README profile selection, deterministic
parent serialization, historical-payload preservation, and fail-closed
ambiguity handling. Link to the three human contracts and the registry rather
than copying full key/profile definitions.

- [x] **Step 3: Correct canonical audit truth**

Describe Release as profile/checker route plus newly implemented template and
routing but no event record. Describe README profiles as an implemented
contract foundation with the 37 status-bearing files still awaiting the next
wave. Describe parent order as deterministic serialization without priority.
Add `_workspace` coverage as independently enforced, excluded from docs
metadata inference, and limited to two tracked READMEs plus ignored non-secret
scratch.

Keep this coverage within the existing WRE narrative or an existing relevant
criterion row. Do not add a twelfth report or a 162nd criterion; the exact
11-report/161-row contract remains binding.

Replace remote-enforcement “unknown” wording only where the dated 2026-07-12
read-only evidence supports the narrower current statement: classic protection
is enabled, twelve contexts are required remotely, the local contract names
fifteen, three contexts are absent remotely, repository rulesets are zero, and
environments are zero. Preserve the distinction between tracked definitions,
observed remote configuration, recent check execution, and enforcement
mutation; this task performs no remote write.

Change criterion state/depth/disposition only when the completed Tasks 1-3
provide direct tracked evidence. Do not infer runtime, remote, provider-global,
model entitlement, deployment, or corpus migration state.

- [x] **Step 4: Validate audit invariants**

```bash
python3 scripts/validation/audit_criterion_contract.py
bash scripts/validation/report-audit-pack-coverage.sh --check
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
python3 -m unittest tests.validation.test_agentic_audit_semantic_freshness -v
git diff --check
```

Expected: 11/161 remains exact; semantic closure assertions remain green; no
dated 2026-07-03/04 snapshot or superseded 2026-07-07 pack changes.

- [x] **Step 5: Review and commit**

Obtain an independent evidence-precision review, then commit:

```bash
git add docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/stage-authoring-matrix.md docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md
git commit -m "docs(audits): reconcile document contract implementation"
```

## Task 5: Repository and CI Contract Enforcement

**Files:**

- Modify `scripts/validation/check-repo-contracts.sh`.
- Modify `tests/validation/test_document_metadata.py` and add a focused
  repository-contract test module only if isolation requires it.
- Modify `.github/workflows/ci-quality.yml` only if RED proves the existing
  `repo-contracts` routing does not execute the new check.
- Modify `scripts/README.md`.
- Update the Stage 04 task ledger.

**Interfaces:** The existing `repo-contracts` CI job remains read-only and
least-privilege. Its current changed/new metadata and repository-contract
commands must fail closed when registry, template mapping, README profile
coverage, Release routing, or human/machine ownership drifts. It must not enable
whole-corpus blocking.

- [x] **Step 1: Add failing integration assertions**

Add tests that mutate a temporary repository or contract fixture and prove the
gate rejects:

- a missing/renamed exact registry extension key;
- duplicate or overlapping README profile ownership;
- a copyable Markdown typed template missing from `template_sources`;
- a template target type inconsistent with the registry;
- missing Release selection/Stage 00/Stage 05 route;
- copied full registry arrays in human support documents when a canonical link
  is required; and
- any attempt to include `_workspace` in docs metadata inventory inference.

- [x] **Step 2: Run RED**

```bash
python3 -m unittest tests.validation.test_document_metadata -v
bash scripts/validation/check-repo-contracts.sh
```

Expected: new adversarial fixtures fail before repository enforcement is
added, while the unmodified repository baseline remains otherwise green.

- [x] **Step 3: Integrate the contract in one existing gate**

Extend the existing repository-contract sections to load the registry through
the metadata checker or its shared parser, require complete typed Markdown
template coverage, require every tracked README to classify exactly once,
require Release route consistency, and assert `_workspace` remains independent.
Avoid a second parser or duplicated schema constants in Bash.

Confirm `.github/workflows/ci-quality.yml` already runs the extended script in
the read-only `repo-contracts` job. Change the workflow only if a test proves a
missing route; do not add permissions, events, dependencies, environments, or
remote claims.

- [x] **Step 4: Run GREEN and workflow security checks**

```bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 -m unittest discover -s tests/validation -q
bash scripts/validation/check-repo-contracts.sh
python3 -c 'import pathlib, yaml; yaml.safe_load(pathlib.Path(".github/workflows/ci-quality.yml").read_text())'
actionlint .github/workflows/ci-quality.yml
zizmor .github/workflows/ci-quality.yml
git diff --check
```

Expected: all tests and contracts pass; actionlint has no errors; zizmor has no
new unsuppressed findings; workflow permissions and events are unchanged.

- [x] **Step 5: Review and commit**

Run Graphify because validation code changed, restore unrelated graph output,
obtain separate Spec and quality approval, then commit:

```bash
git add scripts/validation/check-repo-contracts.sh tests/validation scripts/README.md .github/workflows/ci-quality.yml docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md
git commit -m "ci(docs): enforce canonical document contracts"
```

If `.github/workflows/ci-quality.yml` is unchanged, omit it from `git add` and
record that the existing `repo-contracts` route already supplies CI coverage.

## Task 6: Generated Evidence, Full QA, Reviews, and Closure

**Files:**

- Regenerate
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`.
- Regenerate owner-managed audit matrix and LLM Wiki index/coverage outputs.
- Update `docs/00.agent-governance/memory/progress.md`.
- Complete the Spec, Plan, and Task lifecycle/evidence only after all reviews
  approve.
- Update parent indexes for the final completed state.

**Interfaces:** Generated outputs must be owner-produced and fresh. The
controlled wrapper observes only Git-visible, non-ignored repository paths.
Closure preserves the final corpus baseline as advisory and records all later
program waves as pending.

- [x] **Step 1: Regenerate owner-managed evidence**

```bash
python3 scripts/validation/check-document-metadata.py --mode report --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
```

Review the generated diffs and reject unexpected handwritten-content changes.

- [x] **Step 2: Run the complete local validation bundle**

```bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 -m unittest discover -s tests/validation -q
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e2954cc3
python3 scripts/validation/audit_criterion_contract.py
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
bash scripts/validation/report-audit-pack-coverage.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: all commands pass, audit remains 11/161, and repository contracts
report `failures=0`.

- [x] **Step 3: Run the controlled all-files gate from a clean worktree**

First commit all accepted implementation/generated changes except the final
evidence/lifecycle update. Confirm `git status --short` is empty, then run:

```bash
bash scripts/validation/run-agent-precommit-all-files.sh --task docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md --allow-prefix docs/ --allow-prefix scripts/validation/ --allow-prefix tests/validation/ --allow-prefix .github/ --allow-prefix .pre-commit-config.yaml
```

Record command, exit status, Git-visible modified/new/unexpected paths, review
disposition, and observation boundary in the task ledger. Stop on any
unexpected path; do not clean or hide it.

- [x] **Step 4: Obtain the pre-closure whole-branch review**

Create a review package for `e2954cc3..HEAD`. Give a fresh, most-capable
reviewer Spec 129, this plan, the task evidence, the exact diff package, all
per-task review verdicts, and any remaining Minor findings. Require Spec PASS,
Quality APPROVED, Critical 0, and Important 0 before closure.

- [x] **Step 5: Close lifecycle and commit**

After approval, set Spec/Plan/Task status to `completed`, check every completion
criterion, add final validation/review evidence, update Stage 03/04 indexes and
progress memory, regenerate metadata/Wiki outputs once more, and rerun their
freshness checks.

```bash
git add docs/03.specs/129-document-contract-canonicalization docs/03.specs/README.md docs/04.execution/plans/2026-07-13-document-contract-canonicalization.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md docs/90.references/data/governance/audit-implementation-matrix.md docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
git commit -m "docs(task): close document contract canonicalization"
```

- [ ] **Step 6: Obtain post-closure review, verify, and hand off**

Create a fresh review package for `e2954cc3..HEAD` after the closure commit.
Require a fresh independent post-closure verdict of Spec PASS, Quality
APPROVED, Critical 0, and Important 0. If it returns findings, use one fix
subagent for the complete finding set, rerun covering tests, and repeat the
post-closure review before handoff.

```bash
git status --short
git log --oneline e2954cc3..HEAD
git diff --stat e2954cc3..HEAD
git diff --check e2954cc3..HEAD
```

Expected: clean worktree, at least one logical commit for each of Tasks 1-5,
separate generated/pre-closure and lifecycle-closure commits for Task 6,
post-closure approval, no runtime or remote mutation, and all later migration
waves still explicitly pending.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Unit | Registry schema, frontmatter order, README profiles, parent serialization. | `python3 -m unittest tests.validation.test_document_metadata -v` | All focused and adversarial cases pass. |
| VAL-PLN-002 | Template | Every typed Markdown template instantiates a valid target. | `python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests -v` | Complete mapping including spec children, harness task, and Release. |
| VAL-PLN-003 | Audit | Canonical pack remains structurally and semantically valid. | Criterion, coverage, and semantic freshness commands. | 11 reports, 161 unique rows, zero semantic failures. |
| VAL-PLN-004 | Metadata | Changed foundation and generated inventory are valid/fresh. | Metadata check-changed and report/check workflow. | Zero changed-scope violations; generated output fresh. |
| VAL-PLN-005 | Traceability | Stage links and implementation alignment remain coherent. | Traceability and alignment scripts. | Zero failures. |
| VAL-PLN-006 | Repository | Existing local/CI contract path enforces the foundation. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`; no corpus-wide gate. |
| VAL-PLN-007 | Workflow | CI remains valid and least privilege. | PyYAML parse, actionlint, zizmor. | Parse/actionlint pass; no new unsuppressed security findings. |
| VAL-PLN-008 | Generated | Wiki and audit owner outputs are fresh. | All owner `--check` commands. | Every check reports fresh/pass. |
| VAL-PLN-009 | Controlled QA | Approved all-files hook boundary is clean. | Controlled wrapper from initially clean worktree. | Exit 0; no unexpected Git-visible paths. |
| VAL-PLN-010 | Scope | Runtime, secrets, remote GitHub, and corpus migration remain untouched. | `git diff --name-only e2954cc3..HEAD` plus task evidence. | Only approved foundation/evidence paths; no forbidden mutation. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Registry extensions silently break existing parser behavior. | High | Add RED schema/compatibility tests before editing and preserve all CLI modes. |
| README globs overlap or classify files by accident. | High | Enumerate tracked READMEs, reject zero/multiple matches, and defer actual metadata edits. |
| Frontmatter order is confused with relation priority. | High | Separate presentation and semantic-set tests; serialize by type precedence and ID only. |
| Template typing copies generic sections into real targets. | Medium | Test instantiated metadata only; preserve each template's unique purpose and prohibit copied instructions/placeholders in targets. |
| Release documentation is mistaken for deployment execution. | High | Add routing/template only, require real event evidence, and retain Spec 127 runtime boundary. |
| Human contracts duplicate the machine registry. | High | Link to the sole registry and test ownership markers instead of copying full arrays. |
| Canonical audit becomes policy or overclaims completion. | High | Corroborate only tracked evidence and keep remaining corpus/remote/runtime gaps explicit. |
| Existing historical evidence is rewritten. | High | Limit edits to the canonical pack/research files, capture dated literals, and review exact diffs. |
| Repository enforcement activates a 1,893-finding migration accidentally. | High | Keep report mode advisory and assert changed/new scope only. |
| Graphify or wrapper creates unrelated collateral. | Medium | Treat graph output as advisory, restore unrelated files, and stop wrapper review on unexpected paths. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate:** Every parser/validator/template change uses focused
  RED/GREEN unit and adversarial fixtures before broad repository validation.
- **Sandbox / Canary Rollout:** The changed/new metadata gate remains the only
  blocking corpus boundary. README classification and whole inventory remain
  report-only.
- **Human Approval Gate:** Spec 129 and this plan authorize local foundation
  changes only. Later corpus waves and classic branch-protection mutation need
  their own approved Spec/Plan/Task.
- **Rollback Trigger:** Revert the current logical task commit when schema
  compatibility, template instantiation, historical payload preservation,
  audit invariants, or unexpected-path checks fail.
- **Prompt / Model Promotion Criteria:** Use fresh right-sized implementers and
  reviewers per task; use the most capable available reviewer for the whole
  branch. No provider model policy changes are part of this plan.

## Completion Criteria

- [x] Registry contains and validates the exact three extension keys.
- [x] Canonical frontmatter and parent serialization semantics are tested.
- [x] Every tracked README maps to exactly one declared profile without bulk
      metadata edits.
- [x] Every copyable typed Markdown template maps and instantiates correctly.
- [x] Release template and routing exist without a fictional Release record.
- [x] SDLC, common, and README human contracts have distinct ownership.
- [x] Canonical research is revalidated in place against official sources.
- [x] Stage 00 routing and canonical audit agree with current implementation.
- [x] `_workspace` is covered by the audit and remains independently enforced.
- [x] Existing repository/CI gates fail closed on contract drift without
      corpus-wide blocking.
- [x] Full validation, generated freshness, controlled wrapper, per-task
      reviews, and whole-branch review pass after the post-closure findings are
      remediated and independently re-reviewed.
- [x] No runtime, secret, deployment, ruleset, environment, provider-global,
      model-policy, remote branch-protection, or broad corpus mutation occurs.
- [x] Tasks 1-5 have logical commits; Task 6 has separate generated/pre-closure
      and lifecycle-closure commits; durable evidence records the failed
      post-closure review, remediation, and fresh re-review.

## Related Documents

- **Parent Spec**:
  [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- **Task Evidence**:
  [Document contract canonicalization task](../tasks/2026-07-13-document-contract-canonicalization.md)
- **Parent Program**:
  [Spec 128](../../03.specs/128-agentic-audit-harness-consolidation/spec.md)
- **Documentation Protocol**:
  [Stage 00 protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Metadata Registry**:
  [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- **Template Support**:
  [Stage 99 support](../../99.templates/support/README.md)
- **Canonical Research**:
  [2026-07-05 research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Canonical Audit**:
  [2026-07-05 implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Workspace Contract**:
  [`_workspace` contract](../../../_workspace/README.md)
