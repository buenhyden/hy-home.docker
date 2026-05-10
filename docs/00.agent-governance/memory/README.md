---
layer: agentic
---

# Governance Memory

> Durable governance learnings and reusable incident patterns for agent execution.

## Overview

This folder stores durable, English-only notes that improve future agent runs. It is for governance findings, repeated workflow pitfalls, and reusable remediation patterns.

Memory notes are advisory retrieval context. They help agents remember prior pitfalls and fixes, but they do not define active policy. Current user instructions, system/developer instructions, repository rules, scopes, provider overlays, and live repository evidence always take precedence.

## Audience

This README is for:

- AI Agents
- Documentation Writers
- Repository Maintainers

## Scope

### In Scope

- Keep entries concise, technical, and reusable.
- Store only durable insights, not temporary session chatter.
- Record out-of-scope breakages that should not be fixed during the current task.
- Record repeated failure patterns, validator pitfalls, and resolved governance conflicts.
- Retrieve relevant notes before governance, docs, runtime, or repeated-failure tasks.
- Write entries in English.

### Out of Scope

- Active policy that belongs in `rules/`, `scopes/`, or provider overlays.
- Session transcripts, raw logs, credentials, shell history, or personal notes.
- Human-facing guide, operation, runbook, or incident documents.

## Structure

```text
memory/
├── progress.md  # Governance migration and audit state
├── template.md  # Standard shape for new memory entries
├── *.md         # Durable advisory memory notes
└── README.md    # This file
```

## How to Work in This Area

1. During pre-task discovery, open this README and `progress.md` for governance, docs, runtime, or repeated-failure work.
2. Use targeted `rg` queries over this folder to find at most the relevant memory notes.
3. Treat memory notes as advisory context and corroborate them against live files before acting.
4. Create entries from `template.md` when a finding is durable, reusable, or intentionally out of scope for the current task.
5. Link each entry to related stage docs when applicable.
6. Tag entries by layer and risk type.

## Operational Procedures

- Add an entry after resolving a complex issue or policy conflict.
- Add an entry when a read-only or out-of-scope issue should survive the current task.
- Revisit memory entries during planning for similar tasks.
- Do not copy memory text into active policy without updating the relevant rule, scope, provider, or runtime file.
- Do not store credentials, tokens, private keys, shell history, or raw logs in memory notes.

## Maintenance and Safety

- Archive stale or superseded memory notes.
- Remove duplicated memory entries.
- If memory conflicts with current repository state, follow the live repository state and record the conflict only when it is reusable.

## Related Documents

- [Governance hub](../README.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Task checklists](../rules/task-checklists.md)
- [Memory template](./template.md)
