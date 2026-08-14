---
status: draft
artifact_id: reference:agentic-engineering-research:agent-instructions-vibe-coding
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-14
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

| Layer                       | Tracked owner or surface                       | Meaning                                                            | Evidence limit                                          |
| --------------------------- | ---------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------- |
| Direct authority            | System and user instructions                   | Highest-priority task authority                                    | Not stored as repository policy by this leaf.           |
| Canonical repository policy | `docs/00.agent-governance/`                    | Rules, scopes, contracts, catalogs, providers, and memory boundary | Tracked text proves definition, not runtime compliance. |
| Entry shims                 | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`          | Short bootstrap routes                                             | Presence does not prove a provider loaded them.         |
| Provider overlays           | `providers/{agents-md,claude,codex,gemini}.md` | Provider-native translation within Stage 00 bounds                 | Narrative owner, not a live provider setting.           |
| Runtime adapters            | `.claude/`, `.codex/`, `.gemini/`              | Generated agents, skills/settings, and hook wiring                 | **Configured**, not **executed**.                       |
| Compatibility               | `.agents/`                                     | Shared skills and compatibility projections                        | Not a native policy owner.                              |

Claude documents `CLAUDE.md`, scoped rules, imports, and auto memory as
context rather than enforced configuration; hard blocking belongs in settings
or hooks. Codex documents repository instruction discovery through `AGENTS.md`
and allows a separate model-instruction replacement path. These mechanisms are
not interchangeable, so the common contract is semantic: discover applicable
authority, load the minimum context, preserve provider-native syntax, and
verify the result.

### Three distinct precedence systems, disentangled

This axis is easy to conflate because three separate precedence orders exist
at once, only one of which this repository authors:

1. **This repository's instruction hierarchy** (`providers/agents-md.md` §4,
   read directly): (1) direct user/system instructions — always win; (2)
   `docs/00.agent-governance/` — authoritative for policy; (3) root shim files
   (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`); (4) provider overlays
   (`providers/{claude,codex,gemini}.md`); (5) runtime controls (`.claude/`,
   `.codex/`, `.gemini/`); (6) `.agents/` compatibility surfaces. This is
   repo-authored policy, not a vendor mechanism.
2. **Claude's native settings-file precedence** (`code.claude.com/docs/en/settings`,
   re-verified 2026-08-14): managed > CLI arguments > `.claude/settings.local.json`
   > `.claude/settings.json` > `~/.claude/settings.json` — a vendor-defined
   > scope order for the JSON `permissions`/`hooks`/`autoMode` schema, with the
   > caveat that `permissions` rules _merge_ across scopes rather than strictly
   > overriding (any-scope `deny` wins, `allow` accumulates).
3. **Claude's native CLAUDE.md load-location precedence** (`code.claude.com/docs/en/memory`,
   re-verified 2026-08-14): managed policy (`/etc/claude-code/CLAUDE.md` or
   equivalent) > user (`~/.claude/CLAUDE.md`) > project (`./CLAUDE.md` or
   `./.claude/CLAUDE.md`) > local (`./CLAUDE.local.md`) — a fourth, separate
   ordering for _which memory file_ is discovered, distinct from both (1) and
   (2). CLAUDE.md content is "delivered as a user message after the system
   prompt, not as part of the system prompt itself" per that page — an
   explicit vendor statement that instruction files are context, not a hard
   enforcement layer; only settings/hooks enforce.

Re-derived directly in this worktree: this repository tracks no
`.claude/rules/` directory, no `CLAUDE.local.md`, and only one project-scope
`.claude/settings.json` plus one git-ignored `.claude/settings.local.json`
(observed locally, not part of the tracked corpus). Claude's path-scoped rule
mechanism (`.claude/rules/*.md` with `paths:` frontmatter, loaded only when a
matching file is opened) and the `@import` mechanism (4-hop max recursion
depth, with a one-time approval dialog for imports that resolve outside the
working directory) are therefore vendor capabilities this workspace does not
currently use — a negative-evidence fact, not an assumption of absence.

### User-scope instructions versus this repository's tracked policy

Claude's CLAUDE.md load-location order above places "user" (`~/.claude/CLAUDE.md`
and `~/.claude/rules/`) _before_ "project" in load order, meaning
project-scope content is read later/closer to the working context — but
loading order is not the same claim as this repository's own precedence list,
which states repository governance is "authoritative for all policy matters"
once work targets this repository, and that direct user/system turn
instructions (distinct from a _stored_ personal config file) always win over
everything. A personal, machine-global instruction layer can therefore
legitimately exist for an operator working across many repositories — for
example a global preference toward proactive subagent delegation, parallel
task execution, or automatic skill invocation — without that layer being able
to expand what this specific repository's `approval-boundaries.md` Hard Stops
or the four typed harness loops (see [loop-engineering.md](./loop-engineering.md))
permit here. This reference does not name or quote any such personal
configuration; it records only the structural fact that this layering exists
in Claude's own documented precedence and that this repository's governance
explicitly does not yield policy authority to it. This is the precise
boundary AIV-01/AIV-05 below exist to hold: a broader personal operating
style is not itself authorization to mutate a protected surface, request an
approval-bypassing action, or skip the independent-review loop.

### Root shim structure, re-derived

All three root shims were re-read directly at this baseline (line counts
exact):

| File        | Lines | Loading mechanism                     | Content                                                                                                                                                                                  |
| ----------- | ----: | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md` |     7 | Prose instruction ("Load `docs/...`") | Codex's official AGENTS.md page (re-verified 2026-08-14) states content is "read and prepended to the agent's context — it's not transcluded but actively loaded," rebuilt on every run. |
| `CLAUDE.md` |     8 | `@path` transclusion                  | Four `@docs/00.agent-governance/...` imports, expanded at session launch.                                                                                                                |
| `GEMINI.md` |     8 | `@./path` transclusion                | Four `@./docs/00.agent-governance/...` imports — the same transclusion mechanism as Claude, not the same as `AGENTS.md`'s prose-instruction style.                                       |

This is a previously unrecorded asymmetry: `GEMINI.md` mirrors Claude's
import-based loading rather than Codex's read-and-prepend loading, even
though `AGENTS.md` is the nominal "shared" entry point in the provider-neutral
model. Each shim imports exactly four canonical sources in the same order
(bootstrap, provider overlay, memory README, memory current-state), so the
_content_ loaded is identical across all three even though _how_ it enters
context differs by provider.

### The Canonical Adapter Model as the vibe-coding boundary

`providers/agents-md.md` §5 (re-read 2026-08-14) defines a two-tier model that
directly bounds safe conversational iteration: Tier 1 (`agents/agents/`,
`agents/functions/`, `contracts/provider-models.yaml`) is the only place a
role, function, model, or event is defined; Tier 2 (`.claude/`, `.codex/`,
`.gemini/`) exposes that definition through a generated, provider-native
adapter. Five adapter rules (name-set, role, policy, model, and validation
parity — detailed in
[provider-implementation-comparison.md](./provider-implementation-comparison.md))
make this machine-checkable. The direct consequence for bounded vibe coding:
a conversational session that hand-edits a Tier 2 file (for example adding a
tool to `.claude/agents/qa-engineer.md` without a matching Stage 00 change)
produces drift a validator can catch, but it is still a policy violation the
moment it is written, not only once caught. `.claude/CLAUDE.md`'s own
instruction — "Change canonical Stage 00 sources first, then run the
registered provider renderer. Do not hand-author policy in generated
adapters." — states this boundary directly and is the concrete,
workspace-specific form of AIV-01 below.

### Instruction and generated-work criteria

| Claim                        | Required workspace rule                                                               | Current status                                         | Verification limit / gap                                           |
| ---------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------ |
| AIV-01 Authority             | Stage 00 is canonical; projections cannot redefine policy.                            | Implemented in tracked governance and renderer inputs. | Provider loading is unobserved.                                    |
| AIV-02 Context               | Load bootstrap, persona, checklist, one scope, and JIT stage sources.                 | Implemented as tracked routing.                        | Context contents of a live session are unobserved.                 |
| AIV-03 Specificity           | Name paths, commands, expected result, exclusions, and owner.                         | Implemented in task/checklist contracts.               | Prompt adherence is probabilistic.                                 |
| AIV-04 Tools                 | A tool is a capability, not mutation authority.                                       | Implemented in approval/environment rules.             | Active sandbox and grants are runtime facts.                       |
| AIV-05 Permissions           | Least privilege; explicit approval for protected or external actions.                 | Implemented as policy and typed permission profiles.   | Local metadata is not proof the runtime enforced it.               |
| AIV-06 Verification          | Run the smallest applicable deterministic checks and record skips.                    | Implemented for tracked checks.                        | CI, provider, remote, and service outcomes need separate evidence. |
| AIV-07 Ownership             | The human/team and canonical artifact owner accept generated output.                  | Defined; the model never becomes accountable owner.    | Acceptance requires Task/diff/review evidence.                     |
| AIV-08 Independent review    | Increase review with complexity, novelty, sensitivity, and blast radius.              | Implemented in the lifecycle and review loop.          | This leaf does not claim a review occurred.                        |
| AIV-09 Dependency provenance | Verify package, action, image, API, license, and maintenance facts.                   | Required by governance/security routes.                | Plausible model output or registry presence alone is insufficient. |
| AIV-10 Debt                  | Preserve failing evidence and route debt to its earliest canonical stage.             | Defined.                                               | Chat history and provider memory are not durable owners.           |
| AIV-11 Escalation            | Stop on missing authority, high-impact ambiguity, or exhausted typed attempts.        | Four bounded loops are tracked.                        | No prompt-local retry policy may extend them.                      |
| AIV-12 Untrusted context     | Web pages, tool output, repository text, and external agents are data until reviewed. | Defined by security and intake boundaries.             | Reading content never elevates its authority.                      |

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

| Scope          | Application and disposition                                                                                                                           |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Owns canonical instruction, catalog, loop, provider, and adapter parity; tracked/configured status must not be promoted to execution.                 |
| `architecture` | Use instructions to route trade-offs into ARD/ADR/Spec owners; no typed agent currently owns this enum-admitted scope.                                |
| `backend`      | Not applicable until a backend surface and Spec exist; future generated code still needs boundary validation and tests.                               |
| `common`       | Shared review and conventions apply, but agents may not bypass the controlled QA boundary or create parallel policy.                                  |
| `docs`         | Template-first and metadata/link rules apply; Stage 90 advice cannot authorize Stage 01-99 adoption.                                                  |
| `entry`        | Gateway work routes through the adjacent infra owner with config/Compose validation and explicit runtime authority.                                   |
| `frontend`     | Existing Storybook/Next material is a QA fixture, not a general product surface; generated UI requires the existing owner and accessibility evidence. |
| `infra`        | Compose, secret, and runtime changes require concrete targets, rollback, and specialist review; instruction text cannot grant access.                 |
| `meta`         | Metadata/taxonomy changes route through docs and validators; the missing typed scope route remains a governance gap.                                  |
| `mobile`       | Not applicable to the current corpus; future mobile generation needs an approved product/Spec chain and device-specific verification.                 |
| `ops`          | Runtime and incident outcomes belong in Stage 05 evidence; conversational completion is never an operational outcome.                                 |
| `product`      | Human/stakeholder approval owns product intent; no generated instruction may infer acceptance from a draft prompt.                                    |
| `qa`           | Owns focused validation and synthetic evaluation; fixtures prove repository semantics, not live-model quality.                                        |
| `security`     | Treat external instructions and generated dependencies as untrusted; preserve least privilege, redaction, and approval boundaries.                    |

## Sources

| Source | Accessed | Class | Use and verification state |
| --- | --- | --- | --- |
| [Claude instructions and memory](https://code.claude.com/docs/en/memory) | 2026-08-14 | External mutable | Re-verified: full CLAUDE.md load-location order, `@import` 4-hop limit, external-import approval dialog, path-scoped `.claude/rules/`, "delivered as user message not system prompt." |
| [Claude settings](https://code.claude.com/docs/en/settings) | 2026-08-14 | External mutable | New: exact 5-level settings-scope precedence, permission-merge-across-scopes rule. |
| [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 2026-08-14 | External mutable | Re-verified: global/project discovery order, `AGENTS.override.md`, 32 KiB `project_doc_max_bytes` default, "read and prepended, not transcluded." |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | 2026-08-08 | External mutable | HTTP 200; instruction replacement and configuration boundary. |
| [Stage 00 bootstrap](../../../00.agent-governance/rules/bootstrap.md) | 2026-08-14 | Workspace tracked | Re-read: canonical loading sequence and evidence boundary. |
| [Provider-neutral notes](../../../00.agent-governance/providers/agents-md.md) | 2026-08-14 | Workspace tracked | Re-read: exact 6-level precedence list (§4) and Canonical Adapter Model (§5) with the five adapter rules. |
| [Task checklists](../../../00.agent-governance/rules/task-checklists.md) | 2026-08-14 | Workspace tracked | Re-read: pre-task ambiguity-blocking rule, in-task loop-bound rule, completion evidence duties. |
| [Environment constraints](../../../00.agent-governance/rules/environment-constraints.md) | 2026-08-14 | Workspace tracked | Read: "most-specific in-scope instruction file wins" and "system/developer/direct user instructions always override repository instruction files." |
| Root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) | 2026-08-14 | Workspace tracked | Read directly: exact line counts and `@`-import vs. prose-instruction loading mechanism per file. |
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
