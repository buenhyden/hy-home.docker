---
name: block-absolute-file-link
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.md$
  - field: new_text
    operator: regex_match
    pattern: \]\(file://|href=["']file://
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

**Absolute `file://` link blocked (project rule)**

`docs/00.agent-governance/rules/documentation-protocol.md` — Documentation Standards:

> "Use only relative links; never use absolute `file://` links."

**Why this is forbidden:**

- `file://` links work only on one local machine.
- They break in CI, for other developers, and in GitHub rendering.
- They break SSoT traceability.

**Correct link format:**

```markdown
<!-- BLOCKED: absolute file URL -->
[document link](file:///home/hy/projects/hy-home.docker/docs/01.requirements/prd.md)

<!-- ALLOWED: relative link -->
[document link](../01.requirements/prd.md)
[document link](../../docs/01.requirements/prd.md)
```

Calculate relative paths from the current file location.

## Related Documents

- `docs/00.agent-governance/README.md`
