---
title: "Workspace Staging Surface"
version: "1.2.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-03-05"
---

# Workspace Staging Surface

## Overview

`_workspace` is the repository-local staging surface for short-lived, non-secret
artifacts produced while repository work is in progress. It exists so that an
agent, script, or migration has one declared place for temporary files, instead
of scattering them across documentation stages, runtime configuration, or
durable evidence folders.

Nothing here is authority. A result that must survive the task is summarized
into its canonical owner and the staging copy is discarded.

## Audience

- Agents and scripts that need working files during a task.
- Maintainers reviewing what a task produced before its evidence was
  summarized.
- Anyone auditing that agent scratch output never reached the repository.

## Scope

- Owned: the two tracked contract documents below, and the ignored
  `repo-support/` staging tree that scripts write into.
- Not owned: durable evidence, which belongs in the co-located Stage 03 Task;
  operator procedure, which belongs in `docs/05.operations/`; and any secret
  value, which belongs in `secrets/` and never here.

## Structure

| Path | Tracked | Role |
| :--- | :--- | :--- |
| `README.md` | yes | This contract |
| `repo-support/README.md` | yes | Staging-tree contract |
| `repo-support/**` | no | Ignored runtime artifacts written during a task |

Scripts that write here name their own subdirectory under `repo-support/`, for
example `scripts/security/verify-sample-service-supply-chain.sh` and
`scripts/operations/rehearse-postgres-logical-upgrade.sh`.

## Allowed Surface

Runtime artifacts belong under `repo-support/` and are ignored by default.
Examples include generated analysis summaries, dry-run previews, migration
ledgers, and subagent handoff files that contain no secrets and no raw logs.

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

## Tracking Contract

The root `.gitignore` ignores everything under `_workspace/` and re-includes
only the two tracked contract documents named in Structure. Git never descends
into an excluded directory, so `repo-support/` is re-included and its contents
excluded again before `repo-support/README.md` is restored; changing the outer
pattern without rewriting that ladder silently drops the second document.
Verify the rule rather than trusting this sentence:

```bash
git check-ignore -v --no-index _workspace/repo-support/README.md
git check-ignore -v _workspace/repo-support/scratch.json
git ls-files _workspace/
```

`--no-index` carries the check. Without it git consults the index first and
refuses to call a tracked file ignored, so a dropped negation stays invisible:
the document remains tracked and every question about its ignored state answers
no while the rule that re-included it is gone.

Read the rule, not the exit status. `-v` exits 0 whether the matching pattern
excludes or re-includes, so only the printed rule separates the two: a healthy
ladder answers with the negation `!/_workspace/repo-support/README.md`, and a
broken one answers with the outer `/_workspace/*`. The second command must name
the rule that excludes a scratch path, and the third must list exactly the two
tracked README files; a third tracked path means an artifact escaped the
staging contract.

`test_workspace_contract_documents_stay_reachable` in
[tests/lib/test_surface_ownership.py](../tests/lib/test_surface_ownership.py)
asks the same question with `-q`, whose exit status does separate the two, and
runs on every gate. This contract no longer rests on someone remembering to
type the commands.

## How to Work in This Area

1. Write the artifact under `_workspace/repo-support/<task-slug>/` → `git
   status` stays clean because the path is ignored.
2. Summarize the non-secret result into the co-located Stage 03 Task → the
   durable claim lives with its evidence, not in staging.
3. Run `git ls-files _workspace/` before completing → the output is exactly the
   two tracked contract documents.
4. Leave the artifact in place or delete it → either is fine; nothing here is
   recoverable authority.

## Related Documents

- [Staging tree contract](./repo-support/README.md)
- [Subagent protocol](../.agents/governance/agentic.md)
- [Environment constraints](../.agents/governance/environment-constraints.md)
- [Task checklists](../.agents/governance/task-checklists.md)
- [Repository README](../README.md)
