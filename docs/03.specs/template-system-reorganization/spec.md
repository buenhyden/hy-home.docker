---
status: superseded
---

<!-- Target: docs/03.specs/template-system-reorganization/spec.md -->

# Template System Reorganization Technical Specification

## Overview

This document preserves the earlier design contract for reorganizing
`docs/99.templates` from a flat template folder into a structured template
system with two explicit responsibilities:

- `docs/99.templates/templates/` holds copyable document and contract templates.
- `docs/99.templates/support/` holds non-copyable template governance,
  frontmatter rules, lifecycle vocabulary, selection guidance, and source-backed
  rationale.

This design is superseded by
[Template System Contract Standardization](../template-system-contract-standardization/spec.md).
Use the replacement spec and Stage 99 support contracts for current template,
frontmatter, archive, and governance rules.

## Strategic Boundaries & Non-goals

- The first implementation cycle reorganizes `docs/99.templates`, updates
  contract/governance and validation surfaces that directly depend on the
  template layout, and fixes direct reference fallout caused by the move.
- Existing stage documents are updated only where the template migration creates
  broken links, invalid frontmatter expectations, README contract fallout, or
  validator-visible drift.
- The first implementation cycle does not rewrite every existing stage document
  body into the new template shape.
- The work does not change runtime behavior, Docker Compose configuration,
  secrets, provider credentials, remote GitHub state, or production deployment
  behavior.
- The work may update protected governance and validation surfaces because the
  user explicitly approved contract, governance, and protected-surface changes
  for this template-system task.

## Related Inputs

- **User-approved direction**: 2026-07-02 conversation approval for the
  research-backed `docs/99.templates` reorganization design.
- **Current replacement spec**:
  [Template System Contract Standardization](../template-system-contract-standardization/spec.md)
- **Current Template Catalog**:
  [../../99.templates/README.md](../../99.templates/README.md)
- **Documentation Protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Repository Contract Validator**:
  [../../../scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
- **CommonMark**: [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/)
- **GitHub Flavored Markdown**: [GFM specification](https://github.github.com/gfm/)
- **Frontmatter Convention**:
  [Jekyll front matter](https://jekyllrb.com/docs/front-matter/) and
  [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)
- **YAML Baseline**: [YAML 1.2.2](https://yaml.org/spec/1.2.2/)
- **Schema Validation Model**:
  [JSON Schema specification](https://json-schema.org/specification)
- **Documentation Taxonomy**: [Diataxis](https://diataxis.fr/)
- **Template Practice Reference**:
  [The Good Docs Project templates](https://www.thegooddocsproject.dev/template)
- **Security SDLC Overlay**: [NIST SSDF](https://csrc.nist.gov/projects/ssdf)

## Contracts

| Contract | Required Behavior |
| --- | --- |
| Copyable template boundary | Files under `docs/99.templates/templates/` are the only copyable template artifacts. |
| Support governance boundary | Files under `docs/99.templates/support/` are explanatory or validation-oriented support documents and must not be copied as target document bodies. |
| README role | `docs/99.templates/README.md` is a concise catalog and routing entrypoint, not the primary contract or governance body. |
| Contract separation | Template contracts, frontmatter rules, lifecycle vocabulary, and selection rules live in support documents. |
| Frontmatter normalization | Template sources and target documents use explicit type-appropriate key sets; duplicate-purpose legacy keys are removed. |
| Validator parity | `scripts/validation/check-repo-contracts.sh` recognizes the nested template layout and validates templates recursively where appropriate. |
| Legacy cleanup | Flat legacy template files are removed after all direct references and validator assumptions are updated. |
| Stage compliance | Active SDLC documentation stays under `docs/01` through `docs/05`; templates stay under Stage 99; references and research remain under Stage 90. |

## Core Design

### Target Directory Taxonomy

```text
docs/99.templates/
├── README.md
├── support/
│   ├── README.md
│   ├── template-contract.md
│   ├── template-governance.md
│   ├── frontmatter-contract.md
│   ├── lifecycle-status.md
│   ├── template-selection.md
│   └── external-source-rationale.md
└── templates/
    ├── README.md
    ├── sdlc/
    ├── spec-contracts/
    ├── operations/
    ├── governance/
    └── common/
```

### Template Category Mapping

| Category | Target Directory | Template Roles |
| --- | --- | --- |
| SDLC | `docs/99.templates/templates/sdlc/` | PRD, ARD, ADR, Spec, Plan, Task |
| Spec contracts | `docs/99.templates/templates/spec-contracts/` | API spec, agent design, data model, service contract, tests, OpenAPI, GraphQL, Protobuf |
| Operations | `docs/99.templates/templates/operations/` | Guide, policy, runbook, incident, postmortem |
| Governance | `docs/99.templates/templates/governance/` | Memory note, progress log, harness task contract |
| Common | `docs/99.templates/templates/common/` | README, reference, archive |

### Support Document Roles

| Support Document | Role |
| --- | --- |
| `template-contract.md` | Defines copyable template shape, required source metadata, required target guidance, and Related Documents ownership. |
| `template-governance.md` | Defines who may change templates, how changes propagate, protected surface rules, review expectations, and logical commit boundaries. |
| `frontmatter-contract.md` | Defines type-specific frontmatter key sets, values, duplicate-key removal rules, and legacy key migration rules. |
| `lifecycle-status.md` | Defines allowed status values and lifecycle meaning for template sources, active stage docs, archives, generated files, and governance memory. |
| `template-selection.md` | Maps stage/document purpose to the correct template and explains README profile selection. |
| `external-source-rationale.md` | Records why CommonMark, GFM, YAML, JSON Schema, Diataxis, Good Docs, SDLC, and SSDF sources shape the repo-local rules. |

### README Responsibility

`docs/99.templates/README.md` must remain a short entrypoint with:

- overview
- audience
- scope
- structure
- category catalog
- how to work in the area
- related documents

Detailed lifecycle rules, stale document rules, cross-link rules, README profile
rules, frontmatter schema rules, and validation ownership move to support
documents. This prevents README from becoming both a catalog and a governance
manual.

## Data Modeling & Storage Strategy

The template system uses file paths, frontmatter metadata, and support documents
as its data model.

### Template Path Model

| Field | Meaning |
| --- | --- |
| `category` | One of `sdlc`, `spec-contracts`, `operations`, `governance`, or `common`. |
| `template_role` | The document role, such as `prd`, `spec`, `runbook`, `readme`, or `reference`. |
| `source_path` | The canonical template source path under `docs/99.templates/templates/`. |
| `target_pattern` | The allowed destination path pattern for documents copied from the template. |
| `support_contract` | The support document that defines metadata and section expectations for the template role. |

### Frontmatter Field Families

| Family | Intended Surface | Notes |
| --- | --- | --- |
| Template source metadata | `docs/99.templates/templates/**/*.template.*` | Minimal source metadata; Markdown templates keep `status: draft`. |
| Active stage lifecycle | `docs/01` through `docs/05` and `docs/90` | Uses lifecycle status values and type-appropriate keys only. |
| Archive lifecycle | `docs/98.archive` | Uses `status: archived` and archive-specific provenance keys. |
| Governance memory | `docs/00.agent-governance/memory` | Keeps governance memory fields separate from stage document lifecycle fields. |
| Generated metadata | generated tracked files | Keeps generator fields such as `generated_by` separate from human-authored document type fields. |

## Interfaces & Data Structures

### Proposed Template Inventory

| Current Flat Template | Target Category | Target Path |
| --- | --- | --- |
| `prd.template.md` | SDLC | `docs/99.templates/templates/sdlc/prd.template.md` |
| `ard.template.md` | SDLC | `docs/99.templates/templates/sdlc/ard.template.md` |
| `adr.template.md` | SDLC | `docs/99.templates/templates/sdlc/adr.template.md` |
| `spec.template.md` | SDLC | `docs/99.templates/templates/sdlc/spec.template.md` |
| `plan.template.md` | SDLC | `docs/99.templates/templates/sdlc/plan.template.md` |
| `task.template.md` | SDLC | `docs/99.templates/templates/sdlc/task.template.md` |
| `api-spec.template.md` | Spec contracts | `docs/99.templates/templates/spec-contracts/api-spec.template.md` |
| `agent-design.template.md` | Spec contracts | `docs/99.templates/templates/spec-contracts/agent-design.template.md` |
| `data-model.template.md` | Spec contracts | `docs/99.templates/templates/spec-contracts/data-model.template.md` |
| `service.template.md` | Spec contracts | `docs/99.templates/templates/spec-contracts/service.template.md` |
| `tests.template.md` | Spec contracts | `docs/99.templates/templates/spec-contracts/tests.template.md` |
| `openapi.template.yaml` | Spec contracts | `docs/99.templates/templates/spec-contracts/openapi.template.yaml` |
| `schema.template.graphql` | Spec contracts | `docs/99.templates/templates/spec-contracts/schema.template.graphql` |
| `service.template.proto` | Spec contracts | `docs/99.templates/templates/spec-contracts/service.template.proto` |
| `guide.template.md` | Operations | `docs/99.templates/templates/operations/guide.template.md` |
| `policy.template.md` | Operations | `docs/99.templates/templates/operations/policy.template.md` |
| `runbook.template.md` | Operations | `docs/99.templates/templates/operations/runbook.template.md` |
| `incident.template.md` | Operations | `docs/99.templates/templates/operations/incident.template.md` |
| `postmortem.template.md` | Operations | `docs/99.templates/templates/operations/postmortem.template.md` |
| `memory.template.md` | Governance | `docs/99.templates/templates/governance/memory.template.md` |
| `progress.template.md` | Governance | `docs/99.templates/templates/governance/progress.template.md` |
| `harness-task-contract.template.md` | Governance | `docs/99.templates/templates/governance/harness-task-contract.template.md` |
| `readme.template.md` | Common | `docs/99.templates/templates/common/readme.template.md` |
| `reference.template.md` | Common | `docs/99.templates/templates/common/reference.template.md` |
| `archive.template.md` | Common | `docs/99.templates/templates/common/archive.template.md` |

### Validation Interface

The repository contract validator must expose a single internal template
inventory map instead of repeating flat path assumptions. The inventory should
drive these checks:

- required template existence
- recursive misplaced-template detection
- Markdown template source frontmatter
- target guidance and target-relative link guidance
- machine-readable contract cross-link ownership
- reference, memory, harness, and README profile checks
- changed-doc unknown-type messages

## API Contract (If Applicable)

No runtime API is introduced. The only contract interface is repository-local:

- template paths under `docs/99.templates/templates/`
- support governance paths under `docs/99.templates/support/`
- validator checks in `scripts/validation/check-repo-contracts.sh`
- governance references in Stage 00 rules and hook guidance

Machine-readable API examples remain template artifacts under the spec-contracts
category.

## Agent Role & IO Contract (If Applicable)

| Role | Input | Output |
| --- | --- | --- |
| Documentation Specialist | Current template files, support rules, stage contracts | Reorganized templates and support docs with normalized metadata. |
| Research Orchestrator | External standards and documentation frameworks | Source-backed rationale for local template governance. |
| Reviewer | Final diff, validator output, reference search results | Findings on missing references, validator gaps, or duplicated responsibilities. |

## Tools & Tool Contract (If Applicable)

- Use `rg` and read-only shell commands for repo evidence discovery.
- Use web verification for external documentation and standards whose current
  guidance may change.
- Use `apply_patch` for manual edits.
- Use `git mv` for template relocation so history is preserved.
- Use logical commits:
  1. design spec,
  2. template relocation and support structure,
  3. governance and validator alignment,
  4. direct reference fallout and progress update.

## Prompt / Policy Contract (If Applicable)

- Do not add new active non-stage documentation paths.
- Do not leave flat legacy template files behind as compatibility shims.
- Do not put support governance content back into `docs/99.templates/README.md`
  after it has been moved to support documents.
- Do not claim that frontmatter is CommonMark syntax; treat it as a
  preprocessor convention validated separately from Markdown body parsing.
- Do not keep duplicate-purpose frontmatter keys for the same document type.

## Memory & Context Strategy (If Applicable)

`docs/00.agent-governance/memory/progress.md` records the migration progress and
known gaps. Durable lessons learned from the migration may use the governance
memory template after the template paths are updated.

The Stage 03 spec remains the design memory for the migration and should not be
duplicated into Stage 99 support documents.

## Guardrails (If Applicable)

- Keep SDLC content under `docs/01` through `docs/05`.
- Keep templates under `docs/99.templates/templates/`.
- Keep template rules under `docs/99.templates/support/`.
- Keep source-backed external rationale in support docs without turning it into
  active policy outside Stage 99.
- Do not rewrite historical task, incident, or audit evidence unless validation
  requires a minimal metadata or link repair.
- Treat unrelated validation failures as gaps unless they are caused by this
  migration.

## Evaluation (If Applicable)

The migration is evaluated through repository contract checks, link/path
consistency, and review of source-backed governance separation rather than
runtime tests.

Expected evaluation questions:

- Does every template have one canonical source path?
- Does every support document have one clear non-copyable role?
- Does every moved template reference resolve from governance and validators?
- Does frontmatter guidance distinguish template source metadata from target
  document lifecycle metadata?
- Does `docs/99.templates/README.md` stay an index instead of a policy dump?

## Edge Cases & Error Handling

- If validator recursion accidentally treats support examples as copyable
  templates, adjust template discovery to match `*.template.*` only under the
  `templates/` tree.
- If a direct reference points to a deleted flat template path, update it to the
  new canonical path or a support catalog path depending on whether it means
  copyable template or governance guidance.
- If an existing document contains copied template instructions instead of
  topic-specific content, record the gap unless the document is directly touched
  by validation fallout.
- If an external source changes or becomes unavailable, keep the repo-local rule
  and update only the source rationale in support docs.
- If broad document corpus normalization is still needed after migration, create
  a separate Stage 04 plan rather than expanding the first implementation cycle.

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback |
| --- | --- |
| Template relocation breaks repository contract validation | Update the validator inventory and path classification in the same logical commit. |
| README becomes a governance manual again | Move detailed rules back into support documents and keep README as routing. |
| Frontmatter key set becomes too broad | Split by document type and keep only lifecycle or provenance fields that the type consumes. |
| Legacy flat paths remain referenced | Run reference search, update direct links, and record any historical references that intentionally remain. |
| Existing stage document rewrite scope grows too large | Stop at validation-required fallout and capture remaining corpus normalization as a gap. |

## Verification

The design and later implementation use documentation and repository contract
checks.

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Known unrelated repository drift must be reported as out of scope instead of
being patched during the template migration.

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `docs/99.templates/templates/` contains the single canonical
  copyable template tree.
- **VAL-SPC-002**: `docs/99.templates/support/` contains the single canonical
  non-copyable governance and contract tree.
- **VAL-SPC-003**: No flat legacy `docs/99.templates/*.template.*` source files
  remain after the relocation implementation commit.
- **VAL-SPC-004**: Stage 00 governance and validator checks reference the new
  canonical template paths.
- **VAL-SPC-005**: Frontmatter rules are type-specific and remove
  duplicate-purpose legacy keys.
- **VAL-SPC-006**: Existing stage document fallout is limited to direct broken
  references, frontmatter/README contract fallout, or validator-required
  repairs.
- **VAL-SPC-007**: External-source rationale is recorded in support docs and is
  reflected in local contract rules.

## Related Documents

- [spec README](./README.md)
- [docs/03.specs README](../README.md)
- [template catalog](../../99.templates/README.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [repo contract validator](../../../scripts/validation/check-repo-contracts.sh)
