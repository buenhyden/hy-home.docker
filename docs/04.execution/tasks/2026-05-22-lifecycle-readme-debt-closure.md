---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-05-22-lifecycle-readme-debt-closure.md -->

# Task: Lifecycle README Debt Closure

> Execution evidence for closing lifecycle, README readiness, and hook guidance debt.

## Overview

This document records actual execution status and verification evidence for lifecycle README debt closure work.

## Inputs

- **Parent Plan**: [Lifecycle README debt closure plan](../plans/2026-05-22-lifecycle-readme-debt-closure.md)
- **Previous Remediation**: [Workspace docs and agent governance remediation task](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Template Catalog**: [Template catalog](../../99.templates/README.md)

## Working Rules

- Do not read or record secret values, credentials, private keys, shell history, or log databases.
- Preserve historical evidence meaning. Only normalize template shape, placeholders, links, and factual routing text.
- Root shims stay thin. Put detailed policy in `docs/00.agent-governance/` or provider/runtime files.
- Hook output is advisory context unless the Stop template gate blocks completion.
- Existing untracked `projects/storybook/mcp/` stays untouched.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-LRDC-001 | Add plan/task evidence and execution indexes | doc | Documentation lifecycle | PLN-LRDC-001 | Plan/task files and README links present | doc-writer | Done |
| T-LRDC-002 | Clarify README template and template catalog | doc | README template contract | PLN-LRDC-002 | Repository contract passes | doc-writer | Done |
| T-LRDC-003 | Normalize 4 legacy target-stage documents | doc | Stage template contract | PLN-LRDC-003 | `legacy_target_stage_docs_skipped=0` | doc-writer | Done |
| T-LRDC-004 | Close infra service README readiness debt | doc | Infra README rubric | PLN-LRDC-004 | `infra_service_readmes_rubric_partial=0` | doc-writer | Done |
| T-LRDC-005 | Improve stage README edit hook guidance | guardrail | Hook parity contract | PLN-LRDC-005 | hook smoke tests pass | doc-writer | Done |
| T-LRDC-006 | Run final validation and record evidence | test | Verification plan | PLN-LRDC-006 | required validation commands pass | doc-writer | Done |

## Suggested Types

- `doc`
- `guardrail`
- `test`

## Agent-specific Types (If Applicable)

- `memory`
- `guardrail`
- `eval`

## Phase View (Optional)

### Phase 1

- [x] T-LRDC-001 Add plan/task evidence and execution indexes
- [x] T-LRDC-002 Clarify template guidance
- [x] T-LRDC-003 Normalize legacy target-stage docs

### Phase 2

- [x] T-LRDC-004 Close infra service README readiness debt
- [x] T-LRDC-005 Improve hook guidance

### Phase 3

- [x] T-LRDC-006 Run validation, Graphify update/report, and progress log update

## Verification Summary

- **Test Commands**:
  - PASS: `git diff --check`
  - PASS: `bash -n scripts/validation/check-repo-contracts.sh scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh`
  - PASS: `python3 -m json.tool .claude/settings.json`
  - PASS: `python3 -m json.tool .codex/hooks.json`
  - PASS: `bash scripts/validation/check-repo-contracts.sh` with `legacy_target_stage_docs_skipped=0` and `infra_service_readmes_rubric_partial=0`
  - PASS: `bash scripts/validation/check-doc-traceability.sh`
  - PASS: `bash scripts/validation/check-template-security-baseline.sh`
  - PASS: `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
  - PASS: `bash scripts/validation/validate-docker-compose.sh`
- **Eval Commands**:
  - PASS: PreToolUse sample for target-stage doc edit emitted template guidance.
  - PASS: PreToolUse sample for infra service README edit emitted Service Readiness guidance.
  - PASS: PreToolUse sample for folder/index README edit emitted README template routing guidance.
  - PASS: Stop sample for invalid changed target-stage doc emitted a block decision.
- **Logs / Evidence Location**:
  - This task document and `docs/00.agent-governance/memory/progress.md`.
  - `/home/hy/.local/bin/graphify update .` completed; `bash scripts/knowledge/report-graphify-health.sh` remains `status=advisory` due to `surprising_cross_root_inferred_edges=3`.

## Related Documents

- **Parent Plan**: [Lifecycle README debt closure plan](../plans/2026-05-22-lifecycle-readme-debt-closure.md)
- **Previous remediation task**: [Workspace docs and agent governance remediation task](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Template catalog**: [Template catalog](../../99.templates/README.md)
