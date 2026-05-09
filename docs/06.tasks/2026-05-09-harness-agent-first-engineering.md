---
status: draft
---

# Task: Harness / Agent-first Engineering Documentation

## Overview (KR)

이 작업 문서는 하네스 엔지니어링과 Agent-first Engineering 분석 결과를 공식 stage 문서로 구현하고 검증한 증거를 기록한다.

## Inputs

- [Specification](../04.specs/harness-agent-first-engineering/spec.md)
- [Plan](../05.plans/2026-05-09-harness-agent-first-engineering.md)
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage Authoring Matrix](../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- Templates from `docs/99.templates/` are mandatory for new stage documents.
- Parent README files must be updated when files are added.
- Runtime policy files are not modified unless a concrete validator failure requires it.
- Completion is based on repository checks, not subjective review.

## Task Table

| ID | Type | Task | Status | Validation / Evidence |
| --- | --- | --- | --- | --- |
| HAFE-001 | Analyze | Review root, docs, infra, scripts, governance, runtime, template, and validator files. | Done | Captured in the specification file analysis table. |
| HAFE-002 | Document | Create Spec, Plan, Task, Guide, Operation, and Runbook stage docs. | Done | New docs under `docs/04.specs`, `docs/05.plans`, `docs/06.tasks`, `docs/07.guides`, `docs/08.operations`, `docs/09.runbooks`. |
| HAFE-003 | Sync | Update parent README files for new artifacts. | Done | README structure and related links updated. |
| HAFE-004 | Verify | Run governance, docs, runtime, Compose, and hardening checks. | Done | All planned validation commands passed on 2026-05-09. |
| HAFE-005 | Scan | Confirm no external source-label references in active runtime/governance surfaces. | Done | `rg` returned no matches in active runtime/governance surfaces. |
| HAFE-006 | Context Quality | Add Graphify health fallback so contaminated graph output remains advisory. | Done | `bash scripts/report-graphify-health.sh` exits 0 and reports `status=advisory` for current generated corpus. |

## Suggested Types

- Analyze
- Document
- Sync
- Verify
- Scan

## Agent-specific Types (If Applicable)

- `agentic-analysis`: inspect agent/runtime contracts.
- `runtime-boundary-check`: verify `.claude`/`.codex` boundaries.
- `template-contract-check`: verify stage docs and README traceability.

## Phase View (Optional)

### Phase 1

Analyze existing workspace and runtime contracts, then create template-compliant documentation.

### Phase 2

Run validation commands and record command outcomes in the final response.

## Verification Summary

Executed commands:

```bash
bash scripts/check-repo-contracts.sh
bash scripts/check-doc-traceability.sh
bash scripts/report-graphify-health.sh
bash scripts/validate-docker-compose.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-quickwin-baseline.sh
bash scripts/check-all-hardening.sh
rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md GEMINI.md .claude .codex docs/00.agent-governance --glob '!docs/00.agent-governance/memory/**'
```

Results:

- `check-repo-contracts.sh`: PASS, `failures=0`.
- `check-doc-traceability.sh`: PASS, `catalog_pairs_total=46`, `failures=0`.
- `report-graphify-health.sh`: PASS/non-failing advisory, `status=advisory`, `manifest_volume_paths=223`, `manifest_gitlink_paths=309`, `graph_source_file_contamination_count=282`.
- `validate-docker-compose.sh`: PASS, `services_total=5`.
- `check-template-security-baseline.sh`: PASS, `template_adoption_missing=0`, required security controls enforced.
- `check-quickwin-baseline.sh`: PASS, `services_total=5`, baseline violations all zero.
- `check-all-hardening.sh`: PASS, all tier checks passed.
- Source-label scan: no matches in active runtime/governance surfaces.

## Related Documents

- [Specification](../04.specs/harness-agent-first-engineering/spec.md)
- [Plan](../05.plans/2026-05-09-harness-agent-first-engineering.md)
- [Guide](../07.guides/harness-agent-first-engineering.md)
- [Operations Policy](../08.operations/harness-agent-first-engineering.md)
- [Validation Runbook](../09.runbooks/harness-agent-first-engineering-validation.md)
