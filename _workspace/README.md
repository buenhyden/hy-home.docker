# _workspace

> Repository-local staging surface for non-secret agent and migration support artifacts.

## Purpose

`_workspace` is an isolated repo-support surface for short-lived, non-secret
artifacts created while repository work is in progress.

Use it only when an agent, script, or migration needs temporary files that are
useful during the current task but are not canonical documentation, runtime
configuration, or durable evidence.

## Allowed Surface

Tracked files under `_workspace` are limited to contract documents:

- `_workspace/README.md`
- `_workspace/repo-support/README.md`

Runtime artifacts belong under `_workspace/repo-support/` and are ignored by
default. Examples include generated analysis summaries, dry-run previews,
migration ledgers, and subagent handoff files that do not contain secrets or raw
logs.

## Prohibited Surface

Do not place any of the following under `_workspace`:

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

If a task needs durable evidence, summarize the non-secret result in the
canonical Stage 04 task document, Stage 90 reference, or Stage 00 memory note.

## Tracking Contract

The root `.gitignore` ignores `_workspace/**` by default and re-includes only
the approved contract README files. Repository validation fails if additional
tracked `_workspace` files appear without a future approved contract change.

## Related Documents

- [repo-support README](./repo-support/README.md)
- [workspace support surface spec](../docs/03.specs/106-workspace-support-surface-contract/spec.md)
- [task evidence](../docs/04.execution/tasks/2026-07-05-workspace-support-surface-contract.md)
- [subagent protocol](../docs/00.agent-governance/subagent-protocol.md)
- [environment constraints](../docs/00.agent-governance/rules/environment-constraints.md)
