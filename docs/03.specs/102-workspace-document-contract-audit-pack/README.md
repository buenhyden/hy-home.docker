---
status: active
---

<!-- Target: docs/03.specs/102-workspace-document-contract-audit-pack/README.md -->

# Workspace Document Contract Audit Pack

> Specification entrypoint for the repository-wide document contract audit pack.

## Overview

This folder contains the specification for auditing workspace documentation
contracts before broad normalization work begins. It defines how to classify
document profiles, compare frontmatter and sections against templates, map
CI/CD and QA automation coverage, and record gaps without rewriting historical
evidence.

It remains active as a reusable audit/disposition contract, not as an open
implementation task. Completed Stage 04 plan/task evidence records the
2026-07-03 execution; future document-contract batches should reuse or
supersede this model explicitly instead of treating its active status as broad
permission to rewrite the corpus.

## Audience

This README is for:

- Documentation Specialists
- Agentic Workflow Specialists
- QA Engineers
- Repository Maintainers

## Scope

### In Scope

- Routing for the workspace document contract audit pack spec.
- The contract-first design for future inventory and gap reports.
- Links to template, governance, and validation sources used by the spec.

### Out of Scope

- Implementation task evidence.
- Audit output reports.
- Runtime configuration changes.
- Secret values, credentials, tokens, certificates, or private keys.

## Structure

```text
workspace-document-contract-audit-pack/
├── spec.md    # Audit pack specification
└── README.md  # This file
```

## How to Work in This Area

1. Read [spec.md](./spec.md) before planning document-contract audit work.
2. Keep execution plans under `docs/04.execution/plans/`.
3. Keep task evidence under `docs/04.execution/tasks/`.
4. Keep durable audit outputs under `docs/90.references/audits/` unless a later
   plan defines a more specific canonical path.
5. Preserve the separation between active governance, target corpus
   normalization, historical evidence, and out-of-scope gaps.

## Related Documents

- [Spec](./spec.md)
- [Spec index](../README.md)
- [Template contract](../../99.templates/support/template-contract.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
