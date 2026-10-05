---
title: "Reference: Agent Instructions and Bounded Vibe Coding"
version: "1.2.1"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0002-m0001"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
---

# Reference: Agent Instructions and Bounded Vibe Coding

## Overview

### Overview

## Scope and Method

### Current External Research

This member owns instruction discovery and bounded exploratory coding. Original external pages were opened on **2026-09-27**; preserved `observed_at` and `reviewed_at` describe historical evidence. This research is non-normative. Internal adoption: **Not assessed in this run**. Unless an original explicitly states a maturity label, formal stable/preview/experimental status is **not stated**; current documentation is not a stability guarantee.

### Instruction loading and authority

**C-m0001-01 — source fact.** Codex assembles guidance once at run start: global AGENTS.override.md before AGENTS.md, then one file per directory from project root to working directory, with more specific guidance later. The default combined project limit is 32 KiB. Linked Markdown still needs an explicit read. [Codex instruction guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) (S-learn-chatgpt-com-agents-md, discovery section).

**C-m0001-02 — source fact.** Claude Code now supports AGENTS.md through its bundled agents-md plugin from v2.1.277. The default selects it when no CLAUDE.md variant exists in the launch directory or ancestors; managed/user instructions and .claude/rules can coexist. It ignores AGENTS.override.md, AGENTS.local.md and .agents directory discovery. The instructionFiles switch is user/managed, not project configuration. Some third-party/telemetry-disabled sessions before v2.1.281 lack support. Instruction and memory text are context, not enforced configuration. [Claude instructions](https://code.claude.com/docs/en/memory) (S-code-claude-com-memory, AGENTS.md section).

**C-m0001-03 — interpretation.** A shared filename does not establish identical discovery, precedence or enforcement. A common map can point to the approved task, scope, durable owner and acceptance evidence; provider adapters must retain native loading and trust behavior. [m0012](m0012-provider-implementation-comparison.md#native-capability-matrix) owns permissions, sandbox, skills, hooks and session differences. Repeating a control in prose is not evidence that it is enforced.

### Instruction authoring distinctions

**C-m0001-03 — non-normative authoring interpretation.** The following separates
intent from enforcement using the loading/context limits of C-m0001-01–02. It is
a proposed authoring convention, not a new provider feature or repository policy.

| Kind | What it owns | Scoped example and validation boundary |
| --- | --- | --- |
| Instruction | Context-specific direction for the current work | Name the task, allowed paths, source owners and completion check; verify the applicable text actually loads. |
| Policy | Durable obligations, exceptions and decision authority | Link the approved security or coding owner and its scope; identify the enforcing validator/permission separately. Prose alone cannot grant or enforce access. |
| Role | Responsibility, permitted scope and handoff | Say who authors, who reviews and which decisions require another owner; a role name does not create tools or permissions. |
| Procedure | Ordered steps, inputs, failure handling and evidence | Link one reusable skill/runbook; state prerequisites, stop conditions, recovery and output evidence instead of copying its steps into every adapter. |
| Tool | A concrete operation exposed by an execution surface | Name the available interface, allowed inputs/side effects and failure contract; check actual availability and authorization rather than assuming them from instructions. |
| Output style | Reader, language, detail and presentation preferences | For a technical reviewer, request a concise explanation plus check results; for an operator, request numbered actions and stop conditions. Style cannot override scope, uncertainty or required evidence. |

For a **hypothetical package**, specify the language/framework and permitted
version range by linking its manifest/lockfile owner; do not duplicate mutable
pins in every instruction. Scope coding rules to that package and link its
formatter/linter/test owner, naming the check that would demonstrate compliance.
State explanation language, audience and desired detail separately from those
coding constraints. These are examples of how to write an instruction, not claims
about this repository's stack or installed tools.

When sources conflict, identify their authority, applicable path/task and native
loading order; retain provider-specific exceptions in the adapter. Resolve an
ambiguous controlling rule with its owner before dependent work. A separately
authorized fixture should vary launch directory, nested instructions and trust
state, then compare loaded guidance, effective permissions and output. A drift
review compares each adapter's references and exceptions with the canonical
owner; file copying or symlinking alone proves neither loading nor equivalence.

### Conditional guidance for exploration

**C-m0001-04 — recommendation.** A short exploratory prompt suits a disposable sketch or reversible edit with observable acceptance. Before promotion, put intended behavior, constraints, allowed paths, a stop condition and a concrete check in the existing workflow. A natural-language attempt limit supplies review guidance, not a process kill switch. Ambiguous, cross-cutting or security-sensitive changes benefit from planning and independent evidence review.

Anthropic distinguishes prescribed workflows from dynamically directed agents and recommends simpler compositions first, environmental feedback and stopping conditions. This is design advice, not a quality standard. [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (S-anthropic-com-building-effective-agents; loop implications owned by [m0010](m0010-loop-engineering.md#current-external-research)). A concise instruction map saves repeated context but depends on reliable discovery; a large always-loaded policy increases conflict and context costs. This research does not authorize relocating policy.

### Related Documents

- [Research pack](README.md)
- [Provider implementation comparison](./m0012-provider-implementation-comparison.md)
- [Harness engineering](./m0008-harness-engineering.md)
- [Loop engineering](./m0010-loop-engineering.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)

## Findings

### Historical Workspace Observations

The complete earlier body is preserved at its original cutoff, including then-current external assertions and workspace observations. It is not current implementation authority; its dates are unchanged.

> Historical evidence (not current authority; source: Git history):
>
> Current routing (2026-09-06): [canonical agent governance](../../../../.agents/README.md) and
> [ADR-0032](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md) own the active source location.
> Earlier Stage 00 paths, inventories, provider projections, and check results
> below remain dated observations, not current instructions or new runtime
> acceptance evidence. Source links now navigate to current owners; the
> original `observed_at`, `reviewed_at`, status, and measured facts are preserved.
>
> ## Overview
>
> Agent instructions are scoped context, not proof of enforcement. In this
> workspace, direct system/user authority and tracked canonical agent governance governance own the
> rules; root shims, provider overlays, generated agents, skills, settings, and
> hooks translate those rules for individual runtimes. Conversational or
> "vibe-coding" iteration remains acceptable only inside the same ownership,
> permission, validation, review, and rollback boundaries as other engineering.
>
> This analysis uses tracked state at Task 4 baseline
> `1cd9bc2830db710585348e8ef38b0318cc7f5a10`. Mutable provider behavior was
> rechecked on 2026-08-08; it remains a provider capability observation, not
> evidence that a local session loaded or obeyed a file.
>
> ## Purpose
>
> Define a provider-neutral instruction model and a safe iteration boundary for
> generated work: authority, context loading, tools, permissions, verification,
> generated-code ownership, escalation, and coupled change surfaces.
>
> ## Repository Role
>
> > Historical evidence (not current authority; source: Git history): Recorded source path at the document observation baseline.
> > This Stage 90 reference explains the current system and identifies gaps. It
> > does not create instruction precedence, grant a tool, authorize a mutation, or
> > change provider configuration. Canonical authority remains in
> > `docs/00.agent-governance/`; executable provider mechanics remain in their
> > tracked adapters.
>
> ## Scope
>
> ### In scope
>
> - Instruction authority, discovery, precedence, context size, and lazy loading.
> - Tool and permission boundaries, generated-code ownership, and verification.
> - Bounded conversational implementation and its stop/escalation conditions.
>
> ### Out of scope
>
> - Adding provider configuration, personal instructions, or GitHub-native policy.
> - Treating prompt text, a hook pointer, or tool availability as enforcement.
> - Accepting generated code without an accountable owner and evidence.
>
> ## Definitions / Facts
>
> ### Instruction authority and provider translation
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Layer                       | Tracked owner or surface                       | Meaning                                                            | Evidence limit                                          |
> | --------------------------- | ---------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------- |
> | Direct authority            | System and user instructions                   | Highest-priority task authority                                    | Not stored as repository policy by this leaf.           |
> | Canonical repository policy | `docs/00.agent-governance/`                    | Rules, scopes, contracts, catalogs, providers, and memory boundary | Tracked text proves definition, not runtime compliance. |
> | Entry shims                 | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`          | Short bootstrap routes                                             | Presence does not prove a provider loaded them.         |
> | Provider overlays           | `providers/{agents-md,claude,codex,gemini}.md` | Provider-native translation within Stage 00 bounds                 | Narrative owner, not a live provider setting.           |
> | Runtime adapters            | `.claude/`, `.codex/`, `.gemini/`              | Generated agents, skills/settings, and hook wiring                 | **Configured**, not **executed**.                       |
> | Compatibility               | `.agents/`                                     | Shared skills and compatibility projections                        | Not a native policy owner.                              |
>
> Claude documents `CLAUDE.md`, scoped rules, imports, and auto memory as
> context rather than enforced configuration; hard blocking belongs in settings
> or hooks. Codex documents repository instruction discovery through `AGENTS.md`
> and allows a separate model-instruction replacement path. These mechanisms are
> not interchangeable, so the common contract is semantic: discover applicable
> authority, load the minimum context, preserve provider-native syntax, and
> verify the result.
>
> ### Three distinct precedence systems, disentangled
>
> This axis is easy to conflate because three separate precedence orders exist
> at once, only one of which this repository authors:
>
> > Historical evidence (not current authority; source: Git history): Recorded source path at the document observation baseline.
> >
> > 1. **This repository's instruction hierarchy** (`providers/agents-md.md` §4,
> >    read directly): (1) direct user/system instructions — always win; (2)
> >    `docs/00.agent-governance/` — authoritative for policy; (3) root shim files
> >    (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`); (4) provider overlays
> >    (`providers/{claude,codex,gemini}.md`); (5) runtime controls (`.claude/`,
> >    `.codex/`, `.gemini/`); (6) `.agents/` compatibility surfaces. This is
> >    repo-authored policy, not a vendor mechanism.
> > 2. **Claude's native settings-file precedence** (`code.claude.com/docs/en/settings`,
> >    re-verified 2026-08-14): managed > CLI arguments > `.claude/settings.local.json`
> >    > `.claude/settings.json` > `~/.claude/settings.json` — a vendor-defined
> >    > scope order for the JSON `permissions`/`hooks`/`autoMode` schema, with the
> >    > caveat that `permissions` rules _merge_ across scopes rather than strictly
> >    > overriding (any-scope `deny` wins, `allow` accumulates).
> > 3. **Claude's native CLAUDE.md load-location precedence** (`code.claude.com/docs/en/memory`,
> >    re-verified 2026-08-14): managed policy (`/etc/claude-code/CLAUDE.md` or
> >    equivalent) > user (`~/.claude/CLAUDE.md`) > project (`./CLAUDE.md` or
> >    `./.claude/CLAUDE.md`) > local (`./CLAUDE.local.md`) — a fourth, separate
> >    ordering for _which memory file_ is discovered, distinct from both (1) and
> >    (2). CLAUDE.md content is "delivered as a user message after the system
> >    prompt, not as part of the system prompt itself" per that page — an
> >    explicit vendor statement that instruction files are context, not a hard
> >    enforcement layer; only settings/hooks enforce.
>
> Re-derived directly in this worktree: this repository tracks no
> `.claude/rules/` directory, no `CLAUDE.local.md`, and only one project-scope
> `.claude/settings.json` plus one git-ignored `.claude/settings.local.json`
> (observed locally, not part of the tracked corpus). Claude's path-scoped rule
> mechanism (`.claude/rules/*.md` with `paths:` frontmatter, loaded only when a
> matching file is opened) and the `@import` mechanism (4-hop max recursion
> depth, with a one-time approval dialog for imports that resolve outside the
> working directory) are therefore vendor capabilities this workspace does not
> currently use — a negative-evidence fact, not an assumption of absence.
>
> ### User-scope instructions versus this repository's tracked policy
>
> Claude's CLAUDE.md load-location order above places "user" (`~/.claude/CLAUDE.md`
> and `~/.claude/rules/`) _before_ "project" in load order, meaning
> project-scope content is read later/closer to the working context — but
> loading order is not the same claim as this repository's own precedence list,
> which states repository governance is "authoritative for all policy matters"
> once work targets this repository, and that direct user/system turn
> instructions (distinct from a _stored_ personal config file) always win over
> everything. A personal, machine-global instruction layer can therefore
> legitimately exist for an operator working across many repositories — for
> example a global preference toward proactive subagent delegation, parallel
> task execution, or automatic skill invocation — without that layer being able
> to expand what this specific repository's `approval-boundaries.md` Hard Stops
> or the four typed harness loops (see [loop-engineering.md](./m0010-loop-engineering.md))
> permit here. This reference does not name or quote any such personal
> configuration; it records only the structural fact that this layering exists
> in Claude's own documented precedence and that this repository's governance
> explicitly does not yield policy authority to it. This is the precise
> boundary AIV-01/AIV-05 below exist to hold: a broader personal operating
> style is not itself authorization to mutate a protected surface, request an
> approval-bypassing action, or skip the independent-review loop.
>
> ### Root shim structure, re-derived
>
> All three root shims were re-read directly at this baseline (line counts
> exact):
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | File        | Lines | Loading mechanism                     | Content                                                                                                                                                                                  |
> | ----------- | ----: | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `AGENTS.md` |     7 | Prose instruction ("Load `docs/...`") | Codex's official AGENTS.md page (re-verified 2026-08-14) states content is "read and prepended to the agent's context — it's not transcluded but actively loaded," rebuilt on every run. |
> | `CLAUDE.md` |     8 | `@path` transclusion                  | Four `@docs/00.agent-governance/...` imports, expanded at session launch.                                                                                                                |
> | `GEMINI.md` |     8 | `@./path` transclusion                | Four `@./docs/00.agent-governance/...` imports — the same transclusion mechanism as Claude, not the same as `AGENTS.md`'s prose-instruction style.                                       |
>
> This is a previously unrecorded asymmetry: `GEMINI.md` mirrors Claude's
> import-based loading rather than Codex's read-and-prepend loading, even
> though `AGENTS.md` is the nominal "shared" entry point in the provider-neutral
> model. Each shim imports exactly four canonical sources in the same order
> (bootstrap, provider overlay, memory README, memory current-state), so the
> _content_ loaded is identical across all three even though _how_ it enters
> context differs by provider.
>
> ### The Canonical Adapter Model as the vibe-coding boundary
>
> `providers/agents-md.md` §5 (re-read 2026-08-14) defines a two-tier model that
> directly bounds safe conversational iteration: Tier 1 (`agents/agents/`,
> `agents/functions/`, `contracts/provider-models.yaml`) is the only place a
> role, function, model, or event is defined; Tier 2 (`.claude/`, `.codex/`,
> `.gemini/`) exposes that definition through a generated, provider-native
> adapter. Five adapter rules (name-set, role, policy, model, and validation
> parity — detailed in
> [provider-implementation-comparison.md](./m0012-provider-implementation-comparison.md))
> make this machine-checkable. The direct consequence for bounded vibe coding:
> a conversational session that hand-edits a Tier 2 file (for example adding a
> tool to `.claude/agents/qa-engineer.md` without a matching Stage 00 change)
> produces drift a validator can catch, but it is still a policy violation the
> moment it is written, not only once caught. `.claude/CLAUDE.md`'s own
> instruction — "Change canonical Stage 00 sources first, then run the
> registered provider renderer. Do not hand-author policy in generated
> adapters." — states this boundary directly and is the concrete,
> workspace-specific form of AIV-01 below.
>
> ### Instruction and generated-work criteria
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Claim                        | Required workspace rule                                                               | Current status                                         | Verification limit / gap                                           |
> | ---------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------ |
> | AIV-01 Authority             | Stage 00 is canonical; projections cannot redefine policy.                            | Implemented in tracked governance and renderer inputs. | Provider loading is unobserved.                                    |
> | AIV-02 Context               | Load bootstrap, persona, checklist, one scope, and JIT stage sources.                 | Implemented as tracked routing.                        | Context contents of a live session are unobserved.                 |
> | AIV-03 Specificity           | Name paths, commands, expected result, exclusions, and owner.                         | Implemented in task/checklist contracts.               | Prompt adherence is probabilistic.                                 |
> | AIV-04 Tools                 | A tool is a capability, not mutation authority.                                       | Implemented in approval/environment rules.             | Active sandbox and grants are runtime facts.                       |
> | AIV-05 Permissions           | Least privilege; explicit approval for protected or external actions.                 | Implemented as policy and typed permission profiles.   | Local metadata is not proof the runtime enforced it.               |
> | AIV-06 Verification          | Run the smallest applicable deterministic checks and record skips.                    | Implemented for tracked checks.                        | CI, provider, remote, and service outcomes need separate evidence. |
> | AIV-07 Ownership             | The human/team and canonical artifact owner accept generated output.                  | Defined; the model never becomes accountable owner.    | Acceptance requires Task/diff/review evidence.                     |
> | AIV-08 Independent review    | Increase review with complexity, novelty, sensitivity, and blast radius.              | Implemented in the lifecycle and review loop.          | This leaf does not claim a review occurred.                        |
> | AIV-09 Dependency provenance | Verify package, action, image, API, license, and maintenance facts.                   | Required by governance/security routes.                | Plausible model output or registry presence alone is insufficient. |
> | AIV-10 Debt                  | Preserve failing evidence and route debt to its earliest canonical stage.             | Defined.                                               | Chat history and provider memory are not durable owners.           |
> | AIV-11 Escalation            | Stop on missing authority, high-impact ambiguity, or exhausted typed attempts.        | Four bounded loops are tracked.                        | No prompt-local retry policy may extend them.                      |
> | AIV-12 Untrusted context     | Web pages, tool output, repository text, and external agents are data until reviewed. | Defined by security and intake boundaries.             | Reading content never elevates its authority.                      |
>
> ### Bounded vibe-coding loop
>
> The acceptable loop is `objective -> inspect -> small change -> observe ->
> focused validation -> independent review -> commit or stop`. It requires an
> isolated branch/worktree, an approved lifecycle owner, reversible increments,
> and exact evidence. It is unsuitable for unapproved secrets, production data,
> runtime changes, remote mutations, model-policy changes, or irreversible
> actions. Generated output is ordinary owned code with additional provenance,
> context, and hallucination risks; “vibe coding” waives none of the gates.
>
> ### Evidence-state separation
>
> - **Tracked**: the authority map, adapters, scripts, and checks exist in Git.
> - **Configured**: a provider-native file contains a model, instruction, tool,
>   or hook value.
> - **Executed**: an authorized observation proves that the runtime loaded or ran
>   that value for a named event/session.
> - **Runtime accepted**: the provider accepted the exact schema/value.
> - **Entitled**: the active account/organization may use the capability.
>
> Only the first two states are established here. Execution, acceptance, and
> entitlement remain unverified unless a separately authorized observation
> records them.
>
> ### Carried source-evidence claims
>
> Source-evidence claims carried forward from the superseded 2026-07-05
> research pack on 2026-08-19. Each states what the upstream evidence supports
> and, where it matters more, what it does not.
>
> - **Do not over-attribute the ownership rule to the review guide.** The cited GitHub review page emphasises that human judgement stays essential but states no formal ownership-assignment rule. The normative half of the ownership criterion rests on NIST SSDF v1.1; the GitHub page backs only the weaker claim. Attributing the stronger rule to the secondary source overstates it.
> - **Slopsquatting is why a registry lookup is not verification.** The upstream source names slopsquatting, the registration of package names that models are known to hallucinate. Registry presence alone therefore does not verify a suggested dependency, because the attack works by making the hallucinated name resolve.
> - **The vibe-coding tutorial has six phases, not five.** The tutorial names six phases: Researching with Copilot, Planning the implementation, Building your application with Copilot cloud agent, Testing your application, Iterating on changes, and Improving your software project. An earlier five-phase research, plan, implement, test, iterate summary was wrong and omitted the final phase, and its implementation phase is specific to cloud agents.
> - **Three criteria rest on a source nobody has re-read.** The practical-guide CDN URL resolves and returns a 7,335,065-byte PDF with no extractable text layer, so the claims behind three named criteria — `AIV-04`, `AIV-11` and `AIV-15` — are carried from an earlier verification rather than re-read. The obstacle is extraction, not access. The claims behind `AIV-04`, `AIV-11` and `AIV-15` are `UNVERIFIED` on that basis and must not be read as freshly confirmed. Naming them is load-bearing: an unnamed marker attaches to no criterion, and two of the three carry no marker at their own entries.
>
> ### Instruction layers and generated-work boundary
>
> | Layer | Responsibility | Evidence limit |
> | --- | --- | --- |
> | Direct task authority | Sets the immediate request and higher-priority constraints. | Not a repository runtime proof. |
> | Canonical policy and role | Defines shared ownership, permissions, and completion criteria. | Tracked definition only. |
> | Root entry and provider adapter | Routes bootstrap and native syntax. | Presence does not prove loading. |
> | Skill body | Supplies task-specific instructions through progressive discovery. | Discovery/invocation remains unobserved. |
> | Native configuration/hooks | Encodes provider mechanics. | Configuration is not execution. |
> | Prompt-generated output | Proposed work requiring normal validation and review. | Never self-authenticates. |
>
> A bounded conversational loop begins by discovering the applicable authority
> and only the relevant skill material. It then produces the smallest scoped
> change, checks it with the named gate, and gives an independent reviewer the
> exact diff and evidence. Missing authority, a protected surface, source
> insufficiency, or a failed narrow correction is an escalation point—not an
> invitation to keep prompting.
>
> The retained sources distinguish the native discovery mechanisms: Claude's
> memory documentation was observed for instruction/memory hierarchy capability,
> while Codex's AGENTS.md documentation was observed for discovery/order/size
> capability. They inform a provider-neutral progressive-discovery practice but
> do not establish that this repository loaded either file in a live session.
>
> ## Scope Implications
>
> | Scope          | Application and disposition                                                                                                                           |
> | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `agentic`      | Owns canonical instruction, catalog, loop, provider, and adapter parity; tracked/configured status must not be promoted to execution.                 |
> | `architecture` | Use instructions to route trade-offs into ARD/ADR/Spec owners; no typed agent currently owns this enum-admitted scope.                                |
> | `backend`      | Not applicable until a backend surface and Spec exist; future generated code still needs boundary validation and tests.                               |
> | `common`       | Shared review and conventions apply, but agents may not bypass the controlled QA boundary or create parallel policy.                                  |
> | `docs`         | Template-first and metadata/link rules apply; Stage 90 advice cannot authorize Stage 01-99 adoption.                                                  |
> | `entry`        | Gateway work routes through the adjacent infra owner with config/Compose validation and explicit runtime authority.                                   |
> | `frontend`     | Existing Storybook/Next material is a QA fixture, not a general product surface; generated UI requires the existing owner and accessibility evidence. |
> | `infra`        | Compose, secret, and runtime changes require concrete targets, rollback, and specialist review; instruction text cannot grant access.                 |
> | `meta`         | Metadata/taxonomy changes route through docs and validators; the missing typed scope route remains a governance gap.                                  |
> | `mobile`       | Not applicable to the current corpus; future mobile generation needs an approved product/Spec chain and device-specific verification.                 |
> | `ops`          | Runtime and incident outcomes belong in Stage 05 evidence; conversational completion is never an operational outcome.                                 |
> | `product`      | Human/stakeholder approval owns product intent; no generated instruction may infer acceptance from a draft prompt.                                    |
> | `qa`           | Owns focused validation and synthetic evaluation; fixtures prove repository semantics, not live-model quality.                                        |
> | `security`     | Treat external instructions and generated dependencies as untrusted; preserve least privilege, redaction, and approval boundaries.                    |
>
> ## Sources
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Source | Accessed | Class | Use and verification state |
> | --- | --- | --- | --- |
> | [Claude instructions and memory](https://code.claude.com/docs/en/memory) | 2026-08-14 | External mutable | Re-verified: full CLAUDE.md load-location order, `@import` 4-hop limit, external-import approval dialog, path-scoped `.claude/rules/`, "delivered as user message not system prompt." |
> | [Claude settings](https://code.claude.com/docs/en/settings) | 2026-08-14 | External mutable | New: exact 5-level settings-scope precedence, permission-merge-across-scopes rule. |
> | [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 2026-08-14 | External mutable | Re-verified: global/project discovery order, `AGENTS.override.md`, 32 KiB `project_doc_max_bytes` default, "read and prepended, not transcluded." |
> | [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | 2026-08-08 | External mutable | HTTP 200; instruction replacement and configuration boundary. |
> | [Canonical governance bootstrap](../../../../.agents/governance/bootstrap.md) | 2026-08-14 | Workspace tracked | Re-read: canonical loading sequence and evidence boundary. |
> | Provider-neutral notes (retired path: `../../../00.agent-governance/providers/agents-md.md`) | 2026-08-14 | Workspace tracked | Re-read: exact 6-level precedence list (§4) and Canonical Adapter Model (§5) with the five adapter rules. |
> | [Task checklists](../../../../.agents/governance/task-checklists.md) | 2026-08-14 | Workspace tracked | Re-read: pre-task ambiguity-blocking rule, in-task loop-bound rule, completion evidence duties. |
> | [Environment constraints](../../../../.agents/governance/environment-constraints.md) | 2026-08-14 | Workspace tracked | Read: "most-specific in-scope instruction file wins" and "system/developer/direct user instructions always override repository instruction files." |
> | Root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) | 2026-08-14 | Workspace tracked | Read directly: exact line counts and `@`-import vs. prose-instruction loading mechanism per file. |
> | Graphify report (`graphify-out/GRAPH_REPORT.md`, untracked local output since 2026-09-08) | 2026-08-08 | Workspace stale/advisory | Built from `f8a72211`; corroborated against tracked sources and not used as current proof. |
>
> ## Scope Application
>
> | Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
> | --- | --- | --- | --- | --- |
> | agentic | applies | Resolve instruction layers before work. | Inspect bootstrap precedence, then the matching adapter and selected skill body. | Loading unobserved. |
> | architecture | applies | Route generated design claims to owners. | Review source and authority. | No architecture decision. |
> | common | applies | Keep projections subordinate to policy. | Inspect canonical source first. | No enforcement proof. |
> | docs | applies | Review generated prose and links. | Run focused metadata/link checks. | Plausibility is insufficient. |
> | infra | applies | Escalate runtime-affecting prompts. | Require explicit approval. | No environment access. |
> | ops | applies | Hand off operational generation to ops. | Preserve sanitized evidence. | No runbook execution. |
> | qa | applies | Require independent review after checks. | Inspect exact diff, named validation gate, and reviewer evidence. | No self-acceptance. |
> | security | applies | Reject prompts seeking secrets or bypasses. | Confirm excluded-material boundary. | No security execution. |
>
> ## 2026-09-05 Revalidation
>
> Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
> Claude's current feature guide still separates always-loaded instructions,
> on-demand skills, and deterministic hooks; OpenAI's current Codex material
> likewise treats repository instructions, sandboxing, and approvals as distinct
> control surfaces. The repository maps those ideas through root `AGENTS.md` and
> `CLAUDE.md` into Stage 00 and provider adapters.
>
> | Capability | Repository implementation | Evidence depth | Gap | Verification route |
> | --- | --- | --- | --- | --- |
> | Instruction priority | Root entrypoints load bootstrap plus provider adapter | Configured, Repository-enforced | Provider system prompts remain external | provider-surface and agent-governance checks |
> | Command safety | Approval policy and pre-tool hooks constrain selected actions | Defined, Configured | Native enforcement differs by provider | hook parity report plus bounded provider acceptance |
> | Bounded vibe coding | Spec/Task and quality gates separate intent from edits | Repository-enforced | Adherence quality is not a static property | exact-diff review and Task evidence |
>
> Recommendation: keep durable policy in Stage 00, enforcement in hooks/sandbox,
> and task-specific intent in the active Task; do not copy provider system prompts
> into this repository. Re-opened official sources:
> [Claude features](https://code.claude.com/docs/en/features-overview) and
> [Codex safety](https://openai.com/index/running-codex-safely/).
>
> ## Maintenance
>
> Recheck when instruction discovery, provider precedence, adapter generation,
> permission controls, the typed loops, or generated-code review rules change.
> Preserve the five evidence states above and never infer live compliance from a
> tracked file.

## Limitations

### Future Internal Checks

Candidate surfaces do not assert implementation. These checks require a separate authorized task.

| Topic / claim ID | Analytical scope | Applicability condition | Future surface candidates | Concrete question | Required evidence | Future method | Pass/fail criterion | Additional authorization / risk | Likely role | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0001-01–03 / discovery | Repository/directory/session; governance/instruction discovery | If parity is evaluated | AGENTS.md, canonical bootstrap, provider adapters | Which owners load automatically, explicitly or not at all, and are stack/coding constraints distinct from role/tool authority and output preferences? | Version, launch path, fixture tree, loading trace, canonical owner links and separate coding/style expectations | Approved disposable nested-directory fixture | Expected precedence/read observed; silent omission fails | Separate runtime authorization; no private/global-state export | rules-engineer / reviewer | Not assessed in this run |
| C-m0001-04 / exploration | Task/Spec; implementation/quality/governance | If a draft is promoted | Existing Spec/Plan/Task and review prompts | Are scope, stop and behavior checks recorded? | Representative draft, check output, independent review | Document review then authorized reversible trial | Promotion requires observable acceptance; self-declaration fails | Implementation/runtime checks separately authorized | planner / code-reviewer | Not assessed in this run |

## Sources

### Claims and Sources

| Claim ID | Claim | Source ID / detail section | Publication/revision date | Checked at | Product / version / channel | Fact / interpretation / recommendation | Limits / conflict / recheck | Internal adoption |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0001-01 | Codex instruction discovery | [S-learn-chatgpt-com-agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md); How Codex discovers guidance | Not displayed | 2026-09-27 | Codex CLI / Claude Code; version conditions above | Fact | Current documented behavior; installed version unexamined | Not assessed in this run |
| C-m0001-02 | Claude native AGENTS loading | [S-code-claude-com-memory](https://code.claude.com/docs/en/memory); AGENTS.md and instructionFiles | Not displayed; explicit version boundaries in text | 2026-09-27 | Codex CLI / Claude Code; version conditions above | Fact | Version/plugin/launch-path conditional | Not assessed in this run |
| C-m0001-03 | Shared filenames differ in semantics | [S-learn-chatgpt-com-agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md); How Codex discovers guidance; [S-code-claude-com-memory](https://code.claude.com/docs/en/memory); AGENTS.md and instructionFiles | Not displayed / Not displayed; explicit version boundaries in text | 2026-09-27 | Codex CLI / Claude Code; version conditions above | Interpretation | Common semantics require separate acceptance evidence | Not assessed in this run |
| C-m0001-04 | Bounded exploratory promotion | [S-anthropic-com-building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents); When to use agents / Agents | 2024-12-19 | 2026-09-27 | Codex CLI / Claude Code; version conditions above | Recommendation | Only where scope and completion can be observed | Not assessed in this run |

| Source ID | Original and detail location | Publication/revision date | Checked at | Product/channel/version and stability | Limitation |
| --- | --- | --- | --- | --- | --- |
| S-learn-chatgpt-com-agents-md | [Original](https://learn.chatgpt.com/docs/agent-configuration/agents-md); How Codex discovers guidance | Not displayed | 2026-09-27 | Codex CLI current mutable documentation; no installed version/stability guarantee checked | Legacy developer URL redirected; loading not exercised |
| S-code-claude-com-memory | [Original](https://code.claude.com/docs/en/memory); AGENTS.md and instructionFiles | Not displayed; explicit version boundaries in text | 2026-09-27 | Claude Code bundled plugin v2.1.277+, exceptions before v2.1.281; mutable docs | InstructionsLoaded/import behavior remains native; memory mechanics in m0012 |
| S-anthropic-com-building-effective-agents | [Original](https://www.anthropic.com/engineering/building-effective-agents); When to use agents / Agents | 2024-12-19 | 2026-09-27 | Historical engineering design advice, not product support contract | Later landscape acknowledged; no local outcome established |
