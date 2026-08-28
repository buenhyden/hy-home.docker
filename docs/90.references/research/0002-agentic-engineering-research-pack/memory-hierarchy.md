---
status: draft
artifact_id: reference:agentic-engineering-research-draft:memory-hierarchy
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Memory Hierarchy

## Overview

Memory is partitioned by both time horizon and domain; those axes are not the
same thing. Provider-native memory is advisory product behavior, never a
replacement for current Task evidence, durable canonical documents, or Git.

## Purpose

Describe retained provider controls and a proposed, reviewable memory process
without reading private/user memories or inferring runtime settings.

## Scope

This leaf covers retained primary vendor observations and a conceptual process.
It excludes provider-private stores, user/global files, account settings,
runtime defaults, and any mutation or deletion action.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `MH-001` | Retained Claude subagent documentation defines persistent `user`, `project`, and `local` memory scopes; scope controls storage partition, not the authority of content. | retained official observation | HISTORICAL VERIFIED | provider boundary only | Treat provider memory as advisory. |
| `MH-002` | Retained Codex configuration documentation exposes independent `memories.generate_memories` and `memories.use_memories` controls. | retained official observation | HISTORICAL VERIFIED | provider boundary only | Turning generation off is not deletion, and use is separately controlled. |
| `MH-003` | Effective provider-memory values and overrides for this draft are unknown; no runtime observation was authorized. | runtime boundary | UNVERIFIED | provider adapter and registry boundary | Do not infer defaults from absent tracked fields. |
| `MH-004` | A proposed process is capture → sanitize → provenance → partition → retrieve → expiry review → deletion proof. | advisory synthesis | ADVISORY | future governed memory owner | Adoption needs a typed policy and verification. |

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

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `MH-SRC-001` | `MH-001` | Subagents / Anthropic | [official page](https://code.claude.com/docs/en/sub-agents) | retained official observation | detailed dated leaf; version not recorded | 2026-08-14T13:40:00+09:00 | Provider capability; no local memory directory inspected. |
| `MH-SRC-002` | `MH-002` | Configuration reference / OpenAI | [official page](https://learn.chatgpt.com/docs/config-file/config-reference) | retained official observation | detailed dated leaf; version not recorded | 2026-08-14T13:40:00+09:00 | Public fields do not prove account setting, injection, or deletion. |
| `MH-SRC-003` | `MH-003`, `MH-004` | Codex provider adapter / workspace | [Codex adapter](../../../00.agent-governance/providers/codex.md) | tracked governance | `4481e73d433f6738e0e09b9e94977d4a2ac127cf` | 2026-08-28 | Adapter defines a runtime boundary, not an effective provider-memory value. |

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

Revisit only when retained vendor documentation or a canonical memory policy
changes. A future process must be adopted and verified before it is described
as an operating control.

## Related Documents

- [Research pack README](./README.md)
- [Agent model selection](./agent-model-selection.md)
- [Harness engineering](./harness-engineering.md)
