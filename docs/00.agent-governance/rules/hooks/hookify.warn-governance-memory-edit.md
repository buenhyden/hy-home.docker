---
name: warn-governance-memory-edit
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (^|/)docs/00\.agent-governance/memory/.*\.md$
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Governance memory edit detected**

Memory notes are advisory retrieval context, not active policy.

Before finishing:

- Use `docs/99.templates/memory.template.md` for durable notes.
- Do not store transcripts, raw logs, shell history, credentials, tokens, private keys, or secret values.
- Update `docs/00.agent-governance/memory/progress.md` when creating or materially changing a memory note.

## Related Documents

- `docs/00.agent-governance/README.md`
