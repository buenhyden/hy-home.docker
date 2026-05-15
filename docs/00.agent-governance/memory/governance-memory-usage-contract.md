---
layer: agentic
---

# Memory: governance-memory-usage-contract

- Date: 2026-05-10
- Layer: agentic
- Status: active
- Applies To: `docs/00.agent-governance/memory/`, bootstrap, task checklists, repository validators
- Tags: #governance #memory #agentic
- Retrieval Keywords: governance memory, advisory memory, memory template, progress.md, progress template, out-of-scope findings, repeated failures, memory contract
- Last Verified: 2026-05-10

## Problem

The governance memory folder existed and was referenced as a place to record out-of-scope findings, but it was not clearly wired into the bootstrap flow as pre-task advisory context. The `progress.md` file and ordinary memory notes also lacked dedicated templates in `docs/99.templates/` and explicit requirements for agents to update progress and memory pointers during work.

## Context

`docs/00.agent-governance/memory/` is intended for durable governance notes, repeated pitfalls, and reusable remediation patterns. It must not become active policy or override rules, scopes, provider overlays, direct user instructions, or live repository evidence.

## Resolution

The bootstrap sequence, agentic rule, task checklist, governance hub, memory template, progress template, and repository contract check now make the memory workflow explicit:

- Review memory and `progress.md` for repository work.
- Retrieve only relevant notes with targeted search.
- Treat memory as advisory context.
- Record task progress, verification evidence, and durable memory pointers in `progress.md`.
- Record durable out-of-scope or repeated-failure findings back into memory notes created from `docs/99.templates/memory.template.md`.

## Prevention

Keep active policy in `rules/`, `scopes/`, provider overlays, root shims, and runtime files. Use `progress.md` as the running work log and memory index, use `docs/99.templates/memory.template.md` for memory notes that should survive a single task, then validate the memory contract through `scripts/validation/check-repo-contracts.sh`.

## Evidence

- `AGENTS.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/99.templates/memory.template.md`
- `docs/99.templates/progress.template.md`
- `scripts/validation/check-repo-contracts.sh`
