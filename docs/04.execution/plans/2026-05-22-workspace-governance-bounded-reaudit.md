---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-22-workspace-governance-bounded-reaudit.md -->

# Workspace Governance Bounded Re-audit Implementation Plan

> Plan for a full workspace governance re-audit with bounded, evidence-backed remediation.

## Overview

This document is the implementation plan for a full re-audit of the `hy-home.docker` documentation lifecycle, template contract, cross-links, AI Agent runtime, hooks, subagents, memory, rules, and scope while correcting only verifiable drift.

This work does not create a new system. Because the current validator baseline passes, it fixes only evidence-backed items such as state drift that describes completed work as active, memory notes that conflict with the latest validation results, and missing memory edit hook guidance.

## Context

The current baseline is stable.

- `bash scripts/validation/check-repo-contracts.sh` passes with `failures=0`.
- `bash scripts/validation/check-doc-traceability.sh` passes operations/execution traceability synchronization.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` reports that the generated LLM Wiki index is fresh.
- `bash scripts/knowledge/report-graphify-health.sh` reports no contamination, but remains advisory because `surprising_cross_root_inferred_edges=3`.

The actual drift found in the audit is small. Completed 2026-05-22 plan/task artifacts are described as `Active` in parent READMEs, and some memory notes describe legacy debt that conflicts with the latest validator metrics as if it were current backlog. Target-stage docs and README edits also have PreToolUse guidance, but governance memory note edits do not have guidance at the same level.

## Goals & In-Scope

- **Goals**:
  - `GOV-RA-001`: Re-audit docs/01~05, docs/90, docs/99, README, root shims, runtime surfaces, hooks, subagents, memory, rules, and scopes.
  - `GOV-RA-002`: Describe completed 2026-05-22 execution artifacts as completed/current evidence in parent READMEs.
  - `GOV-RA-003`: Align stale memory notes with the latest validator evidence.
  - `GOV-RA-004`: Add hook/Hookify guidance for memory note edits.
  - `GOV-RA-005`: Make the repository contract catch README drift that describes completed execution artifacts as active.
- **In Scope**:
  - `docs/04.execution/**` plan/task evidence and indexes
  - `docs/00.agent-governance/memory/**`
  - `scripts/hooks/agent-event-hook.sh`
  - `.claude/hookify.*.local.md`
  - `.codex/README.md`
  - `scripts/validation/check-repo-contracts.sh`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Docker runtime behavior, service topology, ports, networks, images, volumes, or secrets are not changed.
  - Historical evidence is not rewritten for style.
  - Root shims are not expanded into policy documents.
- **Out of Scope**:
  - secret values, credentials, private keys, shell history, log databases, and personal runtime settings
  - existing untracked `projects/storybook/mcp/`
  - broad template normalization when validators already prove normalized coverage

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-GOV-RA-001 | Add plan/task evidence and execution index links | `docs/04.execution/**` | GOV-RA-001 | New evidence is reachable from execution READMEs |
| PLN-GOV-RA-002 | Fix completed 2026-05-22 artifacts described as active | `docs/04.execution/README.md`, `plans/README.md`, `tasks/README.md` | GOV-RA-002 | No completed 2026-05-22 execution file is described as active |
| PLN-GOV-RA-003 | Refresh stale memory notes with current validator evidence | `docs/00.agent-governance/memory/*.md` | GOV-RA-003 | Notes no longer present closed debt as current backlog |
| PLN-GOV-RA-004 | Add memory edit guidance to hooks and Hookify | `scripts/hooks/agent-event-hook.sh`, `.claude/hookify.*`, `.codex/README.md` | GOV-RA-004 | Hook smoke test emits memory guidance |
| PLN-GOV-RA-005 | Add validator coverage for completed-vs-active README drift | `scripts/validation/check-repo-contracts.sh` | GOV-RA-005 | Repository contract fails on completed execution docs labeled active |
| PLN-GOV-RA-006 | Run full verification and record evidence | validators, Graphify, hook samples, progress log | GOV-RA-001 | Required checks pass or advisory reason is recorded |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-GOV-RA-001 | Syntax | Shell syntax and patch hygiene | `git diff --check` and `bash -n scripts/validation/check-repo-contracts.sh scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh` | exit code 0 |
| VAL-GOV-RA-002 | JSON | Hook config validity | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | both exit code 0 |
| VAL-GOV-RA-003 | Contract | Repository docs/runtime contract | `bash scripts/validation/check-repo-contracts.sh` | exit code 0 |
| VAL-GOV-RA-004 | Traceability | Execution and operations traceability | `bash scripts/validation/check-doc-traceability.sh` | exit code 0 |
| VAL-GOV-RA-005 | Security Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | exit code 0 |
| VAL-GOV-RA-006 | Generated Docs | LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | exit code 0 |
| VAL-GOV-RA-007 | Compose | Compose static validation | `bash scripts/validation/validate-docker-compose.sh` | exit code 0 |
| VAL-GOV-RA-008 | Hooks | Target-stage, README, memory, and Stop hook smoke tests | sample JSON piped to `scripts/hooks/agent-event-hook.sh` | expected guidance or block decision observed |
| VAL-GOV-RA-009 | Graphify | Graph health status | `bash scripts/knowledge/report-graphify-health.sh` | clean or advisory reason recorded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Re-audit expands into historical rewrites | High | Fix only validator-backed or evidence-backed drift |
| Memory notes become active policy | Medium | Keep notes advisory and link back to rules/templates |
| Hook guidance duplicates policy | Low | Keep hooks as advisory context and document the policy source |
| Validator overreaches on old active plan frontmatter | Medium | Check only completed execution docs described as active in parent READMEs |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repository validators and hook smoke tests pass locally.
- **Sandbox / Canary Rollout**: docs, governance, hook guidance, and validator only; no Docker runtime mutation.
- **Human Approval Gate**: user explicitly requested implementation of this bounded re-audit plan.
- **Rollback Trigger**: any required validation cannot pass without changing runtime behavior or rewriting historical evidence.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Plan/task evidence exists and parent execution READMEs link to both.
- [x] Completed 2026-05-22 artifacts are no longer described as active in execution READMEs.
- [x] Memory notes reflect current validator metrics and closed backlog status.
- [x] Memory edit hook guidance exists and is documented.
- [x] Repository contract catches completed execution docs labeled active in parent README text.
- [x] Required validation commands pass or record a bounded advisory reason.

## Related Documents

- **Task**: [Workspace governance bounded re-audit task](../tasks/2026-05-22-workspace-governance-bounded-reaudit.md)
- **Previous remediation plan**: [Workspace docs and agent governance remediation plan](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Lifecycle closure plan**: [Lifecycle README debt closure plan](./2026-05-22-lifecycle-readme-debt-closure.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Memory README**: [Governance memory README](../../00.agent-governance/memory/README.md)
- **Template catalog**: [Template catalog](../../99.templates/README.md)
