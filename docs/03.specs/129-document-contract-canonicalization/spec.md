---
status: active
artifact_id: spec:129-document-contract-canonicalization
artifact_type: spec
parent_ids:
  - spec:128-agentic-audit-harness-consolidation
---

<!-- Target: docs/03.specs/129-document-contract-canonicalization/spec.md -->

# Document Contract Canonicalization Technical Specification (Spec)

## Overview

This specification defines the first sub-project in the workspace-wide
documentation normalization program. It closes contradictions between the
current Stage 90 audit, Stage 00 authoring governance, Stage 99 template and
metadata contracts, validators, and live repository structure before any broad
corpus migration begins.

The approved program uses contract-first, dependency-ordered waves. Historical
documents receive preservation-oriented normalization: metadata, section
envelopes, routing, and links may be normalized, while dated commands, counts,
decisions, verdicts, timestamps, and execution results remain historical
evidence. Canonical uniqueness is scoped by hierarchy: shared policy and
contract roles have one owner, while service- and folder-specific documents
remain when they contain unique implementation or operational content.

Spec 129 owns the foundation only. Later sub-projects own README and provider
surfaces, SDLC definition documents, execution evidence, operations and
release documents, references and archives, remaining repository surfaces,
corpus-wide blocking, and remote GitHub enforcement.

## Strategic Boundaries & Non-goals

### In Scope

- Reconcile the canonical 2026-07-05 implementation audit with current
  Stage 00, Stage 99, validators, and tracked repository evidence.
- Define one machine-readable document-type and frontmatter-order contract.
- Separate SDLC documentation contracts from common/repository documentation
  contracts without duplicating shared metadata semantics.
- Close typed-template coverage for Release, Markdown spec children, and the
  harness task contract.
- Define explicit README profiles and metadata-consumer rules without bulk
  rewriting README files in this sub-project.
- Correct the parent-ordering contract so semantic relation order and
  deterministic serialization are not conflated.
- Integrate the already implemented `_workspace` contract into the canonical
  audit without moving `_workspace` into the docs metadata corpus.
- Specify the migration manifest, preservation, fail-closed, QA, rollback, and
  remote-evidence interfaces used by later waves.
- Revalidate external source rationale against official sources.

### Out of Scope

- Bulk frontmatter or section migration of the 891-record baseline corpus.
- Editing historical evidence payloads for style or current-state wording.
- Creating `DESIGN.md`; active design artifacts remain in canonical Stage 02
  and Stage 03 paths.
- Inventing PRDs, parents, incidents, postmortems, releases, review dates, or
  live-state evidence solely to satisfy a schema.
- Changing Docker Compose runtime, deployment targets, secret values, auth
  files, tokens, shell history, raw logs, or user-global provider settings.
- Creating GitHub repository rulesets or deployment environments.
- Changing classic `main` protection in this first sub-project. The approved
  remote-enforcement wave will synchronize classic protection only after local
  contracts, exact check names, recent check runs, rollback evidence, and a
  separate Stage 04 task are approved.
- Enabling corpus-wide blocking before every dependency-ordered migration wave
  and its independent review have completed.

## Related Inputs

- **PRD**: No new product requirement is introduced. This is a governance and
  documentation-harness follow-up to the approved audit program.
- **ARD**: No runtime architecture changes are introduced. Documentation
  topology and validator boundaries remain repository-local.
- **Related ADRs**: No new runtime decision is required. Later changes to
  deployment architecture or provider-native behavior require their own
  architecture chain.
- **Parent Spec**:
  [Spec 128](../128-agentic-audit-harness-consolidation/spec.md)
- **Canonical Audit**:
  [2026-07-05 agentic engineering implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Typed Metadata Contract**:
  [frontmatter contract](../../99.templates/support/frontmatter-contract.md)
  and
  [metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- **Template Contracts**:
  [template contract](../../99.templates/support/template-contract.md),
  [template governance](../../99.templates/support/template-governance.md),
  and
  [template selection](../../99.templates/support/template-selection.md)
- **Workspace Support Contract**:
  [`_workspace` contract](../../../_workspace/README.md)

## External Source Basis

External sources inform the local design; repository contracts remain
canonical for this workspace.

| Official source | Design consequence |
| --- | --- |
| [YAML 1.2.2](https://yaml.org/spec/1.2.2/) | Treat frontmatter values as typed data and keep the schema JSON-compatible and deterministic. |
| [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) | Define consumer-specific keys and validate them with a schema instead of copying one universal key set. |
| [GitHub Docs content best practices](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs) | Give each document a clear audience, purpose, content type, and scannable structure. |
| [Diataxis](https://diataxis.fr/) | Keep procedural, reference, explanatory, and learning roles distinct while retaining the workspace SDLC taxonomy. |
| [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) and [GitHub Flavored Markdown](https://github.github.com/gfm/) | Treat Markdown body syntax separately from YAML frontmatter processing. |
| [GitHub ruleset rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) | Require exact, observed check contexts before remote enforcement; do not infer deployment or protection state from local files. |
| [GitHub deployment environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments) | Do not create or claim an environment when the repository has no approved deployment target. |

## Contracts

### Canonical Ownership Contract

| Surface | Canonical responsibility |
| --- | --- |
| `document-metadata-profiles.yaml` | Machine-readable document types, frontmatter keys, value types, status transitions, parent rules, serialization order, README profiles, and exception boundaries. |
| `docs/99.templates/support/` | Human-readable contracts, governance, selection, migration, and source rationale. |
| `docs/99.templates/templates/` | Copyable document and machine-readable contract forms only. |
| `docs/00.agent-governance/` | Agent routing, authoring workflow, approval, and validation duties. |
| Validators and tests | Executable interpretation of the canonical contracts. |
| Stage 90 audit | Evidence and gap reporting; never active policy. |
| README files | Profile-scoped routing and unique local content; never hidden shared governance. |

Detailed governance and contract text must not be copied into catalog README
files. README files link to canonical owners and retain only profile-specific
navigation, local structure, and usage context.

### Documentation Family Contract

The registry distinguishes two contract families:

1. **SDLC documentation**: PRD, ARD, ADR, Spec and spec children, Plan, Task,
   Guide, Policy, Runbook, Incident, Postmortem, and Release.
2. **Common/repository documentation**: Reference, Audit, Archive, README,
   governance, generated output, template source, repo-support, and explicit
   unsupported/native-platform surfaces.

Shared metadata semantics are defined once in the registry. Family-specific
human guidance is kept separate so common README or repository-support rules
cannot silently become SDLC lifecycle requirements.

### Frontmatter Contract

Migrated and changed target documents use this canonical presentation order:

```text
status
artifact_id
artifact_type
parent_ids
supersedes
reviewed_at
review_cycle
generated_by
archived_from
archived_on
archive_reason
current_replacement
```

Only keys allowed by the inferred profile may appear. A key omitted from a
profile remains forbidden unless the profile explicitly allows additional
native-platform keys. Generic duplicate-purpose keys such as `type`,
`document_type`, `template_type`, `owner`, `updated`, and `links` remain
forbidden for typed target documents.

Frontmatter key order is a deterministic presentation contract, not semantic
priority. `parent_ids` is a direct-parent set. Its serialization order follows
the profile's `allowed_parent_types` precedence and then `artifact_id`
lexicographic order. The validator must not claim that list position assigns
semantic priority.

### Template Coverage Contract

- Every copyable Markdown leaf template that creates a typed target declares
  the target `artifact_type` and required typed placeholders.
- The five Markdown spec-child templates instantiate the `spec` profile unless
  a future approved subtype is added.
- `harness-task-contract.template.md` instantiates the `task` profile.
- A Release template, Stage 05 release routing, template selection entry, Stage
  00 authoring entry, and validator fixture must be added together.
- Machine-readable YAML, GraphQL, and Protobuf templates remain comment-driven
  and do not receive Markdown frontmatter.
- Instantiation tests must prove that every template can produce a valid target
  after registered placeholders are replaced.

### README Profile Contract

The machine-readable registry defines these initial README families:

- root/workspace;
- stage index;
- governance catalog;
- provider runtime;
- infrastructure root, tier, and service;
- project root and leaf;
- scripts, tests, and secrets;
- examples and archive;
- template catalog; and
- `_workspace` repo-support.

Each family declares required, optional, and forbidden headings; frontmatter
consumer behavior; allowed local content; and the canonical owner for shared
rules. README frontmatter stays absent by default. `status`, `layer`, or
`generated_by` is allowed only where a real consumer or generated owner is
declared. The 37 status-bearing README baseline must be classified by a later
README migration spec before any bulk addition or removal.

### Release Reconciliation Contract

The current repository contains a Release metadata profile and checker route
but no copyable Release template, template-selection mapping, Stage 00 mapping,
release directory index, or release record. Spec 129 corrects the contract and
audit description. It does not manufacture a release record. A record is
created only when a real release event and evidence exist.

Release documentation remains distinct from deployment runtime. Draft Spec 127
continues to own deployment targets, promotion, rollback, and CD behavior.

### `_workspace` Contract

`_workspace` remains a non-stage, ignored, non-secret repo-support surface.
Only `_workspace/README.md` and `_workspace/repo-support/README.md` may be
tracked. Temporary analysis summaries, dry-run previews, migration ledgers,
and subagent handoffs belong under ignored `_workspace/repo-support/`.

Diagnostics dumps, local or raw logs, auth files, tokens, credentials, private
keys, shell history, secret values, token-bearing output, and full secret file
bodies remain prohibited. Durable non-secret outcomes are promoted to Stage 04,
Stage 90, or Stage 00. The docs metadata checker continues to exclude
`_workspace`; repository contracts enforce it independently.

### Preservation and Canonicality Contract

- Historical commands, counts, decisions, verdicts, timestamps, and execution
  results are immutable evidence payloads.
- Metadata, section names and order, links, and current-routing boundaries may
  be normalized around preserved payloads.
- Shared contracts, governance rules, and templates have one canonical owner.
- Service- and folder-specific documents remain when their implementation or
  operational content is unique.
- Duplicate removal requires a proven replacement, link and README updates,
  task evidence, and rollback instructions.
- Conflicting active documents move to Stage 98 tombstones only after current
  replacement and archive provenance are established.

### Migration Wave Contract

The approved program sequence is:

1. contract canonicalization;
2. README and instruction surfaces;
3. PRD to ARD/ADR to Spec definition chain;
4. Plan and Task execution chain;
5. Guide, Policy, Runbook, Incident, Postmortem, and Release operations chain;
6. Reference, Audit, Archive, and remaining repository surfaces; and
7. corpus-wide enforcement and classic GitHub branch-protection synchronization.

Every later wave requires its own active Spec, Plan, Task evidence, fresh
implementer, separate reviewer, logical commits, generated-output refresh, and
whole-range review.

## Core Design

### Component Boundary

| Component | Responsibility |
| --- | --- |
| Document-type registry | One typed, machine-readable description of profiles, relations, status, key order, template sources, README families, and exceptions. |
| Support contracts | Human-readable shape, family, migration, and governance semantics. |
| Template sources | Copyable forms aligned to the registry. |
| Metadata validator | Parse, infer, validate, report, and later enforce the registry without rewriting files. |
| Template/README validator | Validate source-to-target instantiation and profile-specific section contracts. |
| Migration manifest | Bound each later wave to exact targets, dispositions, relations, preservation evidence, verification, and rollback. |
| Canonical audit | Record current implementation and remaining gaps without owning policy. |
| Repository and CI gates | Execute focused and integrated checks; promote to corpus-wide blocking only at program closure. |
| Remote verifier | Read, compare, apply, and re-read classic branch protection in the final wave. |

### Key Dependencies

- `docs/99.templates/support/document-metadata-profiles.yaml`
- `docs/99.templates/support/*.md`
- `docs/99.templates/templates/**`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `scripts/validation/check-document-metadata.py`
- `scripts/validation/check-repo-contracts.sh`
- `tests/validation/test_document_metadata.py`
- `.pre-commit-config.yaml`
- `.github/workflows/ci-quality.yml`
- `.github/rulesets/main-protection.md`
- the canonical 2026-07-05 implementation audit and generated metadata
  inventory

### Tech Stack

- YAML 1.2-compatible profile data.
- Python standard library plus the repository's existing YAML parser for
  deterministic validation and migration-manifest checks.
- Markdown/CommonMark with GitHub Flavored Markdown rendering conventions.
- Bash repository orchestration and existing generation/check modes.
- GitHub CLI and REST API for read-only discovery in Spec 129 and audited
  classic-protection changes in the final wave.

## Data Modeling & Storage Strategy

### Registry Model

The existing profile file remains the registry root. Spec 129 extends it with
explicit presentation order, documentation families, README families, and
complete template-source mappings rather than creating a parallel schema.

```yaml
common:
  frontmatter_order:
    - status
    - artifact_id
    - artifact_type
    - parent_ids
    - supersedes
    - reviewed_at
    - review_cycle

document_families:
  sdlc: [prd, ard, adr, spec, plan, task, guide, policy, runbook, incident, postmortem, release]
  common: [reference, audit, archive, readme, governance, generated, template-source, repo-support, unsupported]

readme_profiles:
  workspace-root:
    path_globs: [_workspace/README.md]
    frontmatter: forbidden
    required_headings: [Purpose, Allowed Surface, Prohibited Surface, Tracking Contract, Related Documents]
  repo-support:
    path_globs: [_workspace/repo-support/README.md]
    frontmatter: forbidden
    required_headings: [Purpose, Allowed Artifacts, Prohibited Artifacts, Promotion Rule, Related Documents]
```

`frontmatter_order`, `document_families`, and `readme_profiles` are the exact
registry extension keys. The implementation plan defines their validated
members without renaming them, must preserve current parser behavior, and must
not introduce a second profile source.

### Migration Manifest Model

Later waves use a task-owned non-secret manifest with one record per target:

```yaml
- path: docs/03.specs/129-document-contract-canonicalization/spec.md
  profile: spec
  disposition: active-canonical
  canonical_owner: docs/03.specs/129-document-contract-canonicalization/spec.md
  preserved_payload: [dated-verdicts, command-results]
  direct_parent_ids: [spec:128-agentic-audit-harness-consolidation]
  replacement: null
  validation: [metadata, template, links]
  rollback: revert-logical-commit
```

The manifest is evidence and input, not permission to invent missing values.
Ambiguous targets block their wave.

### Baseline and Transition Strategy

The pre-Spec 129 generated inventory baseline contained 891 records. Adding
this specification moved the current generated baseline to 892 records while
retaining 546 records with findings, 1,893 `missing-required-key` findings,
seven `replacement-free-supersession` findings, and 125 `stale-active`
findings. Counts may change through approved additions, removals, or archive
moves; IDs, relations, and dispositions provide continuity.

The full inventory remains advisory during dependency waves. Each reviewed
wave joins the changed/new blocking set. Corpus-wide blocking activates only
after the final inventory has zero unresolved migrated-corpus findings and zero
legacy exceptions.

## Interfaces & Data Structures

### Validator Interfaces

The implementation plan must preserve current commands and add focused modes
only when tests demonstrate a missing interface:

```text
check-document-metadata.py --mode report
check-document-metadata.py --mode check-changed --base-ref "$MERGE_BASE_SHA"
check-document-metadata.py --mode check-active
```

The first sub-project may add template-registry and README-profile validation
to existing commands or a focused companion module. It must not enable final
corpus-wide blocking.

### Remote State Interface

The final enforcement wave, not Spec 129 implementation, uses read-before-write
GitHub API evidence:

```text
GET /repos/buenhyden/hy-home.docker/branches/main/protection
GET /repos/buenhyden/hy-home.docker/rulesets
GET /repos/buenhyden/hy-home.docker/environments
```

Read-only evidence captured on 2026-07-12 is classic protection enabled, zero
repository rulesets, twelve required contexts, Actions enabled, and zero
environments.
The final wave will compare the fifteen locally contracted checks, verify
recent runs, patch only missing contexts, and preserve all unrelated
protection fields.

## API Contract (Not Applicable)

Spec 129 exposes no product or runtime API. GitHub REST calls are external
administrative operations reserved for the final enforcement sub-project and
must be specified with exact request, before-state, after-state, rollback, and
redaction evidence there.

## Agent Role & IO Contract

- **Supervisor**: Owns approved design, task decomposition, evidence, and
  review sequencing.
- **Documentation/Metadata Implementer**: Updates one bounded contract or
  template task and its tests in an isolated worktree.
- **Reviewer**: Independently checks Spec compliance and quality from an exact
  diff package.
- **Inputs**: Spec 129, one extracted task brief, tracked source evidence,
  official external sources, and redacted remote metadata when applicable.
- **Outputs**: Logical commits, test evidence, updated task ledger, generated
  references, and review verdicts.
- **Success Definition**: No task closes without Spec PASS, Quality APPROVED,
  and all Critical/Important findings resolved.

## Tools & Tool Contract

- Use `rg` and tracked parsers for discovery; Graphify remains advisory.
- Use `apply_patch` for authored file edits and owner generators for generated
  outputs.
- Use `git mv` for approved path moves.
- Never read secret value files, auth files, tokens, raw logs, or shell history.
- Network tools are read-only until a later Stage 04 task explicitly binds an
  approved remote mutation to before/after/rollback evidence.
- Run all-files pre-commit only through
  `scripts/validation/run-agent-precommit-all-files.sh` from an initially clean
  linked worktree.

## Prompt / Policy Contract

Root and provider instruction files remain concise routing shims. Shared rules
live in Stage 00. Provider-native behavior remains in `.claude`, `.agents`, or
`.codex` only when the provider consumes it. No task copies the full
documentation contract into root shims, README files, agent prompts, or skills.

## Memory & Context Strategy

- Durable active rules remain in Stage 00 or Stage 99.
- Progress and reusable failure patterns are recorded in Stage 00 memory.
- Audit evidence remains in the canonical Stage 90 pack.
- Task-local non-secret analysis and migration scratch remain ignored under
  `_workspace/repo-support/`.
- Raw logs, diagnostics, auth material, and secret-bearing output are never
  used as context artifacts.

## Guardrails

- **Input Guardrails**: Reject ambiguous profiles, malformed YAML, duplicate
  IDs, unresolved relations, unsafe paths, untracked evidence, and unknown
  source ownership.
- **Output Guardrails**: Reject unresolved placeholders, copied template
  instructions, duplicate-purpose sections, historical payload loss, manual
  generator edits, and policy duplication in README files.
- **Blocked Conditions**: Missing canonical owner, unproven parent or
  replacement, unexpected paths, redaction failure, failing baseline, or
  remote/local protection mismatch.
- **Escalation Rule**: Stop the wave and request human direction when evidence
  cannot select one safe canonical disposition.

## Evaluation

- Profile schema and parser fixtures.
- Template instantiation fixtures for every copyable artifact.
- README profile classification fixtures.
- Parent serialization and semantic-order negative tests.
- Release profile/template/routing consistency tests.
- `_workspace` allowlist and prohibited-content literal tests.
- Historical payload preservation fixtures for later waves.
- Migration manifest coverage and unexpected-path tests.
- Local/remote required-check parity tests for the final wave.

## Edge Cases & Error Handling

| Edge case | Required behavior |
| --- | --- |
| Status-bearing README without declared consumer | Classify in the README migration manifest; do not remove or retain metadata by assumption. |
| Spec child with status-only template | Update template mapping and placeholders before migrating targets. |
| Existing Release profile without template or record | Add the missing contract surfaces; do not create a fictional release event. |
| Multiple direct parents | Validate type and resolution, serialize deterministically, and assign no semantic priority to list position. |
| Active Policy or Runbook without review fields | Review against current evidence in the operations wave; never infer freshness from mtime. |
| Historical document using old paths | Preserve evidence when the path is historical context; fix only active routing and links. |
| Duplicate document with unique local details | Extract shared rules to the canonical owner and retain the local document with unique content. |
| Secret-path documentation | Inspect paths and non-secret metadata only; never open secret values. |
| Required remote check has no recent run | Do not patch protection; generate or await approved CI evidence in the final wave. |

## Failure Modes & Fallback / Human Escalation

| Failure mode | Fallback and escalation |
| --- | --- |
| Registry and human contract disagree | Treat the machine-readable registry as non-authoritative until both are reconciled and tests pass; do not migrate targets. |
| Migration loses evidence | Revert the logical commit and restore the manifest's before snapshot. |
| Parent or replacement is ambiguous | Leave the target advisory and request a canonical-owner decision. |
| Validator introduces broad false positives | Keep corpus mode advisory, fix fixtures and scope, and re-review before promotion. |
| Remote protection update differs from requested payload | Restore the captured before-state immediately and record the failed attempt without claiming enforcement. |
| Full validation fails outside task scope | Record the exact pre-existing failure and stop if it prevents trustworthy verification. |

## Verification

Spec 129 implementation planning must include, at minimum:

```bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 -m unittest discover -s tests/validation -q
python3 scripts/validation/check-document-metadata.py --mode report --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$MERGE_BASE_SHA"
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
git diff --check
```

Template, README, Release, and parent-order fixtures added by the plan must run
as focused RED/GREEN tests before the broad bundle.

## Success Criteria & Verification Plan

### Spec 129 Acceptance

- **VAL-129-001**: One machine-readable registry defines document families,
  canonical frontmatter order, full Markdown template mappings, and README
  profile semantics without a parallel schema.
- **VAL-129-002**: Release profile, template, selection, Stage 00 routing, and
  audit wording agree; no fictional release record is added.
- **VAL-129-003**: Five Markdown spec-child templates and the harness task
  template instantiate valid typed targets.
- **VAL-129-004**: README profile contract covers every current README family
  and requires later classification of all status-bearing README files.
- **VAL-129-005**: Parent list ordering is documented and tested as
  deterministic serialization without semantic priority.
- **VAL-129-006**: `_workspace` appears in canonical audit coverage while
  remaining independently enforced and outside docs metadata inference.
- **VAL-129-007**: Focused tests, full validation, traceability, alignment,
  generated freshness, and repository contracts pass with zero failures.
- **VAL-129-008**: No target corpus wave, runtime, secret, deployment, ruleset,
  environment, or remote branch-protection mutation occurs in this sub-project.

### Program Completion Criteria

- Every copyable artifact and Release role is mapped to one profile and
  template contract.
- Every README is classified under one explicit profile.
- Migrated targets contain no legacy duplicate-purpose keys, unresolved
  placeholders, copied template instructions, or duplicate-purpose sections.
- Final metadata inventory has zero unresolved `missing-required-key`,
  `replacement-free-supersession`, and `stale-active` findings in the approved
  target corpus and zero legacy exceptions.
- Shared contracts, governance, and templates have one canonical owner per
  hierarchy and scope.
- `_workspace` retains exactly two tracked contract README files.
- Full local QA and the controlled all-files wrapper pass.
- Classic `main` protection required checks exactly match the local CI contract
  after audited remote application and API read-back.
- Runtime deployment and secret values remain unchanged and undisclosed.
- Every sub-project task review and the final program review are approved.

## Related Documents

- [Spec 128](../128-agentic-audit-harness-consolidation/spec.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Template support](../../99.templates/support/README.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [Canonical audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Metadata inventory](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md)
- [`_workspace` contract](../../../_workspace/README.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
