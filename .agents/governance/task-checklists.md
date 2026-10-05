---
title: "Task Checklists"
version: "1.3.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
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

### Before Completion

- [ ] Follow the [execution boundary](quality-standards.md#4-execution-boundary)
      for direct pre-commit prohibition and the sole approved all-files route.
- [ ] Run focused tests and validators for each changed authority surface.
- [ ] Regenerate registered projections and prove byte-for-byte freshness.
- [ ] Inspect `git diff --check`, status, and the exact task-owned diff.
- [ ] Record pass, fail, baseline debt, skipped checks, recovery, and review separately.
- [ ] Record final completion receipts before disposition. A completed Stage 03
      package may wait with its completed Plan and completed or validly cancelled
      Tasks; cancelled criteria do not waive remaining Spec acceptance evidence.
- [ ] Bind any later preservation to its prepared source object and separate
      disposition approval. Preserve Task Commit Ledgers and frozen bodies.
- [ ] For reassessment or history-only availability, verify the current assessment,
      original-revision structural record, hold, consumer cutover, recoverability,
      and a separately current trusted-operator authorization for any pending
      removal. A missing, mismatched, or revoked current source blocks the
      operation; archive-record validation is not authentication. Test missing and
      mismatched record integrity in fixtures unless actual removal is authorized.
- [ ] Distinguish worktree, index, commit, and historical-link checks, and report
      missing history or unsupported checkout conversion without claiming success.
- [ ] Create logical Conventional Commits only after review approval.

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Related Documents

- [Agentic policy](agentic.md)
- [Approval boundaries](approval-boundaries.md)
- [Git workflow](git-workflow.md)
- [Postflight checklist](postflight-checklist.md)
