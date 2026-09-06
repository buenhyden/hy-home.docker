---
name: hy-home
description: hy-home.docker workspace presentation — terminal-rendered findings with clickable file:line evidence, routed to canonical governance for language, documentation, and completion policy.
keep-coding-instructions: true
---

You are operating in the `hy-home.docker` workspace.

## Authority

Canonical governance owns what you must do. This style owns only how a Claude
Code response is rendered, and it defines no policy of its own.

- Reporting substance and language: `.agents/governance/output-style.md`.
- Artifact language, template selection, and stage routing:
  `.agents/governance/documentation-protocol.md#authoring-rules`.
- Completion and honesty obligations: `.agents/governance/task-checklists.md`.
- Approval boundaries: `.agents/governance/approval-boundaries.md`.

Where this file and a canonical policy appear to disagree, the policy wins and
the disagreement is a defect in this file.

## Claude Code Rendering

- Responses render as GitHub-flavored Markdown in a terminal. Prefer scannable
  tables and short lists over prose blocks.
- Write evidence as `file:line`; the terminal makes it clickable, so a reader
  reaches the source in one step.
- Keep code blocks runnable as written, and mark a non-executable snippet
  explicitly.
- Show failing output verbatim rather than summarizing it.
