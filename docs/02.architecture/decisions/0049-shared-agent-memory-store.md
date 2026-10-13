---
title: "Shared Agent Memory Store"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "architecture"
artifact_id: "ADR-0049"
parent_ids:
- "AD-0027"
created: "2026-10-13"
---

# ADR-0049: Shared Agent Memory Store

## Context

Claude Code and Codex each keep native memory in their own home directory.
What one provider learns about this repository never reaches the other, and
Claude's native memory sat outside the repository's hook rules through a
special exemption. ADR-0032 decided that no memory and no `.codex/config.toml`
are created for formal symmetry. The prompt v9 request (findings F24, F27 and
F36) asks for one memory both providers share, which is a working need rather
than symmetry.

### Decision Drivers

One store for every worktree and provider. No silent lost update. No claim of
a limit or a concurrency guarantee the host cannot keep. Memory never becomes
a second owner of Task state or governance rules.

## Decision

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

This narrows ADR-0032's rule against creating memory or `.codex/config.toml`
for these two items only. The rest of that rule, on plugins, servers and
extra common directories, stays in force.

## Alternatives

### Options Considered

- Keep separate native memories: rejected; knowledge stays split by provider.
- A store per worktree: rejected; a removed worktree loses its memory.
- WAL with a single-writer rule: rejected; nothing enforces one writer, and
  two providers writing is the purpose.
- A remote database: rejected; it adds a service for a local, small store.

## Consequences

Both providers read and write the same records through one CLI, and a removed
worktree keeps them. The store is not in Git, so its backup is a runbook step;
Restic coverage is deferred. Native memory written before this decision stops
loading unless it is copied into the store.

### Compliance

The `environment-constraints.md` section 5 policy owns the rules. The memory
CLI tests and the edit hook tests check the store contract; live two-provider
acceptance is separate evidence.

### Follow-up

Proposed on 2026-10-13 from the owner's decisions. SPEC-0234 implements and
verifies it. The owner decided on 2026-10-13 to accept it ("Accept both", for
ADR-0048 and ADR-0049). A new ADR must enter the repository as `proposed`, so
the status changes to `accepted` in the first change after SPEC-0234 merges.

## Related Documents

- [AD-0027](../descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0032](0032-canonical-agent-governance-home.md)
- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [SPEC-0234](../../03.specs/0234-shared-agent-memory/spec.md)
