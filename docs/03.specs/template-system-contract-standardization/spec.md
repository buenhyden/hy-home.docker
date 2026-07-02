---
status: draft
---

<!-- Target: docs/03.specs/template-system-contract-standardization/spec.md -->

# Template System Contract Standardization Technical Specification

## Overview

This document defines the design contract for the next `docs/99.templates`
standardization pass. The work combines two approved directions:

- **A: Template system-wide design**: keep `docs/99.templates/support/` as the
  non-copyable contract and governance surface, and keep
  `docs/99.templates/templates/` as the copyable template artifact surface.
- **B: Frontmatter and contract standardization**: define type-specific
  frontmatter, section profiles, target path contracts, and validator rules so
  template sources and target documents do not reuse legacy metadata or
  duplicate-purpose keys.

The design is contract-first. Support documents define the rules first;
templates then implement those rules; validators enforce the contract; target
documents receive only direct fallout fixes unless a separate implementation
plan approves broader corpus normalization.

## Strategic Boundaries & Non-goals

This spec owns the design for Stage 99 template contract standardization. It
does not itself implement the changes.

In scope:

- Audit all files under `docs/99.templates/`, including support documents,
  copyable templates, README indexes, and machine-readable template artifacts.
- Standardize Markdown template source frontmatter to the minimal source
  metadata allowed by the support contract.
- Define target-document frontmatter by document role rather than by generic
  `type`, `owner`, `updated`, or `links` keys.
- Keep template forms and support contracts separate.
- Update validator expectations for template layout, frontmatter, target path,
  and legacy-key drift.
- Apply direct fallout only where changed templates or support contracts create
  broken links, invalid target comments, provider-surface drift, or validator
  failures.

Out of scope:

- Rewriting all target stage documents into the newest template body shape.
- Changing runtime Docker Compose behavior, secrets, credentials, remote GitHub
  state, deployment behavior, or production service configuration.
- Creating new top-level docs stages outside the existing repository taxonomy.
- Treating `docs/99.templates/README.md` as a governance manual.

## Related Inputs

- **Existing template reorganization spec**:
  [../template-system-reorganization/spec.md](../template-system-reorganization/spec.md)
- **Template catalog**:
  [../../99.templates/README.md](../../99.templates/README.md)
- **Template contract**:
  [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**:
  [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Template governance**:
  [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Template selection guide**:
  [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Documentation protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Repository contract validator**:
  [../../../scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
- **Diataxis**: [https://diataxis.fr/](https://diataxis.fr/)
- **The Good Docs Project templates**:
  [https://www.thegooddocsproject.dev/template](https://www.thegooddocsproject.dev/template)
- **CommonMark front matter discussion**:
  [https://talk.commonmark.org/t/front-matter-best-practice/2235](https://talk.commonmark.org/t/front-matter-best-practice/2235)
- **Google developer documentation style guide**:
  [https://developers.google.com/style](https://developers.google.com/style)

## Contracts

### Template System Contract

| Contract Area | Required Behavior |
| --- | --- |
| Copyable artifact boundary | Copyable templates live only under `docs/99.templates/templates/`. |
| Support rule boundary | Non-copyable contracts, governance, lifecycle, frontmatter, and selection rules live under `docs/99.templates/support/`. |
| README role | Stage 99 README files remain catalog, routing, and index surfaces. They do not become the canonical rule body when a support document owns the rule. |
| One canonical role | A document role has one canonical template source. Duplicate templates with the same purpose are removed or merged. |
| Target path ownership | Each template declares a target path pattern that matches `template-selection.md` and validator rules. |
| Validator parity | `check-repo-contracts.sh` enforces the source layout, frontmatter keys, target comments, and legacy path/key bans. |
| Protected surface handling | Changes to templates, validators, provider surfaces, and governance rules require explicit progress evidence and rollback notes. |

### Frontmatter Contract

| Surface | Allowed Metadata |
| --- | --- |
| Markdown template sources | `status: draft` only, unless a future validator accepts an additional source-only key. |
| Machine-readable templates | No YAML frontmatter; use comments for target guidance. |
| Stage 99 support documents | `layer: agentic` when the document is a governance or support entrypoint. |
| Stage 01-05 and Stage 90 target documents | Path-derived role plus lifecycle `status`; no duplicate-purpose `type` key. |
| Archive tombstones | `status: archived` plus archive-specific provenance only when the archive profile requires it. |
| Generated tracked docs | Generator-owned metadata such as `generated_by`; no human-authored lifecycle fields unless the generator contract requires them. |

Legacy metadata keys such as `type`, `owner`, `updated`, and `links` are
disallowed when they duplicate path-derived document role, ownership, or related
documents sections.

## Core Design

### Support Surface

`docs/99.templates/support/` is the rule surface. It should contain a small set
of non-copyable documents with clear ownership:

| Support Document | Design Role |
| --- | --- |
| `template-contract.md` | Defines common template-source requirements, target guidance, placeholder rules, and target document inheritance. |
| `frontmatter-contract.md` | Defines allowed metadata by source family and target family. |
| `template-governance.md` | Defines protected surface handling, change boundaries, review expectations, and commit boundaries. |
| `template-selection.md` | Maps target path patterns to canonical templates. |
| `lifecycle-status.md` | Defines allowed lifecycle values and where each value can appear. |
| `external-source-rationale.md` | Records the external documentation and metadata sources used to justify local rules. |

### Copyable Template Surface

`docs/99.templates/templates/` is the artifact surface. Its subfolders remain:

| Template Category | Responsibility |
| --- | --- |
| `sdlc/` | PRD, ARD, ADR, Spec, Plan, and Task templates. |
| `spec-contracts/` | Child contracts for API, agent design, data model, service, tests, OpenAPI, GraphQL, and Protobuf. |
| `operations/` | Guide, policy, runbook, incident, and postmortem templates. |
| `governance/` | Memory note, progress log, and harness task contract templates. |
| `common/` | README, reference, and archive templates. |

Copyable templates may include usage instructions because those instructions
are removed or replaced when creating target documents. Support documents must
not be copied as target bodies.

### README Surface

README files in Stage 99 are constrained to:

- Overview
- Audience
- Scope
- Structure
- Category or document catalog
- How to Work in This Area
- Related Documents

When a README contains durable rules that belong to a support document, the
implementation should move or summarize the rule in support and leave the README
with a link to the support source.

## Data Modeling & Storage Strategy

The design treats template metadata as a small repository-local schema.

### Template Role Record

| Field | Source | Purpose |
| --- | --- | --- |
| `role` | Path and filename | Identifies the canonical document role. |
| `source_path` | `docs/99.templates/templates/**` | Identifies the copyable template artifact. |
| `target_pattern` | Template target comment and `template-selection.md` | Defines where copied documents may live. |
| `frontmatter_family` | `frontmatter-contract.md` | Defines allowed metadata keys and values. |
| `section_profile` | Template body and support contract | Defines required and forbidden sections. |
| `validator_rule` | `check-repo-contracts.sh` | Enforces the contract. |

### Metadata Normalization Rules

- Use path and template mapping to determine document role.
- Use frontmatter only for lifecycle or generator metadata that cannot be
  reliably inferred from path.
- Prefer `## Related Documents` sections over frontmatter link arrays.
- Prefer support contract tables over repeated long instruction blocks inside
  README files.
- Keep target path examples relative to copied target paths, not template source
  paths.

## Interfaces & Data Structures

### Canonical Template Groups

| Group | Canonical Files |
| --- | --- |
| SDLC | `prd.template.md`, `ard.template.md`, `adr.template.md`, `spec.template.md`, `plan.template.md`, `task.template.md` |
| Spec contracts | `api-spec.template.md`, `agent-design.template.md`, `data-model.template.md`, `service.template.md`, `tests.template.md`, `openapi.template.yaml`, `schema.template.graphql`, `service.template.proto` |
| Operations | `guide.template.md`, `policy.template.md`, `runbook.template.md`, `incident.template.md`, `postmortem.template.md` |
| Governance | `memory.template.md`, `progress.template.md`, `harness-task-contract.template.md` |
| Common | `readme.template.md`, `reference.template.md`, `archive.template.md` |

### Validator Interfaces

The implementation plan should update or confirm these validator behaviors:

- all required template files exist at canonical nested paths
- no template files exist outside `docs/99.templates/templates/`
- Markdown template sources start with `status: draft`
- support documents use `layer: agentic` where applicable
- machine-readable templates do not use Markdown frontmatter
- target comments match `template-selection.md`
- removed legacy paths and legacy frontmatter keys do not reappear
- README files do not become hidden contract manuals when support owns the rule

## API Contract (If Applicable)

This work does not expose an external API.

Machine-readable template files are internal contract artifacts only:

- `docs/99.templates/templates/spec-contracts/openapi.template.yaml`
- `docs/99.templates/templates/spec-contracts/schema.template.graphql`
- `docs/99.templates/templates/spec-contracts/service.template.proto`

## Agent Role & IO Contract (If Applicable)

### Agent Role

Agents working on this implementation act as documentation-system maintainers.
They may edit Stage 99 templates/support docs, direct governance fallout, direct
target-document fallout, validators, provider mirrors, progress logs, and LLM
Wiki indexes.

### Inputs

- Existing Stage 99 templates and support documents.
- Stage 00 documentation governance.
- Repository contract validator behavior.
- External rationale sources listed in `## Related Inputs`.

### Outputs

- Updated Stage 99 support contracts.
- Updated copyable templates.
- Updated validator rules.
- Updated direct fallout references.
- Updated progress evidence.
- Updated generated LLM Wiki index when tracked documentation changes.

### Success Definition

The work succeeds when Stage 99 has one canonical template per role, frontmatter
rules are explicit and enforced, README surfaces remain indexes, and validation
shows no template-system regressions. Known infra image/version drift remains
out of scope and must be reported as a gap.

## Tools & Tool Contract (If Applicable)

- Use `rg` and `find` for inventory and stale reference searches.
- Use `git mv` for template relocation when any remaining path move is needed.
- Use `apply_patch` for manual document edits.
- Use `bash scripts/operations/sync-provider-surfaces.sh --check` after
  provider-facing template or skill text changes.
- Use `bash scripts/knowledge/generate-llm-wiki-index.sh` after adding, moving,
  or deleting tracked docs.

## Prompt / Policy Contract (If Applicable)

Implementation agents must treat this as a protected documentation governance
change. They must not modify runtime configuration, secret values, provider
credentials, or remote GitHub settings. If a target document contains copied
template instructions that require broad rewriting, the agent records a gap
unless that document is in the approved implementation scope.

## Memory & Context Strategy (If Applicable)

Update `docs/00.agent-governance/memory/progress.md` with:

- scope summary
- protected surfaces touched
- verification commands and outcomes
- known out-of-scope gaps
- commit boundaries

Do not paste raw command logs or secrets into memory.

## Guardrails (If Applicable)

- Do not add new top-level docs stages.
- Do not keep compatibility shims for legacy template paths unless explicitly
  approved in a separate plan.
- Do not add generic frontmatter keys that duplicate path-derived role.
- Do not hide governance rules inside README files when support documents own
  the rule.
- Do not modify unrelated stage documents except direct fallout from template
  contract changes.
- Do not resolve existing infra image/version drift in this implementation.

## Evaluation (If Applicable)

Evaluation is repository validation plus targeted stale-reference scans.

- Template inventory scan reports no duplicate canonical roles.
- Legacy path scan reports no references to removed flat template paths.
- Frontmatter scan reports only allowed key families.
- Provider sync reports no drift.
- LLM Wiki index freshness check passes after tracked documentation changes.

## Edge Cases & Error Handling

- **Existing target document has template instructions copied verbatim**:
  update only when it is direct fallout; otherwise record a gap.
- **README contains rules that overlap support**: move the durable rule to
  support and leave a concise README link.
- **Validator fails on unrelated infra drift**: report the drift as out of
  scope; do not mix runtime fixes into template commits.
- **Frontmatter key appears useful but duplicates path role**: remove it and
  make the role path-derived.
- **Machine-readable template needs metadata**: use comments, not YAML
  frontmatter.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Template relocation creates many stale links.
  **Fallback**: pause relocation, run a targeted stale path inventory, and split
  the work into a path-only commit before content normalization.
- **Failure Mode**: Validator contract becomes too broad and blocks unrelated
  docs.
  **Fallback**: narrow the validator to Stage 99 or changed target surfaces.
- **Failure Mode**: Existing documents require broad body rewrites.
  **Fallback**: record the documents as follow-up gaps unless the implementation
  plan explicitly includes them.
- **Human Escalation**: Ask for approval before deleting a template role when
  two files appear to serve overlapping but not identical purposes.

## Verification

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-TPL-001**: Stage 99 has a documented contract-first design for support
  docs, copyable templates, frontmatter, README role, and validator parity.
- **VAL-TPL-002**: No implementation change starts until this spec is reviewed
  and approved.
- **VAL-TPL-003**: The implementation plan derived from this spec separates
  support contract edits, template edits, validator edits, direct fallout, and
  generated index updates into logical commits where practical.
- **VAL-TPL-004**: Full repo contract validation has no template-system
  failures; existing infra image/version drift may remain as an out-of-scope
  gap.

## Related Documents

- **Prior Template System Spec**:
  [../template-system-reorganization/spec.md](../template-system-reorganization/spec.md)
- **Template catalog**:
  [../../99.templates/README.md](../../99.templates/README.md)
- **Template contract**:
  [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**:
  [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Template governance**:
  [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Template selection guide**:
  [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Documentation protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
