---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-provider-semantic-parity-validator.md -->

# Provider Semantic Parity Validator Implementation Plan

## Overview

This plan implements a scoped provider semantic parity gate for Stage 00 agent
role scopes. It closes the `AEA-AUTO-002` audit candidate by making provider
sync and repo contracts preserve the canonical role scope defined in Stage 00.

## Context

The existing provider validation already enforces provider name-set parity,
model policy, generated Codex skill mirrors, and Gemini pointer shape. A focused
review found that Codex TOML adapters were generated from the Stage 00 catalog
frontmatter `layer: agentic`, while the actual role scope is stored in the
catalog `Scope import` line and in `subagent-protocol.md`. This is a semantic
parity gap rather than a structural one.

## Goals & In-Scope

- **Goals**:
  - Derive generated provider agent scope from the Stage 00 catalog `Scope
    import` literal.
  - Regenerate Codex and Gemini provider agent adapters.
  - Add repo-contract validation for Claude, Codex, Gemini, and subagent
    protocol role-scope parity.
  - Update audit and execution evidence.
- **In Scope**:
  - `scripts/operations/sync-provider-surfaces.sh`
  - `scripts/validation/check-repo-contracts.sh`
  - `.codex/agents/*.toml`
  - `.agents/agents/*.md`
  - Stage 03/04 evidence, audit candidate, generated indexes, and progress
    memory.

## Non-Goals & Out-of-Scope

- No natural-language semantic diff engine.
- No model policy changes.
- No hook behavior changes.
- No provider runtime configuration changes beyond generated adapter metadata.
- No secret, credential, token, private-key, raw-log, shell-history, or `.env`
  reads or writes.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-PSPV-001 | Create Stage 03/04 evidence. | `docs/03.specs/107-provider-semantic-parity-validator/**`, this plan, task evidence, indexes | VAL-SPC-001 | Spec, plan, and task are linked and indexed. |
| PLN-PSPV-002 | Update provider sync generator to use canonical role scope. | `scripts/operations/sync-provider-surfaces.sh`, generated provider adapters | VAL-SPC-001, VAL-SPC-002 | Provider sync `--write` then `--check` passes. |
| PLN-PSPV-003 | Add semantic parity repo-contract validation. | `scripts/validation/check-repo-contracts.sh` | VAL-SPC-003, VAL-SPC-004 | Repo contracts fail on role-scope drift and pass on the current tree. |
| PLN-PSPV-004 | Update audit/progress evidence and close. | Stage 90 audit candidate, progress memory, generated indexes | VAL-SPC-004 | Final validation summary is recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Generator | Regenerate provider adapters. | `bash scripts/operations/sync-provider-surfaces.sh --write` | Codex/Gemini adapters updated from Stage 00. |
| VAL-PLN-002 | Generator | Check provider sync freshness. | `bash scripts/operations/sync-provider-surfaces.sh --check` | `sync-provider-surfaces: no drift`. |
| VAL-PLN-003 | Syntax | Check shell syntax. | `bash -n scripts/operations/sync-provider-surfaces.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-004 | Contracts | Check full repo contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |
| VAL-PLN-005 | Docs | Check docs and generated index. | `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | All pass. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Generated provider adapters become noisy | Medium | Limit generation changes to agent metadata, not prompt bodies or model values. |
| Validator overreaches into historical docs | Medium | Validate only active Stage 00 catalog, provider adapter files, and subagent protocol. |
| `.agents` write is blocked by sandbox permissions | Low | Use the approved scoped provider surface write path and record evidence. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: N/A; this is deterministic provider metadata validation.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: User continued the broader provider/document contract
  cleanup on 2026-07-05.
- **Rollback Trigger**: Revert the logical commit and rerun provider sync if
  contracts fail due to this batch.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Stage 03/04 evidence exists and is indexed.
- [x] Provider sync derives Codex/Gemini agent scope from canonical Stage 00
      role scope.
- [x] Repo contracts enforce provider semantic role-scope parity.
- [x] Audit/progress evidence and generated indexes are updated.
- [x] Final validation passes.

## Related Documents

- **Spec**: [../../03.specs/107-provider-semantic-parity-validator/spec.md](../../03.specs/107-provider-semantic-parity-validator/spec.md)
- **Task**: [../tasks/2026-07-05-provider-semantic-parity-validator.md](../tasks/2026-07-05-provider-semantic-parity-validator.md)
- **Provider capability matrix**: [../../00.agent-governance/rules/provider-capability-matrix.md](../../00.agent-governance/rules/provider-capability-matrix.md)
- **Provider adapter model**: [../../00.agent-governance/providers/agents-md.md](../../00.agent-governance/providers/agents-md.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
