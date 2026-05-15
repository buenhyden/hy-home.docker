---
layer: agentic
---

# Memory: Harness and Agent-first Gap Audit

- Date: 2026-05-09
- Layer: agentic
- Status: active
- Applies To: `AGENTS.md`, `.claude/settings.json`, graphify workflow, agent-first runtime surfaces
- Tags: #harness #agent-first #runtime #governance
- Retrieval Keywords: agent-first gap audit, graphify CLI fallback, rg permission, runtime governance surface
- Last Verified: 2026-05-10

## Problem

The workspace already implements most of the harness and Agent-first engineering
surface, but the audit found two operational gaps that could cause agents to
either skip a useful repository discovery tool or claim an impossible graph
refresh.

## Context

The audit compared root shims, governance docs, runtime mirrors, hooks, and
repository contract checks against the intended agent-first execution model.

## Harness Engineering Components

- Entry shims: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` route agents into the
  repository governance layer.
- Governance SSOT: `docs/00.agent-governance/` owns shared rules, scopes,
  provider notes, memory, and protocol documents.
- Runtime mirror: `.claude/agents/` and `.claude/skills/` mirror the governance
  agent and function catalog.
- Orchestration split: `workflow-supervisor` remains the supervisor, while
  worker agents remain scoped domain executors.
- Scope imports: runtime agents import exactly one governance scope.
- Hooks and gates: pre-tool context, post-edit validation, repository contracts,
  hardening checks, and Docker Compose validation provide guardrails.
- Context graph: `graphify-out/` provides repository graph context for agent
  discovery and architecture/codebase answers.
- Provider boundaries: `.codex` remains a hook/context surface, not a parallel
  delegated-agent catalog.

## Agent-first Engineering Components

- Bootstrap: agents load shared rules, persona guidance, checklists, one scope,
  and task-specific docs only when needed.
- Canonical routing: active docs stay in numbered stage folders and templates
  govern any new stage artifacts.
- Minimal change discipline: root shims stay thin and detailed policy remains in
  governance documents.
- Verification: repository contracts, traceability checks, security baselines,
  hardening checks, and compose validation define completion evidence.
- Safety: provider notes, permissions, deny lists, and local/global boundary
  rules keep runtime changes auditable.
- Handoff: memory notes and progress entries preserve decisions without making
  memory the policy source of truth.

## Gaps

- `AGENTS.md` required `graphify update .` after code edits even when the
  `graphify` CLI was unavailable in the local runtime.
- `.claude/settings.json` allowed `grep` but did not allow `rg`, even though
  repository and developer guidance prefer `rg` for discovery.

## Resolution

- Keep root shims thin and update only the Graphify fallback wording.
- Add `Bash(rg:*)` as a read-only Claude discovery permission.
- Extend `scripts/validation/check-repo-contracts.sh` so these two runtime expectations are
  covered by the existing repository contract gate.
- Do not add stage docs, GitHub-native instruction files, global configuration,
  or a parallel Codex agent catalog.

## Prevention

- Keep graphify usage advisory when the CLI is unavailable or output is noisy.
- Keep read-only discovery commands such as `rg` available to runtime agents.
- Verify runtime-surface assumptions through `scripts/validation/check-repo-contracts.sh`.

## Evidence

- `AGENTS.md`
- `.claude/settings.json`
- `scripts/validation/check-repo-contracts.sh`
- `docs/00.agent-governance/memory/progress.md`

## Related Documents

- `AGENTS.md`
- `.claude/settings.json`
- `scripts/validation/check-repo-contracts.sh`
- `docs/00.agent-governance/memory/progress.md`
- `docs/00.agent-governance/memory/agentic-harness-contract-hardening.md`
