---
layer: agentic
---

# Governance Memory

> Durable governance learnings and reusable incident patterns for agent execution.

## Overview

This folder stores durable, English-only notes that improve future agent runs.
It provides one bounded current-state record, historical navigation, governance
findings, repeated workflow pitfalls, and reusable remediation patterns.

Memory notes are advisory retrieval context. They help agents remember prior
pitfalls and fixes, but they do not define active policy or path authority.
Current user instructions, system/developer instructions, typed Stage 00
contracts, repository rules, scopes, provider overlays, and live repository
evidence always take precedence.

`current.md` is the only shared current-state route. It is advisory, not policy
authority. Provider-local or user-global memory may supplement a runtime
session, but it may not replace, override, or fork this repository record.

## Audience

This README is for:

- AI Agents
- Documentation Writers
- Repository Maintainers

## Scope

### In Scope

- Keep entries concise, technical, and reusable.
- Replace `current.md` in place when the active task, verified commit, blockers,
  or next handoff changes.
- Store only durable insights, not temporary session chatter.
- Record out-of-scope breakages that should not be fixed during the current task.
- Record repeated failure patterns, validator pitfalls, and resolved governance conflicts.
- Retrieve relevant notes before governance, docs, runtime, or repeated-failure tasks.
- Create or update memory notes from `docs/99.templates/templates/governance/memory.template.md`.
- Write entries in English.

### Out of Scope

- Active policy that belongs in `rules/`, `scopes/`, or provider overlays.
- Session transcripts, raw command output, policy bodies, credentials, tokens,
  private provider state, shell history, or personal notes.
- Human-facing guide, operation, runbook, or incident documents.

## Structure

```text
memory/
├── current.md   # Bounded active task and verified-state handoff
├── progress.md  # Append-preserved historical navigation
├── *.md         # Durable advisory memory notes
└── README.md    # This file
```

## How to Work in This Area

1. During pre-task discovery, open this README and `current.md`.
2. Use targeted `rg` queries over this folder to find at most the relevant memory notes.
3. Treat memory notes as advisory context and corroborate them against live files before acting.
4. Validate the `Current task` and `Verified commit` labels before relying on
   current state. A current Task must exist with `draft` or `active` status,
   and the verified commit must be an ancestor of `HEAD`.
5. Replace stale `current.md` state instead of appending another current-state
   section. Its exact seven-section envelope is limited to 32 KiB and 400
   lines.
6. Create entries from `docs/99.templates/templates/governance/memory.template.md` when a finding is durable, reusable, or intentionally out of scope for the current task.
7. Link each entry to related stage docs when applicable.
8. Use `progress.md` only to navigate preserved historical work. Durable
   implementation and review evidence belongs in the applicable Stage 04 Task.

## Operational Procedures

- Add an entry after resolving a complex issue or policy conflict.
- Add an entry when a read-only or out-of-scope issue should survive the current task.
- Use `docs/99.templates/templates/governance/memory.template.md` as the only
  source for new Memory notes.
- Keep the current-state owner aligned with the active Task owner. Update
  `current.md` after an approved decision or verified-state change, then have
  the Task's independent governance reviewers verify the handoff.
- Keep `current.md` to its registered sections and value-free labels. Link
  durable evidence; do not paste transcripts, output streams, command logs,
  policy bodies, shell history, authentication material, or private runtime
  memory.
- Link reusable findings to separate Memory notes created from the Stage 99
  source. Preserve `progress.md` rows and use them only as historical pointers.
- Revisit memory entries during planning for similar tasks.
- Do not copy memory text into active policy without updating the relevant rule, scope, provider, or runtime file.
- If the current record fails bounds, content, Task-state, or Git-ancestry
  validation, stop using it as current context and repair or replace it from
  durable evidence.

## Maintenance and Safety

- Compact `current.md` by replacing obsolete bullets, never by adding a second
  current-state file. Preserve durable facts in Stage 04 before compaction.
- Archive stale or superseded advisory notes only after their durable evidence
  and Git provenance are confirmed.
- Remove duplicated memory entries.
- If memory conflicts with current repository state, follow the live repository state and record the conflict only when it is reusable.
- Keep provider overlays limited to loading mechanics; they may not copy the
  current-state body.

## Related Documents

- [Governance hub](../README.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Task checklists](../rules/task-checklists.md)
- [Current project memory](./current.md)
- [Historical progress navigation](./progress.md)
- [Memory template](../../99.templates/templates/governance/memory.template.md)
