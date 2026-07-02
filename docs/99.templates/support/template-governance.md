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

## Commit Boundaries

- Keep support-contract edits, template-source edits, validator edits, direct fallout edits, and generated-index refreshes in separate commits where practical.
- Use `git mv` for path moves.
- Review path-only moves separately from content rewrites.
- Record existing unrelated validation failures as gaps.

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

- Run reference search after removing or moving template paths.
- Run LLM Wiki regeneration after adding or moving tracked docs.
- Run repository contract validation after validator or governance changes.
- Run provider sync checks when agent-facing surfaces change.
- Keep README documents as routing and index surfaces; detailed rules belong in
  support documents.

## Related Documents

- [support README](./README.md)
- [template contract](./template-contract.md)
- [template selection](./template-selection.md)
- [task evidence](../../04.execution/tasks/2026-07-02-template-system-reorganization.md)
- [contract standardization task evidence](../../04.execution/tasks/2026-07-03-template-system-contract-standardization.md)
