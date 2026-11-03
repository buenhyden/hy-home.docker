---
title: "Task Checklists"
version: "1.4.2"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-03"
---

# Task Checklists

## Overview

Check scope, implementation evidence, and completion before changing repository state.

## Scope

Approved repository edits, ongoing implementation, and completion evidence.

## Rules

### Before Editing

- [ ] Confirm the approved objective, editable paths, protected surfaces, and exclusions.
- [ ] Load applicable Requirement, Architecture, Spec, Plan, Task, policy, and skill sources.
- [ ] Bind high-risk policy, runtime, CI, template, secret, remote, model, and
      provider changes to explicit approval, validation, and recovery.
- [ ] Define acceptance checks and inspect the shared worktree.

### During Work

- [ ] Keep changes traceable to the approved Plan Task.
- [ ] Keep canonical sources separate from generated provider projections.
- [ ] Preserve secrets and private state; record metadata only.
- [ ] Update affected links and eliminate conflicting active guidance.
- [ ] Record actual evidence in the Task, not a second progress or handoff document.
- [ ] Stop on missing authority, destructive ambiguity, or unexpected scope.

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Verification

### Before Completion

- [ ] Follow the [execution boundary](quality-standards.md#4-execution-boundary)
      for staged lint/format immediately before local commit, server PR final
      defense, direct pre-commit prohibition and the separate all-files route.
- [ ] Run focused tests and validators for each changed authority surface.
- [ ] For registered projections whose inputs changed, regenerate through the
      registered renderer and prove byte-for-byte freshness; do not write
      unaffected projections.
- [ ] Inspect `git diff --check`, status, and the exact task-owned diff.
- [ ] Record pass, fail, baseline debt, skipped checks, recovery, and review separately.
- [ ] Record final criterion acceptance before disposition. A Stage 03 package
      may wait once it is [ready for removal review](sdlc.md#sequence);
      cancelled criteria do not waive remaining Spec acceptance evidence, and
      only a `not-required` decision closes a criterion without PASS.
- [ ] Before removing a retired document, summarize its still-current meaning
      into the owner's Traceability, update every inbound consumer, and add its
      number to the Registry `reserved_history`.
- [ ] Distinguish the worktree, index, and commit a review examined, and report
      missing history or unsupported checkout conversion without claiming success.
- [ ] Create logical Conventional Commits after the review findings are resolved.

## Related Documents

- [Agentic policy](agentic.md)
- [Approval boundaries](approval-boundaries.md)
- [Git workflow](git-workflow.md)
- [Postflight checklist](postflight-checklist.md)
