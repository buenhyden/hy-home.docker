# _workspace/repo-support

> Ignored staging area for non-secret repository support artifacts.

## Purpose

`_workspace/repo-support` is the only approved `_workspace` location for
short-lived agent, migration, dry-run, and analysis artifacts.

This directory is for task-local support files that help an agent complete
repository work. It is not an active documentation stage, archive, operations
folder, runtime config surface, or long-term evidence store.

## Allowed Artifacts

The following non-secret artifacts may be created here during a task:

- generated analysis summaries;
- dry-run previews by ID, path, or planned action;
- migration ledgers;
- subagent handoff files;
- temporary comparison tables;
- validation scratch notes that contain no raw logs or secret-bearing output.

## Prohibited Artifacts

Do not create or retain:

- diagnostics dumps;
- local logs or raw logs;
- auth files;
- tokens;
- credentials;
- private keys;
- shell history;
- secret values;
- token-bearing command output;
- full secret file bodies.

## Promotion Rule

Before task completion, promote the durable non-secret outcome to the canonical
owner:

- implementation evidence goes to `docs/04.execution/tasks/`;
- stable reference context goes to `docs/90.references/`;
- governance memory goes to `docs/00.agent-governance/memory/`.

Leave raw scratch artifacts ignored unless the user explicitly approves a
future non-secret promotion.

## Related Documents

- [workspace README](../README.md)
- [workspace support surface spec](../../docs/03.specs/106-workspace-support-surface-contract/spec.md)
- [workspace support surface task](../../docs/04.execution/tasks/2026-07-05-workspace-support-surface-contract.md)
