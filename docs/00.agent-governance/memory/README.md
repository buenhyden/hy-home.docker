---
layer: agentic
---

# Governance Memory

> Durable governance learnings and reusable incident patterns for agent execution.

## Overview

This folder stores durable, English-only notes that improve future agent runs. It is for governance findings, repeated workflow pitfalls, and reusable remediation patterns.

## Audience

This README is for:

- AI Agents
- Documentation Writers
- Repository Maintainers

## Scope

### In Scope

- Keep entries concise, technical, and reusable.
- Store only durable insights, not temporary session chatter.
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
└── README.md    # This file
```

## How to Work in This Area

1. Create entries from `template.md`.
2. Link each entry to related stage docs when applicable.
3. Tag entries by layer and risk type.

## Operational Procedures

- Add an entry after resolving a complex issue or policy conflict.
- Revisit memory entries during planning for similar tasks.

## Maintenance and Safety

- Archive stale or superseded memory notes.
- Remove duplicated memory entries.

## Related Documents

- [Governance hub](../README.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Task checklists](../rules/task-checklists.md)
- [Memory template](template.md)
