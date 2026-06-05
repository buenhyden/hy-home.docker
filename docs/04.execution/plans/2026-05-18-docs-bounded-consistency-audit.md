---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-18-docs-bounded-consistency-audit.md -->

# Docs Bounded Consistency Audit Plan

## Overview

이 문서는 `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, 루트 `README.md`의 bounded consistency audit 실행 계획이다. 범위는 사실 불일치, stale inventory, README 진입성, Related Documents, 검증 스크립트로 확인 가능한 drift에 한정한다.

## Context

최근 stage별 문서 보정 작업으로 repository validators는 통과하고 있다. 다만 루트 `README.md`의 현재 인벤토리 수치와 canonical README 상태값처럼 validator가 직접 잡지 못하는 entrypoint drift가 남아 있다.

이 계획은 broad rewrite나 historical evidence 재작성을 하지 않고, 사람이 첫 화면에서 보는 문서 진입점과 재현 가능한 inventory만 정리한다.

## Goals & In-Scope

- **Goals**:
  - 루트 `README.md`의 현재 인벤토리를 재현 가능한 command 기준으로 갱신한다.
  - canonical stage README가 실제 entrypoint 역할과 충돌하지 않도록 상태를 정규화한다.
  - `docs/04.execution`의 plan/task index에 이 audit 작업을 연결한다.
  - focused scans와 repository validators로 변경 범위를 검증한다.
- **In Scope**:
  - `README.md`
  - `docs/01.requirements/README.md`
  - `docs/02.architecture/README.md`
  - `docs/02.architecture/requirements/README.md`
  - `docs/02.architecture/decisions/README.md`
  - `docs/04.execution/README.md`
  - `docs/04.execution/plans/README.md`
  - `docs/04.execution/tasks/README.md`
  - `docs/04.execution/plans/2026-05-18-docs-bounded-consistency-audit.md`
  - `docs/04.execution/tasks/2026-05-18-docs-bounded-consistency-audit.md`
  - `docs/90.references/llm-wiki/index.md` when regenerated to include the new audit paths
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not create new PRD, ARD, ADR, or Spec documents.
  - Do not bulk-rewrite leaf PRDs, ARDs, ADRs, Specs, operations documents, or historical execution evidence.
  - Do not normalize prose style across all docs.
  - Do not edit `docs/99.templates` unless a concrete template gap is discovered and separately planned.
- **Out of Scope**:
  - Runtime Docker Compose behavior, service configuration, or deployment changes.
  - Secret values, credential contents, token contents, certificate bodies, or shell history.
  - Existing untracked `projects/storybook/mcp/`.
  - Branch history cleanup, PR creation, deployment, or external publishing.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create bounded audit plan/task artifacts | `docs/04.execution/plans/2026-05-18-docs-bounded-consistency-audit.md`, `docs/04.execution/tasks/2026-05-18-docs-bounded-consistency-audit.md` | DOC-AUDIT-001 | New docs have frontmatter, Target comments, required sections, and working links |
| PLN-002 | Sync execution indexes to the audit artifacts | `docs/04.execution/README.md`, `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md` | DOC-AUDIT-002 | Parent READMEs link the plan/task pair |
| PLN-003 | Refresh root README inventory facts | `README.md` | DOC-AUDIT-003 | Inventory values are derived from documented commands |
| PLN-004 | Normalize canonical README status drift | `docs/01.requirements/README.md`, `docs/02.architecture/README.md`, `docs/02.architecture/requirements/README.md`, `docs/02.architecture/decisions/README.md` | DOC-AUDIT-004 | Canonical entrypoint READMEs no longer present as draft-only artifacts |
| PLN-005 | Run focused scans and validators | validation commands | DOC-AUDIT-005 | Focused scans and repository validators pass |
| PLN-006 | Record completion evidence | `docs/00.agent-governance/memory/progress.md`, task evidence | DOC-AUDIT-006 | Progress log and task evidence summarize checks without raw logs or secrets |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-AUDIT-001 | Inventory | Count Compose files including `.yml` and `.yaml` | `git ls-files 'infra/**/docker-compose*.yml' 'infra/**/docker-compose*.yaml' \| wc -l` | Root README matches the command output |
| VAL-AUDIT-002 | Inventory | Count Compose service directories | `git ls-files 'infra/**/docker-compose.yml' \| xargs -n1 dirname \| sort -u \| wc -l` | Root README matches the command output |
| VAL-AUDIT-003 | Inventory | Count secret value/cert files without reading contents | `find secrets -type f -not -path '*/README.md' \| wc -l` | Root README matches the command output; no secret contents are read |
| VAL-AUDIT-004 | Inventory | Count tracked README files | `git ls-files '*README.md' \| wc -l` | Root README matches the command output |
| VAL-AUDIT-005 | Discoverability | Check Related Documents coverage | `rg --files-without-match "## Related Documents" README.md docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references` | No output |
| VAL-AUDIT-006 | Placeholders | Check for real placeholder/fake-link drift | Focused `rg` placeholder scan, manually classify true placeholders versus literal examples | No actionable placeholder drift remains in edited docs |
| VAL-AUDIT-007 | Repository Contract | Verify repository Docker/docs contracts | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-AUDIT-008 | Traceability | Verify execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-AUDIT-009 | LLM Wiki Freshness | Verify generated LLM Wiki index | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS or regenerate index and rerun |
| VAL-AUDIT-010 | Diff Hygiene | Check whitespace and conflict markers | `git diff --check` | PASS |
| VAL-AUDIT-011 | Graphify Health | Report graph navigation health | `bash scripts/knowledge/report-graphify-health.sh` | `clean`, or `advisory` only for known cross-root inferred edges |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Audit expands into broad rewrite | High | Limit edits to README entrypoints, reproducible inventory facts, and current audit artifacts |
| Historical evidence meaning changes | High | Do not rewrite leaf historical plan/task/PRD/ARD/ADR content unless a concrete factual error is discovered |
| Secret data is exposed while counting files | High | Count file paths only; do not open secret value/cert contents |
| Graphify advisory edges are treated as truth | Medium | Use Graphify only as a navigation aid; corroborate with tracked source and governance docs |
| Existing untracked Storybook MCP files are touched | High | Do not edit or stage `projects/storybook/mcp/`; verify with `git status` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Focused scans and repository validators must pass before completion.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only audit.
- **Human Approval Gate**: The user approved this bounded consistency audit plan.
- **Rollback Trigger**: Revert only scoped docs changes if validators cannot pass without broad rewrites.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] New audit plan/task artifacts exist and are linked from parent READMEs.
- [x] Root `README.md` inventory values match the documented commands.
- [x] Canonical README entrypoints do not present as draft-only artifacts.
- [x] Related Documents and placeholder focused scans pass or have only intentional literal examples.
- [x] Repository validators pass.
- [x] Governance progress log records final evidence.

## Related Documents

- **Execution README**: [../README.md](../README.md)
- **Execution Task**: [../tasks/2026-05-18-docs-bounded-consistency-audit.md](../tasks/2026-05-18-docs-bounded-consistency-audit.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Root README**: [../../../README.md](../../../README.md)
