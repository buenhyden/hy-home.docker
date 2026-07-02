---
layer: agentic
---

# Governance Memory

> Durable governance learnings and reusable incident patterns for agent execution.

## Overview

This folder stores durable, English-only notes that improve future agent runs. It is for governance findings, repeated workflow pitfalls, reusable remediation patterns, and the mandatory agent progress log.

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
- Create or update memory notes from `docs/99.templates/templates/governance/memory.template.md`.
- Write entries in English.

### Out of Scope

- Active policy that belongs in `rules/`, `scopes/`, or provider overlays.
- Session transcripts, raw logs, credentials, shell history, or personal notes.
- Human-facing guide, operation, runbook, or incident documents.

## Structure

```text
memory/
├── progress.md  # Mandatory agent progress log and memory index
├── template.md  # Local mirror of docs/99.templates/templates/governance/memory.template.md
├── *.md         # Durable advisory memory notes
└── README.md    # This file
```

## How to Work in This Area

1. During pre-task discovery, open this README and `progress.md` for repository work.
2. Use targeted `rg` queries over this folder to find at most the relevant memory notes.
3. Treat memory notes as advisory context and corroborate them against live files before acting.
4. Create entries from `docs/99.templates/templates/governance/memory.template.md` when a finding is durable, reusable, or intentionally out of scope for the current task.
5. Link each entry to related stage docs when applicable.
6. Tag entries by layer and risk type.
7. Update `progress.md` from `docs/99.templates/templates/governance/progress.template.md` before declaring completion.

## Operational Procedures

- Add an entry after resolving a complex issue or policy conflict.
- Add an entry when a read-only or out-of-scope issue should survive the current task.
- Use `docs/99.templates/templates/governance/memory.template.md` for new notes and keep `template.md` synchronized as the local mirror.
- Update `progress.md` with the current task status, verification evidence, and durable memory note path.
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
- [Memory template](../../99.templates/templates/governance/memory.template.md)
- [Local memory template mirror](./template.md)
