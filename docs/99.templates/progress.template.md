---
status: draft
---

<!-- Target: docs/00.agent-governance/memory/progress.md -->

# Agent Progress Log

> Running repo-local log for agent work, progress, verification, and durable memory pointers.

## Usage Contract

- AI agents must update `docs/00.agent-governance/memory/progress.md` during repository work.
- Record task progress as concise entries; do not paste transcripts, raw logs, shell history, or secrets.
- Link durable reusable findings to separate memory notes created from `docs/00.agent-governance/memory/template.md`.
- Keep active policy in `rules/`, `scopes/`, provider overlays, runtime files, and root shims; use this file as an audit log and memory index.
- Update the final entry before declaring completion.
- When copied to `docs/00.agent-governance/memory/progress.md`, replace this template frontmatter with `layer: agentic` and `status: active`.
- Target-relative links in `## Related Documents` are calculated from `docs/00.agent-governance/memory/progress.md`, not from `docs/99.templates/`.

## Current Work Log

| Date       | Task         | Status                           | Progress              | Memory                    | Evidence                        |
| ---------- | ------------ | -------------------------------- | --------------------- | ------------------------- | ------------------------------- |
| YYYY-MM-DD | {task-title} | Planned/In Progress/Done/Blocked | {short progress note} | {memory note path or N/A} | {commands, docs, or validators} |

## Phase Tracker

| Phase              | Status                           | Completed  | Notes        |
| ------------------ | -------------------------------- | ---------- | ------------ |
| P0 - {phase-title} | Planned/In Progress/Done/Blocked | YYYY-MM-DD | {short note} |

## Layer Audit

| Layer           | Status                           | Remediation  |
| --------------- | -------------------------------- | ------------ |
| L1 {layer-name} | Planned/In Progress/Done/Blocked | {short note} |

## Open Issues

- None.

## Related Documents

- [Memory README](./README.md)
- [Memory template mirror](./template.md)
- [Bootstrap rules](../rules/bootstrap.md)
- [Task checklists](../rules/task-checklists.md)
