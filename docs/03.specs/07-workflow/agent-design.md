---
status: active
---
<!-- Target: docs/03.specs/07-workflow/agent-design.md -->

# Workflow Cross-Validation Agent Design

## Overview

This document defines the workflow cross-validation agent design that sequentially calls `security-auditor` and `iac-reviewer` immediately after infrastructure changes. Its purpose is to manage infrastructure-change validation through canonical stage documents and record security, drift, and performance validation results through a consistent message contract and memory rule.

## Parent Documents

- **Spec**: [./spec.md](./spec.md)
- **PRD**: There is no dedicated PRD; the upper-level workflow tier context follows [../../01.requirements/019-workflow-optimization-hardening.md](../../01.requirements/019-workflow-optimization-hardening.md).
- **ARD**: There is no dedicated ARD; the structural upper-level context follows [../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md).
- **Related ADRs**: There is no dedicated ADR; agent governance follows [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md) and [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md).

## Scope & Non-goals

- **Covers**:
  - cross-validation orchestration after infrastructure changes
  - agent-to-agent handoff contract
  - audit result persistence and reporting rules
  - memory/context strategy for the workflow
- **Does Not Cover**:
  - individual infrastructure service implementation details
  - creation of new PRD/ARD/ADR stage artifacts
  - global skill repository changes

## Agent Role

- **Primary Role**: cross-validation coordinator that safely orchestrates the independent validation chain after infrastructure changes
- **Primary User / Caller**: `infra-implementer` or the routing `workflow-supervisor`
- **Success Definition**: after post-flight checks, `security-auditor` and `iac-reviewer` run in the defined order and message contract, and results are recorded consistently in `_workspace/` and `docs/00.agent-governance/memory/progress.md`.

## Inputs / Outputs

- **Inputs**:
  - changed file list
  - `infra-validate` pre/post results
  - active governance context (`AGENTS.md`, `documentation-protocol.md`, relevant scopes)
  - downstream agent responses
- **Outputs**:
  - `"audit-request: <file-list>"`
  - `"validate-request: <file-list>"`
  - `"validate-complete: PASS|WARN <summary>"`
  - `"BLOCK: <reason>"`
  - `_workspace/cross-validate_<YYYY-MM-DD>.md`
  - `docs/00.agent-governance/memory/progress.md` append entry
- **Expected Structured Format**:
  - message payloads are plain-text, deterministic, and severity-coded as `PASS`, `WARN`, or `BLOCK`

## Orchestration Model

- `handoff`
- **Why this model**:
  - The existing agent catalog already separates role-level responsibilities, so ordered handoff is smaller and clearer than a central orchestrator.
  - `security-auditor` and `iac-reviewer` own different validation responsibilities, so phased delegation is appropriate.
- **Escalation / Handoff rules**:
  - `infra-implementer` → `security-auditor`: `"audit-request"` after post-flight success
  - `security-auditor` → `infra-implementer`: `"BLOCK"` on critical findings
  - `security-auditor` → `iac-reviewer`: `"validate-request"` after critical findings are clear
  - `iac-reviewer` → `infra-implementer`: `"validate-complete: PASS|WARN <summary>"`
  - `BLOCK` immediately escalates to the user.

## Tools & Permissions

| Tool | Purpose | Allowed Actions | Forbidden Actions | Failure Handling |
| --- | --- | --- | --- | --- |
| `docker compose config` | Compose static validation | Read-only config expansion | Applying infra mutations | Stop and report validation failure |
| `docker compose ps` | Post-flight health check | Read service health | Restarting or tearing down services | Record missing health evidence |
| `docker image ls` | Image audit evidence | Inspect image tag/digest state | Pulling or retagging images | Downgrade to WARN when audit evidence is partial |
| `docker inspect` | Drift/performance inspection | Read container config and limits | Modifying live containers | Report unreachable target as validation gap |
| `bash scripts/validation/check-*.sh` | Policy gate execution | Run approved repository validation scripts | Running unrelated mutation scripts | Attach stderr/stdout summary to report |
| `Read` / workspace file writes | Evidence persistence | Write `_workspace/` report and progress note | Writing plaintext secrets | Redact and halt on secret exposure |

## Prompt / Policy Contract

- **System Instruction Summary**:
  - root shims stay thin
  - governance lives in `docs/00.agent-governance/`
  - active docs must use canonical stage paths only
- **Policy Constraints**:
  - never create active spec/plan content under `docs/superpowers/`
  - never store plaintext secrets in reports or memory
  - keep provider-specific behavior out of generic governance files
- **Versioning Rule**:
  - canonical workflow agent behavior changes belong in `docs/03.specs/07-workflow/agent-design.md`
  - execution sequencing changes belong in `docs/04.execution/plans/`

## Context & Memory Strategy

- **Session Context**:
  - changed file set
  - current post-flight validation result
  - active scope/rule documents for infra and docs layers
  - latest agent responses in the current validation chain
- **Retrieval Strategy**:
  - filter by layer (`infra`, `docs`) and artifact type before reading broader history
  - prefer canonical stage docs (`docs/03.specs`, `docs/04.execution/plans`) over ad-hoc notes
  - use `progress.md` only for durable outcome recall, not as a source of full design detail
- **Persistent Memory Rule**:
  - persist only stable outcomes: changed file list summary, severity, blocking reason, follow-up requirement
  - keep transient reasoning inside the current session; do not store speculative notes
- **Privacy / Retention Notes**:
  - never store secret values, tokens, or raw credentials
  - reports may reference secret mount paths or policy names, but not materialized secret contents

## Guardrails

- **Input Guardrails**:
  - cross-validation starts only after `infra-validate(post)` success
  - changed file list must be explicit and traceable
- **Output Guardrails**:
  - every terminal state must be one of `PASS`, `WARN`, or `BLOCK`
  - every warning or block must include evidence and next action
- **Blocked Conditions**:
  - post-flight validation absent or failed
  - plaintext secret exposure detected
  - destructive rollback or infra mutation required without user-authorized path
  - active design or plan attempts to use non-stage `docs/*` paths
- **Human Escalation Rule**:
  - any `BLOCK`, ambiguous rollback decision, or permissions gap escalates to the user immediately

## Failure Modes & Fallback

- **Failure Mode 1**: `security-auditor` unreachable or returns incomplete response
- **Fallback 1**: record agent response gap in `_workspace/` and escalate to user without fabricating audit completion
- **Failure Mode 2**: `iac-reviewer` can inspect drift but lacks performance evidence
- **Fallback 2**: return `WARN` with explicit missing evidence instead of `PASS`
- **Failure Mode 3**: legacy references point to removed non-stage docs
- **Fallback 3**: treat as documentation defect, rewrite to canonical path, and fail verification until fixed

## Evaluation Plan

- **Offline Evals**:
  - clean infra change path: audit passes and reviewer returns `PASS`
  - critical finding path: auditor emits deterministic `BLOCK`
  - partial evidence path: reviewer emits `WARN`
- **Online Signals**:
  - `_workspace/cross-validate_<date>.md` created
  - `progress.md` receives durable summary
  - no active references remain to removed `docs/superpowers` artifacts
- **Acceptance Thresholds**:
  - 100% deterministic terminal status vocabulary
  - 0 active spec/plan documents in non-stage paths
  - 0 broken related-document links in changed files
- **Linked Plan / Task / Eval Docs**: [../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md), [../../04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md)

## Observability

- **Trace fields**:
  - `task_id`
  - `changed_files`
  - `audit_phase`
  - `severity`
  - `report_path`
- **Logs / Events**:
  - audit request sent
  - audit decision received
  - drift/performance review completed
  - durable memory append completed
- **Redaction / Privacy Rules**:
  - redact secret values and tokens
  - log only policy names, paths, and high-level findings

## Related Documents

- **Workflow Spec**: [./spec.md](./spec.md)
- **Implementation Plan**: [../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md)
- **Implementation Task**: [../../04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md)
- **Policy**: [../../05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/policies/07-workflow/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/runbooks/07-workflow/optimization-hardening.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
