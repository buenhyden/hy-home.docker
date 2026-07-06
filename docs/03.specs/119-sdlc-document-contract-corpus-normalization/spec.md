---
status: active
---

<!-- Target: docs/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md -->

# SDLC Document Contract Corpus Normalization Technical Specification

## Overview

This specification defines the contract-first normalization program for the
remaining SDLC documentation corpus drift in `hy-home.docker`.

The repository already migrated PRD files to
`docs/01.requirements/NNN-feature-or-system.md`, Spec folders to
`docs/03.specs/NNN-feature-id/`, and Stage 99 templates into a separated
`support/` and `templates/` model. This spec does not repeat that completed
path migration. It covers the next layer: stale rule text, validator coverage
gaps, Stage 03/04 lifecycle decisions, operations leaf naming polish, and
closure evidence for changes that affect how agents and humans consume the
documentation system.

The design is intentionally staged. This spec creates no target corpus edits by
itself. Implementation must proceed through Stage 04 plan and task evidence,
with logical commits per wave.

## Strategic Boundaries & Non-goals

### Goals

- Align stale PRD and Spec path guidance with the numbered path contract.
- Extend validator coverage so obsolete PRD/Spec examples are caught outside
  Stage 99 template files.
- Decide and document whether sibling README files under `docs/03.specs/NNN-*`
  are mandatory, optional, or required only for new/current workstreams.
- Classify Stage 04 plan/task naming asymmetry as historical evidence,
  accepted task-only evidence, or future rename candidate before enforcement.
- Review remaining operations leaf naming candidates without collapsing guide,
  policy, and runbook purposes.
- Preserve the existing `_workspace` protected-surface contract.
- Keep external sources as rationale while preserving Stage 00 and Stage 99 as
  repository-local policy owners.

### Non-goals

- No Docker Compose runtime, service image, secret, credential, deployment, or
  remote GitHub mutation in the design wave.
- No broad Markdown rewrite for style alone.
- No automatic enforcement of plan/task exact-stem pairing until Stage 04
  evidence proves the rule and exception set.
- No conversion of accepted historical evidence into active current guidance.
- No new active spec, plan, or task artifacts under non-stage paths such as
  `docs/superpowers/`.
- No CI hard gate for dependency audit, Graphify, SLSA provenance, SBOM, or
  attestation without a separate approved automation design.

## Related Inputs

- **PRD**: Not required. The user approval for this governance/documentation
  normalization wave is the initiating requirement source.
- **ARD**: Not required. Existing Stage 00 governance and Stage 99 support
  contracts define the architecture boundary.
- **Related ADRs**:
  - [Stage 00 canonical adapter model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Numbered SDLC path migration**:
  [../099-template-system-numbered-sdlc-paths/spec.md](../099-template-system-numbered-sdlc-paths/spec.md)
- **Template contract standardization**:
  [../100-template-system-contract-standardization/spec.md](../100-template-system-contract-standardization/spec.md)
- **Document restructure disposition contract**:
  [../103-document-restructure-audit-contract-archive/spec.md](../103-document-restructure-audit-contract-archive/spec.md)
- **Workspace support surface contract**:
  [../106-workspace-support-surface-contract/spec.md](../106-workspace-support-surface-contract/spec.md)
- **Documentation protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Template governance**:
  [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Template selection**:
  [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Frontmatter contract**:
  [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Lifecycle status**:
  [../../99.templates/support/lifecycle-status.md](../../99.templates/support/lifecycle-status.md)
- **External rationale**:
  - [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
  - [OWASP SAMM](https://owaspsamm.org/model/)
  - [Diataxis](https://diataxis.fr/)
  - [The Good Docs Project templates](https://www.thegooddocsproject.dev/template)
  - [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
  - [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
  - [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)
  - [SLSA specification](https://slsa.dev/spec/)
  - [CommonMark](https://spec.commonmark.org/spec)
  - [GitHub Flavored Markdown](https://github.github.com/gfm/)
  - [Jekyll front matter](https://jekyllrb.com/docs/front-matter/)
  - [Git ignore documentation](https://git-scm.com/docs/gitignore)
  - [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

## Contracts

### Config Contract

- This design does not change runtime configuration.
- Validator updates are allowed only through a Stage 04 plan/task wave that
  records before evidence, after evidence, rollback path, and redaction
  boundary.
- GitHub workflow changes remain protected automation surfaces and require
  explicit approval if a later wave proposes them.

### Data / Interface Contract

| Surface | Required Contract |
| --- | --- |
| PRD path | `docs/01.requirements/NNN-feature-or-system.md` is the canonical active PRD path form. |
| Spec path | `docs/03.specs/NNN-feature-id/spec.md` is the canonical parent Spec path form. |
| Stage 04 plan/task path | Date-prefixed execution evidence remains valid unless a future plan/task lifecycle wave changes it. |
| Stage 03 sibling README | Optional for historical folders until this program decides the policy; recommended for new active design folders that need routing context. |
| Stage 05 operations leaves | Guide, policy, and runbook documents remain separate role surfaces even when path names are normalized. |
| Stage 90 reports | Evidence-only. Reports may classify drift but must not become active policy or runtime truth. |
| Stage 98 archive | Tombstone-only. Archive records original path, archive reason, and current replacement or `N/A`. |
| `_workspace` | Repo-support staging only. Durable results must be promoted to canonical stages. |

### Governance Contract

- Stage 00 owns agent-facing behavior, stage routing, and bootstrap policy.
- Stage 99 support documents own template, frontmatter, lifecycle, selection,
  archive, and destructive-change rules.
- README files remain routing/index surfaces and must not become hidden policy
  manuals.
- External sources justify local design choices but do not override repository
  contracts.
- Historical evidence is preserved unless an active-consumption conflict is
  proven and recorded.

## Core Design

### Component Boundary

This program has five implementation waves:

| Wave | Scope | Default Commit Boundary |
| --- | --- | --- |
| Wave 1 | Contract text cleanup for stale PRD/Spec path guidance. | `docs(governance): Align SDLC path guidance` |
| Wave 2 | Validator coverage for legacy PRD/Spec guidance across Stage 00, Stage 01/03 README files, and `.github` templates. | `test(docs): Extend SDLC contract drift checks` |
| Wave 3 | Stage 03/04 lifecycle decision and audit for sibling README policy and plan/task naming asymmetry. | `docs(execution): Classify SDLC lifecycle normalization gaps` |
| Wave 4 | Operations leaf naming polish for approved exact candidates. | `docs(ops): Normalize operations leaf naming` |
| Wave 5 | Closure evidence, generated indexes, progress memory, and residual gap register updates. | `docs(tasks): Close SDLC corpus normalization` |

### Key Dependencies

- `scripts/validation/check-repo-contracts.sh`
- `scripts/validation/check-doc-traceability.sh`
- `scripts/validation/check-doc-implementation-alignment.sh`
- `scripts/knowledge/generate-llm-wiki-index.sh`
- `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md`
- `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md`

### Tech Stack

- Markdown stage documents.
- Repository-local shell/Python validation scripts.
- Git path moves only when an implementation wave has exact candidates.
- Stage 90 reference/audit reports for evidence that should not be active
  policy.

## Data Modeling & Storage Strategy

### Normalization Finding Record

Each implementation wave should classify findings with this shape in task
evidence or a Stage 90 audit report:

| Field | Meaning |
| --- | --- |
| `id` | Stable finding ID, preferably `SDCN-GAP-###`. |
| `surface` | Exact file, folder, validator, or workflow surface. |
| `finding` | Short statement of the mismatch or candidate. |
| `disposition` | `active-canonical`, `historical-archive`, `duplicate-remove`, `conflict-remove-or-archive`, `evidence-preserve`, or `validator-gap`. |
| `owner_stage` | Canonical owner stage for the fix. |
| `wave` | Implementation wave that may mutate the surface. |
| `validation` | Command or manual check that proves the disposition. |

### Initial Finding Seeds

| ID | Surface | Finding | Initial Disposition | Wave |
| --- | --- | --- | --- | --- |
| `SDCN-GAP-001` | `docs/01.requirements/README.md` | Stale date-based PRD naming guidance conflicts with numbered PRD path contract. | `conflict-remove-or-archive` for text only | Wave 1 |
| `SDCN-GAP-002` | `docs/00.agent-governance/scopes/meta.md` | Stale date-prefixed feature-id guidance mixes PRD and plan naming. | `conflict-remove-or-archive` for text only | Wave 1 |
| `SDCN-GAP-003` | `scripts/validation/check-repo-contracts.sh` | Legacy PRD/Spec guidance scan is narrower than the surfaces where stale guidance appeared. | `validator-gap` | Wave 2 |
| `SDCN-GAP-004` | `.github/ISSUE_TEMPLATE/bug_report.yml` | Spec placeholder uses an unnumbered feature-id path instead of numbered folder guidance. | `conflict-remove-or-archive` for example text only | Wave 2 |
| `SDCN-GAP-005` | `docs/03.specs/091`, `092`, `100`, `110`-`118` | Some spec folders lack sibling README files, but current validators do not require them. | `evidence-preserve` until policy decision | Wave 3 |
| `SDCN-GAP-006` | `docs/04.execution/plans/**` and `docs/04.execution/tasks/**` | Historical plan/task filename stems are not always exact pairs. | `evidence-preserve` until lifecycle audit | Wave 3 |
| `SDCN-GAP-007` | `docs/05.operations/**/01.*.md` candidates | Some operations leaves retain numeric-dot legacy names. | `active-canonical` or rename candidate after exact review | Wave 4 |
| `SDCN-GAP-008` | Stage 90 frontmatter residuals | Prior audit accepted missing frontmatter residuals; reopen only if contract changes. | `evidence-preserve` | Wave 5 |

## Interfaces & Data Structures

### Validator Interfaces

Wave 2 may update `scripts/validation/check-repo-contracts.sh` so it rejects
stale active guidance such as:

- date-prefixed PRD filename patterns as active PRD target guidance outside
  historical migration tables.
- unnumbered `docs/03.specs/feature-id/spec.md` style examples as active Spec
  target guidance.
- ambiguous statements that combine PRD and plan naming under one
  date-prefixed feature-id rule.

The validator must preserve historical evidence exceptions for completed
specs, tasks, audit packs, and migration tables.

### Traceability Interfaces

Wave 3 should decide whether Stage 04 plan/task checks remain link-based or add
an advisory pair-classification report. Exact-stem matching must not become a
hard gate until the historical exception list is explicit.

### README Interfaces

New active governance/design Spec folders may include sibling README files for
routing. Historical folders without README files are not invalid unless a
future Stage 99 or Stage 00 rule explicitly makes them invalid.

## API Contract (If Applicable)

This work exposes no external API.

No OpenAPI, GraphQL, or Protobuf contract is required for this documentation
normalization program.

## Agent Role & IO Contract

| Role | Input | Output |
| --- | --- | --- |
| Documentation Specialist | Stage 00 rules, Stage 99 support contracts, current corpus evidence | Spec, plan, task, README, audit, and closure evidence. |
| Validator Maintainer | Current repo-contract checks and exact stale-guidance examples | Focused validator extensions with exception handling. |
| Operations Reviewer | Stage 05 guide/policy/runbook buckets and exact candidates | Role-safe operations naming recommendations. |
| Security Reviewer | Protected-surface and secret boundaries | Confirmation that no secret, raw log, credential, or runtime mutation is introduced. |

## Tools & Tool Contract

- Use `rg` and tracked file reads for local evidence.
- Use official external sources only as rationale for SDLC, documentation,
  CI/CD, Docker Compose, security, and metadata claims.
- Use `git mv` for approved path moves.
- Use `apply_patch` for manual content edits.
- Do not read secret values, raw logs, shell history, `.env` values,
  credentials, tokens, certificates, or private keys.
- Treat Graphify as advisory when its report is stale relative to `HEAD`.

## Prompt / Policy Contract

- Superpowers brainstorming gates require design approval before
  implementation. This spec is the approved design artifact for A:
  contract-first staged cleanup.
- Implementation must use Stage 04 plan/task evidence before mutating target
  corpus surfaces.
- Subagents may gather read-only evidence or execute disjoint implementation
  slices after a written plan assigns exact ownership.

## Memory & Context Strategy

- Use `docs/00.agent-governance/memory/progress.md` as the running work log.
- Promote durable findings to Stage 90 references or Stage 00 memory only when
  they are reusable and not active policy.
- Keep `_workspace/repo-support/` for ignored, short-lived, non-secret
  intermediate artifacts only.

## Guardrails

- Do not create or preserve alias documents at legacy PRD or Spec paths.
- Do not leave placeholder links in final target documents.
- Do not add lifecycle frontmatter to README files merely to resemble leaf
  target-stage documents unless the current folder profile already uses it.
- Do not move or delete active documents without an exact path list,
  disposition, replacement pointer, link synchronization, rollback path, and
  validation evidence.
- Do not convert accepted historical evidence into active policy.
- Do not make README files the durable owner for template, archive,
  frontmatter, or lifecycle rules.

## Evaluation

Evaluation is repository-local and evidence-based:

| Eval | Purpose |
| --- | --- |
| Repo contract check | Proves template, frontmatter, numbered path, reference, `_workspace`, and documentation contracts. |
| Doc traceability check | Proves plan/operations traceability surfaces remain synchronized. |
| Implementation alignment check | Proves active docs still align with tracked implementation surfaces. |
| LLM Wiki freshness | Proves generated navigation includes moved or added tracked docs. |
| Targeted stale-guidance scan | Proves old PRD/Spec target examples do not remain outside approved historical contexts. |

## Edge Cases & Error Handling

- **Historical migration tables contain old paths**: preserve them when the
  table explicitly records a migration.
- **Stage 04 task-only evidence has no parent plan**: classify it before
  enforcement; do not rename or delete it automatically.
- **Spec folder lacks README but has a valid `spec.md`**: record as policy
  decision candidate, not immediate failure.
- **Operations numeric-dot filename is linked and current**: update links only
  after exact candidate approval; otherwise record as accepted residual.
- **Validator false positive**: keep the rule advisory until exceptions are
  encoded and validation passes.

## Failure Modes & Fallback / Human Escalation

- **Validator change would fail historical evidence**: stop the hard-gate
  change and record an advisory audit row.
- **Destructive cleanup ambiguity**: ask for exact approval before moving or
  deleting active documents.
- **Remote GitHub or CI change becomes necessary**: split into a new protected
  automation task with rollback guidance.
- **Runtime or secret-adjacent evidence is requested**: record metadata only
  and request explicit scoped approval before touching the surface.

## Verification

Design and implementation waves use these checks as applicable:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash -n scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-repo-contracts.sh
```

If a wave changes generated navigation, run the generator without `--check`
first, commit the generated update in the same logical unit, then run the
freshness check.

Graphify refresh is required after code changes when the CLI is available. For
documentation-only waves, record whether Graphify was refreshed or skipped by
policy.

## Success Criteria & Verification Plan

- **VAL-SDCN-001**: The design lives under the canonical Stage 03 path and does
  not create active artifacts under non-stage docs paths.
- **VAL-SDCN-002**: The design distinguishes completed numbered path migration
  from the remaining stale-guidance and validator-coverage work.
- **VAL-SDCN-003**: Implementation waves preserve Stage 00 and Stage 99 policy
  ownership and keep README files as routing/index surfaces.
- **VAL-SDCN-004**: Validator changes preserve historical evidence exceptions
  while catching active stale guidance.
- **VAL-SDCN-005**: Stage 03 sibling README and Stage 04 plan/task pairing rules
  are decided before any hard enforcement.
- **VAL-SDCN-006**: Operations naming work preserves guide, policy, and
  runbook role separation.
- **VAL-SDCN-007**: Closure evidence updates progress memory, generated indexes,
  and any residual gap register without touching secrets, raw logs, or runtime
  state.

## Related Documents

- [Spec README](./README.md)
- [Stage 03 README](../README.md)
- [Numbered SDLC path migration spec](../099-template-system-numbered-sdlc-paths/spec.md)
- [Template contract standardization spec](../100-template-system-contract-standardization/spec.md)
- [Document restructure disposition spec](../103-document-restructure-audit-contract-archive/spec.md)
- [Workspace support surface contract spec](../106-workspace-support-surface-contract/spec.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Template governance](../../99.templates/support/template-governance.md)
- [Template selection](../../99.templates/support/template-selection.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [Lifecycle status](../../99.templates/support/lifecycle-status.md)
- [Document restructure gap register](../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md)
