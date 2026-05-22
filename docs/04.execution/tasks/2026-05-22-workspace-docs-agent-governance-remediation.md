---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-05-22-workspace-docs-agent-governance-remediation.md -->

# Task: Workspace Docs and Agent Governance Remediation

> Execution evidence for workspace documentation lifecycle, template contract, and agent governance remediation.

## Overview (KR)

이 문서는 workspace docs and agent governance remediation 작업의 실제 수행 상태와 검증 evidence를 기록한다.

## Inputs

- **Parent Plan**: [Workspace docs and agent governance remediation plan](../plans/2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- Historical evidence documents are preserved unless they duplicate a canonical document or live in a non-canonical path.
- Duplicate documents are removed only after references are migrated to the canonical target.
- Runbook recovery content must be factual. If no verified recovery step exists, record N/A with a safe escalation path.
- Do not read or copy secret values, private keys, shell history, log databases, or personal settings.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add remediation plan/task evidence and execution README links | doc | Documentation protocol | PLN-001 | Plan/task files and README links exist in `docs/04.execution/README.md`, `plans/README.md`, and `tasks/README.md` | doc-writer | Done |
| T-002 | Update template guidance for lifecycle, duplicate cleanup, and runbook recovery | doc | Template catalog | PLN-002 | Template guidance updated and template/security baseline passes | doc-writer | Done |
| T-003 | Normalize README and target-stage metadata/heading drift | doc | README contract | PLN-003 | Full-stage template gate passes with `normalized_changed_template_docs_total=268` | doc-writer | Done |
| T-004 | Remove duplicate infra_net ARD/ADR after reference migration | doc | Architecture stage | PLN-004 | Deleted duplicate architecture paths have no remaining direct references | doc-writer | Done |
| T-005 | Align root/runtime governance, RTK guidance, Hookify tracked exception | guardrail | Agent governance | PLN-005 | JSON, bash syntax, runtime catalog, and hook parity checks pass | doc-writer | Done |
| T-006 | Expand repository contract validator to full-stage target docs | guardrail | Repository contract | PLN-006 | `check-repo-contracts.sh` passes with `failures=0` | doc-writer | Done |
| T-007 | Refresh LLM Wiki index and governance progress log | doc | LLM Wiki contract | PLN-007 | Generator check passes and progress log updated | doc-writer | Done |
| T-008 | Run verification suite and record final evidence | test | Verification plan | VAL-PLN-* | Test Plan commands passed; Graphify health remains advisory | doc-writer | Done |

## Suggested Types

- `doc`
- `guardrail`
- `ops`
- `test`

## Agent-specific Types (If Applicable)

- `tool`
- `memory`
- `guardrail`
- `eval`

## Phase View (Optional)

### Phase 1

- [x] T-001 Add plan/task evidence and README links
- [x] T-002 Update template guidance
- [x] T-006 Prepare validator contract expansion

### Phase 2

- [x] T-003 Normalize README and stage docs
- [x] T-004 Remove duplicate infra_net ARD/ADR
- [x] T-005 Align agent/runtime governance and Hookify exception

### Phase 3

- [x] T-007 Refresh generated docs and progress log
- [x] T-008 Run final verification

## Verification Summary

- **Test Commands**:
  - PASS: `git diff --check`
  - PASS: `bash -n scripts/validation/check-repo-contracts.sh scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh`
  - PASS: `python3 -m json.tool .claude/settings.json`
  - PASS: `python3 -m json.tool .codex/hooks.json`
  - PASS: `bash scripts/validation/check-repo-contracts.sh`
  - PASS: `bash scripts/validation/check-doc-traceability.sh`
  - PASS: `bash scripts/validation/check-template-security-baseline.sh`
  - PASS: `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
  - PASS: `bash scripts/validation/validate-docker-compose.sh`
- **Eval Commands**:
  - PASS: `PreToolUse` sample emitted target-stage template guidance.
  - PASS: `PostToolUse` sample routed to repository contract and traceability checks.
  - PASS: `Stop` sample emitted JSON `decision: block` for a temporary invalid target-stage task document; the temporary file was removed.
- **Logs / Evidence Location**:
  - This task document and `docs/00.agent-governance/memory/progress.md`.

## Related Documents

- **Parent Plan**: [Workspace docs and agent governance remediation plan](../plans/2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Template catalog**: [Template catalog](../../99.templates/README.md)
- **Agent governance hub**: [Agent governance README](../../00.agent-governance/README.md)
- **LLM Wiki index**: [Generated LLM Wiki index](../../90.references/llm-wiki/index.md)
