---
status: active
---
<!-- Target: docs/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md -->

# Task: Agent Governance Phase 3 Implementation

## Overview (KR)

이 문서는 Phase 2 산출물인 `2026-06-01-agent-governance-phase2-alignment.md`를 검증·검토한 뒤, 승인된 결정 게이트를 Phase 3 구현 작업으로 추적하기 위한 task 문서다.

## Inputs

- **Parent Plan**: [Agent governance Phase 2 alignment plan](../plans/2026-06-01-agent-governance-phase2-alignment.md)

## Working Rules

- Implement only the Phase 2 confirmed decision set.
- Treat Stage 00 as the canonical governance source.
- Preserve historical evidence unless a normalization task explicitly requires a structural update.
- Run repository contract checks after each logical implementation batch.
- Do not treat green checks as proof of semantic completeness; record manual evidence for policy and adapter semantics.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Verify and review the Phase 2 plan and current repository state. | eval | N/A | PLN-001 | `git status --short --branch`; Phase 2 plan re-read; Graphify corroboration rule observed. | Codex | Completed |
| T-002 | Establish Stage 00 canonical adapter policy and update provider docs away from Claude-canonical wording. | doc | N/A | PLN-002, PLN-007 | Stage 00 docs define canonical catalog plus provider adapter responsibilities. | Codex | Completed |
| T-003 | Transition Codex agent surface from `.md` mirror assumptions to `.toml` adapter definitions. | doc/tool | N/A | PLN-005 | `.codex/agents/*.toml` exists and validator checks model and reasoning effort fields. | Codex | Completed |
| T-004 | Encode strict 2026-05-29 Model Policy evidence and reasoning-effort handling. | doc/eval | N/A | PLN-006 | Official OpenAI release/model evidence predates or covers the 2026-05-29 baseline for `gpt-5.5` and `gpt-5.4-mini`; the policy now forbids later-doc-only promotion of new IDs. | Codex | Completed |
| T-005 | Normalize all target-stage template deviations in planned batches. | doc | N/A | PLN-004 | Deviation inventory moved from 502/503 normalized to 503/503 normalized; `legacy_target_stage_docs_skipped=0` is now a failing gate if it regresses. | Codex | Completed |
| T-006 | Add validator or manual-gate coverage for Phase 1 blind spots. | test | N/A | PLN-008 | Validator covers adapter parity, TOML model fields, Markdown fence balance, status vocabulary, and full template normalization. Catalog-depth semantics remain review-only. | Codex | Completed |
| T-007 | Record verification evidence, Graphify advisory status, LLM Wiki freshness, and progress log updates. | eval/memory | N/A | PLN-009 | Verification summary and `memory/progress.md` are updated; LLM Wiki index regenerated after staging new tracked paths. | Codex | Completed |

## Suggested Types

- `doc`
- `test`
- `eval`
- `memory`
- `tool`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`

## Phase View (Optional)

### Batch 1 — Governance And Adapter Baseline

- [x] T-001 Verify Phase 2 plan and current repository state.
- [x] T-002 Establish Stage 00 canonical adapter policy.
- [x] T-003 Create Codex TOML adapter baseline.
- [x] T-004 Encode strict model-policy evidence boundary.

### Batch 2 — Full Normalization And Guardrails

- [x] T-005 Normalize all target-stage template deviations.
- [x] T-006 Expand validator/manual-gate coverage.
- [x] T-007 Record final evidence and progress.

## Verification Summary

- **Test Commands**:
  - `bash scripts/operations/sync-provider-surfaces.sh` — PASS (`no drift`).
  - `bash -n scripts/validation/check-repo-contracts.sh` — PASS.
  - `bash scripts/validation/check-repo-contracts.sh` — PASS (`failures=0`; `target_stage_docs_total=503`; `normalized_target_stage_docs_total=503`; `legacy_target_stage_docs_skipped=0`).
  - `bash scripts/validation/check-doc-traceability.sh` — PASS (`failures=0`; `catalog_pairs_total=46`).
  - `bash scripts/knowledge/generate-llm-wiki-index.sh` — regenerated `docs/90.references/llm-wiki/index.md` with 1018 paths after staging new tracked files.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — PASS after regeneration.
  - `bash scripts/knowledge/report-graphify-health.sh` — advisory (`surprising_cross_root_inferred_edges=3`).
  - `python3 -m json.tool .codex/hooks.json` — PASS.
  - `git diff --check` — PASS.
  - Status vocabulary inventory — PASS (`draft=26`, `active=324`, `completed=60`, `superseded=1`; no unsupported values).
- **Eval Commands**:
  - Graphify report read first and treated as advisory; Stage 00/provider facts were corroborated against tracked docs and scripts.
  - Official OpenAI evidence checked for the 2026-05-29 model baseline:
    [GPT-5.5 API model page](https://developers.openai.com/api/docs/models/gpt-5.5),
    [GPT-5.4 mini API model page](https://developers.openai.com/api/docs/models/gpt-5.4-mini),
    [OpenAI model release notes](https://help.openai.com/en/articles/9624314-model-release-notes),
    and [OpenAI API model overview](https://developers.openai.com/api/docs/models).
    Local validators prove repository policy shape only; future model promotions still require official archived/provider evidence or a repository-approved evidence note.
- **Logs / Evidence Location**:
  - This task document.
  - `docs/00.agent-governance/memory/progress.md`

## Related Documents

- **Parent Plan**: [Agent governance Phase 2 alignment plan](../plans/2026-06-01-agent-governance-phase2-alignment.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Provider Notes**: [AGENTS.md provider-neutral notes](../../00.agent-governance/providers/agents-md.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Subagent Protocol**: [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
