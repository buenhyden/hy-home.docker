---
layer: agentic
---

# Memory: governance-memory-usage-contract

- Date: 2026-05-10
- Layer: agentic
- Status: active
- Applies To: `docs/00.agent-governance/memory/`, bootstrap, task checklists, repository validators
- Tags: #governance #memory #agentic
- Retrieval Keywords: governance memory, advisory memory, out-of-scope findings, repeated failures, memory contract
- Last Verified: 2026-05-10

## Problem

The governance memory folder existed and was referenced as a place to record out-of-scope findings, but it was not clearly wired into the bootstrap flow as pre-task advisory context.

## Context

`docs/00.agent-governance/memory/` is intended for durable governance notes, repeated pitfalls, and reusable remediation patterns. It must not become active policy or override rules, scopes, provider overlays, direct user instructions, or live repository evidence.

## Resolution

The bootstrap sequence, agentic rule, task checklist, governance hub, and repository contract check now make the memory workflow explicit:

- Review memory for governance, docs, runtime, or repeated-failure work.
- Retrieve only relevant notes with targeted search.
- Treat memory as advisory context.
- Record durable out-of-scope or repeated-failure findings back into memory.

## Prevention

Keep active policy in `rules/`, `scopes/`, provider overlays, root shims, and runtime files. Use memory notes to preserve reusable context and findings that should survive a single task, then validate the memory contract through `scripts/check-repo-contracts.sh`.

## Evidence

- `AGENTS.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `scripts/check-repo-contracts.sh`
