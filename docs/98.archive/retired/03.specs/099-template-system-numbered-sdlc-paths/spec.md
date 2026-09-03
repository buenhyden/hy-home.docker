---
status: completed
---

<!-- Target: docs/03.specs/099-template-system-numbered-sdlc-paths/spec.md -->

# Template System Numbered SDLC Paths Technical Specification

## Overview

This document defines the design contract for migrating PRD and Spec target
paths to deterministic three-digit numbered names. The migration updates the
entire corpus under `docs/01.requirements/` and `docs/03.specs/`, then aligns
Stage 99 templates, support contracts, Stage 00 governance, validators, README
indexes, and cross-links with the new target rules.

The design is intentionally path-first. Existing document content remains the
source of truth for domain facts and historical evidence; the implementation
changes names, links, and contracts unless validator fallout proves that a small
body correction is required.

## Strategic Boundaries & Non-goals

In scope:

- Rename every PRD Markdown file under `docs/01.requirements/` from
  date-prefixed filenames to the `NNN-feature-or-system.md` form.
- Rename every Spec folder under `docs/03.specs/` to the
  `NNN-feature-id/` form.
- Resolve the existing duplicate `04-*` domain numbering by assigning unique
  three-digit IDs.
- Update Stage 99 copyable templates and support contracts so PRD and Spec
  target examples use the new path rules.
- Update Stage 00 governance and validator references that still describe
  date-prefixed PRD filenames or unnumbered Spec folders.
- Rewrite repository-local cross-links and generated LLM Wiki index entries
  after the moves.

Out of scope:

- Changing runtime infrastructure, Compose services, secrets, credentials,
  remote GitHub state, or deployment behavior.
- Rewriting all PRD or Spec body sections into the newest template shape.
- Keeping alias documents at legacy paths.
- Moving Plan or Task filenames away from their existing date-prefixed
  execution-evidence contract in this wave.

## Related Inputs

- **Template system contract standardization**:
  [../100-template-system-contract-standardization/spec.md](../100-template-system-contract-standardization/spec.md)
- **Template system reorganization**:
  [../101-template-system-reorganization/spec.md](../101-template-system-reorganization/spec.md)
- **Template selection**:
  [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Template contract**:
  [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**:
  [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Documentation protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Repository contract validator**:
  [../../../scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
- **Google developer documentation filename guidance**:
  [https://developers.google.com/style/filenames](https://developers.google.com/style/filenames)
- **Google developer documentation date guidance**:
  [https://developers.google.com/style/dates-times](https://developers.google.com/style/dates-times)
- **Diataxis**: [https://diataxis.fr/](https://diataxis.fr/)
- **NIST SSDF**: [https://csrc.nist.gov/pubs/sp/800/218/final](https://csrc.nist.gov/pubs/sp/800/218/final)
- **IEEE 1012-2024**:
  [https://standards.ieee.org/ieee/1012/7324/](https://standards.ieee.org/ieee/1012/7324/)

## Contracts

### Path Contract

| Surface | Required Target Rule |
| --- | --- |
| PRD | `docs/01.requirements/NNN-feature-or-system.md` |
| Spec root | `docs/03.specs/NNN-feature-id/spec.md` |
| Spec child docs | `docs/03.specs/NNN-feature-id/child.md` |
| Spec machine contracts | `docs/03.specs/NNN-feature-id/contracts/contract-file` |
| Plan | Existing date-prefixed `docs/04.execution/plans/` rule remains unchanged. |
| Task | Existing date-prefixed `docs/04.execution/tasks/` rule remains unchanged. |

The `NNN` prefix is a zero-padded three-digit decimal ID. The prefix is part
of the canonical path, not frontmatter metadata.

### Numbering Contract

| Range | Owner | Rule |
| --- | --- | --- |
| `001`-`049` | Product and domain capabilities | Stable domain, service, and capability specs. |
| `050`-`089` | Reserved expansion | Future product or architecture domains. |
| `090`-`199` | Documentation, governance, audit, and migration workstreams | Historical and active documentation-system specs. |

The implementation may not reuse a number for two canonical siblings in the
same stage. When an old corpus has duplicate semantic numbers, the migration
must assign unique three-digit IDs and update all cross-links.

### Legacy Removal Contract

- Legacy date-prefixed PRD path comments are removed from templates, support
  contracts, governance rules, and active README indexes.
- Legacy unnumbered Spec path comments are removed from templates, support
  contracts, governance rules, and active README indexes.
- Historical dates are preserved only as document content, provenance, task
  evidence, or archive context; they are not PRD filenames after migration.
- No redirect or duplicate alias file is created at a legacy path.

## Core Design

### PRD Migration Map

| Current Path | Target Path |
| --- | --- |
| `docs/01.requirements/2026-03-26-01-gateway.md` | `docs/01.requirements/001-gateway.md` |
| `docs/01.requirements/2026-03-26-02-auth.md` | `docs/01.requirements/002-auth.md` |
| `docs/01.requirements/2026-03-26-03-security.md` | `docs/01.requirements/003-security.md` |
| `docs/01.requirements/2026-03-26-04-data.md` | `docs/01.requirements/004-data.md` |
| `docs/01.requirements/2026-03-26-04-data-analytics.md` | `docs/01.requirements/005-data-analytics.md` |
| `docs/01.requirements/2026-03-26-05-messaging.md` | `docs/01.requirements/006-messaging.md` |
| `docs/01.requirements/2026-03-26-06-observability.md` | `docs/01.requirements/007-observability.md` |
| `docs/01.requirements/2026-03-26-07-workflow.md` | `docs/01.requirements/008-workflow.md` |
| `docs/01.requirements/2026-03-26-08-ai.md` | `docs/01.requirements/009-ai.md` |
| `docs/01.requirements/2026-03-26-09-tooling.md` | `docs/01.requirements/010-tooling.md` |
| `docs/01.requirements/2026-03-26-10-communication.md` | `docs/01.requirements/011-communication.md` |
| `docs/01.requirements/2026-03-26-11-laboratory.md` | `docs/01.requirements/012-laboratory.md` |
| `docs/01.requirements/2026-03-27-08-ai-open-webui.md` | `docs/01.requirements/013-ai-open-webui.md` |
| `docs/01.requirements/2026-03-28-02-auth-optimization-hardening.md` | `docs/01.requirements/014-auth-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-03-security-optimization-hardening.md` | `docs/01.requirements/015-security-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-04-data-optimization-hardening.md` | `docs/01.requirements/016-data-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-05-messaging-optimization-hardening.md` | `docs/01.requirements/017-messaging-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-06-observability-optimization-hardening.md` | `docs/01.requirements/018-observability-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-07-workflow-optimization-hardening.md` | `docs/01.requirements/019-workflow-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-08-ai-optimization-hardening.md` | `docs/01.requirements/020-ai-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-09-tooling-optimization-hardening.md` | `docs/01.requirements/021-tooling-optimization-hardening.md` |
| `docs/01.requirements/2026-03-28-11-laboratory-optimization-hardening.md` | `docs/01.requirements/022-laboratory-optimization-hardening.md` |
| `docs/01.requirements/2026-04-01-standardize-infra-net.md` | `docs/01.requirements/023-standardize-infra-net.md` |
| `docs/01.requirements/2026-06-01-agent-governance-standardization.md` | `docs/01.requirements/024-agent-governance-standardization.md` |

### Spec Migration Map

| Current Folder | Target Folder |
| --- | --- |
| `docs/03.specs/01-gateway/` | `docs/03.specs/001-gateway/` |
| `docs/03.specs/02-auth/` | `docs/03.specs/002-auth/` |
| `docs/03.specs/03-security/` | `docs/03.specs/003-security/` |
| `docs/03.specs/04-data/` | `docs/03.specs/004-data/` |
| `docs/03.specs/04-data-analytics/` | `docs/03.specs/005-data-analytics/` |
| `docs/03.specs/05-messaging/` | `docs/03.specs/006-messaging/` |
| `docs/03.specs/06-observability/` | `docs/03.specs/007-observability/` |
| `docs/03.specs/07-workflow/` | `docs/03.specs/008-workflow/` |
| `docs/03.specs/08-ai/` | `docs/03.specs/009-ai/` |
| `docs/03.specs/09-tooling/` | `docs/03.specs/010-tooling/` |
| `docs/03.specs/10-communication/` | `docs/03.specs/011-communication/` |
| `docs/03.specs/11-laboratory/` | `docs/03.specs/012-laboratory/` |
| `docs/03.specs/workspace-audit-2026-05/` | `docs/03.specs/090-workspace-audit-2026-05/` |
| `docs/03.specs/workspace-doc-consistency-2026-05/` | `docs/03.specs/091-workspace-doc-consistency-2026-05/` |
| `docs/03.specs/workspace-consistency-2026-05b/` | `docs/03.specs/092-workspace-consistency-2026-05b/` |
| `docs/03.specs/docs-taxonomy-agent-first-migration/` | `docs/03.specs/093-docs-taxonomy-agent-first-migration/` |
| `docs/03.specs/harness-agent-first-engineering/` | `docs/03.specs/094-harness-agent-first-engineering/` |
| `docs/03.specs/infra-secrets-docs-refresh/` | `docs/03.specs/095-infra-secrets-docs-refresh/` |
| `docs/03.specs/llm-wiki-agent-first-completion/` | `docs/03.specs/096-llm-wiki-agent-first-completion/` |
| `docs/03.specs/home-docker-revalidation-deferred-follow-up/` | `docs/03.specs/097-home-docker-revalidation-deferred-follow-up/` |
| `docs/03.specs/standardize-infra-net/` | `docs/03.specs/098-standardize-infra-net/` |
| `docs/03.specs/099-template-system-numbered-sdlc-paths/` | `docs/03.specs/099-template-system-numbered-sdlc-paths/` |
| `docs/03.specs/template-system-contract-standardization/` | `docs/03.specs/100-template-system-contract-standardization/` |
| `docs/03.specs/template-system-reorganization/` | `docs/03.specs/101-template-system-reorganization/` |
| `docs/03.specs/workspace-document-contract-audit-pack/` | `docs/03.specs/102-workspace-document-contract-audit-pack/` |
| `docs/03.specs/document-restructure-audit-contract-archive/` | `docs/03.specs/103-document-restructure-audit-contract-archive/` |
| `docs/03.specs/agentic-research-pack-refresh/` | `docs/03.specs/104-agentic-research-pack-refresh/` |
| `docs/03.specs/agentic-engineering-implementation-audit-pack/` | `docs/03.specs/105-agentic-engineering-implementation-audit-pack/` |

### Contract Fallout Surfaces

The implementation must update these surfaces after path moves:

| Surface | Required Change |
| --- | --- |
| `docs/99.templates/templates/sdlc/prd.template.md` | Target comment, target examples, and downstream links use numbered PRD and Spec paths. |
| `docs/99.templates/templates/sdlc/spec.template.md` | Target comment, target examples, PRD links, and child contract examples use numbered Spec paths. |
| `docs/99.templates/templates/spec-contracts/*` | Child target examples use `docs/03.specs/NNN-feature-id/...`. |
| `docs/99.templates/support/template-selection.md` | Stage and child mappings use numbered PRD and Spec target locations. |
| `docs/99.templates/support/template-contract.md` | Placeholder and target-comment rules ban legacy PRD/Spec path patterns outside historical context. |
| `docs/99.templates/support/template-governance.md` | Protected-surface rules mention corpus-wide path migration evidence and no-alias cleanup. |
| `docs/99.templates/support/external-source-rationale.md` | External rationale includes filename, date, V&V, and secure SDLC references. |
| `docs/00.agent-governance/rules/*` | Stage routing references use numbered Spec paths and numbered PRD targets where explicit examples exist. |
| `scripts/validation/check-repo-contracts.sh` | Enforce numbered PRD filenames and numbered Spec folders; keep template-source exceptions scoped. |
| README indexes | Replace old path examples and related-document links with moved paths. |
| LLM Wiki index | Regenerate after path moves. |

## Data Modeling & Storage Strategy

The path prefix is the durable routing key. It is intentionally not duplicated
as a frontmatter key because path-derived document role and ordering should not
compete with metadata.

The implementation preserves lifecycle frontmatter such as `status: active`,
`status: completed`, or `status: superseded`. If a moved historical document
contains date provenance in its title or body, that provenance remains content.
If it only had provenance in the old filename, the implementation may add a
short history note only when traceability would otherwise be lost.

## Interfaces & Data Structures

### Validator Interfaces

The repository validator must reject:

- date-prefixed PRD targets under `docs/01.requirements/`.
- two-digit PRD targets under `docs/01.requirements/`.
- non-numbered target folders under `docs/03.specs/`, excluding
  `docs/03.specs/README.md`.
- two-digit target folders under `docs/03.specs/` after the migration.
- Legacy target comments in Stage 99 template files unless the comment is part
  of an explicitly named historical migration table.

The validator must allow:

- Stage 99 templates to mention numbered PRD placeholders.
- Stage 99 templates to mention numbered Spec placeholders.
- Stage 04 Plan and Task filenames to remain date-prefixed.

## API Contract (If Applicable)

This work does not expose an external API.

## Agent Role & IO Contract (If Applicable)

### Agent Role

Agents working on this implementation act as documentation-system maintainers.
They may edit Stage 01, Stage 03, Stage 99, directly affected Stage 00
governance, validators, README indexes, generated LLM Wiki index, and progress
memory. Runtime, secret, deployment, and remote GitHub changes stay out of
scope.

### Inputs

- Approved user request for full corpus path migration.
- Current PRD and Spec corpus inventory.
- Stage 99 templates and support contracts.
- Stage 00 documentation governance.
- Repository contract validators.
- External rationale sources listed in `## Related Inputs`.

### Outputs

- Renamed PRD files.
- Renamed Spec folders.
- Updated template, support, governance, validator, README, cross-link, and LLM
  Wiki surfaces.
- Stage 04 plan and task evidence for the implementation wave.
- Logical commits per batch.

### Success Definition

The work succeeds when all PRD and Spec paths follow the new numbered contract,
legacy path patterns no longer appear as active rules or links, validation
passes, and the implementation evidence records each path-migration batch.

## Tools & Tool Contract (If Applicable)

- Use `rg`, `find`, and `git status` for inventory.
- Use `git mv` for every path rename.
- Use `apply_patch` for manual document and validator edits.
- Use existing repository validators before adding new checks.
- Regenerate `docs/90.references/llm-wiki/llm-wiki-index.md` after path moves.
- Do not inspect, print, or store secret values.

## Prompt / Policy Contract (If Applicable)

Agent prompts and provider instructions must refer to canonical stage paths.
They may mention legacy paths only as historical migration evidence, never as
active target guidance.

## Memory & Context Strategy (If Applicable)

- Update `docs/00.agent-governance/memory/progress.md` after the design commit
  and after each implementation batch.
- Create a separate memory note only if the migration uncovers a reusable
  policy conflict or an intentionally deferred out-of-scope breakage.

## Guardrails (If Applicable)

- Do not leave duplicate alias files at old PRD or Spec paths.
- Do not delete historical content merely because its folder is being renamed.
- Do not rewrite template bodies into target docs except for direct fallout
  from changed path contracts.
- Stop before mutating runtime, secret, remote GitHub, or deployment surfaces.
- Treat broken links after path moves as implementation fallout that must be
  fixed before completion.

## Evaluation (If Applicable)

The implementation is evaluated through repository validation:

- path inventory checks for PRD and Spec target shapes
- stale legacy-pattern scans
- link and traceability checks
- template contract validation
- LLM Wiki freshness check

## Edge Cases & Error Handling

- If two target paths collide, preserve the earlier domain number and move the
  later document to the next free number in the same range; update this spec
  and the implementation plan before performing the conflicting move.
- If a legacy path appears in an archive tombstone or historical migration
  table, keep it only when the surrounding text clearly marks it as historical.
- If a path appears inside a code fence as an example command, update it unless
  it is intentionally demonstrating legacy migration.
- If generated artifacts change only because paths moved, record them as
  generated-index fallout rather than source-authored policy edits.

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback | Human Escalation |
| --- | --- | --- |
| Validator rejects a new numbered path rule | Patch the validator to match this spec and rerun checks. | Escalate if the validator conflict implies a different stage contract. |
| Link rewrite creates ambiguous targets | Prefer the canonical moved path from the migration table. | Escalate if two current documents claim the same canonical role. |
| Corpus move touches unexpected protected surface | Stop and record the protected surface in task evidence. | Ask before changing runtime, secrets, remote GitHub, or deployment state. |

## Verification

The Stage 04 implementation plan must include at least these checks:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Focused scans must also verify there are no active legacy PRD/Spec target
patterns outside explicit historical migration tables.

## Success Criteria & Verification Plan

- **VAL-NSP-001**: Every PRD file under `docs/01.requirements/` except
  `README.md` matches `^[0-9]{3}-[a-z0-9][a-z0-9-]*\.md$`.
- **VAL-NSP-002**: Every Spec folder under `docs/03.specs/` matches
  `^[0-9]{3}-[a-z0-9][a-z0-9-]*$`.
- **VAL-NSP-003**: Stage 99 PRD and Spec templates declare numbered target
  comments and target-relative examples.
- **VAL-NSP-004**: Stage 99 support contracts and Stage 00 governance no longer
  publish date-prefixed PRD or unnumbered Spec target rules.
- **VAL-NSP-005**: Repository-local Markdown links resolve after the moves.
- **VAL-NSP-006**: Full repository contract validation passes or any unrelated
  failure is recorded as an out-of-scope gap with evidence.

## Implementation Handoff

The implementation should be split into these logical batches:

1. Stage 04 plan and task evidence for the numbered path migration.
2. PRD file moves and PRD README/link updates.
3. Spec folder moves and Spec README/link updates.
4. Stage 99 template/support and Stage 00 governance path-rule updates.
5. Validator and generated-index updates.
6. Final cross-link, stale-pattern, and validation closure.

## Related Documents

- **README**: [README.md](./README.md)
- **Template selection**: [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Template contract**: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Template governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Frontmatter contract**: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Stage authoring matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Repository validator**: [../../../scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
