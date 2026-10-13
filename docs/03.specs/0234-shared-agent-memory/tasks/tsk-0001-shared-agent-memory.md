---
title: "Shared Agent Memory Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0234-TSK-0001"
parent_ids:
- "SPEC-0234-PLAN-0001"
created: "2026-10-13"
---

# Shared Agent Memory Task

## Objective

Give Claude and Codex one shared memory store in place of separate native
memories, as SPEC-0234 states.

## Inputs and Authorization

- **Request:** the owner asked on 2026-10-13 to proceed with the shared memory
  work (prompt v9 F24, F27, F36), and earlier chose a separate Spec for it.
- **This round's scope:** read-only investigation and this draft package.
- **Not done:** no setting, store, native memory file or user-global
  configuration was changed or read beyond what W1 lists.
- **Baseline:** `main` `b1a6976f4`.
- **Owner decisions:** answered on 2026-10-13 and recorded in the Spec Scope:
  ignored store in the main checkout, native memories left unread, logical
  limits only, the existing backup runbook, project Codex config with trust.

## Work Log

### W1 Starting State

Repository, read on `b1a6976f4`:

- `.claude/settings.json` has the keys `autoMode`, `deniedMcpServers`,
  `hooks`, `outputStyle` and `permissions`. It has no `autoMemoryEnabled`.
- No tracked subagent under `.claude/agents/` or `.agents/roles/` declares
  `memory:`.
- `.codex/` has no `config.toml`.
- `tool_payload.py:20-44` exempts one regular, singly linked `.md` file
  directly in `~/.claude/projects/<slug>/memory/` when that directory is a
  physical directory outside the repository.
  - The slug is computed from the session project root.
  - `_repository_edit` applies the exemption at line 241.
- `.gitignore:111` ignores `.claude/agent-memory-local/`. Neither
  `.workspace-memory/` nor `.agents/memory/` exists.
- `_workspace/repo-support/README.md:58-59` keeps task context in the Task,
  with no governance memory root.
- No governance policy owns memory rules.

Official documentation, read 2026-10-13:

- **Claude Code** (<https://code.claude.com/docs/en/memory>):
  - Auto memory is on by default in local sessions.
  - A project turns it off with `"autoMemoryEnabled": false` in its settings,
    or with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
  - The directory is `~/.claude/projects/<project>/memory/`. The `<project>`
    path is derived from the git repository, so all worktrees share one
    directory.
  - A subagent's own memory, set with its `memory` field, is a separate
    directory.
  - `autoMemoryDirectory` set in project settings follows the workspace trust
    rule for hooks.
- **Codex config reference**
  (<https://learn.chatgpt.com/docs/config-file/config-reference>, redirected
  from developers.openai.com):
  - `features.memories` is off by default.
  - `memories.generate_memories` and `memories.use_memories` both default to
    `true`. `false` stops storing new threads as inputs and stops injecting
    memories.
  - Project config loads only for a trusted project.
  - The page neither lists the memories keys as project-allowed nor lists
    them as ignored. Whether they work in a project `config.toml` is
    NOT_VERIFIED.

Host observations, from this machine only:

- Python 3.12.3 links SQLite 3.45.1.
- Installed tools: Claude Code 2.1.296 and codex-cli 0.162.1.
- The Claude native memory directory for this repository exists. Its
  contents were not read.
- `~/.codex/config.toml` sets no `memories` keys. Only key names were
  searched.

Open findings:

- **Slug may not match.** The documentation derives the memory directory from
  the git repository, while `tool_payload.py` derives the slug from the
  session root. In a session started inside a linked worktree the two may
  differ, so the exemption would not apply. Not reproduced; NOT_VERIFIED.
- **SQLite 3.45.1 and the WAL-reset fix.** The prompt cites the SQLite WAL
  page for a fix in 3.51.3 and backports 3.44.6 and 3.50.7. 3.45.1 is not
  among them. A distribution backport is NOT_VERIFIED, so concurrent writers
  are not accepted on this host yet.

### W2 Governance Owner

`.agents/governance/environment-constraints.md` (1.3.0) section 5 owns the
memory rules: the one store and how worktrees reach it, the CLI as its only
writer with expected-revision updates, native memory off in both providers,
records as context only and never secrets, logical limits with no quota
claim, and the backup step. `_workspace/repo-support/README.md` (1.0.1) routes
agent memory to that section instead of saying there is no memory root.

### W3 Store and CLI

`scripts/operations/agent_memory.py` resolves the store as
`<git common dir parent>/.workspace-memory/memory.sqlite3`, so a linked
worktree writes the main checkout's file; outside a repository, or when the
common directory is not a `.git` directory, it exits 2
`MEMORY_UNAVAILABLE` and creates nothing. The directory is created 0700 and
the file 0600. One `revisions` table holds the Spec envelope
(`schema_version`, `workspace_id`, `memory_id`, `tier`, `revision`, `owner`,
`created_at`, `source_refs`, `eligibility`, `sensitivity`, `body`) with CHECK
constraints on tier, eligibility and sensitivity (`public`, `internal`; no
secret class). Commands: `get`, `history` (at most 50), `list`, `put`,
`set-eligibility`, `usage`, `export`, `backup`, `restore`. `put` and
`set-eligibility` run under `BEGIN IMMEDIATE`; a revision other than the
expected one exits 3 `MEMORY_REVISION_CONFLICT` and writes nothing. The store
runs in WAL mode with a 5 s busy timeout. The CLI has no option that points it
at another store.

### W4 Limits, Failures and Backup

Logical limits, checked inside the write transaction: 16 KiB per revision
body, 10,000 revisions, 32 MiB of body bytes in total. Crossing one exits 4
`MEMORY_CAPACITY_EXCEEDED`; nothing is deleted, summarized or moved. A held
write lock past the timeout exits 5 `MEMORY_STORE_BUSY`, `SQLITE_FULL` exits 6
`MEMORY_STORE_FULL`, and both roll back. A failed passive checkpoint after a
commit is reported as `MEMORY_CHECKPOINT_DEFERRED`; the revision stands.
`backup --output` writes a temporary file with the online backup API, runs
`integrity_check`, sets 0600 and replaces the target atomically; a failure
exits 7 and keeps the previous backup. `restore --input` rebuilds a missing
store only and refuses an existing one. The backup runbook (RUN-0021 1.4.16)
has the backup and restore commands. Adding the file to the
`hyhome-backup.service` Restic snapshot is an infrastructure change and is
`NOT_RUN`.

### W5 Hook Rule and Exclusions

`tool_payload.py` no longer exempts `~/.claude/projects/<slug>/memory/`; such
a path is outside the project root like any other and is refused. An edit
whose target is under `.workspace-memory/` is refused with "the shared memory
store is written only by the memory CLI", so a Write or Edit tool cannot
change the store and a read-only reviewer gains nothing. The earlier
slug-mismatch finding no longer applies. `.gitignore` ignores
`.workspace-memory/`. No tracked procedure runs `git clean` or deletes ignored
files, and `.worktrees/` removal and `_workspace` cleanup do not reach the
main checkout's `.workspace-memory/`. The `export` command prints current
records as JSON.

### W6 Native Memory Settings

`.claude/settings.json` sets `"autoMemoryEnabled": false`; the file is a
tracked native config, not renderer output. `.codex/config.toml` is new and
sets `[memories] generate_memories = false` and `use_memories = false`;
Codex reads it only after the user trusts the project. The provider renderer
reports no drift. Whether either provider honors the setting in a live
session is W8 and `NOT_RUN`. Native memory files were not read or changed.

### W7 Verification

`tests/lib/hooks/test_tool_payload.py` was rewritten first and failed 5 cases
on the old code, then passed (15). `tests/lib/hooks/test_agent_memory.py` (8)
covers private WAL store, stale revisions, the three limits, two concurrent
writers racing for the last room (exactly one wins), a full database, a failed
backup keeping the previous file, restore, and a linked worktree writing the
main checkout's store that survives `git worktree remove`. The leaf
`leaf.local-hook-rule-tests` runs both modules and the agent-governance
selector covers the CLI. Script manifest, workflow contract and manifest tests
(90), the routing suite, provider renderer and governance contract pass. The
retired-token check flagged a W1 sentence, which was reworded.
`test_every_test_module_is_reachable_from_the_full_profile` fails on
`test_opsflow_database_rehearsal` here and on `main` `b1a6976f4`; it is not
part of this change. An independent security review, the changed gate and
`candidate-quality` are `NOT_RUN`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Starting state | 5, 6 | W1 | Read-only file and settings inventory | `b1a6976f4` | PASS | W1 Starting State | - |
| Provider settings | 1 | W1 | Official Claude and Codex documentation | Pages read 2026-10-13 | PASS | W1 Starting State | - |
| Host library | 3 | W1 | Linked SQLite version | This host | PASS | W1 Starting State | - |
| Governance owner | 6 | W2 | Governance contract | Branch | PASS | W2 Governance Owner | - |
| Store and CLI | 2, 3 | W3 | `test_agent_memory` (8) | Branch | PASS | W3 Store and CLI | - |
| Failure handling | 3 | W4 | Stale, limits, race, full, backup failure, restore tests | Branch | PASS | W4 Limits, Failures and Backup | - |
| Hook rule | 4, 5 | W5 | `test_tool_payload` RED (5) then GREEN (15) | Branch | PASS | W5 Hook Rule and Exclusions | - |
| Native settings | 1 | W6 | JSON and TOML parse; provider renderer `--check` | Branch | PASS | W6 Native Memory Settings | - |
| Security review | 7 | W7 | Independent security audit of store and CLI | - | NOT_RUN | W7 Verification | - |
| Gate | 7 | W7 | Changed gate; candidate quality | - | NOT_RUN | W7 Verification | - |
| Native acceptance | 1, 2, 4 | W8 | Two providers, two worktrees, one store | - | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |
| 6 | pending | - | - |
| 7 | pending | - | - |

## Review and Completion

W2 to W6 are implemented on the branch. The security review, gates and the
two-provider acceptance (W8) are open. No criterion is accepted.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
