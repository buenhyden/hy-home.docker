---
layer: agentic
---

# Template Artifacts

> copyable template artifacts for stage documents and reusable contracts

## Overview

`docs/99.templates/templates` contains the files that may be copied to create a
new document or machine-readable contract. Files in this tree are template
artifacts; rules for using them live in [../support/](../support/README.md).

## Templates

| Category | Path | Templates |
| --- | --- | --- |
| SDLC | [sdlc/](./sdlc/README.md) | `prd`, `ard`, `adr`, `spec`, `plan`, `task` |
| Spec contracts | [spec-contracts/](./spec-contracts/README.md) | `api-spec`, `agent-design`, `data-model`, `service`, `tests`, `openapi`, `schema`, `proto` |
| Operations | [operations/](./operations/README.md) | `guide`, `policy`, `runbook`, `incident`, `postmortem` |
| Governance | [governance/](./governance/README.md) | `memory`, `progress`, `harness-task-contract` |
| Common | [common/](./common/README.md) | `readme`, `reference`, `archive` |

## Target Rules

- Use [template selection](../support/template-selection.md) to map a target
  path to one copyable template source.
- Markdown templates target stage documents and use target-relative related
  document links after copying.
- Machine-readable contract templates target child contract files and use
  in-file `Cross-links:` comments.
- Template source metadata follows
  [frontmatter contract](../support/frontmatter-contract.md); durable template
  rules live under [support](../support/README.md).

## Related Documents

- [template catalog](../README.md)
- [support README](../support/README.md)
- [template contract](../support/template-contract.md)
- [template selection](../support/template-selection.md)
