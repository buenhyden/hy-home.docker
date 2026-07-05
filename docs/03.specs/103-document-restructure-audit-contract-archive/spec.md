---
status: active
---

<!-- Target: docs/03.specs/103-document-restructure-audit-contract-archive/spec.md -->

# Document Restructure Audit, Contract, and Archive Technical Specification

## Overview

This specification defines the second document-system restructure wave for
`hy-home.docker`. The wave combines an evidence-first audit pack with a
template-contract baseline, then prepares archive-centered restructuring for
historical `docs/03.specs` work products and operations buckets under
`docs/05.operations/{guides,policies,runbooks}`.

The work is intentionally staged. The design commit creates no target document
moves, deletions, validator changes, GitHub workflow changes, or runtime
configuration changes. Those changes require a Stage 04 implementation plan,
task evidence, and logical commits.

## Status Boundary

This spec intentionally remains `status: active` as the current
document-restructure disposition contract. The paired Stage 04 plan and task are
completed execution evidence for the 2026-07-04 restructure wave; that closure
does not retire this spec because future exact-candidate batches still use its
archive/removal model, protected-surface boundaries, and `DRA-GAP-*` routing
rules.

Move this spec to `status: completed` only when a newer active restructure spec
supersedes it, all active gap-register references are retargeted, or a future
task explicitly retires this restructure model with replacement evidence.

## Strategic Boundaries & Non-goals

### Goals

- Produce a new Stage 90 audit pack that classifies document structure,
  template/frontmatter drift, CI/QA/formatting contract coverage, and historical
  active-stage work products.
- Strengthen Stage 99 support contracts so template selection, frontmatter,
  archive decisions, and destructive restructure rules are owned by support
  documents rather than README catalog text.
- Define archive-centered treatment for completed historical `docs/03.specs`
  work products.
- Define archive-centered treatment for operations bucket documents under
  `docs/05.operations/{guides,policies,runbooks}` across `00-workspace`,
  `01-*` through `12-*`, and the legacy `90-knowledge` bucket.
- Remove or archive conflicting and duplicate active documents only when a
  canonical replacement, tombstone, or gap record preserves traceability.

### Non-goals

- No broad Markdown corpus rewrite in the design commit.
- No immediate CI hard gate or remote GitHub branch protection mutation.
- No secret-value inspection.
- No replacement of Stage 00 governance with Stage 99 support documents.
- No `docs/superpowers` output path because this repository only allows active
  stage artifacts under the canonical docs taxonomy.

## Related Inputs

- **PRD**: Not required for this governance/documentation restructure design;
  the user request is the approval source for this Stage 03 design.
- **ARD**: Not required; existing Stage 00 governance and Stage 99 support
  contracts are the architecture boundary.
- **Related ADRs**:
  - [Stage 00 canonical adapter model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Prior audit pack**:
  - [Workspace document contract audit pack](../102-workspace-document-contract-audit-pack/spec.md)
- **Template support**:
  - [Template contract](../../99.templates/support/template-contract.md)
  - [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
  - [Template governance](../../99.templates/support/template-governance.md)
  - [Template selection](../../99.templates/support/template-selection.md)
  - [Lifecycle status](../../99.templates/support/lifecycle-status.md)

## Contracts

- **Config Contract**: No runtime config is changed by this design. Future
  implementation may update validators or CI only through approved Stage 04 task
  evidence with rollback and redaction boundaries.
- **Data / Interface Contract**: Audit reports must classify target documents
  using stable dispositions: `active-canonical`, `historical-archive`,
  `duplicate-remove`, `conflict-remove-or-archive`, and `evidence-preserve`.
- **Governance Contract**: README files remain routing and index surfaces.
  Durable template, archive, frontmatter, and destructive-change rules live in
  `docs/99.templates/support`. Stage 00 governance changes are limited to
  agent-facing behavior or stage-authoring policy changes.

## Core Design

### Component Boundary

The restructure program has four design components:

1. **Audit pack** under `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/`.
   This is evidence-only and does not mutate target documents.
2. **Template contract baseline** under `docs/99.templates/support/`, with
   minimal Stage 00 updates only when agent-facing policy changes.
3. **Archive/removal decision model** for `docs/03.specs` historical work
   products and operations stage buckets.
4. **Stage 04 implementation handoff** with batch boundaries, validation, and
   commit guidance.

### Key Dependencies

- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/99.templates/support/*.md`
- `scripts/validation/check-repo-contracts.sh`
- `scripts/validation/check-doc-traceability.sh`
- `scripts/validation/check-doc-implementation-alignment.sh`
- `scripts/knowledge/generate-llm-wiki-index.sh`

### Tech Stack

- Markdown and repository-local shell validators.
- Stage 90 audit references for durable evidence.
- Stage 99 support contracts for reusable rules.
- Stage 04 plans/tasks for implementation execution evidence.

## Disposition Model

| Disposition | Meaning | Default Action |
| --- | --- | --- |
| `active-canonical` | Current implementation, operations, or governance source of truth. | Keep active; normalize template/frontmatter/sections when approved. |
| `historical-archive` | Completed historical work product not needed in the active chain. | Move to `docs/98.archive/<original-stage>/...` with tombstone/provenance. |
| `duplicate-remove` | Same role is already covered by a canonical document. | Remove from active chain after README/link synchronization and traceability evidence. |
| `conflict-remove-or-archive` | Document contradicts current implementation or contract. | Archive with replacement pointer or record a gap if no replacement exists. |
| `evidence-preserve` | Audit, task, baseline, or migration evidence whose historical wording matters. | Preserve body; optionally add context through a new evidence/reference document. |

Completed historical work products default to `historical-archive`. A document
can stay active only if it is current operational/spec guidance or a canonical
contract. Conflicting or duplicate documents must not remain as active guidance.

## Audit Pack Design

The audit pack will live under
`docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/` and contain:

| Report | Purpose |
| --- | --- |
| `README.md` | Scope, reading order, and audit-pack role. |
| `template-contract-drift.md` | Conflicts among templates, support contracts, governance, README catalog text, and legacy sections. |
| `frontmatter-profile-inventory.md` | Current frontmatter keys and values by document type, including legacy or duplicate-purpose keys. |
| `sdlc-spec-archive-candidates.md` | `docs/03.specs` active, archive, duplicate, conflict, and evidence-preserve candidates. |
| `operations-bucket-restructure.md` | `docs/05.operations/{guides,policies,runbooks}` bucket-level archive/consolidation candidates across `00-workspace`, `01-*` through `12-*`, and `90-knowledge`. |
| `ci-qa-formatting-contract.md` | Current CI/CD, QA, and formatting coverage plus manual-review and future-hardening candidates. |
| `restructure-gap-register.md` | Stable gap IDs, batch assignments, approvals, validation commands, and residual risks. |

Audit rows must include evidence paths, command evidence when useful, a
disposition, and a recommended implementation batch. Secret values, raw logs,
credentials, tokens, private keys, shell history, and `.env` values are never
recorded.

## Template Contract Baseline

The implementation plan should review and, if needed, update these support
documents:

- `template-contract.md`: one primary template role per target document, with
  explicit boundaries for SDLC, operations, reference/audit, and archive
  tombstone documents.
- `frontmatter-contract.md`: lifecycle `status`, governance `layer`, archive
  provenance, generated metadata, and disallowed duplicate-purpose keys.
- `template-selection.md`: routing table for `03.specs` historical work
  products and `05.operations` bucket documents.
- `template-governance.md`: destructive move/delete conditions, rollback
  expectations, approval evidence, and logical commit boundaries.
- `lifecycle-status.md`: transitions among `draft`, `active`, `completed`, and
  `archived` in an archive-centered restructure.

Stage 00 governance receives only minimal updates when agent-facing rules,
stage authoring policy, or validation expectations change.

## Operations Bucket Restructure Model

The operations target includes the full purpose and service-bucket taxonomy:

- `docs/05.operations/guides/{00-workspace,01-*...12-*,90-knowledge}`
- `docs/05.operations/policies/{00-workspace,01-*...12-*,90-knowledge}`
- `docs/05.operations/runbooks/{00-workspace,01-*...12-*,90-knowledge}`

The model keeps active canonical guide/policy/runbook documents that map to
current operations and tracked implementation. Completed historical bucket
artifacts default to archive. Duplicate or conflicting documents are removed
from active routing after canonical replacement and traceability evidence are
recorded.

`90-knowledge` is a legacy operations purpose bucket, not a service tier. LLM
Wiki maintenance operations belong under `00-workspace` because they govern the
repository-wide reference index and agent navigation workflow. The reference
facts remain under `docs/90.references/llm-wiki/`; only operational guide,
policy, and runbook procedures move into `00-workspace`.

The approved `PLN-DRA-005` implementation closes this legacy-bucket case by
moving the LLM Wiki maintenance guide, policy, and runbook into `00-workspace`
and removing the empty tracked `90-knowledge` bucket indexes. Service buckets
from `01-gateway` through `12-infra-net` remain active in place until a future
exact candidate row proves a duplicate or conflict.

The model does not merge guide, policy, and runbook roles into one document.
Those roles remain separate because the Stage Authoring Matrix and operations
templates give them different purposes.

## 03.specs Restructure Model

Historical specs under `docs/03.specs` default to archive when they describe
completed work and no longer serve as the active implementation contract.
Current domain specs, active design specs, and evidence-required audit specs can
remain active when they serve current implementation or approved future work.

Archive candidates must preserve original path, archive reason, replacement or
canonical pointer, and validation evidence. If a completed spec is still linked
as active current guidance, the implementation batch must update parent README
and related links before moving it.

## CI/CD, QA, and Formatting Contract

The audit pack should separate:

- **Current hard gates**: validators or CI jobs already enforced locally or
  remotely.
- **Repo-local soft gates**: scripts that provide evidence but are not blocking
  remote checks.
- **Manual review gates**: policies that cannot safely become scripts yet.
- **Future hardening candidates**: stable checks that may become CI or local
  validators after separate approval.

No new CI hard gate is introduced by this design. Future hard gates must be
backed by audit evidence, rollback guidance, and owner approval.

The approved `PLN-DRA-006` decision keeps the current CI quality workflow,
local QA runner, repository contracts, formatting hygiene, and LLM Wiki
freshness checks as the active validation set for this restructure wave.
Networked dependency-audit hard gates and Graphify blocking gates remain future
Security/QA candidates because they require protected workflow or validator
changes, thresholds, exception handling, and rollback design.

## External Source Basis

The restructure uses external sources as supporting rationale, not as direct
policy owners:

- [Diátaxis](https://diataxis.fr/) supports separating tutorials/how-to guides,
  references, and explanation by user need.
- [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) supports
  integrating secure development practices into SDLC rather than treating them
  as afterthoughts.
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
  supports treating workflow changes as protected automation surfaces.
- [CommonMark](https://spec.commonmark.org/) supports preserving Markdown
  syntax boundaries and treating frontmatter as a repository convention.
- [The Good Docs Project templates](https://www.thegooddocsproject.dev/template)
  support reusable template patterns while keeping target documents
  context-specific.
- [DORA metrics](https://dora.dev/guides/dora-metrics/) support distinguishing
  delivery-performance measurement from documentation structure.
- [OpenSSF Scorecard](https://scorecard.dev/) supports classifying security
  automation as evidence-backed hardening candidates.
- [Google Testing Blog on end-to-end tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
  supports keeping QA gates layered instead of relying only on broad end-to-end
  checks.

## Edge Cases & Error Handling

- **Historical evidence mistaken for active drift**: preserve the evidence body
  and record context in the new audit pack instead of rewriting history.
- **Archive candidate still linked from active README**: update links before the
  move or classify as a gap.
- **Conflicting document with no canonical replacement**: do not delete it
  silently; create a gap row with owner and remediation batch.
- **Generated output**: preserve generator-owned files unless the generator is
  changed in an approved batch.
- **Secret-adjacent documentation**: record metadata and redaction boundaries
  only.

## Failure Modes & Fallback / Human Escalation

- **Audit scope too large for one implementation pass**: split by stage or
  bucket and keep stable gap IDs.
- **Validator false positives**: keep the rule manual-review-only until a stable
  repo-local command proves it.
- **Destructive move/delete ambiguity**: stop and request approval before
  removing active documents.
- **Remote GitHub or CI setting uncertainty**: record read-only evidence and
  require separate remote-setting approval before mutation.

## Implementation Handoff

The implementation plan should use these batches:

| Batch | Scope | Commit Boundary |
| --- | --- | --- |
| Audit pack | Create `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/` evidence reports and gap register. | `docs(audits): Add document restructure audit pack` |
| Template contract | Update Stage 99 support contracts and minimal Stage 00 governance if needed. | `docs(templates): Define archive-centered restructure contracts` |
| `03.specs` archive | Move/archive/remove approved historical spec work products and sync links. | `docs(specs): Archive historical spec work products` |
| Operations buckets | Restructure historical `guides`, `policies`, and `runbooks` buckets across `00-workspace`, `01-*` through `12-*`, and legacy `90-knowledge`. | `docs(ops): Restructure historical operations buckets` |
| Validator/CI/QA | Add only stable repo-local validator rules; record CI hard gates as approved future work if risky. | `test(docs): Enforce restructure documentation contracts` |
| Closure | Update task evidence, gap register, progress, and LLM Wiki index. | `docs(tasks): Close document restructure remediation` |

Each batch needs Stage 04 task evidence with approved surfaces, before/after
evidence, rollback path, redaction boundary, and validation results.

## Verification

The design commit and future implementation batches use these checks as
applicable:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash -n scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-repo-contracts.sh
```

Implementation batches that touch Compose or infra docs must also run the
relevant Compose and hardening checks defined by the affected task evidence.

## Success Criteria & Verification Plan

- **VAL-DRA-001**: The design is stored under canonical Stage 03 paths and does
  not create non-taxonomy `docs/superpowers` artifacts.
- **VAL-DRA-002**: The design identifies audit, contract, archive, operations,
  validator, and closure batches with separate commit boundaries.
- **VAL-DRA-003**: The classification model covers active canonical,
  historical archive, duplicate remove, conflict remove/archive, and evidence
  preserve dispositions.
- **VAL-DRA-004**: The design names external rationale sources without making
  them repository policy owners.
- **VAL-DRA-005**: Repository validation passes after adding the design and
  updating indexes.

## Related Documents

- **README**: [README.md](./README.md)
- **Previous document contract audit pack**: [../102-workspace-document-contract-audit-pack/spec.md](../102-workspace-document-contract-audit-pack/spec.md)
- **Template contract**: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Template governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Template selection**: [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Lifecycle status**: [../../99.templates/support/lifecycle-status.md](../../99.templates/support/lifecycle-status.md)
- **Stage authoring matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
