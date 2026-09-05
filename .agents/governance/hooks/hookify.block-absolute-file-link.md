---
title: "BLOCKED: absolute file:// link"
version: "1.0.1"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
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

<!-- markdownlint-disable MD041 MD040 -->

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

<!-- ALLOWED: relative link -->
[document link](../../../docs/01.requirements/0001-gateway.md)
[document link](../../../docs/01.requirements/0001-gateway.md)
```

Calculate relative paths from the current file location.

## Related Documents

- `.agents/README.md`
