---
status: active
---

<!-- Target: docs/03.specs/122-agentic-research-pack-consolidation/README.md -->

# Agentic Research Pack Consolidation

> Design contract for consolidating the workspace's agentic engineering research into one current, source-backed canonical pack.

## Overview

This folder defines the design for refreshing the canonical 2026-07-05
agentic engineering research pack, merging verified material from the duplicate
2026-07-07 update, and marking the duplicate pack superseded.

The design also introduces a cutoff-bound provider model landscape covering the
official Claude, OpenAI/Codex, and Gemini model catalogs as of
2026-07-10 10:00 KST (01:00 UTC).

## Audience

- Documentation maintainers
- Agentic workflow maintainers
- AI agent and provider reviewers
- QA and security reviewers

## Scope

### In Scope

- Canonical Stage 90 research-pack consolidation and source revalidation.
- Workspace-to-external-practice comparison for every requested research area.
- Provider model status and task-fit analysis at the approved cutoff.
- Supersession of the duplicate 2026-07-07 research pack.
- Stage 04 planning, task evidence, logical commits, and documentation checks.

### Out of Scope

- Runtime, Docker Compose, CI, provider adapter, hook, secret, or model-policy
  changes.
- Adoption of external recommendations as active workspace policy.
- Deletion or rewriting of completed Stage 03/04 historical evidence.
- Claims about provider capability or model availability without current
  official evidence.

## Structure

```text
122-agentic-research-pack-consolidation/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Read [spec.md](./spec.md) for the approved consolidation and evidence
   contracts.
2. Treat the 2026-07-05 Stage 90 pack as the only active canonical research
   target.
3. Merge earlier overlapping research content only after repo-local and
   external-source verification.
4. Preserve completed Stage 03/04 artifacts as traceability evidence; link them
   instead of copying their bodies.
5. Record runtime, policy, CI, security, or provider changes as follow-up gaps.

## Implementation State

Tasks 1-6 have clean task-scoped reviews, and T-ARC-006/VAL-ARC-006 are
satisfied at that gate. This specification remains active: the first
whole-branch preclosure review returned findings, so its clean repeat, the
separate lifecycle-closure commit, and the post-closure review are still
required. No completed status or merge-readiness claim is made here.

## Related Documents

- [Technical specification](./spec.md)
- [Implementation plan](../../04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md)
- [Task evidence](../../04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md)
- [Previous research refresh specification](../104-agentic-research-pack-refresh/spec.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Duplicate research pack to supersede](../../90.references/research/2026-07-07-agentic-research-pack-update/README.md)
- [Research category](../../90.references/research/README.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
