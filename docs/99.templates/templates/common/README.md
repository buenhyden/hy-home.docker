---
layer: agentic
---

# Common Templates

> reusable README, reference, and archive tombstone templates

## Overview

`docs/99.templates/templates/common` contains copyable templates that are shared
across stages. Use these templates when the target document is a routing README,
a stable reference, or an archive tombstone rather than an SDLC, contract,
operations, or governance record.

## Use When

| Need | Template |
| --- | --- |
| Create a repository, stage, folder, service, contract, or purpose-folder README | [readme.template.md](./readme.template.md) |
| Record stable facts, source rules, and maintenance expectations | [reference.template.md](./reference.template.md) |
| Replace a removed or superseded document with a minimal archive tombstone | [archive.template.md](./archive.template.md) |

## Do Not Use For

- Active requirements, architecture, specs, plans, or tasks; use
  [SDLC templates](../sdlc/README.md).
- Feature child contracts; use
  [spec-contracts](../spec-contracts/README.md).
- Active operational procedures or controls; use
  [operations](../operations/README.md).

## Target Rules

- README files are routing and orientation surfaces; detailed policy and
  governance rules belong in the owning support or governance document.
- Reference documents must separate stable facts from active procedures.
- Archive tombstones preserve replacement and provenance pointers; do not keep
  stale body text in the tombstone.
- Do not copy README template metadata examples into final README files.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [frontmatter contract](../../support/frontmatter-contract.md)
