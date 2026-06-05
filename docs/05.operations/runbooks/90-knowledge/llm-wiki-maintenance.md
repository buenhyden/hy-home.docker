---
status: active
---
<!-- Target: docs/05.operations/runbooks/90-knowledge/llm-wiki-maintenance.md -->

# LLM Wiki Maintenance Runbook

## Overview

이 런북은 `runbooks/90-knowledge/llm-wiki-maintenance.md` 대상의 반복 실행 절차, 검증 evidence, 실패 시 중단 기준을 정의한다.

## LLM Wiki Maintenance Runbook Procedure

> Scope: LLM Wiki Maintenance Runbook operational execution

### Purpose

- LLM Wiki Maintenance Runbook 작업을 반복 가능하고 검증 가능한 절차로 수행한다.
- 실행 전후 evidence, rollback 또는 escalation 기준을 명확히 남긴다.

### Canonical References

- [Operations index](../../README.md)
- **Policy**: N/A — no upstream source
- **Guide**: N/A — no upstream source

## When to Use

- Root entrypoints, agent governance docs, operations docs, script inventory, infrastructure indexes, or LLM Wiki files changed.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` reports stale generated output.
- Repository contract validation fails in the LLM Wiki contract section.

## Procedure

### Checklist

- [ ] 관련 policy, guide, runbook handoff를 확인한다.
- [ ] 현재 상태와 변경 범위를 기록한다.

1. Review the changed paths and decide whether they affect LLM-facing navigation.
2. Run the generator.

   ```bash
   bash scripts/knowledge/generate-llm-wiki-index.sh
   ```

3. Confirm the generated index is fresh.

   ```bash
   bash scripts/knowledge/generate-llm-wiki-index.sh --check
   ```

4. Run repository contracts after LLM Wiki changes.

   ```bash
   bash scripts/validation/check-repo-contracts.sh
   bash scripts/validation/check-doc-traceability.sh
   ```

5. If Graphify output is needed for navigation, report its advisory health instead of treating it as source truth.

   ```bash
   bash scripts/knowledge/report-graphify-health.sh
   ```

### Steps

1. 이 runbook의 trigger와 checklist를 확인한다.
2. 기존 절차가 문서에 포함되어 있으면 그 순서대로 수행한다.
3. 실행 중 생성된 명령 출력과 판단 근거를 evidence로 남긴다.
4. 검증 실패, secret exposure 위험, 파괴적 변경 필요 시 즉시 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- [ ] 관련 validation script 또는 수동 확인을 실행한다.
- [ ] 변경 결과가 policy, guide, runbook handoff와 충돌하지 않는지 확인한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 runbook 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## AI Agent Policy Section

- **Model / Prompt Change Process**: `wiki-curator` uses `model: sonnet` and imports `docs/00.agent-governance/scopes/docs.md`.
- **Eval / Guardrail Threshold**: stale index, unsafe path inclusion, or forbidden wording is a blocking validation failure.
- **Log / Trace Retention**: record final verification evidence in `docs/00.agent-governance/memory/progress.md`; do not paste raw secret-adjacent logs.
- **Safety Incident Thresholds**: suspected secret exposure or public-scope drift requires immediate stop and user escalation.

## Evidence

- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` passes.
- `bash scripts/validation/check-repo-contracts.sh` passes.
- `bash scripts/validation/check-doc-traceability.sh` passes.
- LLM Wiki files contain no absolute filesystem links, filesystem URI links, public-site scope drift, or Graphify-as-authority wording.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

- Stop if verification fails or secret exposure risk appears.
- Escalate to the owning operator before making runtime changes outside this runbook.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/90-knowledge/llm-wiki-maintenance.md)
- [Operations policy](../../policies/90-knowledge/llm-wiki-maintenance.md)
