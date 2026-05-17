---
status: active
---

# LLM Wiki Maintenance Runbook

## Overview (KR)

이 런북은 `runbooks/llm-wiki-maintenance.md` 대상의 반복 실행 절차, 검증 evidence, 실패 시 중단 기준을 정의한다.

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

## Exceptions

- Do not add a new LLM Wiki source category when the same navigation need is already covered by `repository-map.md` or the generated index.
- Do not add runtime hooks for LLM Wiki refresh unless a later task establishes a concrete failure mode that the existing post-tool validation cannot catch.
- Escalate to the user before including any path that may expose private values or user-specific runtime data.

## Verification

- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` passes.
- `bash scripts/validation/check-repo-contracts.sh` passes.
- `bash scripts/validation/check-doc-traceability.sh` passes.
- LLM Wiki files contain no absolute filesystem links, filesystem URI links, public-site scope drift, or Graphify-as-authority wording.

## Review Cadence

- Review after changes to root entrypoints, `docs/00.agent-governance/`, `docs/05.operations/`, `docs/90.references/llm-wiki/`, `infra/README.md`, `scripts/README.md`, or `secrets/README.md`.
- Review during repository contract failures that mention LLM Wiki freshness or boundary wording.

## AI Agent Policy Section

- **Model / Prompt Change Process**: `wiki-curator` uses `model: sonnet` and imports `docs/00.agent-governance/scopes/docs.md`.
- **Eval / Guardrail Threshold**: stale index, unsafe path inclusion, or forbidden wording is a blocking validation failure.
- **Log / Trace Retention**: record final verification evidence in `docs/00.agent-governance/memory/progress.md`; do not paste raw secret-adjacent logs.
- **Safety Incident Thresholds**: suspected secret exposure or public-scope drift requires immediate stop and user escalation.

## Escalation

- Stop if verification fails or secret exposure risk appears.
- Escalate to the owning operator before making runtime changes outside this runbook.

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/llm-wiki-maintenance.md)
- [Operations policy](../policies/llm-wiki-maintenance.md)
- [Operations template](../../99.templates/operation.template.md)
