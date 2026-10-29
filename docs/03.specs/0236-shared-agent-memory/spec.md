---
title: "Shared Agent Memory"
version: "0.5.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0236"
parent_ids:
- "REQ-0024"
- "AD-0027"
- "ADR-0049"
created: "2026-10-13"
---

# Shared Agent Memory

## Overview

Prompt v9 findings F24, F27 and F36 ask that Claude and Codex read and revise
one shared memory store instead of each keeping its own native memory. On
`main` `b1a6976f4` (2026-10-13) the repository has no such store and no owner
for memory rules:

- `.claude/settings.json` sets `autoMemoryEnabled` nowhere; its keys are
  `autoMode`, `deniedMcpServers`, `hooks`, `outputStyle` and `permissions`.
  Claude auto memory is on by default, and this repository's Claude sessions
  use `~/.claude/projects/<project>/memory/`.
- `.codex/` holds `agents/`, `hooks.json`, `provider.md` and `README.md`, with
  no project `config.toml`, so nothing sets `memories.*`.
- `scripts/lib/hooks/tool_payload.py:20-44` exempts one `.md` file directly
  under `~/.claude/projects/<slug>/memory/` from repository edit policy, with
  the slug built from the session project root. Tests:
  `tests/lib/hooks/test_tool_payload.py:76-121`.
- `_workspace/repo-support/README.md:58-59` keeps task context in the current
  Task and says there is no separate governance memory root.
- `.gitignore:111` ignores `.claude/agent-memory-local/` only; no
  `.workspace-memory/` or `.agents/memory/` exists.
- No file under `.agents/governance/` owns memory rules.
  `hookify.warn-governance-memory-edit.md`, registered at
  `.agents/governance/providers/registry.yaml:44`, warns on governance file
  edits, not memory.

This Spec defines the contract and records the owner decisions under Scope.

## Scope

In scope:

- project settings that turn native provider memory off;
- one shared store with a registered persistent runtime root, its schema and a
  CLI that both providers call;
- the hook payload rule for that root;
- the governance owner and workspace guidance;
- ignore, export and cleanup handling;
- the acceptance tests.

Out of scope:

- moving or deleting existing native memory files, or reading them outside
  the one migration in decision 2;
- user-global or managed provider settings;
- syncing across machines or clones;
- automatic collection from transcripts or Task evidence;
- remote databases.

The owner decided on 2026-10-13:

1. **Store location:** `.workspace-memory/memory.sqlite3` in the main
   checkout, ignored by Git, outside `.worktrees/` and `_workspace/` cleanup,
   and shared by every worktree of that checkout.
2. **Existing native memories:** left in place. Turning native memory off
   stops their loading. Revised later the same day: after merge, the main
   session reads the Claude native memory files once and enters each eligible
   one into the shared store through the CLI (W9). The native files are not
   changed.
3. **Limits:** logical limits only, enforced by the CLI on row count and byte
   totals. No filesystem hard quota exists and none is claimed. The numbers
   are set in W4 and recorded in the Task.
4. **Backup target:** an SQLite online-backup snapshot added to the existing
   backup and restore runbook. Including that backup in the Restic snapshot of
   `hyhome-backup.service` is deferred to a separate Spec.
5. **Codex activation:** `.codex/config.toml` sets
   `memories.generate_memories` and `memories.use_memories` to `false`, and
   the user marks the project trusted. Whether Codex honors these keys is
   checked in a live session in W8.
6. **Journal mode:** the store uses a rollback journal (`journal_mode=DELETE`)
   instead of WAL. Ubuntu's libsqlite3 3.45.1-1ubuntu2.8 changelog shows no
   backport of the WAL-reset fix.
7. **Runbook authority:** RUN-0021 is promoted to `active`, and the memory
   CLI's manifest row is `mutation: runtime` with RUN-0021 as its authority
   (answer "Promote RUN-0021 to active").
8. **Decision status:** ADR-0049 is to be accepted (answer "Accept both",
   which also covers ADR-0048). A new ADR enters as `proposed`, so its status
   changes in the first change after this Spec merges.

## Contracts

1. **Native memory off.** The project setting `.claude/settings.json` sets
   `"autoMemoryEnabled": false`. The project setting `.codex/config.toml` sets
   `memories.generate_memories = false` and `memories.use_memories = false`.
   - Each setting is merged into the existing file, never replaces it.
   - No tracked subagent declares `memory:`.
   - Turning native memory off never deletes native memory files.
2. **One store.** The store is one SQLite database under one registered
   persistent runtime root that `.gitignore` ignores.
   - Its location is resolved from the main worktree through
     `git rev-parse --git-common-dir`. A linked worktree never creates its own
     store.
   - The root is outside `.worktrees/`, `_workspace/` and provider home
     directories, so removing a worktree or cleaning `_workspace` cannot
     delete it.
   - If the root cannot be resolved, the CLI reports memory as unavailable and
     creates no second store.
3. **Schema.** Every record has one envelope for both providers:
   `schema_version`, `workspace_id`, `memory_id`, `tier` (`short-term`,
   `long-term`, `domain`), `revision`, `owner`, `created_at`, `source_refs`,
   `eligibility`, `sensitivity` and `body`.
   - What a record may not hold is stated once, in
     [environment constraints section 5](../../../.agents/governance/environment-constraints.md#5-shared-agent-memory).
4. **CLI.** One repository CLI is the only sanctioned writer. It supports current
   lookup, bounded history lookup, an update that requires the expected
   revision, eligibility correction, usage report and backup.
   - Both providers call the same command.
   - A write succeeds only after commit.
   - A stale expected revision preserves every committed revision and returns
     a conflict. Its incoming payload is retained when capacity permits;
     otherwise `stored=false` names the expected and current revisions.
5. **Storage safety.** The store uses a rollback journal on a local
   filesystem, takes the single write lock with `BEGIN IMMEDIATE`, sets
   `busy_timeout`, and handles `SQLITE_BUSY` and `SQLITE_FULL` explicitly.
   - The linked SQLite library version is recorded when the store ships. WAL
     is used only on a library with the WAL-reset fix or a documented
     distribution backport.
   - The store directory and file are not symbolic links. A backup is created
     private before data is written, in a 0700 directory, and never over the
     store. A restore creates the store exclusively, accepts only the store
     schema, and leaves no partial store.
   - Size limits are reported as hard limits only where a filesystem quota or
     isolated volume enforces them. Otherwise they are logical limits, and the
     report says so.
   - Exceeding a limit rejects the new write with `MEMORY_CAPACITY_EXCEEDED`
     and never deletes, summarizes or moves existing revisions.
6. **Backup and recovery.** A backup is one container refreshed with the
   SQLite online backup API.
   - It is written to a temporary file, checked, then atomically replaced.
   - A failed backup keeps the previous good backup.
   - Recovery restores the records only. It never revives retired governance
     or QA.
7. **Hook payload.** `tool_payload.py` refuses an Edit or Write that targets
   the shared store; the CLI writes it through SQLite, not an edit tool. Shell
   commands are not covered, as section 5 states.
   - The native memory exemption is removed once contract 1 lands.
   - A read-only reviewer gains no Write, Edit or shell permission because of
     memory.
8. **Export and cleanup.** Template export, site build and the
   `_workspace`/`.worktrees` cleanup procedures exclude the runtime root.
   - The workspace guidance names the root and its owner.
   - Git exclusion is not a backup.

### R10 currentness and retention amendment

Existing schema 1 rows and native migration provenance remain lossless. New
revisions use `schema_version=2` for the contract that includes review state,
domain ID and request identity in separate provenance. Unpinned existing records
are never promoted to current automatically. Default `get`/`list` return only
eligible records reviewed as current whose source pins match. Historical bodies
are accessed explicitly through `get --historical`, `history`, `list --all` or
`export`. Source-pin formats, allowed paths and tier/domain/metadata/page limits
belong to [environment constraints section 5](../../../.agents/governance/environment-constraints.md#5-shared-agent-memory).
Comparison uses the caller worktree; source changes, deletion or inaccessibility
invalidate current reuse. Personal native memories are not collected again.

An optional request key binds the complete target, expected revision, body,
sources and allowed scope within the same transaction. Different inputs never
return a previous success. Conflicts are retained in the same store and charged
against capacity. Database page limits are reapplied on every reconnect.
Concurrent online backups serialize through the source inode lock and replace
the previous good copy atomically. Restore checks schema 1/2 and revision-to-
provenance relationships, builds a unique temporary file, then publishes only
to an absent target.

Execution, synthetic tests and review of this amendment belong to
[SPEC-0212 current Task W22/criterion 17](../0212-request-baseline-and-reconciliation/tasks/tsk-0007-r10-reconciliation.md).
This package's existing criteria and W8/W9 acceptance records receive no duplicate
acceptance. Actual provider/worktree and Restic evidence dated 2026-10-13 is
reused within its original scope; the new engine is tested only on synthetic
databases. Applying the amendment to the real private store and observing the
effective Codex project-memory settings remain separate, uncompleted work.

## Acceptance Criteria

1. Project settings for both providers turn native memory off. A fresh session
   of each, started after the settings are trusted, shows it off.
2. Claude writes a record, Codex reads the same `memory_id`, `revision` and
   body from another worktree, and Claude then sees Codex's revision. These
   are two real provider sessions on one physical store.
3. A stale expected revision, a concurrent quota race, a full database and a
   failed backup each fail explicitly and leave existing records unchanged.
   This is shown with a small test database.
4. Removing a worktree and cleaning `_workspace` leave the store intact, and
   an Edit or Write targeting the store is refused while the CLI still reads
   and writes it.
5. `tool_payload.py` has no native memory exemption, and its tests cover the
   store path rule.
6. One governance owner states the memory rules, and the workspace guidance
   routes to it.
7. The changed gate and `candidate-quality` pass.

## Failure Conditions

Unresolvable main-store identity must report memory unavailable without
creating a second store. Stale revisions, busy/full storage, capacity limits
and failed backups must preserve committed records and the last good copy;
unreviewed or changed source pins cannot yield current memory, and source
settings do not establish effective native-memory suppression.

## Related Documents

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md),
  REQ-0024-FR-0015
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0049](../../02.architecture/decisions/0049-shared-agent-memory-store.md)
- [Plan](plan.md)
- [Task](tasks/tsk-0001-shared-agent-memory.md)
