---
title: "BLOCKED: absolute file:// link"
version: "1.0.3"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
action: "block"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "\\.md$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "\\]\\(file://|href=[\"']file://"
enabled: true
event: "file"
name: "block-absolute-file-link"
---

# BLOCKED: absolute file:// link

## Overview

Apply the declared `block` action for block-absolute-file-link.

## Scope

Applies to the `block-absolute-file-link` rule on the `file` event. The frontmatter of this document owns the exact matcher.

## Rules

**Absolute `file://` link blocked (project rule)**

The document link contract and this hook require portable repository links.
Use a relative path instead of a machine-specific `file://` URL.

**Why this is forbidden:**

- `file://` links work only on one local machine.
- They break in CI, for other developers, and in GitHub rendering.
- They break SSoT traceability.

**Correct link format:**

```markdown
<!-- BLOCKED: absolute file URL -->
[document link](file:///home/hy/projects/hy-home.docker/docs/01.requirements/0001-gateway.md)

<!-- ALLOWED from inside docs/: relative link -->
[document link](../01.requirements/0001-gateway.md)

<!-- ALLOWED from outside docs/: entry point plus the path as text -->
[Documentation index](../../../docs/README.md) - `docs/01.requirements/0001-gateway.md`
```

Calculate relative paths from the current file location.

The declared action applies when the pattern matches.

## Exceptions

No exception is declared by this rule.

## Verification

The declared `file` event and structured `conditions` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
