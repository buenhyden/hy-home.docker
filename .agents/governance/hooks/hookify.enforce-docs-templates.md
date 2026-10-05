---
title: "WARNING: template use required"
version: "1.0.1"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)docs/(0[1-5]|90)\\."
enabled: true
event: "file"
name: "enforce-docs-templates"
---

# WARNING: template use required

## Overview

Apply the declared `warn` action for enforce-docs-templates.

## Scope

The declared `file` event and structured `conditions` define the matching scope; native event delivery remains a separate observation.

## Rules

**Template use required (project rule)**

When creating or editing documents under `docs/01` through `docs/05` or
`docs/90`, follow the mapped template under `docs/99.templates/templates/`.

The canonical `.agents/governance/documentation-protocol.md` authoring rules
require selecting the Stage 99 profile and preserving its metadata, links, and
stage-specific contract. The Registry owns the mapped template for each profile.

**Required actions:**

1. Read the mapped template under `docs/99.templates/templates/` before editing.
2. Preserve required heading structure.
3. Remove all temporary placeholders before saving.
4. Include a `## Related Documents` section in every Markdown document.

After completion, run `python3 scripts/validation/run-ci-gate.py --profile changed` to
verify that template contracts still hold.

## Exceptions

No exception is declared by this rule.

## Related Documents

- [Documentation protocol](../documentation-protocol.md)
- [Stage authoring matrix](../stage-authoring-matrix.md)
