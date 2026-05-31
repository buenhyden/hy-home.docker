---
status: active
---
<!-- Target: docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md -->

# Task: Standardizing Agent Governance

---

## Overview (KR)

이 문서는 AI Agent 거버넌스 정비 작업의 구현 및 검증 태스크 목록이다. 계획(Plan)에서 정의된 아키텍처 정비 단계를 추적 가능한 태스크 항목으로 나누어 관리하고 검증한다.

## Inputs

- **Parent Plan**: [Execution plan](../plans/2026-05-30-standardizing-agent-governance.md)

## Working Rules

- Verify parity rules across Claude, Codex, and Gemini.
- Core behavior must comply with the Provider Parity Model and the 2026-05-31
  Codex model policy: `gpt-5.5` supervisor, `gpt-5.4-mini` default workers.
- Run validation scripts after policy, runtime mirror, and template mapping changes.
- Preserve `.codex/agents/*.md` YAML frontmatter as the Codex harness shape.

## Task Table

| Task ID | Description | Type | Parent Plan | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | Stage 00 clarification duty and concept alignment | doc | PLN-001 | Added shared clarification duty and core concepts in `docs/00.agent-governance/README.md`, `rules/agentic.md`, and `rules/task-checklists.md`. | Codex | Completed |
| T-002 | Template Contract mapping reconciliation | doc | PLN-002 | Replaced stale operations policy mapping with `policy.template.md`; updated `docs/99.templates/README.md` and runtime ops skill references. `rg "operation\\.template"` returned no active hits in governance/runtime surfaces. | Codex | Completed |
| T-003 | Codex Model Policy update | doc/script | PLN-004 | Updated `subagent-protocol.md`, capability matrix, Codex provider notes, sync script, validator, and `.codex/agents/*.md` models: supervisor `gpt-5.5`, workers `gpt-5.4-mini`. | Codex | Completed |
| T-004 | Runtime parity and QA scope alignment | doc/runtime | PLN-004, PLN-005 | Updated canonical `.claude/agents/qa-engineer.md` to `scopes/qa.md`, regenerated `.codex/` and `.agents/` with `sync-provider-surfaces.sh --write`, then verified no drift. | Codex | Completed |
| T-005 | English-only Stage 00 cleanup | doc | PLN-006 | Translated `github-governance.md`, hookify messages, and remaining Korean progress-log text. `rg -n "[가-힣]" docs/00.agent-governance` returned no hits. | Codex | Completed |
| T-006 | QA/CI/CD job taxonomy cleanup | doc | PLN-007 | Rewrote GitHub governance taxonomy to classify local scripts, inline shell, npm frontend gates, Storybook coverage, and GitHub-only `zizmor` SARIF gate. | Codex | Completed |
| T-007 | Verification and evidence update | eval/doc | PLN-008 | Recorded graphify update, repository validators, traceability, LLM Wiki freshness, Graphify advisory, language/model scans, and diff hygiene in this task. | Codex | Completed |

## Verification Summary

- **Test Commands**:
  - `/home/hy/.local/bin/graphify update .`
  - `bash -n scripts/operations/sync-provider-surfaces.sh`
  - `bash -n scripts/validation/check-repo-contracts.sh`
  - `python3 -m json.tool .codex/hooks.json >/dev/null`
  - `bash scripts/operations/sync-provider-surfaces.sh`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
  - `bash scripts/knowledge/report-graphify-health.sh`
  - `rg -n "[가-힣]" docs/00.agent-governance`
  - `rg -n "gpt-5\\.5-instant|operation\\.template" .claude .codex .agents docs/00.agent-governance scripts/validation scripts/operations docs/99.templates/README.md`
  - `rg -n "^(model|model_reasoning_effort):" .codex/agents/*.md`
  - `git diff --check`
- **Logs / Evidence Location**:
  - `check-repo-contracts.sh`: `failures=0`, `PASS: repository Docker/docs contracts are synchronized`, `target_stage_docs_total=499`, `normalized_target_stage_docs_total=498`, `legacy_target_stage_docs_skipped=1`.
  - `check-doc-traceability.sh`: `catalog_pairs_total=46`, `failures=0`, PASS.
  - `generate-llm-wiki-index.sh --check`: PASS, generated LLM Wiki index is fresh.
  - `report-graphify-health.sh`: `status=advisory`, `manifest_paths_total=791`, `surprising_cross_root_inferred_edges=3`; advisory corroborated against tracked governance/stage docs.
  - `sync-provider-surfaces.sh`: `sync-provider-surfaces: no drift`.
  - Stage 00 language scan and stale model/template scan returned no hits.
  - Codex model audit shows `workflow-supervisor` on `gpt-5.5` and all workers on `gpt-5.4-mini`; no `model_reasoning_effort` frontmatter exists.
  - `git diff --check`: PASS.

## Deviation Notes

- `gpt-5.3-codex` was documented only as a future explicit code-specialized worker override. No active worker uses it because this pass had no per-agent coding-specialized exception that justified splitting the default worker tier.
- `graphify` was available at `/home/hy/.local/bin/graphify`, not on `PATH`; the update completed and refreshed `graphify-out/`.
- The first provider sync write attempt hit sandbox read-only behavior for `.codex/agents`; the same scoped sync command succeeded after approval to rerun outside the sandbox.

## Related Documents

- **Parent Plan**: [Execution plan](../plans/2026-05-30-standardizing-agent-governance.md)
- **Operations / References**: [Operations index](../../05.operations/README.md)
