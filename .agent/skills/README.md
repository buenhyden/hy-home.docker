# Agent Skills

This directory contains specialized skill packages used by AI agents.

## Expected Structure

```text
.agent/skills/
  <skill-name>/
    SKILL.md
    scripts/
    examples/
```

## Rules

- Each skill must define one focused capability.
- `SKILL.md` must include frontmatter with `name` and `description`.
- Keep execution logic in scripts where possible.
