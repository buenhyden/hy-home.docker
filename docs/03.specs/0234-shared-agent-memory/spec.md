---
title: "Shared Agent Memory"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0234"
parent_ids:
- "REQ-0024"
- "AD-0027"
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

This Spec defines the contract. The owner decisions listed under Scope
must be made before the Plan's implementation units start.

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
- reading, moving or deleting existing native memory files;
- user-global or managed provider settings;
- syncing across machines or clones;
- automatic collection from transcripts or Task evidence;
- remote databases.

Owner decisions required before any implementation unit starts, not
decided here:

1. **Store location:** a repository-ignored root such as the v9 candidate
   `.workspace-memory/memory.sqlite3` in the main worktree, or another
   host-local path.
2. **Existing native memories:** whether `~/.claude/projects/<project>/memory/`
   records are migrated, copied by the owner, or left in place unread.
   Turning native memory off stops their loading.
3. **Limits:** the per-tier, per-revision, database and total storage numbers.
   v9 proposes 64/128/256 MiB tiers, 256 KiB per revision, a 1 GiB database
   and 4 GiB total, but these are suggestions, not approved values. Also
   decide whether any of them must be a hard filesystem quota.
4. **Backup target:** where the backup container lives, and whether it joins
   the existing backup runbook.
5. **Codex activation:** whether to trust the project so `.codex/config.toml`
   loads at all.


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
   - A memory record is never Task status, QA result, approval or acceptance
     evidence, and never a second copy of a governance rule.
4. **CLI.** One repository CLI is the only writer. It supports current
   lookup, bounded history lookup, an update that requires the expected
   revision, eligibility correction, usage report and backup.
   - Both providers call the same command.
   - A write succeeds only after commit.
   - A stale expected revision returns a conflict and changes nothing. There
     is no silent last-write-wins.
5. **Storage safety.** The store uses WAL on a local filesystem with a single
   writer, `busy_timeout`, and explicit handling of `SQLITE_BUSY`,
   `SQLITE_FULL` and checkpoint failure.
   - The linked SQLite library version is recorded when the store ships.
     Concurrency is accepted only on a library with the WAL-reset fix or a
     documented distribution backport.
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
7. **Hook payload.** `tool_payload.py` treats the shared store path as outside
   repository edit policy only for the CLI's own writes.
   - The native memory exemption is removed once contract 1 lands.
   - A read-only reviewer gains no Write, Edit or shell permission because of
     memory.
8. **Export and cleanup.** Template export, site build and the
   `_workspace`/`.worktrees` cleanup procedures exclude the runtime root.
   - The workspace guidance names the root and its owner.
   - Git exclusion is not a backup.

## Acceptance Criteria

1. Project settings for both providers turn native memory off. A fresh session
   of each, started after the settings are trusted, shows it off.
2. Claude writes a record, Codex reads the same `memory_id`, `revision` and
   body from another worktree, and Claude then sees Codex's revision. These
   are two real provider sessions on one physical store.
3. A stale expected revision, a concurrent quota race, a full database and a
   failed backup each fail explicitly and leave existing records unchanged.
   This is shown with a small test database.
4. Removing a worktree and cleaning `_workspace` leave the store intact, and a
   read-only reviewer can read but not write it.
5. `tool_payload.py` has no native memory exemption, and its tests cover the
   store path rule.
6. One governance owner states the memory rules, and the workspace guidance
   routes to it.
7. The changed gate and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-shared-agent-memory.md)
