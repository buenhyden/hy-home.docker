---
layer: ops
---

# Documentation Maintenance Runbook

This runbook describes the procedure for maintaining, updating, and verifying the integrity of the repository's documentation system.

## 1. Adding a New Document

1. **Identify the Role**: Determine if the document is a Decision (ADR), Requirement (ARD/PRD), Spec, Plan, or Runbook.
2. **Select the Template**: Go to `templates/` and copy the relevant template.
3. **Place in Taxonomy**: Save the file in the matching `docs/<category>/` folder.
4. **Metadata**: Ensure the `layer` frontmatter is present.
5. **Cross-Reference**: Link the new document in the relevant category's `README.md`.

## 2. Integrity Verification

Pre-flight checklist for documentation changes:

```bash
# Check for missing layer metadata
grep -r "layer:" docs/

# Check for absolute filesystem links (Anti-pattern)
grep -r "file://" docs/

# Validate relative links
# (Use md-link-checker or manual inspection)
```

## 3. Link Maintenance

If a folder is moved or renamed:

1. Update `docs/agentic/gateway.md` immediately.
2. Update `docs/agentic/core-governance.md` lazy-loading paths.
3. Run a global search for links to the old path.
