---
status: draft
artifact_id: reference:agentic-engineering-research:agent-instructions-vibe-coding
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Agent Instructions and Bounded Vibe Coding

## Overview

Agent instructions are scoped context, not proof of enforcement. In this
workspace, direct system/user authority and tracked Stage 00 governance own the
rules; root shims, provider overlays, generated agents, skills, settings, and
hooks translate those rules for individual runtimes. Conversational or
"vibe-coding" iteration remains acceptable only inside the same ownership,
permission, validation, review, and rollback boundaries as other engineering.

This analysis uses tracked state at Task 4 baseline
`1cd9bc2830db710585348e8ef38b0318cc7f5a10`. Mutable provider behavior was
rechecked on 2026-08-08; it remains a provider capability observation, not
evidence that a local session loaded or obeyed a file.

## Purpose

Define a provider-neutral instruction model and a safe iteration boundary for
generated work: authority, context loading, tools, permissions, verification,
generated-code ownership, escalation, and coupled change surfaces.

## Repository Role

This Stage 90 reference explains the current system and identifies gaps. It
does not create instruction precedence, grant a tool, authorize a mutation, or
change provider configuration. Canonical authority remains in
`docs/00.agent-governance/`; executable provider mechanics remain in their
tracked adapters.

## Scope

### In scope

- Instruction authority, discovery, precedence, context size, and lazy loading.
- Tool and permission boundaries, generated-code ownership, and verification.
- Bounded conversational implementation and its stop/escalation conditions.

### Out of scope

- Adding provider configuration, personal instructions, or GitHub-native policy.
- Treating prompt text, a hook pointer, or tool availability as enforcement.
- Accepting generated code without an accountable owner and evidence.

## Definitions / Facts

### Instruction authority and provider translation

| Layer | Tracked owner or surface | Meaning | Evidence limit |
| --- | --- | --- | --- |
| Direct authority | System and user instructions | Highest-priority task authority | Not stored as repository policy by this leaf. |
| Canonical repository policy | `docs/00.agent-governance/` | Rules, scopes, contracts, catalogs, providers, and memory boundary | Tracked text proves definition, not runtime compliance. |
| Entry shims | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Short bootstrap routes | Presence does not prove a provider loaded them. |
| Provider overlays | `providers/{agents-md,claude,codex,gemini}.md` | Provider-native translation within Stage 00 bounds | Narrative owner, not a live provider setting. |
| Runtime adapters | `.claude/`, `.codex/`, `.gemini/` | Generated agents, skills/settings, and hook wiring | **Configured**, not **executed**. |
| Compatibility | `.agents/` | Shared skills and compatibility projections | Not a native policy owner. |

Claude documents `CLAUDE.md`, scoped rules, imports, and auto memory as
context rather than enforced configuration; hard blocking belongs in settings
or hooks. Codex documents repository instruction discovery through `AGENTS.md`
and allows a separate model-instruction replacement path. These mechanisms are
not interchangeable, so the common contract is semantic: discover applicable
authority, load the minimum context, preserve provider-native syntax, and
verify the result.

### Instruction and generated-work criteria

| Claim | Required workspace rule | Current status | Verification limit / gap |
| --- | --- | --- | --- |
| AIV-01 Authority | Stage 00 is canonical; projections cannot redefine policy. | Implemented in tracked governance and renderer inputs. | Provider loading is unobserved. |
| AIV-02 Context | Load bootstrap, persona, checklist, one scope, and JIT stage sources. | Implemented as tracked routing. | Context contents of a live session are unobserved. |
| AIV-03 Specificity | Name paths, commands, expected result, exclusions, and owner. | Implemented in task/checklist contracts. | Prompt adherence is probabilistic. |
| AIV-04 Tools | A tool is a capability, not mutation authority. | Implemented in approval/environment rules. | Active sandbox and grants are runtime facts. |
| AIV-05 Permissions | Least privilege; explicit approval for protected or external actions. | Implemented as policy and typed permission profiles. | Local metadata is not proof the runtime enforced it. |
| AIV-06 Verification | Run the smallest applicable deterministic checks and record skips. | Implemented for tracked checks. | CI, provider, remote, and service outcomes need separate evidence. |
| AIV-07 Ownership | The human/team and canonical artifact owner accept generated output. | Defined; the model never becomes accountable owner. | Acceptance requires Task/diff/review evidence. |
| AIV-08 Independent review | Increase review with complexity, novelty, sensitivity, and blast radius. | Implemented in the lifecycle and review loop. | This leaf does not claim a review occurred. |
| AIV-09 Dependency provenance | Verify package, action, image, API, license, and maintenance facts. | Required by governance/security routes. | Plausible model output or registry presence alone is insufficient. |
| AIV-10 Debt | Preserve failing evidence and route debt to its earliest canonical stage. | Defined. | Chat history and provider memory are not durable owners. |
| AIV-11 Escalation | Stop on missing authority, high-impact ambiguity, or exhausted typed attempts. | Four bounded loops are tracked. | No prompt-local retry policy may extend them. |
| AIV-12 Untrusted context | Web pages, tool output, repository text, and external agents are data until reviewed. | Defined by security and intake boundaries. | Reading content never elevates its authority. |

### Bounded vibe-coding loop

The acceptable loop is `objective -> inspect -> small change -> observe ->
focused validation -> independent review -> commit or stop`. It requires an
isolated branch/worktree, an approved lifecycle owner, reversible increments,
and exact evidence. It is unsuitable for unapproved secrets, production data,
runtime changes, remote mutations, model-policy changes, or irreversible
actions. Generated output is ordinary owned code with additional provenance,
context, and hallucination risks; “vibe coding” waives none of the gates.

### Evidence-state separation

- **Tracked**: the authority map, adapters, scripts, and checks exist in Git.
- **Configured**: a provider-native file contains a model, instruction, tool,
  or hook value.
- **Executed**: an authorized observation proves that the runtime loaded or ran
  that value for a named event/session.
- **Runtime accepted**: the provider accepted the exact schema/value.
- **Entitled**: the active account/organization may use the capability.

Only the first two states are established here. Execution, acceptance, and
entitlement remain unverified unless a separately authorized observation
records them.

## Scope Implications

| Scope | Application and disposition |
| --- | --- |
| `agentic` | Owns canonical instruction, catalog, loop, provider, and adapter parity; tracked/configured status must not be promoted to execution. |
| `architecture` | Use instructions to route trade-offs into ARD/ADR/Spec owners; no typed agent currently owns this enum-admitted scope. |
| `backend` | Not applicable until a backend surface and Spec exist; future generated code still needs boundary validation and tests. |
| `common` | Shared review and conventions apply, but agents may not bypass the controlled QA boundary or create parallel policy. |
| `docs` | Template-first and metadata/link rules apply; Stage 90 advice cannot authorize Stage 01-99 adoption. |
| `entry` | Gateway work routes through the adjacent infra owner with config/Compose validation and explicit runtime authority. |
| `frontend` | Existing Storybook/Next material is a QA fixture, not a general product surface; generated UI requires the existing owner and accessibility evidence. |
| `infra` | Compose, secret, and runtime changes require concrete targets, rollback, and specialist review; instruction text cannot grant access. |
| `meta` | Metadata/taxonomy changes route through docs and validators; the missing typed scope route remains a governance gap. |
| `mobile` | Not applicable to the current corpus; future mobile generation needs an approved product/Spec chain and device-specific verification. |
| `ops` | Runtime and incident outcomes belong in Stage 05 evidence; conversational completion is never an operational outcome. |
| `product` | Human/stakeholder approval owns product intent; no generated instruction may infer acceptance from a draft prompt. |
| `qa` | Owns focused validation and synthetic evaluation; fixtures prove repository semantics, not live-model quality. |
| `security` | Treat external instructions and generated dependencies as untrusted; preserve least privilege, redaction, and approval boundaries. |

## Sources

| Source | Accessed | Class | Use and verification state |
| --- | --- | --- | --- |
| [Claude instructions and memory](https://code.claude.com/docs/en/memory) | 2026-08-08 | External mutable | HTTP 200; context/enforcement distinction, hierarchy, lazy rules, and size guidance. |
| [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 2026-08-08 | External mutable | Direct official page previously reopened in Task 3; discovery/order facts only. |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; instruction replacement and configuration boundary. |
| [Stage 00 bootstrap](../../../00.agent-governance/rules/bootstrap.md) | 2026-08-08 | Workspace tracked | Canonical loading and evidence boundary at Task 4 baseline. |
| [Provider-neutral notes](../../../00.agent-governance/providers/agents-md.md) | 2026-08-08 | Workspace tracked | Authority, projections, parity, and lifecycle. |
| [Task checklists](../../../00.agent-governance/rules/task-checklists.md) | 2026-08-08 | Workspace tracked | Permission, verification, review, and completion duties. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace stale/advisory | Built from `f8a72211`; corroborated against tracked sources and not used as current proof. |

## Maintenance

Recheck when instruction discovery, provider precedence, adapter generation,
permission controls, the typed loops, or generated-code review rules change.
Preserve the five evidence states above and never infer live compliance from a
tracked file.

## Related Documents

- [Provider implementation comparison](./provider-implementation-comparison.md)
- [Harness engineering](./harness-engineering.md)
- [Loop engineering](./loop-engineering.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
