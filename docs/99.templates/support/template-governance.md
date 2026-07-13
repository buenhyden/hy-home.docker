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
- Use a fresh implementation review, then independent specification and
  quality review when the active Plan requires them. Do not self-assign an
  independent PASS or APPROVED verdict.
- Resolve Critical and Important findings before the logical task closes.
  Record Minor findings and their disposition in Stage 04 evidence.
- Preserve remote, runtime, secret, deployment, and provider boundaries unless
  the task explicitly approves them.

## Archive and Removal Governance

Archive-centered restructure work must classify a target before changing it.
Use these dispositions when a task proposes archive, removal, or preservation:

| Disposition | Meaning | Required Action Before Mutation |
| --- | --- | --- |
| `active-canonical` | Current source of truth for implementation, operations, governance, or reference context. | Keep active; normalize only within an approved target-document batch. |
| `historical-archive` | Completed work product that no longer needs to remain in the active chain. | Verify active links, record replacement or `N/A`, then create an archive tombstone if the active file is moved out of the active chain. |
| `duplicate-remove` | Same role is already covered by a canonical document. | Prove the canonical replacement, update active links, and record deletion evidence in the task and gap register. |
| `conflict-remove-or-archive` | Document contradicts current implementation or contract. | Prefer a replacement pointer plus tombstone; if no replacement exists, record a gap before removing active guidance. |
| `evidence-preserve` | Audit, task, baseline, migration, or historical evidence whose wording matters. | Preserve body semantics; add context in new evidence instead of rewriting history. |

Destructive target changes require all of the following before commit:

- exact target path list
- disposition row or task evidence for every target
- replacement or current-canonical pointer when one exists
- active link and README routing review
- rollback or recovery path
- LLM Wiki regeneration when tracked paths change
- validation results after the move, removal, or tombstone update

Archive tombstones use
[`archive.template.md`](../templates/common/archive.template.md). They are not
used to preserve stale original bodies; historical body preservation belongs in
task evidence or Stage 90 references when needed.

## Commit Boundaries

- Create at least one logical Conventional Commit for each approved task.
- Keep support-contract edits, template-source edits, validator edits, direct fallout edits, and generated-index refreshes in separate logical commits where the Plan requires independent rollback or review.
- Use `git mv` for path moves.
- Review path-only moves separately from content rewrites.
- Record existing unrelated validation failures as gaps.

## Preservation and Migration

- Migrate direct consumers only when the matched contract or link requires it;
  broad corpus waves require their own approved Spec and Plan.
- Preserve historical dates, commands, counts, verdicts, approvals, and
  outcomes. Never invent missing review or runtime evidence to satisfy a form.
- Use generators for generated outputs and record before/after freshness
  evidence. Do not hand-edit generated bodies.
- Treat destructive replacement as a linked change: remove stale routes,
  preserve the required evidence owner, create a tombstone when applicable,
  and keep rollback possible through the logical commit boundary.

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
- [task evidence](../../04.execution/tasks/2026-07-02-template-system-reorganization.md)
- [contract standardization task evidence](../../04.execution/tasks/2026-07-03-template-system-contract-standardization.md)
