---
title: "<title>"
type: governance/hook-policy
layer: agentic
owner: "@buenhyden"
name: enforce-docs-templates
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (^|/)docs/(0[1-5]|90)\.
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Template use required (project rule)**

When creating or editing documents under `docs/01` through `docs/05` or
`docs/90`, follow the mapped template under `docs/99.templates/templates/`.

**AGENTS.md policy:**
> Use mapped templates from `docs/99.templates/templates/` for every new or modified target-stage document under `docs/01` to `docs/05`, and `docs/90`.

**Required actions:**

1. Read the mapped template under `docs/99.templates/templates/` before editing.
2. Preserve required heading structure.
3. Remove all temporary placeholders before saving.
4. Include a `## Related Documents` section in every Markdown document.

After completion, run `python3 scripts/validation/run-ci-gate.py --profile changed` to
verify that template contracts still hold.
