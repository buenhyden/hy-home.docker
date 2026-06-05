---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-22-lifecycle-readme-debt-closure.md -->

# Lifecycle README Debt Closure Plan

> Plan for closing the remaining lifecycle, README readiness, and agent governance debt after the workspace remediation baseline.

## Overview

이 문서는 `hy-home.docker`의 문서 lifecycle과 agent governance 잔여 debt를 닫기 위한 실행 계획이다. 기존 workspace docs and agent governance remediation을 기준선으로 삼고, 남은 legacy-shape 문서와 infra service README readiness gap을 정리한다.

## Context

현재 repository contract와 doc traceability 검증은 통과한다. 다만 `check-repo-contracts.sh`가 report-first 지표로 보여주는 잔여 debt가 남아 있다.

- target-stage 문서 463개 중 4개가 legacy template-shape로 분류된다.
- infra service leaf README 42개가 `Service Readiness` 필드 기준으로 partial 상태다.
- Graphify health는 `surprising_cross_root_inferred_edges=3` 때문에 advisory이며, codebase 결론은 tracked source files와 stage docs로 교차확인해야 한다.

## Goals & In-Scope

- **Goals**:
  - `DOC-LRDC-001`: target-stage legacy-shape 문서 4개를 현재 template contract에 맞춘다.
  - `DOC-LRDC-002`: infra service leaf README의 `Service Readiness` debt를 닫는다.
  - `DOC-LRDC-003`: README template과 template catalog가 folder-index/service-leaf 책임을 더 명확히 설명하게 한다.
  - `DOC-LRDC-004`: stage edit hook guidance와 Hookify stage-doc rule이 relative/absolute path 모두를 다루게 한다.
  - `DOC-LRDC-005`: validators는 changed/new docs hard-fail과 repository-wide report-first 지표를 유지한다.
- **In Scope**:
  - `docs/99.templates/README.md`
  - `docs/99.templates/readme.template.md`
  - selected target-stage docs under `docs/03.specs`, `docs/04.execution`, and `docs/05.operations`
  - infra service leaf `README.md` files
  - `.claude/hookify.warn-stage-doc-edit.local.md`
  - `scripts/hooks/agent-event-hook.sh`
  - execution README/index documents and governance progress log

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Docker Compose runtime behavior, service topology, image versions, ports, networks, or secret files are not changed.
  - Historical evidence dates, commands, outcomes, and recorded decisions are not reinterpreted.
  - Root shims are not expanded into monolithic policy files.
- **Out of Scope**:
  - secret values, credentials, private keys, shell history, and log databases
  - user-global runtime settings
  - existing untracked `projects/storybook/mcp/`

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-LRDC-001 | Add plan/task evidence and execution indexes | `docs/04.execution/**` | DOC-LRDC-001 | New plan/task are discoverable from execution READMEs |
| PLN-LRDC-002 | Clarify README template and template catalog rules | `docs/99.templates/README.md`, `docs/99.templates/readme.template.md` | DOC-LRDC-003 | Template inventory and repo contract checks pass |
| PLN-LRDC-003 | Normalize the 4 legacy target-stage documents | selected `docs/03.specs`, `docs/04.execution`, `docs/05.operations` files | DOC-LRDC-001 | `legacy_target_stage_docs_skipped=0` |
| PLN-LRDC-004 | Add/align infra service `Service Readiness` tables | `infra/**/README.md` service leaves | DOC-LRDC-002 | `infra_service_readmes_rubric_partial=0` |
| PLN-LRDC-005 | Improve stage README edit hook guidance | `.claude/hookify.*`, `scripts/hooks/agent-event-hook.sh` | DOC-LRDC-004 | hook smoke tests emit expected guidance |
| PLN-LRDC-006 | Verify repository contracts and generated knowledge surfaces | validators, LLM Wiki, Graphify report | DOC-LRDC-005 | Required validation commands pass or record explicit advisory reason |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-LRDC-001 | Syntax | Shell syntax and patch hygiene | `git diff --check` and `bash -n scripts/validation/check-repo-contracts.sh scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh` | exit code 0 |
| VAL-LRDC-002 | JSON | Hook config validity | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | both exit code 0 |
| VAL-LRDC-003 | Contract | Repository docs/runtime contract | `bash scripts/validation/check-repo-contracts.sh` | exit code 0 and debt metrics closed |
| VAL-LRDC-004 | Traceability | Execution and operations traceability | `bash scripts/validation/check-doc-traceability.sh` | exit code 0 |
| VAL-LRDC-005 | Security Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | exit code 0 |
| VAL-LRDC-006 | Generated Docs | LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | exit code 0 |
| VAL-LRDC-007 | Compose | Compose static validation | `bash scripts/validation/validate-docker-compose.sh` | exit code 0 |
| VAL-LRDC-008 | Hooks | Stage edit, README edit, and Stop hook smoke tests | sample JSON piped to `scripts/hooks/agent-event-hook.sh` | expected guidance or block decision observed |
| VAL-LRDC-009 | Graphify | Graph health refresh and status report | `graphify update .` if available, then `bash scripts/knowledge/report-graphify-health.sh` | clean or advisory reason recorded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Infra README tables overstate runtime facts | High | Derive only path, file, and non-secret linkage evidence; use `N/A` or `Not declared` where evidence is absent |
| Historical docs are rewritten beyond template debt | Medium | Limit edits to headings, placeholders, links, and factual current-path wording |
| Validator becomes too strict for old evidence | Medium | Keep changed/new hard-fail behavior and report-first full-repo metrics unless all known debt is closed |
| Hook guidance duplicates policy | Low | Keep policy in governance docs and hooks as advisory context only |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repository validators and hook smoke tests pass locally.
- **Sandbox / Canary Rollout**: documentation and hook guidance only; no Docker runtime mutation.
- **Human Approval Gate**: user explicitly approved modifying docs, templates, runtime hook files, and validators for this plan.
- **Rollback Trigger**: any required validation cannot pass without changing runtime behavior or inventing operational facts.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Plan/task evidence exists and parent execution READMEs link to both.
- [x] The 4 legacy-shape target-stage docs no longer appear as skipped debt.
- [x] Infra service README readiness debt is closed.
- [x] README template and template catalog explain folder-index/service-leaf routing clearly.
- [x] Hook guidance handles stage docs and README edits.
- [x] Required validation commands pass or record a bounded advisory reason.

## Related Documents

- **Task**: [Lifecycle README debt closure task](../tasks/2026-05-22-lifecycle-readme-debt-closure.md)
- **Previous remediation plan**: [Workspace docs and agent governance remediation plan](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Template catalog**: [Template catalog](../../99.templates/README.md)
- **README template**: [README template](../../99.templates/readme.template.md)
