---
layer: agentic
---

# Template Artifacts

> copyable template artifacts for stage documents and reusable contracts

## Overview

`docs/99.templates/templates` contains the files that may be copied to create a
new document or machine-readable contract. Files in this tree are template
artifacts; rules for using them live in [../support/](../support/README.md).

## Audience

이 README의 주요 독자:

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- Markdown document templates
- Machine-readable contract templates
- Category-level routing for copyable templates

### Out of Scope

- Template governance and lifecycle policy
- Frontmatter schema rationale
- Active stage document content

## Category Catalog

| Category | Path | Templates |
| --- | --- | --- |
| SDLC | [sdlc/](./sdlc/README.md) | `prd`, `ard`, `adr`, `spec`, `plan`, `task` |
| Spec contracts | [spec-contracts/](./spec-contracts/README.md) | `api-spec`, `agent-design`, `data-model`, `service`, `tests`, `openapi`, `schema`, `proto` |
| Operations | [operations/](./operations/README.md) | `guide`, `policy`, `runbook`, `incident`, `postmortem` |
| Governance | [governance/](./governance/README.md) | `memory`, `progress`, `harness-task-contract` |
| Common | [common/](./common/README.md) | `readme`, `reference`, `archive` |

## Structure

```text
templates/
├── README.md
├── common/
│   ├── README.md
│   └── *.template.md
├── governance/
│   ├── README.md
│   └── *.template.md
├── operations/
│   ├── README.md
│   └── *.template.md
├── sdlc/
│   ├── README.md
│   └── *.template.md
└── spec-contracts/
    ├── README.md
    ├── *.template.md
    ├── *.template.yaml
    ├── *.template.graphql
    └── *.template.proto
```

## How to Work in This Area

1. Use [template selection](../support/template-selection.md) to choose one source template.
2. Copy only files from this `templates/` tree.
3. Replace placeholders before saving the target document.
4. Calculate links from the copied target path, not from this template source path.
5. Keep template source metadata aligned with [frontmatter contract](../support/frontmatter-contract.md).

## Related Documents

- [template catalog](../README.md)
- [support README](../support/README.md)
- [template contract](../support/template-contract.md)
- [template selection](../support/template-selection.md)
