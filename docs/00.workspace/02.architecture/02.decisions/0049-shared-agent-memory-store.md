---
title: "Shared Agent Memory Store"
version: "1.2.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "architecture"
artifact_id: "ADR-0049"
parent_ids:
- "AD-0027"
created: "2026-10-13"
---

# ADR-0049: Shared Agent Memory Store

## Context

### Problem and Drivers

Claude Code and Codex each keep native memory in their own home directory.
What one provider learns about this repository never reaches the other, and
Claude's native memory sat outside the repository's hook rules through a
special exemption. ADR-0032 decided that no memory and no `.codex/config.toml`
are created for formal symmetry. The prompt v9 request (findings F24, F27 and
F36) asks for one memory both providers share, which is a working need rather
than symmetry.

One store for every worktree and provider. No silent lost update. No claim of
a limit or a concurrency guarantee the host cannot keep. Memory never becomes
a second owner of Task state or governance rules.

#### Sources

- [AD-0027](../01.descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0032](0032-canonical-agent-governance-home.md)
- [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md)
- SPEC-0236

### Decision Scope

This decision covers the memory store shared by Claude Code and Codex for this repository and all of its worktrees. Memory is context only and never becomes a second owner of Task state or governance rules.

## Options

### Considered Options

- Keep separate native memories: rejected; knowledge stays split by provider.
- A store per worktree: rejected; a removed worktree loses its memory.
- WAL with a single-writer rule: rejected; nothing enforces one writer, and
  two providers writing is the purpose.
- A remote database: rejected; it adds a service for a local, small store.

### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep separate native memories | The ADR records no benefit for this option. | Knowledge stays split by provider. | Rejected; knowledge stays split by provider. |
| A store per worktree | The ADR records no benefit for this option. | A removed worktree loses its memory. | Rejected; a removed worktree loses its memory. |
| WAL with a single-writer rule | The ADR records no benefit for this option. | Nothing enforces one writer, and two providers writing is the purpose. | Rejected; nothing enforces one writer, and two providers writing is the purpose. |
| A remote database | The ADR records no benefit for this option. | It adds a service for a local, small store. | Rejected; it adds a service for a local, small store. |
| One shared SQLite store `.workspace-memory/memory.sqlite3` written only through `scripts/operations/agent_memory.py`, with native provider memory off (chosen) | Both providers read and write the same records through one CLI, and a removed worktree keeps them. | The store is not in Git, so its backup is a runbook step and Restic coverage is deferred; native memory written before this decision stops loading unless copied into the store. | Chosen; it gives one store for every worktree and provider with no silent lost update, using a rollback journal because the host's SQLite lacks the WAL-reset fix. |

Each rejected option is rejected for the reason stated in its entry above: separate native memories keep knowledge split by provider, a per-worktree store loses memory with a removed worktree, WAL with a single-writer rule has no enforced writer, and a remote database adds a service for a local, small store.

## Decision

### Chosen Option

1. Claude and Codex share one SQLite store,
   `.workspace-memory/memory.sqlite3` in the main checkout. Git ignores it,
   and every linked worktree reaches it through the Git common directory.
2. Native provider memory is off: `autoMemoryEnabled` is `false` in
   `.claude/settings.json`, and `.codex/config.toml` turns Codex memory
   generation and use off. Native memory files are not deleted.
3. `scripts/operations/agent_memory.py` is the only sanctioned writer. Every
   update names the revision it expects, and a stale one changes nothing.
   Edit tools are refused on the store; shell access is a rule, not a guard.
4. The store uses a rollback journal, not WAL, because the host's SQLite
   lacks the WAL-reset fix.
5. Limits are logical, enforced by the CLI, and never presented as a quota.
6. A memory record is context only. What a record may not hold is stated
   once, in `environment-constraints.md` section 5.

### Authority and Effect

Decided by the owner, @buenhyden, who decided on 2026-10-13 to accept it; status `accepted`, set in change #450 (`40f194e99`) as the Follow-up records. Effective from 2026-10-13.

#### Supersession

This narrows ADR-0032's rule against creating memory or `.codex/config.toml`
for these two items only. The rest of that rule, on plugins, servers and
extra common directories, stays in force.

## Consequences

### Impacts

Both providers read and write the same records through one CLI, and a removed
worktree keeps them. The store is not in Git and is excluded from backups.
Native memory written before this decision stops
loading unless it is copied into the store.

### Follow-up

On 2026-11-18 the owner, @buenhyden, directed that the store be excluded from
backups and its backup code removed; the Impacts sentence on backups is
amended in place to match.

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

Proposed on 2026-10-13 from the owner's decisions. SPEC-0236 implements and
verifies it. The owner decided on 2026-10-13 to accept it ("Accept both", for
ADR-0048 and ADR-0049). A new ADR must enter the repository as `proposed`, so
the status changed to `accepted` in the first change after SPEC-0236 merged
(#450, `40f194e99`).

#### Compliance

The `environment-constraints.md` section 5 policy owns the rules. The memory
CLI tests and the edit hook tests check the store contract; live two-provider
acceptance is separate evidence.
