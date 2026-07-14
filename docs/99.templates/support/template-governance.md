---
layer: agentic
---

# Template Governance

## Overview

This document defines the governance workflow for changing templates, support
contracts, and validation rules.

## Change Boundaries

| Surface | Governance Rule |
| --- | --- |
| Template artifacts | Change only under `docs/99.templates/templates/` and keep one canonical file per role. |
| Support rules | Change under `docs/99.templates/support/`; do not hide rules in catalog README files. |
| Validators | Update `scripts/validation/check-repo-contracts.sh` when template paths or contracts change. |
| Stage 00 governance | Update only when the template system changes agent-facing rules or bootstrap behavior. |
| Target documents | Update only direct fallout unless a separate plan approves broad corpus normalization. |
| Repo-support staging | Keep `_workspace` tracked surface limited to approved contract README files; runtime artifacts remain ignored under `_workspace/repo-support/`. |

## Approval and Review

- Record the approved scope, exact paths, validation commands, rollback or
  recovery, and redaction boundary before changing protected template,
  registry, validator, or governance surfaces.
- Use a fresh implementation review, then independent specification and quality review
  when the active Plan requires them. Do not self-assign an
  independent PASS or APPROVED verdict.
- Resolve Critical and Important findings before the logical task closes.
  Record Minor findings and their disposition in Stage 04 evidence.
- Preserve remote, runtime, secret, deployment, and provider boundaries unless
  the task explicitly approves them.

## Migration and Archive Approval Boundary

This document approves changes to template-system surfaces; it does not own
corpus classification, archive admission, retention thresholds, provenance
verification, or ledger derivation. Those semantics route to the
[corpus migration contract](./corpus-migration-contract.md) and
[archive and retention contract](./archive-retention-contract.md).

Before a migration or archive-related template-system change, the owning Stage
04 Task records the approved wave and exact paths, the affected support and
template owners, validation commands, rollback or recovery, redaction boundary,
and the required independent reviews. Mutation remains blocked while the
machine contract, human owner, copyable form, validator, or review evidence
disagrees.

## Commit Boundaries

- Create at least one logical Conventional Commit for each approved task.
- Keep support-contract edits, template-source edits, validator edits, direct fallout edits, and generated-index refreshes in separate logical commits where the Plan requires independent rollback or review.
- Use `git mv` for path moves.
- Review path-only moves separately from content rewrites.
- Record existing unrelated validation failures as gaps.

## Preservation and Generated Evidence Governance

- Broad corpus waves require their own approved Spec, Plan, and Task boundary.
- Preserve historical dates, commands, counts, verdicts, approvals, and
  outcomes. Never invent missing review or runtime evidence to satisfy a form.
- Use canonical generators for generated outputs, record before/after freshness
  evidence, and keep generated fallout in the logical boundary required by the
  active Plan. Do not hand-edit generated bodies.
- Keep rollback possible at the reviewed logical commit boundary.

## Numbered Path Governance

- PRD and Spec path-rule changes are protected template-system changes.
- A PRD path-rule change must update copyable templates, template selection,
  support contracts, Stage 00 governance, validators, active cross-links, and
  generated reference indexes as applicable.
- A Spec path-rule change must update parent Spec templates, spec-child
  templates, provider-facing examples, Stage 00 governance, validators, active
  cross-links, and generated reference indexes as applicable.
- Do not create alias documents at legacy PRD or Spec paths unless a later
  approved rollback task explicitly requires one.

## Protected Surface Rules

Template and validation changes are protected because they affect agent behavior
and repository contract checks. A task touching these surfaces must record:

- approval source
- target path
- before evidence
- after evidence
- rollback or recovery path
- redaction boundary

## Review Rules

- Confirm the registry remains the sole machine owner and that human contracts
  do not copy complete key, transition, path-glob, heading, or validator logic.
- Review SDLC/common role ownership and README profile routing in their separate
  support contracts before approving template-system changes.
- Run reference search after removing or moving template paths.
- Run LLM Wiki regeneration after adding or moving tracked docs.
- Run repository contract validation after validator or governance changes.
- Run provider sync checks when agent-facing surfaces change.
- Run focused `_workspace` reference checks after changing repo-support staging
  rules.
- Keep README documents as routing and index surfaces; detailed rules belong in
  support documents.

## Related Documents

- [support README](./README.md)
- [template contract](./template-contract.md)
- [template selection](./template-selection.md)
- [SDLC document contract](./sdlc-document-contract.md)
- [common document contract](./common-document-contract.md)
- [README profile contract](./readme-profile-contract.md)
- [corpus migration contract](./corpus-migration-contract.md)
- [archive and retention contract](./archive-retention-contract.md)
- [task evidence](../../04.execution/tasks/2026-07-02-template-system-reorganization.md)
- [contract standardization task evidence](../../04.execution/tasks/2026-07-03-template-system-contract-standardization.md)
