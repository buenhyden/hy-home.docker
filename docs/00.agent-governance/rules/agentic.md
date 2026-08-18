---
layer: agentic
---

# AI Agent-first Engineering Rule

Standard behavior contract for repo-local, auditable agent execution.

## 1. Context and Objective

- Treat AI agents as first-class engineering workers with explicit routing,
  scoped ownership, and verification evidence.
- Keep outcomes deterministic, auditable, verifiable, and context-efficient.
- Prefer repository evidence, explicit assumptions, and traceable decisions over
  implicit behavior.

## 2. Requirements and Constraints

- Start with non-mutating discovery before any change.
- Produce implementation plans for multi-step work before edits, unless the user
  already supplied an implementation-ready plan.
- Keep audit, planning, implementation, and verification roles separate when a
  workflow prompt defines those phases.
- Do not execute implementation-agent changes until the approved plan path
  required by the workflow exists and the requested edits map to that plan.
- Ask for clarification before changing state when a request is underspecified,
  constraints conflict, or a plausible assumption could change the outcome.
  Record low-risk assumptions explicitly when proceeding without a question.
- Use the registered agent identity and primary scope selected by
  `contracts/agent-catalog.yaml`; `rules/bootstrap.md` owns the load order.
- Use the local agent/function catalog as the runtime boundary:
  - Provider agent adapters under `.claude/agents/`, `.codex/agents/`, and
    `.gemini/agents/` must map to a same-named Stage 00 catalog entry.
  - Shared skill projections use `.claude/skills/<id>/SKILL.md` and
    `.agents/skills/<id>/SKILL.md`; provider projections do not own policy.
  - Runtime baselines: Claude uses `.claude/`, Codex uses `.codex/`, Gemini
    uses `.gemini/`, and `.agents/` remains compatibility/shared skills.
  - `docs/00.agent-governance/subagent-protocol.md` defines delegation rules.
- Do not import external harness identities or create GitHub-native instruction
  layers for local execution policy.
- Use `docs/00.agent-governance/memory/README.md` and `memory/current.md` for
  the bounded active handoff, and use other Memory notes only as advisory
  retrieval context. `memory/progress.md` is append-preserved historical
  navigation. Memory must not override current rules, scopes, provider
  overlays, direct user instructions, or live repository evidence.
- Route document language through
  `rules/documentation-protocol.md#31-language-boundary-by-document-role` and
  conversational language through `rules/output-style.md`.

## 3. Workflow Routing

`rules/workflows.md` owns the provider-neutral lifecycle and supporting
workflows. This rule supplies execution constraints only and does not define a
second sequence. Use `rules/task-checklists.md` for pre-task, in-task, and
completion evidence.

### Typed Harness and Workflow

- `contracts/provider-models.yaml` owns exactly eight control-plane layers:
  canonical contract, role/function routing, permission/mutation boundary,
  provider model/reasoning policy, semantic event hooks, controlled QA and
  validation, tracked CI, and sanitized evidence/handoff.
- The lifecycle and its exact state order are owned by
  [`workflows.md`](./workflows.md). This rule adds no second sequence.
- Harness layers apply controls to lifecycle states; they are not another
  phase sequence. Existing `harness_loops` are bounded retry/event controls and
  must name their applicable `workflow_states`.
- Failed validation returns to `implement`, rejected design remains in
  `design/plan`, missing authority remains in `approval`, and exhausted
  attempts stop without expanding scope.
- Approval is explicit user or governing evidence and cannot be inferred from
  a provider handoff, hook event, model selection, or tool transition.
- Layer, state, and loop evidence remains limited to `command`, `result`,
  `rollback`, and `skipped_checks`.

## 4. Operational Procedures

- Provide concise progress updates during long operations.
- Stop and request clarification when constraints conflict.
- Stop and request clarification when the task is underspecified and a wrong
  assumption could cause policy drift, data loss, security exposure, or unrelated
  edits.
- Prefer root-cause analysis over symptom patching.
- Route cross-domain or multi-agent work through `workflow-supervisor`.
- Delegate only to workers listed in `subagent-protocol.md`; do not invent
  runtime teams or untracked roles.
- Prefer existing repository validators before adding new checks.

## 5. Maintenance and Safety

- Keep policy text short and actionable.
- Remove contradictory guidance immediately.
- Keep provider-specific behavior in provider files, not in generic scope/rule files.
- Keep runtime behavior synchronized across the active provider's runtime surface and the corresponding
  `docs/00.agent-governance/agents/` catalog entries.
- Record work progress and final evidence in the applicable co-located Task and
  keep `docs/00.agent-governance/memory/current.md` bounded to the next handoff.
- Record historical notes under `docs/00.agent-governance/memory/` from
  `docs/99.templates/templates/governance/memory.template.md`; do not use memory notes as active policy.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/persona.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/subagent-protocol.md`
