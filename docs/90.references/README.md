---
title: References
version: 1.0.0
type: common/readme
layer: references
status: active
owner: "@buenhyden"
---

# References

## Overview

`docs/90.references/` stores supplementary evidence in exactly three package categories. It helps active lifecycle stages evaluate facts but never overrides Stage 00 policy, Stage 01 requirements, Stage 02 architecture, Stage 03 specifications, or Stage 05 operations.

## Scope

- `research/`: external evidence and source-backed analysis (`RES-####`).
- `audits/`: point-in-time gap and conformance assessment (`AUD-####`).
- `data/`: repository inventories and structured reference data (`DATA-####`).

## Structure

```text
docs/90.references/
├── README.md
├── research/####-<slug>/
├── audits/####-<slug>/
└── data/####-<slug>/
```

Package paths are numeric, prefixless, and date-free. Stable IDs remain in frontmatter. Observation dates remain in `observed_at`; generated Data packages retain `generated_by` provenance.

### Authority Boundary

Stage 90 is non-normative. When evidence conflicts with a current owner, follow the current Stage 00/01/02/03/05 document and update or supersede the reference package. Executable OpenAPI, GraphQL, or Proto contracts remain with their Stage 03 Spec Package.

Deprecated redirects, compatibility copies, `learning/`, and `llm-wiki/` are not current categories. Learning material is classified by meaning as a Stage 05 Guide or Research package; LLM navigation outputs are registered Data packages.

### Lifecycle and Naming

- Use the Stage 99 `research`, `audit`, or `data` profile and its template.
- Do not reuse an issued ID.
- Use `status`, `supersedes`, and `superseded_by` for lifecycle history.
- Store dates in frontmatter, never in package names.
- Preserve citations and identify external observation dates and limitations.

### Current Categories

- [Research packages](./research/README.md)
- [Audit packages](./audits/README.md)
- [Data packages](./data/README.md)

## How to Work in This Area

1. Choose the evidence category by purpose, not by file format.
2. Copy the mapped Stage 99 template and issue the next registered stable ID.
3. Link the active owner in Traceability and keep normative instructions there.
4. Run the metadata, link, reference-package, and generator freshness checks.

## Related Documents

- [Documentation protocol](../00.agent-governance/policies/documentation-protocol.md)
- [Stage authoring matrix](../00.agent-governance/policies/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)
- [Research template](../99.templates/templates/references/research-pack.template.md)
- [Audit template](../99.templates/templates/references/audit-pack.template.md)
- [Data template](../99.templates/templates/references/data-pack.template.md)
