---
title: "Shared Agent Memory Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0234-PLAN-0001"
parent_ids:
- "SPEC-0234"
created: "2026-10-13"
---

# Shared Agent Memory Plan

## Overview

The investigation is complete and the owner decisions are recorded in the
Spec. W2 to W7 implement them; W8 needs two real provider sessions. W9 runs
once after merge.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2, 3, 4, 5, 6 | Starting state, official settings and host library | None | TSK-0001 | Task evidence |
| W2 | 6 | Governance owner for memory rules; workspace guidance | W1 | TSK-0001 | Task evidence |
| W3 | 2, 3 | Store root resolution, schema and CLI with expected-revision writes | W2 | TSK-0001 | Task evidence |
| W4 | 3 | Limits, busy/full handling and refreshable backup | W3 | TSK-0001 | Task evidence |
| W5 | 4, 5 | Hook payload rule, ignore, export and cleanup exclusions | W3 | TSK-0001 | Task evidence |
| W6 | 1 | Project settings that turn native memory off | W3 | TSK-0001 | Task evidence |
| W7 | 7 | Changed gate and candidate quality | W2, W3, W4, W5, W6 | TSK-0001 | Task evidence |
| W8 | 1, 2, 4 | Two-provider, two-worktree acceptance on one store | W7 | TSK-0001 | Task evidence |
| W9 | 1 | Enter eligible Claude native memories into the store through the CLI, once, after merge | W7 | TSK-0001 | Task evidence |

## Verification Plan

- Unit tests run on temporary SQLite databases for each failure in criterion
  3. The real store is never touched.
- `tool_payload` tests cover the store path and read-only reviewer denial.
- Run the changed gate and the remote candidate.
- Native acceptance means a new Claude session and a new Codex session read
  and revise the same record from two worktrees. A single-process synthetic
  test does not count as acceptance.

## Risks and Rollback

- **Lost native recall.** Turning native memory off stops what Claude loads
  today. Order W6 after the CLI exists and after the migration decision.
- **WAL-reset risk.** The library on this host is 3.45.1, and Ubuntu's
  changelog shows no backport of the WAL-reset fix. The store uses a rollback
  journal instead, so the bug cannot apply; readers wait during a write.
- **Codex trust.** An untrusted project ignores `.codex/config.toml`.
- **Migration.** W9 reads the native memory files once, by owner decision,
  and copies only eligible records. It never changes or deletes those files.
- **Rollback.** Revert the commits. The store stays ignored and unread, and
  native memory files were never changed.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-shared-agent-memory.md)
