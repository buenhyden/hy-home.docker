---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-06-02-agent-governance-phase-3-approved-surface-activation.md -->

# Task: Agent Governance Phase 3 Approved Surface Activation

## Overview

이 문서는 Phase 2 strategy integration 이후 사용자가 승인한 policy, runtime, CI, templates, secrets, remote GitHub, model policy, and provider adapter 표면을 Phase 3 repository contract로 반영한 실제 작업 evidence를 기록한다.

## Inputs

- **Parent Plan**: [Agent Governance Phase 3 Approved Surface Activation Plan](../plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md)
- **Phase 2 Plan**: [Agent Governance Phase 2 Strategy Integration Plan](../plans/2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Phase 2 Task**: [Agent Governance Phase 2 Strategy Integration Task](./2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Task Checklist**: [Task Checklists](../../00.agent-governance/rules/task-checklists.md)
- **Task Template**: [Task template](../../99.templates/task.template.md)

## Working Rules

- User approval covers policy, runtime, CI, templates, secrets, remote GitHub, model policy, and provider adapter surfaces for this Phase 3 pass.
- Approval is bound to evidence. Secret values, private keys, token-bearing logs, shell history, and full secret file bodies must not be printed, committed, or summarized.
- Remote GitHub work in this pass is read-only verification because no concrete remote mutation target was provided.
- Runtime work in this pass is protocol activation only because no concrete service target was provided.
- Model/provider adapter work in this pass is protocol activation only because no concrete model value, role, provider, and validation target was provided.
- Graphify remains advisory when health reports cross-root inferred edges; architecture and policy claims are corroborated against tracked Stage 00/04 docs and validators.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Policy | User approval on 2026-06-02 | Stage 00 checklist/scopes/governance docs | Phase 2 deferred high-risk surfaces behind approval gates. | High-risk evidence protocols added to Stage 00 docs. | Revert Phase 3 policy-doc commit. | No secrets or token-bearing logs. |
| Runtime | User approval on 2026-06-02 | Runtime mutation protocol only | Phase 2 out-of-scope live runtime mutation. | Infra scope now requires target/precheck/rollback/postcheck; no live mutation performed. | Revert infra scope change; runtime state unchanged. | No service logs or secrets captured. |
| CI | User approval on 2026-06-02 | Repo-contract validator | No approved-surface template check existed. | `check-repo-contracts.sh` validates task template approved-surface section. | Revert validator/template changes. | No secrets. |
| Templates | User approval on 2026-06-02 | `task.template.md` and template catalog | Task template lacked high-risk evidence section. | Task template includes optional `## Approved Surface Evidence`. | Revert template/catalog changes. | Placeholder section only. |
| Secrets | User approval on 2026-06-02 | Metadata-only count evidence | Secrets scope allowed Docker/Vault guidance but lacked approved-secrets evidence boundary. | Security scope requires metadata-only evidence unless concrete redacted target exists; count-only check reports 97 files. | Revert security scope change; no value mutation performed. | No secret values read or printed. |
| Remote GitHub | User approval on 2026-06-02 | Read-only repo verification | Remote mutation remained approval-gated. | GitHub governance now requires before/after/rollback evidence; read-only `gh repo view` confirmed repo `buenhyden/hy-home.docker`, default branch `main`, public repo. | Revert GitHub governance change; no remote mutation performed. | No GitHub secrets or tokens printed. |
| Model policy | User approval on 2026-06-02 | Model/provider protocol only | Model changes required Stage 00/sync/validator support. | Subagent protocol now states exact coupled surfaces required before model changes; no model value changed. | Revert subagent protocol change. | No provider credentials or secret values. |
| Provider adapters | User approval on 2026-06-02 | Provider adapter protocol only | Provider adapter redesign remained approval-gated. | Provider sync remains required; no adapter drift introduced. | Revert subagent protocol change; adapters unchanged. | No provider credentials or secret values. |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-P3-001 | Inspect Phase 2 evidence, Graphify report, Stage 00 policy surfaces, provider sync policy, task template, remote GitHub identity, and secrets metadata count. | eval | N/A | PLN-P3-001 | Graphify read first; remote read-only and secret count-only evidence collected. | Codex | Completed |
| T-P3-002 | Add approved high-risk surface protocols to Stage 00 checklist, infra, security, QA, GitHub governance, and subagent/model/provider docs. | doc | N/A | PLN-P3-001 | Policy docs updated; no live runtime, secret value, remote mutation, model value, or adapter change. | Codex | Completed |
| T-P3-003 | Add approved-surface evidence section to task template and catalog. | doc | N/A | PLN-P3-002 | `task.template.md` and `docs/99.templates/README.md` updated. | Codex | Completed |
| T-P3-004 | Add repo-contract validation for task template approved-surface evidence. | guardrail | N/A | PLN-P3-003 | `bash -n` and repo contracts validate the new check. | Codex | Completed |
| T-P3-005 | Create Phase 3 plan/task artifacts and update Stage 04 indexes and progress log. | doc/memory | N/A | PLN-P3-004 | Stage 04 artifacts and indexes updated. | Codex | Completed |
| T-P3-006 | Refresh generated evidence and run validation gates. | eval | N/A | PLN-P3-005 | Verification summary records final command outcomes. | Codex | Completed |

## Suggested Types

- `doc`
- `eval`
- `guardrail`
- `memory`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`
- `policy`

## Phase View (Optional)

### Phase 1 - Approval Surface Inspection

- [x] T-P3-001 Inspect Phase 2, Stage 00, remote, secrets metadata, and graph evidence.

### Phase 2 - Contract Activation

- [x] T-P3-002 Update Stage 00 policy surfaces.
- [x] T-P3-003 Update task template and catalog.
- [x] T-P3-004 Add repo-contract validation.

### Phase 3 - Evidence Closure

- [x] T-P3-005 Create Phase 3 plan/task/index/progress evidence.
- [x] T-P3-006 Run final validation gates.

## Verification Summary

- **Test Commands**:
  - `bash -n scripts/validation/check-repo-contracts.sh` — PASS.
  - `git diff --check` — PASS.
  - `bash scripts/validation/check-repo-contracts.sh` — PASS (`failures=0`; `changed_template_docs_total=5`; `normalized_changed_template_docs_total=5`; `target_stage_docs_total=526`; `normalized_target_stage_docs_total=526`; approved-surface template check present).
  - `bash scripts/validation/check-doc-traceability.sh` — PASS (`failures=0`; `catalog_pairs_total=46`).
  - `bash scripts/knowledge/generate-llm-wiki-index.sh` — regenerated `docs/90.references/llm-wiki/index.md` with 1028 paths after staging the new Phase 3 Stage 04 artifacts.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — PASS.
- **Eval Commands**:
  - `gh repo view --json nameWithOwner,defaultBranchRef,isPrivate` — PASS; read-only output confirmed `buenhyden/hy-home.docker`, default branch `main`, `isPrivate=false`.
  - `find secrets -type f -printf '%p\n' | wc -l` — PASS; metadata-only count reported 97 files and no secret values.
  - `bash scripts/operations/sync-provider-surfaces.sh` — PASS (`no drift`).
  - `/home/hy/.local/bin/graphify update .` — regenerated `graphify-out` with 2412 nodes, 2833 edges, and 125 communities.
  - `bash scripts/knowledge/report-graphify-health.sh` — advisory (`manifest_paths_total=821`; `surprising_cross_root_inferred_edges=3`; no volume, gitlink, generated/minified contamination, or meaningless god nodes).
- **Logs / Evidence Location**:
  - This task document.
  - [Progress log](../../00.agent-governance/memory/progress.md)
  - [LLM Wiki index](../../90.references/llm-wiki/index.md)

## Scope Safety

- Stage 00 policy changed: Yes, bounded high-risk evidence protocols only.
- Template contract changed: Yes, task template approved-surface evidence section added.
- CI/validator changed: Yes, repo-contract template check added.
- Docker runtime changed: No.
- Secrets values read or printed: No.
- Secrets metadata count inspected: Yes, count-only evidence.
- Remote GitHub read-only check performed: Yes.
- Remote GitHub mutation performed: No.
- Model values changed: No.
- Provider adapters changed: No.
- Provider sync drift introduced: No.
- Broad HADS rollout performed: No.

## Related Documents

- **Parent Plan**: [Agent Governance Phase 3 Approved Surface Activation Plan](../plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md)
- **Phase 2 Plan**: [Agent Governance Phase 2 Strategy Integration Plan](../plans/2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Phase 2 Task**: [Agent Governance Phase 2 Strategy Integration Task](./2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Task Checklist**: [Task Checklists](../../00.agent-governance/rules/task-checklists.md)
- **Subagent Protocol**: [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- **Security Scope**: [Security Enforcement Scope](../../00.agent-governance/scopes/security.md)
- **Infrastructure Scope**: [Infrastructure Operational Scope](../../00.agent-governance/scopes/infra.md)
- **QA Scope**: [Quality Assurance Scope](../../00.agent-governance/scopes/qa.md)
- **GitHub Governance**: [GitHub Governance Policy](../../00.agent-governance/rules/github-governance.md)
- **Task Template**: [Task template](../../99.templates/task.template.md)
