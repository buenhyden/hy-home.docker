---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-22-workspace-docs-agent-governance-remediation.md -->

# Workspace Docs and Agent Governance Remediation Plan

> Workspace documentation lifecycle, template contract, and agent runtime governance remediation plan.

## Overview

This document is the implementation plan for aligning the `hy-home.docker` documentation lifecycle, template contract, cross-links, AI Agent governance, and hook/runtime surfaces with the current workspace purpose.

The core direction is a contract-first staged workflow. First align `docs/99.templates`, validators, and canonical path criteria, then use that basis to normalize stage documents and agent runtime documents.

## Context

This repository aims to separate a Docker Compose-based home server and personal development infrastructure into layers, connecting requirements through operations knowledge via the `docs/01` through `docs/05` lifecycle. The governance hub, templates, runtime hook, and agent/function mirror already exist, but the following drift remains.

- `check-repo-contracts.sh` fails because of a stale LLM Wiki index.
- Some historical stage documents do not fully follow the current template metadata or heading contract.
- `docs/02.architecture` contains dated duplicate ARD/ADR candidates that conflict with the canonical `0026-standardize-infra-net.md`.
- Some README and operations leaf documents diverge from the current contract in `readme.template.md`, `guide.template.md`,
  `policy.template.md`, or `runbook.template.md`.
- Agent runtime documents contain stale section references, unavailable `rtk` guidance, and Hookify `.local.md` tracking convention drift.

## Goals & In-Scope

- **Goals**:
  - Bring the lifecycle and template contract for `docs/01` through `docs/05`, `docs/90`, and `docs/99` into a verifiable state.
  - Migrate references from duplicate/non-canonical documents to the canonical targets, then delete the duplicate/non-canonical documents.
  - Keep historical evidence documents while making them satisfy the current required template shape and rules.
  - Preserve Claude/Codex hook parity and the `.agents` compatibility boundary.
- **In Scope**:
  - `docs/99.templates`, stage README, selected stage leaf docs, generated LLM Wiki index
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `RTK.md`, `docs/00.agent-governance/**`
  - `.claude/**`, `.codex/**`, `.agents/**` documentation and hook-related contracts
  - `scripts/validation/check-repo-contracts.sh` full-stage template gate expansion

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Docker runtime behavior, service topology, secrets, or compose service definitions are not changed.
  - Historical evidence content is not rewritten for style only.
  - New active stage taxonomy is not introduced.
- **Out of Scope**:
  - Secret values, private keys, shell history, log databases, and personal runtime settings
  - Existing untracked `projects/storybook/mcp/`
  - Reverting pre-existing `graphify-out/GRAPH_REPORT.md` dirty state

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add execution plan and task evidence for this remediation | `docs/04.execution/plans/`, `docs/04.execution/tasks/`, execution READMEs | DOC-GOV-001 | Plan/task files follow templates and are linked from parent READMEs |
| PLN-002 | Strengthen template guidance before normalizing target docs | `docs/99.templates/*.template.*`, `docs/99.templates/README.md` | DOC-GOV-002 | Template contract scan passes and no unresolved placeholder leaks into target docs |
| PLN-003 | Normalize README and stage document metadata/heading drift | `README.md`, `docs/**/README.md`, stage leaf docs | DOC-GOV-003 | Full-stage template gate passes |
| PLN-004 | Remove duplicate infra_net ARD/ADR after reference migration | `docs/02.architecture/**`, linked stage docs, validator allowlists | DOC-GOV-004 | No reference to deleted duplicate files remains |
| PLN-005 | Align agent/runtime governance and Hookify tracking exception | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `RTK.md`, `.claude/`, `.codex/`, `.agents/`, governance docs | DOC-GOV-005 | Hook parity and runtime catalog checks pass |
| PLN-006 | Extend validator from changed-file gate to full-stage gate | `scripts/validation/check-repo-contracts.sh` | DOC-GOV-006 | Full repository contract check passes |
| PLN-007 | Refresh generated LLM Wiki index and progress evidence | `docs/90.references/llm-wiki/llm-wiki-index.md`, `docs/00.agent-governance/memory/progress.md` | DOC-GOV-007 | LLM Wiki generator check passes |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Syntax | Shell hook and validator syntax check | `bash -n scripts/validation/check-repo-contracts.sh scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh` | exit code 0 |
| VAL-PLN-002 | JSON | Runtime hook JSON validity | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | both exit code 0 |
| VAL-PLN-003 | Contract | Repository docs/runtime contract | `bash scripts/validation/check-repo-contracts.sh` | exit code 0 |
| VAL-PLN-004 | Traceability | Execution and operations traceability | `bash scripts/validation/check-doc-traceability.sh` | exit code 0 |
| VAL-PLN-005 | Security baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | exit code 0 |
| VAL-PLN-006 | Generated docs | LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | exit code 0 |
| VAL-PLN-007 | Compose | Compose validation when infra README/docs trigger it | `bash scripts/validation/validate-docker-compose.sh` | exit code 0 or explicit not-run reason |
| VAL-PLN-008 | Hook behavior | Stage edit guidance, post-edit validation, Stop gate samples | sample JSON piped to `scripts/hooks/agent-event-hook.sh` | expected guidance/blocking behavior observed |
| VAL-PLN-009 | Diff hygiene | Whitespace and patch sanity | `git diff --check` | exit code 0 |
| VAL-PLN-010 | Graphify | Advisory graph health report | `bash scripts/knowledge/report-graphify-health.sh` | clean or advisory with reason recorded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical document meaning changes during template alignment | High | Add only metadata, required headings, target links, and factual context derived from the same document or canonical linked docs |
| Runbook rollback steps are invented | High | Use factual-only recovery content; when not verified, record explicit N/A reason and escalation path |
| Full-stage validator becomes too strict for intentional historical evidence | Medium | Normalize target docs first, then add named exemptions only for intentional examples or generated docs |
| Duplicate ARD/ADR deletion breaks links | Medium | Run reference search before deletion and remove validator allowlist entries tied to the duplicates |
| Hookify `.local.md` convention is misunderstood | Low | Document tracked team-shared Hookify rule exception in `.claude`/provider guidance |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repository validators and hook smoke tests pass locally.
- **Sandbox / Canary Rollout**: changes remain docs/runtime governance only; no Docker runtime mutation.
- **Human Approval Gate**: this plan is based on the approved user plan and follow-up decisions on legacy cleanup, runbook recovery, Hookify tracking, and full-stage validator scope.
- **Rollback Trigger**: validator cannot pass without deleting historical evidence or inventing operational procedures.
- **Prompt / Model Promotion Criteria**: not applicable; no model or prompt production surface changes.

## Completion Criteria

- [x] Plan/task evidence exists and parent execution READMEs link to both.
- [x] Template guidance matches lifecycle, duplicate cleanup, and factual-only recovery policy.
- [x] README and stage docs satisfy full-stage template gate.
- [x] Duplicate `2026-04-01-standardize-infra-net.md` ARD/ADR files are removed after reference migration.
- [x] Agent/runtime guidance stays thin, current, and provider-aligned.
- [x] LLM Wiki index freshness check passes.
- [x] Required validation commands pass or have explicit not-run reasons.

## Related Documents

- **Task**: [Workspace docs and agent governance remediation task](../tasks/2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Docs index**: [Docs README](../../README.md)
- **Governance hub**: [Agent governance README](../../00.agent-governance/README.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Templates**: [Template catalog](../../99.templates/README.md)
- **LLM Wiki index**: [Generated LLM Wiki index](../../90.references/llm-wiki/llm-wiki-index.md)
