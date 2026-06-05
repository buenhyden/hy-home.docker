---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-05-18-docs-05-operations-purpose-remediation.md -->

# Task: docs/05.operations Purpose Remediation

## Overview

이 문서는 `docs/05.operations` purpose-profile remediation의 실행 작업과 검증 evidence를 추적한다.

## Inputs

- **Parent Plan**: [docs/05.operations purpose remediation plan](../plans/2026-05-18-docs-05-operations-purpose-remediation.md)
- **Operations Stage**: [Operations index](../../05.operations/README.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- Do not change runtime service behavior or secret material.
- Do not touch or stage untracked `projects/storybook/mcp/`.
- Keep changes traceable to the parent plan.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Move DAG deployment policy from guide bucket to policy bucket and update references | doc | N/A | OPS-001 | Stale path scan returns no active references | doc-writer | Done |
| T-002 | Normalize LLM Wiki maintenance guide/policy/runbook profiles | doc | N/A | OPS-002 | Purpose profile scan passes for the three files | doc-writer | Done |
| T-003 | Add missing policy scope/verification and runbook escalation headings | doc | N/A | OPS-003 | Purpose profile scan reports zero flagged files | doc-writer | Done |
| T-004 | Remove nested duplicate Related Documents sections | doc | N/A | OPS-004 | `rg "^#### Related Documents$"` returns no matches under `docs/05.operations` | doc-writer | Done |
| T-005 | Update template and repo contract for operations profile enforcement | test | N/A | OPS-005 | `bash scripts/validation/check-repo-contracts.sh` passes | doc-writer | Done |
| T-006 | Refresh LLM Wiki index and record progress evidence | doc | N/A | OPS-006 | LLM Wiki freshness check and progress log updated | wiki-curator/doc-writer | Done |

## Suggested Types

- `doc`
- `test`
- `ops`

## Phase View

### Phase 1

- [x] T-001 Move DAG deployment policy and fix links
- [x] T-002 Normalize LLM Wiki maintenance profile split
- [x] T-003 Add missing policy and runbook profile headings
- [x] T-004 Remove duplicate nested Related Documents sections

### Phase 2

- [x] T-005 Add operations purpose profile contract to template and validator
- [x] T-006 Refresh generated index, validate, and record evidence

## Verification Summary

- **Test Commands**:
  - Custom Python purpose profile scan over `docs/05.operations/{guides,policies,runbooks}`: PASS (`guides=0`, `policies=0`, `runbooks=0`)
  - `rg -n "guides/07-workflow/01\\.dag-deployment|01\\.dag-deployment\\.md" docs/05.operations README.md AGENTS.md CLAUDE.md GEMINI.md infra scripts`: PASS, no stale active references
  - `rg -n "^#### Related Documents$" docs/05.operations -g "*.md"`: PASS, no duplicate nested related-doc sections
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`: PASS
  - `bash scripts/validation/check-doc-traceability.sh`: PASS
  - `bash scripts/validation/check-repo-contracts.sh`: PASS
  - `git diff --check`: PASS
  - `/home/hy/.local/bin/graphify update .`: completed; `bash scripts/knowledge/report-graphify-health.sh` remains advisory due to 3 cross-root inferred edges
- **Eval Commands**: N/A
- **Logs / Evidence Location**: This task document and `docs/00.agent-governance/memory/progress.md`

## Related Documents

- **Parent Plan**: [docs/05.operations purpose remediation plan](../plans/2026-05-18-docs-05-operations-purpose-remediation.md)
- **Operations index**: [../../05.operations/README.md](../../05.operations/README.md)
- **Repository contract validator**: [../../../scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
