---
layer: agentic
---

# Common Templates

> reusable README, reference, audit, and archive tombstone templates

## Overview

`docs/99.templates/templates/common` contains copyable templates that are shared
across stages. Use these templates when the target document is a routing README,
a stable reference, a bounded audit, or an archive tombstone rather than an SDLC, contract,
operations, or governance record.

## Templates

| Need | Template |
| --- | --- |
| Create a repository, stage, folder, service, contract, or purpose-folder README | [readme.template.md](./readme.template.md) |
| Record stable facts, source rules, and maintenance expectations | [reference.template.md](./reference.template.md) |
| Record bounded criteria, evidence, findings, and disposition | [audit.template.md](./audit.template.md) |
| Replace a removed or superseded document with a minimal archive tombstone | [archive.template.md](./archive.template.md) |

## Target Rules

- `readme.template.md` targets repository, stage, folder, service, contract, and
  purpose-folder `README.md` files.
- `reference.template.md` targets
  `docs/90.references/{data,learning,llm-wiki,research}/**/*.md`.
- `audit.template.md` targets `docs/90.references/audits/**/*.md` except the
  generated metadata inventory.
- `archive.template.md` targets
  `docs/98.archive/<original-stage>/<original-path>.md`.
- Calculate target-relative links from the copied document path.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [frontmatter contract](../../support/frontmatter-contract.md)
