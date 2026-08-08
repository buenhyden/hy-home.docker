---
status: draft
artifact_id: reference:agentic-engineering-research:memory-hierarchy
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Agent Memory Hierarchy and Lifecycle

## Overview

The workspace has one bounded current-state handoff, seven durable advisory
notes, and one append-preserved historical navigation file, all governed by a
README. Only the current handoff has typed size, section, Task-state, Git
ancestry, timestamp, and forbidden-material checks. Promotion, durable-note
retention, domain partition, eviction/deletion, and archival remain mostly
human procedures rather than a closed lifecycle contract.

Measurements below use tracked files only at Task 4 baseline
`1cd9bc2830db710585348e8ef38b0318cc7f5a10`. No session transcript, raw
interaction, ignored file, provider-private memory, or secret value was read or
recorded.

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

It found 10 Markdown files, 2,277 lines, and 1,233,871 bytes:

| Tier / owner | Files | Lines | Bytes | Current rule |
| --- | ---: | ---: | ---: | --- |
| Contract README | 1 | 122 | 5,675 | Defines advisory authority, privacy, retrieval, and maintenance. |
| Bounded current handoff | 1 | 134 | 7,743 | Exactly seven `##` sections; maximum 400 lines / 32 KiB. |
| Durable advisory notes | 7 | 637 | 26,933 | Template-based notes; no aggregate bound or typed retention field. |
| Historical navigation | 1 | 1,384 | 1,193,520 | Append-preserved; navigation only, not current state or active policy. |

The current handoff is about 24% of its byte bound and 34% of its line bound.
The historical file is intentionally outside that bound and must not be loaded
or described as the current handoff.

### Full lifecycle matrix

| Lifecycle concern | Required meaning | Tracked implementation | Status / gap |
| --- | --- | --- | --- |
| Short-term memory | Bounded state needed to resume the active unit | `memory/current.md`, replaced in place and linked to active Task/commit/time | Implemented for shared handoff; raw session memory is deliberately excluded. |
| Long-term memory | Durable reusable learning after the task | Seven template-based advisory notes plus Stage 04 evidence links | Partial; values and continued usefulness are not typed/validated. |
| Domain memory | Durable knowledge partitioned by scope/subject | Free-text tags, retrieval keywords, and `Applies To` lines | Missing typed partition, owner enum, and per-domain route. |
| Promotion | Move a verified reusable finding from active work to durable owner | Human cues in README; durable facts first belong in Stage 04 or active policy owners | Partial; no threshold, duplicate check, or validator-enforced promotion decision. |
| Retrieval | Load only relevant current/domain facts | Bootstrap loads README/current; targeted `rg` retrieves at most relevant notes; corroboration required | Implemented as procedure, not relevance scoring. |
| Retention | Define how long/usefully a durable note remains | Review when relevant; remove duplicates; follow live state on conflict | Partial; no review-by/TTL/last-used field or stale-note gate. |
| Eviction/deletion | Remove obsolete, duplicate, sensitive, or invalid memory safely | Replace current in place; remove duplicates; provider-private/raw material prohibited | Partial; no durable-note deletion manifest, consumer proof, or automated eviction. |
| Archive | Preserve provenance after memory is no longer active retrieval material | Archive stale/superseded notes only after durable evidence and Git provenance are confirmed | Procedural only; no archive location/profile is defined for Memory notes. |
| Partition | Prevent unrelated domains/users/repos from contaminating retrieval | Repository-local tracked directory; provider-private memory excluded | Partial; repo boundary exists, domain and identity partitions are untyped. |
| Privacy | Prevent sensitive/raw material from becoming shared memory | Prohibits transcripts, raw output/logs, credentials, tokens, shell history, personal notes, and private provider state | Strong tracked rule; enforcement is strongest only on `current.md`. |
| Size | Bound high-priority index/context | `current.md` 32 KiB/400 lines; exact provider-native limits are external | Implemented for current only; durable/historical tiers unbounded. |
| Freshness | Show that a fact still matches live tracked state | Current Task active/draft, commit ancestor, timestamp; notes rely on manual verification metadata | Implemented for current; partial/missing for durable and historical tiers. |

### Provider-native boundaries

| Concern | Claude Code public capability | Codex public capability | Local adoption/evidence boundary |
| --- | --- | --- | --- |
| Cross-session memory | Auto memory writes a per-repository, machine-local `MEMORY.md` plus on-demand topic files. | Config reference exposes generation, consolidation, use/injection, age, idle-time, unused-time, and raw-memory caps. | No provider-private memory was inspected; tracked repo config does not prove either mechanism ran. |
| Partition | Claude shares one project memory across worktrees; subagent memory is separate. | Public config describes thread/global extraction controls; no local domain taxonomy is inferred. | Repository Memory remains the only shared tracked handoff. |
| Size/retrieval | First 200 lines or 25 KiB of `MEMORY.md` loads; topic files are on demand. | Auto-compaction has a configurable token threshold; memory injection can be disabled. | Provider limits do not replace the 32 KiB/400-line repository contract. |
| Retention/freshness | Near-limit guidance merges/drops stale entries; frontmatter may receive a `modified` timestamp; users can edit/delete files. | Config exposes maximum rollout age, unused days, per-startup candidates, and consolidation cap. | These are external configurable capabilities, not local policy or execution evidence. |
| Privacy control | Machine-local store, project toggle, editable/deleteable plain Markdown. | `disable_on_external_context` can exclude threads using MCP/web/tool search; generation and use are separately toggleable. | Public settings do not prove the active account's privacy configuration or deletion outcome. |
| Enforcement | Claude explicitly calls instructions/memory context, not enforced configuration. | Config values describe product behavior, not this repository's policy hierarchy. | Stage 00 and canonical stage artifacts always outrank provider memory. |

The Codex config reference is particularly important because it separates
`generate_memories` from `use_memories`: stopping new extraction and stopping
future injection are different controls. Neither establishes deletion of
already generated material. Likewise, age/unused limits control eligibility
for generation/consolidation, not a repository retention policy.

### Required future lifecycle contract

A future Stage 03 memory-governance specification should define a typed domain
enum and owner; promotion trigger and evidence; retrieval index/query and
corroboration; last-verified/review-by/last-used metadata; retention and legal
hold exceptions; eviction versus deletion semantics; deletion consumer and
provenance proof; an archive/tombstone route; per-domain size/freshness bounds;
privacy classification and redaction; provider export/sync prohibition; and a
validator plus migration plan. Until then, durable notes remain advisory and
human-curated.

## Scope Implications

| Scope | Application and disposition |
| --- | --- |
| `agentic` | Owns memory authority, bootstrap/retrieval, provider boundaries, and current validator; no provider memory may override it. |
| `architecture` | Durable architecture decisions belong in ADR/Spec owners; Memory may link a reusable pitfall but cannot replace them. |
| `backend` | No current surface; future backend-domain memory requires an approved domain owner and privacy/retention contract. |
| `common` | Reusable cross-scope findings need one canonical note, duplicate control, and corroboration before use. |
| `docs` | Owns current/durable note stewardship, template use, bounds, links, and any future archive route. |
| `entry` | Gateway operational facts belong in tracked config/runbooks/incidents; secrets/certificates/log payloads never enter Memory. |
| `frontend` | Current fixture learnings remain QA-owned unless a product surface creates a domain route. |
| `infra` | Runtime state, raw logs, secret values, backups, and provider-local files stay outside shared Memory; link value-free evidence only. |
| `meta` | A future typed domain/freshness/retention schema and validator route through docs/meta governance. |
| `mobile` | Not applicable today; future device/user data needs explicit privacy, deletion, and partition controls. |
| `ops` | Incident chronology/outcomes stay in Stage 05; Memory may retain only reusable, sanitized patterns linked to the owner. |
| `product` | Product decisions remain in requirements/approval artifacts; preferences or provider memory cannot become stakeholder intent. |
| `qa` | Validate bounds, section envelope, ancestry, prohibited material, retrieval fixtures, and migration/deletion behavior. |
| `security` | Own privacy classification, redaction, deletion proof, provider-memory boundaries, and prompt-injection resistance. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [Governance Memory contract](../../../00.agent-governance/memory/README.md) | 2026-08-08 | Workspace tracked | Direct owner for advisory authority, privacy, retrieval, replacement, retention, and archive cues. |
| [Current project memory](../../../00.agent-governance/memory/current.md) | 2026-08-08 | Workspace tracked | Only headings/size/current labels needed for bounded analysis; no raw/private interaction data recorded. |
| [Memory stewardship function](../../../00.agent-governance/agents/functions/project-memory-stewardship.md) | 2026-08-08 | Workspace tracked | 32 KiB/400-line/seven-section/evidence gates. |
| [Current-memory validator](../../../../scripts/validation/agent_governance_contract.py) | 2026-08-08 | Workspace tracked | Bounds, sections, Task state, ancestry, timestamps, and forbidden-material checks. |
| [Claude instructions and auto memory](https://code.claude.com/docs/en/memory) | 2026-08-08 | External mutable | HTTP 200; public project memory, partition, size, freshness, edit/delete, and context boundary. |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; public `memories.*` generation/use/consolidation/age/privacy controls and compaction fields. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace stale/advisory | Built from `f8a72211`; not used for counts or lifecycle proof. |

## Maintenance

Rerun the tracked `wc` derivation and inspect only safe metadata when Memory
files, the current profile, bootstrap route, provider memory docs, or validator
changes. Never inspect provider-private stores merely to refresh this leaf.

## Related Documents

- [Loop engineering](./loop-engineering.md)
- [Agent instructions](./agent-instructions-vibe-coding.md)
- [Provider implementation comparison](./provider-implementation-comparison.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
