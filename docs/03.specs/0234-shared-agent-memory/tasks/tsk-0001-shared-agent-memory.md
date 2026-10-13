---
title: "Shared Agent Memory Task"
version: "0.1.0"
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
- The Claude project memory directory for this repository exists. Its
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Starting state | 5, 6 | W1 | Read-only file and settings inventory | `b1a6976f4` | PASS | W1 Starting State | - |
| Provider settings | 1 | W1 | Official Claude and Codex documentation | Pages read 2026-10-13 | PASS | W1 Starting State | - |
| Host library | 3 | W1 | Linked SQLite version | This host | PASS | W1 Starting State | - |
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

The owner decisions in the Spec are open, and no implementation unit has
started. No criterion is accepted.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
