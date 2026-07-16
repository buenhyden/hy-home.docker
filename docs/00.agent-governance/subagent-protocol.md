---
layer: agentic
---

# Subagent Protocol

Spawning, communication, and lifecycle rules for subagents in `hy-home.docker`.

## 1. Spawn Rules

- Spawn subagents through the active runtime's delegated-agent facility — never via inline prompt embedding.
- The Stage 00 catalog entry for the supervisor is
  `docs/00.agent-governance/agents/agents/workflow-supervisor.md`; each
  provider exposes a runtime adapter for that role.
- Each subagent MUST load exactly one primary scope file through the active
  runtime's supported context or delegation mechanism before acting.
- Pass the scope path explicitly in the task prompt; do not rely on ambient context.
- The supervising/orchestrating agent uses the top-spec model; worker subagents use the right-sized model per the Model Policy below.
- Each runtime's agent frontmatter MUST carry that provider's own model identifier; never copy another provider's model name across surfaces.

### Model Policy (work-profile mapping)

Exact provider status, entitlement, runtime acceptance, supported controls,
fallbacks, source URLs, and the historical cutoff are owned by
`contracts/provider-models.yaml`. This table is the human routing view.

| Work profile | Claude | GPT / Codex | Gemini |
| --- | --- | --- | --- |
| Supervision, architecture, final synthesis | `claude-opus-4-8` (adaptive thinking; `high` effort) | `gpt-5.6` (`xhigh`) | `gemini-3.5-flash` (`high`) |
| Complex implementation, security, precision review | `claude-sonnet-5` (adaptive thinking; `high` effort) | `gpt-5.6` (`high`) | `gemini-3.5-flash` (`high`) |
| Exploration, large reads, repetitive organization | `claude-haiku-4-5-20251001` (extended thinking; no effort control) | `gpt-5.6-terra` (`low`) | `gemini-3.1-flash-lite` (`minimal`) |

- `workflow-supervisor` is the only supervisor-tier role. Other agents select
  the profile declared in `contracts/agent-catalog.yaml`.
- Generated Claude agents never emit per-agent `thinking`; Claude inherits
  thinking from the session. Native subagent `effort` is distinct and
  overrides the session value, so Sonnet and Opus work profiles emit `high`
  while the Haiku profile omits the key. Stage 00 separately records model
  capability: Fable/Mythos use always-on adaptive thinking, Opus 4.8 uses
  opt-in adaptive thinking, Sonnet 5 defaults to adaptive thinking and permits
  disabling it, and Haiku 4.5 uses extended thinking. Supported effort values
  for Fable, Mythos, Opus, and Sonnet are `low`, `medium`, `high`, `xhigh`, and
  `max`.
- Codex TOML adapters include `model_reasoning_effort`. The repository pins
  only controls allowed by the selected model record.
- Gemini adapters select a model but do not invent a per-agent sandbox or
  reasoning field. Least privilege is expressed through agent tools and the
  executing runtime's policy/sandbox controls.
- OpenAI lists GPT-5.6 Sol/Terra but does not assign a stable lifecycle label.
  The contract therefore records `listed` / `unclassified-listed`, separates
  the 2026-07-10 10:00 KST cutoff from the later retrieval, and leaves local
  entitlement/runtime acceptance at `needs_revalidation`.
- Fable, Spark, Mythos, deprecated entries, and Gemini Pro preview are
  catalog-only. Mutable catalogs retrieved after the cutoff are explicitly
  `historical-state-unverified`. A degraded fallback references one typed
  provider/source/target/profile edge in `fallback_approvals`, whose authority
  resolves to Spec 132 `#approved-fallback-edges`; Sonnet 5 complex work may
  escalate to Opus 4.8 only through that recorded edge. Historical status can
  become verified only through a typed evidence record on an allowlisted
  official domain with `published_at` at or before cutoff and `observed_at`
  equal to retrieval. The current evidence registry is intentionally empty,
  including for unresolved GPT-5.6 history.

### Model and Provider Adapter Change Protocol

User approval may authorize model policy or provider adapter changes, but those
changes are valid only when the same task updates all coupled surfaces:

- this Model Policy table or the documented override rule,
- provider adapter generation logic,
- generated provider adapters,
- repository validators that enforce allowed values,
- Stage 04 task evidence with the exact approved value, target role, source of
  evidence, and provider sync result.

If the task does not name a concrete model value, role, provider, and validation
path, the approval is recorded as verified-only and existing model/provider
adapter values remain unchanged.

## 2. Required Delegation Envelope

```text
Primary scope: docs/00.agent-governance/scopes/<layer>.md
# Role: <agent-name> — <one-line purpose>
# Pattern: <pattern-name>
```

## 3. Agent Catalog Reference

### Supervising Runtime Agent

| Governance Role | Scope Import | Stage 00 Catalog | Claude Adapter | Codex Adapter | Compatibility Projection |
| --- | --- | --- | --- | --- | --- |
| `workflow-supervisor` | `scopes/agentic.md` | `agents/agents/workflow-supervisor.md` | `.claude/agents/workflow-supervisor.md` | `.codex/agents/workflow-supervisor.toml` | `.agents/agents/workflow-supervisor.md` |

The supervisor coordinates workers and should not be treated as a generic worker replacement.

### Worker Agents

All worker agents use the same adapter pattern:

| Governance Role | Scope Import | Stage 00 Catalog | Claude Adapter | Codex Adapter | Compatibility Projection |
| --- | --- | --- | --- | --- | --- |
| `infra-implementer` | `scopes/infra.md` | `agents/agents/infra-implementer.md` | `.claude/agents/infra-implementer.md` | `.codex/agents/infra-implementer.toml` | `.agents/agents/infra-implementer.md` |
| `security-auditor` | `scopes/security.md` | `agents/agents/security-auditor.md` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` | `.agents/agents/security-auditor.md` |
| `incident-responder` | `scopes/ops.md` | `agents/agents/incident-responder.md` | `.claude/agents/incident-responder.md` | `.codex/agents/incident-responder.toml` | `.agents/agents/incident-responder.md` |
| `code-reviewer` | `scopes/common.md` | `agents/agents/code-reviewer.md` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` | `.agents/agents/code-reviewer.md` |
| `doc-writer` | `scopes/docs.md` | `agents/agents/doc-writer.md` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` | `.agents/agents/doc-writer.md` |
| `iac-reviewer` | `scopes/infra.md` | `agents/agents/iac-reviewer.md` | `.claude/agents/iac-reviewer.md` | `.codex/agents/iac-reviewer.toml` | `.agents/agents/iac-reviewer.md` |
| `drift-detector` | `scopes/infra.md` | `agents/agents/drift-detector.md` | `.claude/agents/drift-detector.md` | `.codex/agents/drift-detector.toml` | `.agents/agents/drift-detector.md` |
| `qa-engineer` | `scopes/qa.md` | `agents/agents/qa-engineer.md` | `.claude/agents/qa-engineer.md` | `.codex/agents/qa-engineer.toml` | `.agents/agents/qa-engineer.md` |
| `eval-engineer` | `scopes/qa.md` | `agents/agents/eval-engineer.md` | `.claude/agents/eval-engineer.md` | `.codex/agents/eval-engineer.toml` | `.agents/agents/eval-engineer.md` |
| `ci-cd-engineer` | `scopes/ops.md` | `agents/agents/ci-cd-engineer.md` | `.claude/agents/ci-cd-engineer.md` | `.codex/agents/ci-cd-engineer.toml` | `.agents/agents/ci-cd-engineer.md` |
| `skill-creator` | `scopes/agentic.md` | `agents/agents/skill-creator.md` | `.claude/agents/skill-creator.md` | `.codex/agents/skill-creator.toml` | `.agents/agents/skill-creator.md` |
| `hook-developer` | `scopes/agentic.md` | `agents/agents/hook-developer.md` | `.claude/agents/hook-developer.md` | `.codex/agents/hook-developer.toml` | `.agents/agents/hook-developer.md` |
| `rules-engineer` | `scopes/agentic.md` | `agents/agents/rules-engineer.md` | `.claude/agents/rules-engineer.md` | `.codex/agents/rules-engineer.toml` | `.agents/agents/rules-engineer.md` |

Per the Stage 00 Canonical Adapter Model (`providers/agents-md.md` §5): Stage 00
is canonical, provider surfaces are adapters, and all surfaces carry the same
agent name set.

## 4. Communication Protocol

- **Data handoff**: write non-secret runtime intermediate artifacts to `_workspace/repo-support/<phase>_<agent>_<artifact>.<ext>`.
- **Audit handoff**: write orchestration reports, matrices, plans, and approval handoffs to `.agent-work/report/` when a workflow prompt requires that location.
- **Status updates**: use the active runtime's status mechanism and the shared
  `in_progress` → `completed` or `failed` semantics.
- **Conflict**: if file ownership conflicts arise, halt and escalate to user — do not overwrite.
- **Prohibited data**: do not store diagnostics dumps, local logs, raw logs,
  auth files, tokens, credentials, private keys, shell history, secret values,
  or token-bearing command output in `_workspace`.

## 5. Error Handling

`contracts/provider-models.yaml` owns the exact semantic loop values. Agents
must not invent an additional retry policy in prompts or provider adapters.

1. Bootstrap has one attempt and escalates when the bootstrap contract does
   not pass.
2. Implementation has at most two attempts. After the first focused-check
   failure, narrow scope; after the second, escalate.
3. Independent review has at most two attempts and stops only when Critical and
   Important findings are zero. The reviewer must differ from the loop owner.
4. The approved all-files gate has one attempt through the controlled wrapper;
   on failure, record the result and stop.
5. Evidence contains only `command`, `result`, `rollback`, and
   `skipped_checks`. Never include raw logs, auth files, credentials, tokens,
   secret values, or shell history.
6. Never silently discard output. Record the value-free failure code and the
   unresolved gap in Stage 04 task evidence.

## 6. Lifecycle

```text
Spawn → load scope → execute → write repo-support artifact → report completion → promote durable evidence or cleanup ignored scratch
```

Ignored `_workspace/repo-support/` scratch files are task-local. Promote durable
non-secret outcomes to Stage 04 task evidence, Stage 90 references, or Stage 00
memory before completion. Do not delete user-created scratch artifacts without
explicit approval.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/postflight-checklist.md`
- `docs/01.requirements/024-agent-governance-standardization.md`
- `docs/02.architecture/requirements/0027-agent-governance-canonical-adapter.md`
- `docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md`
- `AGENTS.md` — Runtime Surfaces
- `docs/00.agent-governance/agents/README.md`
- `.claude/agents/workflow-supervisor.md`
