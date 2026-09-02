---
title: Task Checklists
type: governance/policy
layer: agentic
owner: "@buenhyden"
---

# Task Checklists

## Before Editing

- [ ] Confirm the approved objective, editable paths, protected surfaces, and exclusions.
- [ ] Load applicable Requirement, Architecture, Spec, Plan, Task, policy, and skill sources.
- [ ] Bind high-risk policy, runtime, CI, template, secret, remote, model, and
      provider changes to explicit approval, validation, and recovery.
- [ ] Define acceptance checks and inspect the shared worktree.

## During Work

- [ ] Keep changes traceable to the approved Plan Task.
- [ ] Keep canonical sources separate from generated provider projections.
- [ ] Preserve secrets and private state; record metadata only.
- [ ] Update affected links and eliminate conflicting active guidance.
- [ ] Record actual evidence in the Task, not a second progress or handoff document.
- [ ] Stop on missing authority, destructive ambiguity, or unexpected scope.

## Before Completion

- [ ] Never run `pre-commit run` directly; use
      `scripts/validation/run-agent-precommit-all-files.sh` only when the
      all-files gate is approved and the work is Git-visible, non-ignored repository state.
- [ ] Run focused tests and validators for each changed authority surface.
- [ ] Regenerate registered projections and prove byte-for-byte freshness.
- [ ] Inspect `git diff --check`, status, and the exact task-owned diff.
- [ ] Record pass, fail, baseline debt, skipped checks, recovery, and review separately.
- [ ] Create logical Conventional Commits only after review approval.

## Related Documents

- [Agentic policy](agentic.md)
- [Approval boundaries](./approval-boundaries.md)
- [Git workflow](./git-workflow.md)
- [Postflight checklist](./postflight-checklist.md)
