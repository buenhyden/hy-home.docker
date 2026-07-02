---
status: draft
---

<!-- Target: docs/00.agent-governance/memory/{short-title}.md -->

# Memory: {short-title}

> Use this template for durable advisory memory notes under `docs/00.agent-governance/memory/`.
>
> Rules:
>
> - Memory notes are advisory retrieval context, not active policy.
> - Do not store transcripts, raw logs, shell history, credentials, tokens, private keys, or secret values.
> - Keep the note concise, reusable, and evidence-backed.
> - Update `docs/00.agent-governance/memory/progress.md` when creating or materially changing a memory note.
> - When copied to `docs/00.agent-governance/memory/<short-title>.md`, replace this template frontmatter with `layer: agentic`.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.

- Date: YYYY-MM-DD
- Layer: {architecture|backend|frontend|infra|security|ops|qa|docs|meta|product|mobile|entry|common|agentic}
- Status: active
- Applies To: {paths, task types, or runtime surfaces}
- Tags: #governance #quality #incident
- Retrieval Keywords: {keywords agents should search for}
- Last Verified: YYYY-MM-DD

## Problem

Describe the exact issue.

## Context

List relevant files, constraints, and runtime conditions.

## Resolution

Describe what changed and why it worked.

## Prevention

List concrete guardrails for future runs.

## Evidence

List related commands, validators, docs, or follow-up task references.

## Related Documents

- [Memory README](./README.md)
- [Progress log](./progress.md)
- [Memory template](../../99.templates/templates/governance/memory.template.md)
