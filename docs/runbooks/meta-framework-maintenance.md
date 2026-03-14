---
title: 'Meta-Framework Maintenance Runbook'
layer: 'runbooks'
---

# Meta-Framework Maintenance Runbook

Procedures for maintaining the documentation hierarchy and the agentic instruction set.

## 1. Adding a New Agent Rule

### Step 1: Create rule file

- Location: `docs/agentic/rules/<domain>-rule.md`
- Template: Use `docs/agentic/rules/doc-maintenance-rule.md` as a baseline.

### Step 2: Register in Gateway

- Update `docs/agentic/gateway.md`.
- Add a new row to the **Intent-Based Discovery** table.
- Assign a unique `[LOAD:RULES:CATEGORY]` marker.

## 2. Documentation Audit

### Metadata check

Run the following to find files missing the `layer:` key:

```bash
grep -rL "layer:" docs/
```

### Link integrity

Ensure all relative links resolve. Use a crawler or manual `rg` check for common patterns like `\[.*\]\(.*\.md\)`.

## 3. Slimming the Root

- Periodically check `README.md` and `ARCHITECTURE.md`.
- If a section grows beyond 20 lines of procedural detail, move it to `docs/guides/`.
