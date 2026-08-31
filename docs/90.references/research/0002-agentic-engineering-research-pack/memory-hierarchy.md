---
status: active
artifact_id: reference:agentic-engineering-research:memory-hierarchy
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Reference: Agent Memory Hierarchy and Lifecycle

## Overview

The workspace has one bounded current-state handoff, eight durable advisory
notes, and one append-preserved historical navigation file, all governed by a
README. Only the current handoff has typed size, section, Task-state, Git
ancestry, timestamp, and forbidden-material checks. Promotion, durable-note
retention, domain partition, eviction/deletion, and archival remain mostly
human procedures rather than a closed lifecycle contract.

Measurements below were re-derived from tracked files at commit
`7a88efc1adbc061a121d565c7906e41591ddc3b7` (2026-08-11), which adds one
durable note (`ignored-sdd-scratch-deletion.md`) and a shorter `current.md`
relative to the Task 4 baseline `1cd9bc2830db710585348e8ef38b0318cc7f5a10`;
that baseline remains valid historical provenance for the earlier count. No
session transcript, raw interaction, ignored file, provider-private memory, or
secret value was read or recorded.

A further re-measurement at repository commit
`ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` (2026-08-14) finds the same 11
tracked files now totaling 2,308 lines and 1,234,111 bytes (+16 lines,
+1,189 bytes). `git log 7a88efc1a..ece3eda9` shows exactly two memory files
changed: `current.md` (replaced in place, +17 lines) and
`ignored-sdd-scratch-deletion.md` (a small in-place correction) — in-place
replacement consistent with the README's contract, not uncontrolled growth.
This pass also reopens the current Claude Code and Codex configuration
references to resolve mechanics this leaf previously described only
qualitatively, and surveys current external research on agent memory
architecture for comparison.

## Purpose

Satisfy REQ-30 by covering short-term, long-term, and domain memory plus
promotion, retrieval, retention, eviction/deletion, archival, partition,
privacy, size/freshness, and provider-native boundaries.

## Repository Role

This Stage 90 reference does not become memory policy. The active contract
remains `docs/00.agent-governance/memory/README.md`; current-state validation
remains in `agent_governance_contract.py`; durable evidence remains in its
canonical Stage 03/04/05 owner.

## Scope

### In scope

- Tracked memory files, their metadata/size, retrieval routes, and validators.
- Full repository memory lifecycle and explicit missing controls.
- Public Claude and Codex memory/configuration capability boundaries.

### Out of scope

- Raw conversations, logs, shell history, ignored/private files, provider-global memory, or credentials.
- Changing Memory files, bounds, hooks, schemas, retention, or provider settings.
- Claiming provider-native generation/retrieval happened in this workspace.

## Definitions / Facts

### Safe tracked measurement

The exact tracked measurement was:

```bash
git ls-files 'docs/00.agent-governance/memory/*.md' | sort | xargs wc -l -c
```

It found 11 Markdown files, 2,292 lines, and 1,232,922 bytes:

| Tier / owner            | Files | Lines |     Bytes | Current rule                                                           |
| ----------------------- | ----: | ----: | --------: | ---------------------------------------------------------------------- |
| Contract README         |     1 |   122 |     5,675 | Defines advisory authority, privacy, retrieval, and maintenance.       |
| Bounded current handoff |     1 |    59 |     2,493 | Exactly seven `##` sections; maximum 400 lines / 32 KiB.               |
| Durable advisory notes  |     8 |   727 |    31,234 | Template-based notes; no aggregate bound or typed retention field.     |
| Historical navigation   |     1 | 1,384 | 1,193,520 | Append-preserved; navigation only, not current state or active policy. |

The current handoff is about 8% of its byte bound and 15% of its line bound.
The historical file is intentionally outside that bound and must not be loaded
or described as the current handoff.

Re-running the identical command at commit `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`
(2026-08-14) gives:

| Tier / owner            | Files | Lines |     Bytes | Change from 2026-08-11                                                                                  |
| ----------------------- | ----: | ----: | --------: | ------------------------------------------------------------------------------------------------------- |
| Contract README         |     1 |   122 |     5,675 | Unchanged.                                                                                              |
| Bounded current handoff |     1 |    76 |     3,689 | +17 lines / +1,196 bytes, in place.                                                                     |
| Durable advisory notes  |     8 |   726 |    31,227 | -1 line / -7 bytes (one note edit within `ignored-sdd-scratch-deletion.md`; file count unchanged at 8). |
| Historical navigation   |     1 | 1,384 | 1,193,520 | Unchanged.                                                                                              |

`current.md` is now 19% of its line bound and 11% of its byte bound —
still bounded, and the seven-heading envelope from the prior measurement is
unchanged (verified by direct read: `Current objective`, `Approved
decisions`, `Active boundary`, `Verified state`, `Blockers and unverified
facts`, `Evidence links`, `Next handoff`). The durable-note count stayed at
8 files; only `ignored-sdd-scratch-deletion.md` changed content within its
existing file.

### Current-memory validator: exact bounds and forbidden-material patterns

`scripts/lib/agent_governance/agent_governance_contract.py` implements the current-
handoff checks this leaf's lifecycle matrix references only qualitatively.
Direct read of the module resolves the exact constants and rules:

| Check                | Exact rule                                                                                                                                                                                                                  | Source                                                                    |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Byte bound           | `CURRENT_MEMORY_MAX_BYTES = 32 * 1024` (32,768 bytes)                                                                                                                                                                       | `agent_governance_contract.py:57`                                         |
| Line bound           | `CURRENT_MEMORY_MAX_LINES = 400`                                                                                                                                                                                            | `agent_governance_contract.py:58`                                         |
| Section envelope     | Exactly the ordered 7-tuple `Current objective`, `Approved decisions`, `Active boundary`, `Verified state`, `Blockers and unverified facts`, `Evidence links`, `Next handoff` — any mismatch is `section-envelope-mismatch` | `agent_governance_contract.py:59-67`                                      |
| Required labels      | Exactly one value each for `Current task`, `Verified commit`, `Verified at` — zero or multiple is `label-cardinality-mismatch`                                                                                              | `agent_governance_contract.py:79`                                         |
| Task-path validity   | `Current task` must be a safe repository path starting with `docs/04.execution/tasks/` and ending in `.md`                                                                                                                  | `agent_governance_contract.py:80`, enforced in `_validate_current_memory` |
| Task-state freshness | The named Task's own frontmatter `status` must be `draft` or `active`, or the check fails as `AGC-MEMORY-STALE-STATE` / `task-state-stale`                                                                                  | validator logic around the task-path check                                |
| Commit format        | `Verified commit` must match `[0-9a-f]{40}` (full lowercase Git SHA)                                                                                                                                                        | validator logic                                                           |
| Commit ancestry      | The verified commit must resolve as an ancestor of `HEAD` via `_git_commit_is_ancestor`, or the check fails as `verified-commit-stale`                                                                                      | same                                                                      |
| Timestamp validity   | `Verified at` must parse as a timezone-aware ISO 8601 value; naive timestamps fail as `invalid-verification-time`                                                                                                           | same                                                                      |

Forbidden material is enforced by 7 distinct regular-expression categories
applied to the Markdown body (frontmatter stripped first), any one of which
trips `AGC-MEMORY-FORBIDDEN-MATERIAL` / `forbidden-material-present`:

1. Fenced or indented code blocks (three or more `` ` `` or `~` at line
   start) — prevents pasted transcripts or logs disguised as code.
2. The words `credential(s)`, `token(s)`, `secret(s)` in any case.
3. Auth/authorization config file paths (for example
   `~/.config/auth.json`) or the phrase "auth files".
4. `.bash_history`, `.zsh_history`, `.fish_history`, or the phrase "shell
   history".
5. Phrases naming provider-global or private provider state, or literal
   `~/.claude`, `~/.codex`, `~/.gemini` paths.
6. The phrase "policy body", or modal/normative language such as "must",
   "shall", "always", "never", "required", "forbidden" — this is what keeps
   `current.md` a value-free state record rather than a restated policy.
7. Raw command/output markers: lines starting with a shell prompt (`$` or
   `>`) or labels like `command:`, `stdout:`, `stderr:`, `traceback:`,
   `command log:`, `raw output:`, `exit code:`.

This is materially more precise than "prohibits transcripts, raw output/logs,
credentials, tokens, shell history, personal notes, and private provider
state": categories 1 and 7 target command/output material specifically,
category 6 is the only one that also polices _policy-like prose_ rather than
sensitive data, and none of the 7 categories apply outside `current.md` —
the 8 durable notes and the historical file have no automated check.

### Full lifecycle matrix

| Lifecycle concern | Required meaning                                                        | Tracked implementation                                                                                                 | Status / gap                                                                       |
| ----------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Short-term memory | Bounded state needed to resume the active unit                          | `memory/current.md`, replaced in place and linked to active Task/commit/time                                           | Implemented for shared handoff; raw session memory is deliberately excluded.       |
| Long-term memory  | Durable reusable learning after the task                                | Eight template-based advisory notes plus Stage 04 evidence links                                                       | Partial; values and continued usefulness are not typed/validated.                  |
| Domain memory     | Durable knowledge partitioned by scope/subject                          | Free-text tags, retrieval keywords, and `Applies To` lines                                                             | Missing typed partition, owner enum, and per-domain route.                         |
| Promotion         | Move a verified reusable finding from active work to durable owner      | Human cues in README; durable facts first belong in Stage 04 or active policy owners                                   | Partial; no threshold, duplicate check, or validator-enforced promotion decision.  |
| Retrieval         | Load only relevant current/domain facts                                 | Bootstrap loads README/current; targeted `rg` retrieves at most relevant notes; corroboration required                 | Implemented as procedure, not relevance scoring.                                   |
| Retention         | Define how long/usefully a durable note remains                         | Review when relevant; remove duplicates; follow live state on conflict                                                 | Partial; no review-by/TTL/last-used field or stale-note gate.                      |
| Eviction/deletion | Remove obsolete, duplicate, sensitive, or invalid memory safely         | Replace current in place; remove duplicates; provider-private/raw material prohibited                                  | Partial; no durable-note deletion manifest, consumer proof, or automated eviction. |
| Archive           | Preserve provenance after memory is no longer active retrieval material | Archive stale/superseded notes only after durable evidence and Git provenance are confirmed                            | Procedural only; no archive location/profile is defined for Memory notes.          |
| Partition         | Prevent unrelated domains/users/repos from contaminating retrieval      | Repository-local tracked directory; provider-private memory excluded                                                   | Partial; repo boundary exists, domain and identity partitions are untyped.         |
| Privacy           | Prevent sensitive/raw material from becoming shared memory              | Prohibits transcripts, raw output/logs, credentials, tokens, shell history, personal notes, and private provider state | Strong tracked rule; enforcement is strongest only on `current.md`.                |
| Size              | Bound high-priority index/context                                       | `current.md` 32 KiB/400 lines; exact provider-native limits are external                                               | Implemented for current only; durable/historical tiers unbounded.                  |
| Freshness         | Show that a fact still matches live tracked state                       | Current Task active/draft, commit ancestor, timestamp; notes rely on manual verification metadata                      | Implemented for current; partial/missing for durable and historical tiers.         |

### Provider-native boundaries

| Concern              | Claude Code public capability                                                                                                | Codex public capability                                                                                                    | Local adoption/evidence boundary                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Cross-session memory | Auto memory writes a per-repository, machine-local `MEMORY.md` plus on-demand topic files.                                   | Config reference exposes generation, consolidation, use/injection, age, idle-time, unused-time, and raw-memory caps.       | No provider-private memory was inspected; tracked repo config does not prove either mechanism ran. |
| Partition            | Claude shares one project memory across worktrees; subagent memory is separate.                                              | Public config describes thread/global extraction controls; no local domain taxonomy is inferred.                           | Repository Memory remains the only shared tracked handoff.                                         |
| Size/retrieval       | First 200 lines or 25 KiB of `MEMORY.md` loads; topic files are on demand.                                                   | Auto-compaction has a configurable token threshold; memory injection can be disabled.                                      | Provider limits do not replace the 32 KiB/400-line repository contract.                            |
| Retention/freshness  | Near-limit guidance merges/drops stale entries; frontmatter may receive a `modified` timestamp; users can edit/delete files. | Config exposes maximum rollout age, unused days, per-startup candidates, and consolidation cap.                            | These are external configurable capabilities, not local policy or execution evidence.              |
| Privacy control      | Machine-local store, project toggle, editable/deleteable plain Markdown.                                                     | `disable_on_external_context` can exclude threads using MCP/web/tool search; generation and use are separately toggleable. | Public settings do not prove the active account's privacy configuration or deletion outcome.       |
| Enforcement          | Claude explicitly calls instructions/memory context, not enforced configuration.                                             | Config values describe product behavior, not this repository's policy hierarchy.                                           | Stage 00 and canonical stage artifacts always outrank provider memory.                             |

The Codex config reference is particularly important because it separates
`generate_memories` from `use_memories`: stopping new extraction and stopping
future injection are different controls. Neither establishes deletion of
already generated material. Likewise, age/unused limits control eligibility
for generation/consolidation, not a repository retention policy.

### Claude Code subagent memory (exact mechanics, 2026-08-14 reopen)

The 2026-08-14 reopen of the Claude Code subagents reference resolves a
mechanism this leaf's "Partition" row previously only summarized as
"subagent memory is separate." A subagent's `memory` frontmatter field
enables a persistent directory scoped one of three ways:

| Scope     | Exact path                                    | Use when                                                                        |
| --------- | --------------------------------------------- | ------------------------------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | The subagent should remember learnings across all projects.                     |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | The subagent's knowledge is project-specific and shareable via version control. |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | The subagent's knowledge is project-specific but should not be checked in.      |

When enabled, the subagent's system prompt is extended with memory
read/write instructions and the first 200 lines or 25 KiB of its own
`MEMORY.md` (whichever comes first), and Read/Write/Edit tools are
auto-enabled for that directory. This is a per-agent instance of the same
200-line/25 KiB main auto-memory limit documented above, not a new number.
Subagent memory depends on `autoMemoryEnabled`: when auto memory is off
(`autoMemoryEnabled` setting or `CLAUDE_CODE_DISABLE_AUTO_MEMORY`), the
`memory` field has no effect and the subagent launches without the memory
instructions or tool access.

Two size regimes now coexist and must not be conflated: this repository's
`current.md` bound (400 lines / 32 KiB, enforced by
`agent_governance_contract.py`) and Claude's native `MEMORY.md` bound (200
lines / 25 KiB, enforced by the Claude Code client, per-project or
per-subagent). Neither bound is derived from the other; the repository
bound is roughly double the provider bound in both dimensions, by
repository policy choice rather than by inheriting the provider default.
`project`-scoped subagent memory (`.claude/agent-memory/<name>/`) is a
tracked-repository-adjacent location this repository's Memory contract does
not currently govern, mention, or exclude — it is neither the
`docs/00.agent-governance/memory/` handoff nor explicitly out of scope for
it, which is named as a gap below.

### Codex `memories.*` exact configuration fields (2026-08-14 reopen)

The 2026-08-14 reopen of the Codex configuration reference resolves the
exact field names and defaults this leaf's "Retention/freshness" row
previously summarized only as "age, idle-time, unused-time, and raw-memory
caps":

| Field                                  | Type    | Default | Clamp range                                                                                            |
| -------------------------------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------ |
| `memories.generate_memories`           | boolean | `true`  | —                                                                                                      |
| `memories.use_memories`                | boolean | `true`  | —                                                                                                      |
| `memories.consolidation_model`         | string  | (unset) | Optional model override for global memory consolidation.                                               |
| `memories.max_rollout_age_days`        | number  | `30`    | Clamped to 0-90.                                                                                       |
| `memories.min_rollout_idle_hours`      | number  | `6`     | Clamped to 1-48.                                                                                       |
| `memories.max_unused_days`             | number  | `30`    | Clamped to 0-365.                                                                                      |
| `memories.disable_on_external_context` | boolean | `false` | When `true`, excludes threads using MCP tool calls, web search, or tool search from memory generation. |

`generate_memories` and `use_memories` are confirmed as independently
toggleable (matching the leaf's prior claim), and none of these seven
fields establishes deletion of already-generated material — they only
control eligibility for future generation, consolidation, or injection.
This repository's tracked configuration does not set any `memories.*`
field, so all seven remain at documented defaults for any Codex session
running against this workspace, unobserved by any tracked file.

### External research on agent memory architecture (comparative, not adopted)

A 2026-08-14 survey of current academic work on LLM agent memory (External
mutable summary; individual papers below are External fixed where
versioned) situates this repository's approach in a broader taxonomy. A 2026
taxonomy paper proposes a 3-axis framework — temporal scope, representational
substrate, control policy — and identifies five mechanism families:
context-resident compression, retrieval-augmented stores, reflective
self-improvement, hierarchical virtual context, and policy-learned
management. This repository's Memory contract implements exactly one family
in a strict form: context-resident, human-curated notes with no automated
retrieval scoring, reflective loop, hierarchical compression, or learned
promotion/eviction policy — retrieval is `rg` plus human corroboration (see
"Retrieval" above). That is a legitimate design point for a governance-gated
repository that prizes reviewability and provenance over automated recall;
this leaf does not recommend adopting any of the other four families, only
names the comparison for a future Stage 03 decision.

### Required future lifecycle contract

A future Stage 03 memory-governance specification should define a typed domain
enum and owner; promotion trigger and evidence; retrieval index/query and
corroboration; last-verified/review-by/last-used metadata; retention and legal
hold exceptions; eviction versus deletion semantics; deletion consumer and
provenance proof; an archive/tombstone route; per-domain size/freshness bounds;
privacy classification and redaction; provider export/sync prohibition; and a
validator plus migration plan. Until then, durable notes remain advisory and
human-curated.

Two additional gaps surfaced by this 2026-08-14 pass belong in that future
specification: first, `.claude/agent-memory/<name>/` (Claude's
`project`-scoped subagent memory) is a real, provider-native, project-
committable location that this repository's Memory contract neither
governs nor excludes today — a future spec should state explicitly whether
subagent-memory directories are in scope, out of scope, or require their own
governance. Second, the 7-category forbidden-material check enforced by
`agent_governance_contract.py` applies only to `current.md`; the 8 durable
notes and `progress.md` have no equivalent automated check today, so a
credential or raw-log fragment pasted into a durable note would not be
caught by any tracked validator, only by human review at note-creation time.

### Provider mechanics and local hierarchy

The 2026-08-14 retained Claude observation documents three subagent-memory
partitions: user, project, and local. It also states that the setting is gated
by Claude's auto-memory control and injects memory instructions/content into a
subagent when enabled. These are provider mechanics, not local policy and not
evidence that any such directory was present or read.

The retained Codex reference distinguishes generation from later use. Thus,
disabling generation does not demonstrate removal of material already made,
and disabling use does not itself establish deletion. The retained settings
also describe age/idle/unused limits as configuration behavior; absent tracked
configuration is not evidence that defaults applied to any real session.

For local reasoning, short/long time horizon is separate from domain partition:
a current Task is short-lived execution evidence; a durable canonical artifact
owns durable decisions; Git history is recovery evidence. Provider memory may
be helpful advisory context but cannot become policy. The proposed process
requires sanitization and provenance before retrieval, scoped partitioning,
expiry review, and deletion proof; it is explicitly not an executed workflow.

### Proposed domain partition and lifecycle boundary

This is ADVISORY design, not an adopted memory policy. The time axis answers
how long evidence is useful: short-session working context is transient,
whereas long-lived knowledge belongs in a durable canonical artifact with Git
history as recovery evidence. The domain axis answers what the evidence is
about and is orthogonal to time: for example, an architecture decision belongs
to its ADR/Spec owner, an infrastructure compatibility observation to its
infra owner, and an operations incident pattern to its incident owner. A
provider's `user`/`project`/`local` storage scopes are a third, separate
storage-partition axis; they neither choose a domain owner nor confer policy
authority.

| Proposed domain | Evidence owner and provenance | Allowed retrieval boundary | Staleness, conflict, expiry, and deletion condition |
| --- | --- | --- | --- |
| architecture | Architecture owner; source artifact and revision are recorded with the decision. | Retrieve the canonical ADR/Spec, not provider memory as authority. | Re-review on architecture change; conflicts defer to the canonical artifact; expiry/deletion needs approved policy and a recoverable proof. |
| infra | `infra-implementer`; source target, safe revision, and value-free observation record are required. | Retrieve only approved, sanitized target evidence. | Revalidate when target/configuration changes; conflicting observations stop for owner review; retention/deletion needs approved policy. |
| ops | `incident-responder`; provenance is the owned incident/runbook record. | Retrieve sanitized reusable patterns, never private provider stores. | Review after incident resolution or supersession; conflicts defer to the incident owner; deletion requires approved lifecycle evidence. |

No row above authorizes capture, retention, retrieval, expiry, or deletion. A
future typed policy must specify the owner, provenance fields, retrieval
authorization, review period, conflict resolution, and deletion evidence
before this process can be treated as an operating control.

## Scope Implications

| Scope          | Application and disposition                                                                                                                                                                                                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Owns memory authority, bootstrap/retrieval, provider boundaries, and current validator; no provider memory may override it.                                                                                                                                                                                                  |
| `architecture` | Durable architecture decisions belong in ADR/Spec owners; Memory may link a reusable pitfall but cannot replace them.                                                                                                                                                                                                        |
| `backend`      | No current surface; future backend-domain memory requires an approved domain owner and privacy/retention contract.                                                                                                                                                                                                           |
| `common`       | Reusable cross-scope findings need one canonical note, duplicate control, and corroboration before use.                                                                                                                                                                                                                      |
| `docs`         | Owns current/durable note stewardship, template use, bounds, links, and any future archive route.                                                                                                                                                                                                                            |
| `entry`        | Gateway operational facts belong in tracked config/runbooks/incidents; secrets/certificates/log payloads never enter Memory.                                                                                                                                                                                                 |
| `frontend`     | Current fixture learnings remain QA-owned unless a product surface creates a domain route.                                                                                                                                                                                                                                   |
| `infra`        | Runtime state, raw logs, secret values, backups, and provider-local files stay outside shared Memory; link value-free evidence only.                                                                                                                                                                                         |
| `meta`         | A future typed domain/freshness/retention schema and validator route through docs/meta governance.                                                                                                                                                                                                                           |
| `mobile`       | Not applicable today; future device/user data needs explicit privacy, deletion, and partition controls.                                                                                                                                                                                                                      |
| `ops`          | Incident chronology/outcomes stay in Stage 05; Memory may retain only reusable, sanitized patterns linked to the owner.                                                                                                                                                                                                      |
| `product`      | Product decisions remain in requirements/approval artifacts; preferences or provider memory cannot become stakeholder intent.                                                                                                                                                                                                |
| `qa`           | Validate bounds, section envelope, ancestry, prohibited material, retrieval fixtures, and migration/deletion behavior.                                                                                                                                                                                                       |
| `security`     | Own privacy classification, redaction, deletion proof, provider-memory boundaries, and prompt-injection resistance; the 7-category forbidden-material regex set (see "Current-memory validator" above) is the only automated enforcement, and it covers `current.md` only, not durable notes or subagent-memory directories. |

## Sources

| Source                                                                                                          | Accessed                  | Class                    | Verification state                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------- | ------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| Governance Memory contract (retired path: `../../../00.agent-governance/memory/README.md`)                                     | 2026-08-11                | Workspace tracked        | Direct owner for advisory authority, privacy, retrieval, replacement, retention, and archive cues.                                 |
| Current project memory (retired path: `../../../00.agent-governance/memory/current.md`)                                        | 2026-08-11                | Workspace tracked        | Re-read at commit `7a88efc1a`; still seven headings, now 59 lines/2,493 bytes; no raw/private data.                                |
| Memory stewardship function (retired path: `../../../00.agent-governance/agents/functions/project-memory-stewardship.md`)      | 2026-08-11                | Workspace tracked        | 32 KiB/400-line/seven-section/evidence gates; unchanged on re-read.                                                                |
| [Current-memory validator](../../../../scripts/lib/agent_governance/agent_governance_contract.py)                         | 2026-08-11                | Workspace tracked        | Bounds, sections, Task state, ancestry, timestamps, and forbidden-material checks; unchanged on re-read.                           |
| [Claude instructions and auto memory](https://code.claude.com/docs/en/memory)                                   | 2026-08-11                | External mutable         | HTTP 200; public project memory, partition, size, freshness, edit/delete, and context boundary confirmed unchanged.                |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)                    | 2026-08-11                | External mutable         | HTTP 200; public `memories.*` generation/use/consolidation/age/privacy controls and compaction fields confirmed unchanged.         |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                     | 2026-08-08                | Workspace stale/advisory | Built from `f8a72211`; not used for counts or lifecycle proof.                                                                     |
| Current project memory (retired path: `../../../00.agent-governance/memory/current.md`)                                        | 2026-08-14                | Workspace tracked        | Re-read at commit `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`; still seven headings, now 76 lines/3,689 bytes; no raw/private data. |
| Memory directory listing (retired path: `../../../00.agent-governance/memory/`)                                                | 2026-08-14                | Workspace tracked        | Direct `git ls-files` + `wc -l -c` re-run; 11 files, 2,308 lines, 1,234,111 bytes at HEAD.                                         |
| [Current-memory validator](../../../../scripts/lib/agent_governance/agent_governance_contract.py)                         | 2026-08-14                | Workspace tracked        | Direct read of lines 57-102 (bounds, sections, labels, forbidden-pattern regexes) and surrounding validation logic.                |
| [Claude Code subagents reference](https://code.claude.com/docs/en/sub-agents)                                   | 2026-08-14T13:40:00+09:00 | External mutable         | HTTP 200; exact `memory` frontmatter scopes, paths, 200-line/25 KiB limit, `autoMemoryEnabled` dependency.                         |
| [Claude instructions and auto memory](https://code.claude.com/docs/en/memory)                                   | 2026-08-14T13:40:00+09:00 | External mutable         | Re-read; HTTP 200; confirms 200-line/25 KiB `MEMORY.md` limit and machine-local storage, unchanged.                                |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)                    | 2026-08-14T13:40:00+09:00 | External mutable         | Re-read; HTTP 200; exact `memories.*` field names, types, defaults, and clamp ranges.                                              |
| [Memory in the Age of AI Agents: a Survey (paper list)](https://github.com/Shichun-Liu/Agent-Memory-Paper-List) | 2026-08-14                | External mutable         | Curated paper index; source for the 5-mechanism-family comparison, not adopted as policy.                                          |
| [A Survey of Context Engineering for Large Language Models](https://arxiv.org/pdf/2507.13334)                   | 2026-08-14                | External fixed           | Versioned arXiv preprint; source of the temporal-scope/substrate/control-policy taxonomy used for comparison.                      |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | `workflow-supervisor` keeps Task evidence distinct from advisory memory. | Inspect Task and canonical-owner links. | No provider memory read. |
| architecture | applies | Architecture owner keeps durable decisions in their canonical artifact. | Review ADR/Spec ownership when approved. | No memory replaces a decision. |
| common | applies | `code-reviewer` checks provenance before reusable guidance is relied upon. | Review source binding. | Retrieval behavior unobserved. |
| docs | applies | `doc-writer` records the proposed lifecycle without creating memory policy. | Inspect this leaf and owner path. | No memory files mutated. |
| infra | applies | `infra-implementer` assesses storage, retention, and concrete machine-local targets before adoption. | Review an approved target-specific design. | Private stores untouched. |
| ops | applies | `incident-responder` keeps operational chronology in its owned record. | Inspect an incident record when applicable. | No incident memory imported. |
| qa | applies | `qa-engineer` would verify expiry/deletion evidence for an adopted process. | Require a typed test plan. | No lifecycle process executed. |
| security | applies | `security-auditor` reviews sanitization, partition, and deletion-proof design. | Review approved policy/evidence. | No private or user data accessed. |

## Maintenance

Rerun the tracked `wc` derivation and inspect only safe metadata when Memory
files, the current profile, bootstrap route, provider memory docs, or validator
changes. Never inspect provider-private stores merely to refresh this leaf.

## Related Documents

- [Loop engineering](./loop-engineering.md)
- [Agent instructions](./agent-instructions-vibe-coding.md)
- [Provider implementation comparison](./provider-implementation-comparison.md)
- [Scope application matrix](./scope-application-matrix.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
