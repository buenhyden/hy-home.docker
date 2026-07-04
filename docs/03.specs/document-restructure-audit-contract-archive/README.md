---
status: active
---

<!-- Target: docs/03.specs/document-restructure-audit-contract-archive/README.md -->

# Document Restructure Audit, Contract, and Archive

> Stage 03 design entrypoint for the second document-system restructure wave.

## Overview

This folder contains the approved design for the second document-system
restructure wave. The work starts with an evidence-only audit pack, strengthens
template and frontmatter contracts, then hands off archive-centered
restructuring for historical `docs/03.specs` work products and historical
`docs/05.operations/{guides,policies,runbooks}` stage buckets.

The design is intentionally separate from the earlier workspace document
contract audit pack. The earlier pack closed template/frontmatter/profile drift
that was already identified. This design defines the next program: classify
remaining historical work products, archive completed history by default, remove
conflicting or duplicate active documents when a canonical replacement exists,
and keep implementation batches reviewable.

It remains active as a reusable restructure/disposition contract, not as an open
implementation task. Completed Stage 04 plan/task evidence records the
2026-07-04 restructure wave; future archive, removal, validator, workflow, or
runtime-adjacent batches must either reuse this model with exact candidate rows
or supersede it explicitly.

## Audience

This README is for:

- Documentation Specialists
- Agentic Workflow Specialists
- QA Engineers
- Repository Maintainers

## Scope

### In Scope

- Design for the new Stage 90 document-restructure audit pack.
- Design for Stage 99 template/support contract reinforcement.
- Design for archive-centered restructuring of historical `docs/03.specs`
  work products.
- Design for `docs/05.operations/{guides,policies,runbooks}` `01-*` bucket
  consolidation and historical archive/removal decisions.
- Implementation handoff batches and validation gates.

### Out of Scope

- Moving, deleting, or rewriting target documents during the design commit.
- Mutating `.github` workflows, CI required checks, remote GitHub settings, or
  runtime provider configuration.
- Inspecting or storing secret values, credentials, tokens, private keys, raw
  logs, shell history, or `.env` values.
- Replacing the Stage 00 governance hub with Stage 99 template support rules.

## Structure

```text
document-restructure-audit-contract-archive/
├── README.md  # This file
└── spec.md    # Approved design and implementation handoff contract
```

## How to Work in This Area

1. Read [spec.md](./spec.md) for the approved design.
2. Use the implementation handoff batches in the spec to create a Stage 04 plan
   before mutating target-stage documents.
3. Keep audit evidence, template/support contract changes, archive moves,
   operations bucket restructuring, validator changes, and closure evidence in
   separate logical commits.
4. Preserve historical evidence unless the implementation plan classifies a
   document as duplicate or conflicting active guidance with a canonical
   replacement.

## Related Documents

- **Spec**: [spec.md](./spec.md)
- **Previous document contract audit pack**: [../workspace-document-contract-audit-pack/spec.md](../workspace-document-contract-audit-pack/spec.md)
- **Template contract**: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Template governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Stage authoring matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
