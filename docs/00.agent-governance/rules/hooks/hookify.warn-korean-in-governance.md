---
name: warn-korean-in-governance
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: docs/00\.agent-governance/.*\.md$
  - field: new_text
    operator: regex_match
    pattern: '[\uac00-\ud7a3\u3131-\u318e]'
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Korean text detected in governance documentation (project rule)**

`docs/00.agent-governance/rules/standards.md` — Language Standards violation:

> "Governance and provider policy files in `docs/00.agent-governance/` must be English."

**Language policy summary:**

| Area | Language |
| ---- | -------- |
| `docs/00.agent-governance/` | **English only** |
| User-facing replies | Korean by default |
| Human-facing repository guides | Korean |
| Technical identifiers and code | Preserve source form |

**Correct approach:**

- Write governance policy explanations in English.
- Put Korean explanations in human-facing `docs/01` through `docs/99` documents when needed.
- Prefer English comments inside code blocks in governance files.

Governance files under `docs/00.agent-governance/` are shared policy inputs for
all AI agents. English keeps multi-provider behavior consistent across Claude,
Gemini, and Codex.

## Related Documents

- `docs/00.agent-governance/README.md`
