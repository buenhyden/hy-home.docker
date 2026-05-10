---
status: completed
---

# Scripts Lifecycle Contract Cleanup Plan

## Overview (KR)

이 문서는 `scripts/` 디렉터리의 live audit 결과를 바탕으로 script lifecycle, README template alignment, repository contract 표현을 정리하는 실행 계획이다. 현재 근거로 삭제가 정당화되는 스크립트는 없으므로, 이번 작업은 삭제가 아니라 문서와 검증 계약의 의미를 명확히 하는 cleanup이다.

## Context

사용자 요청이 `docs/04.execution/plans` 작성 권한을 명시적으로 부여했다. Live audit 기준 `scripts/`에는 root shell script 22개와 `scripts/lib/hardening-lib.sh` 1개가 있으며, 각 root script는 inventory, lifecycle category, repository reference, 또는 explicit standalone exemption으로 설명되어야 한다.

Graphify output is advisory for this task. `graphify-out/GRAPH_REPORT.md` includes generated-volume contamination and meaningless god nodes, so conclusions must be corroborated against tracked source files, `scripts/README.md`, `scripts/check-repo-contracts.sh`, and repository validators.

## Goals & In-Scope

- **Goals**:
  - `scripts/README.md`를 `docs/99.templates/readme.template.md`의 base structure에 맞춘다.
  - script lifecycle table과 usage examples는 유지한다.
  - `scripts/check-repo-contracts.sh`의 external-reference exemption 의미를 명확히 한다.
  - 새 plan과 parent README traceability를 유지한다.
- **In Scope**:
  - `scripts/README.md`
  - `scripts/check-repo-contracts.sh`
  - `docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md`
  - `docs/04.execution/plans/README.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - root script 삭제, rename, CLI interface 변경
  - CI, hook, pre-commit, Docker Compose execution contract 변경
  - `check-repo-contracts.sh` failure condition 변경
- **Out of Scope**:
  - `docs/00.agent-governance/memory/*` 수정
  - secret value, token, private key, generated certificate content 열람 또는 문서화
  - `graphify-out` generated artifact hand edit
  - 신규 PRD, ARD, ADR, Spec, Task, Operation, Runbook 생성

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | README base sections 추가 | `scripts/README.md` | REQ-SCRIPT-001 | `Audience`, `Scope`, `Structure`, `How to Work in This Area` 존재 |
| PLN-002 | Script lifecycle contract wording 정리 | `scripts/README.md` | REQ-SCRIPT-002 | manual operation과 standalone exemption 의미가 분리됨 |
| PLN-003 | External-reference exemption naming 정리 | `scripts/check-repo-contracts.sh` | REQ-SCRIPT-003 | `manual_root_scripts` naming이 제거되고 동작은 동일함 |
| PLN-004 | Plan artifact 추가 | `docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md` | REQ-DOC-001 | plan template 필수 섹션과 실제 related links 포함 |
| PLN-005 | Parent README sync | `docs/04.execution/plans/README.md` | REQ-DOC-002 | 새 plan이 structure와 related documents에 연결됨 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository contract 확인 | `bash scripts/check-repo-contracts.sh` | failures=0 |
| VAL-PLN-002 | Structural | Docs traceability 확인 | `bash scripts/check-doc-traceability.sh` | failures=0 |
| VAL-PLN-003 | Syntax | Bash syntax 확인 | `bash -n scripts/*.sh scripts/lib/*.sh .claude/hooks/*.sh` | no syntax errors |
| VAL-PLN-004 | Advisory | Graphify corpus health 확인 | `bash scripts/report-graphify-health.sh` | exits 0; advisory status is not treated as architecture authority |
| VAL-PLN-005 | Optional | Graphify refresh | `graphify update .` | run only if CLI is available after script code changes; otherwise report skipped |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| README normalization removes useful inventory detail | Medium | Preserve the existing inventory, lifecycle table, usage examples, and references. |
| Manual operations are mistaken for reference exemptions | Medium | Use external-reference exemption wording and keep the exemption set explicit. |
| Contract checker behavior changes accidentally | High | Rename variables/messages only and verify with `check-repo-contracts.sh`. |
| Secret examples expose sensitive material | High | Keep examples procedural and avoid generated values, tokens, keys, or certificate bodies. |
| Graphify output is over-trusted | Medium | Treat Graphify as advisory and rely on tracked source plus validators. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repository contract, docs traceability, and Bash syntax checks pass.
- **Sandbox / Canary Rollout**: 적용하지 않는다. 런타임 동작 변경이 없다.
- **Human Approval Gate**: script deletion, CLI rename, generated secret inspection, or memory maintenance requires a separate explicit request.
- **Rollback Trigger**: validator failure or behavior-changing diff in `check-repo-contracts.sh`.
- **Prompt / Model Promotion Criteria**: 적용하지 않는다.

## Completion Criteria

- [x] `scripts/README.md` includes the required README base sections.
- [x] `scripts/check-repo-contracts.sh` uses clear external-reference exemption wording without behavior changes.
- [x] The new plan is linked from `docs/04.execution/plans/README.md`.
- [x] Required verification commands pass or are explicitly reported as skipped with reason.

## Related Documents

- [scripts README](../../../scripts/README.md)
- [Repository contract checker](../../../scripts/check-repo-contracts.sh)
- [Plan template](../../99.templates/plan.template.md)
- [README template](../../99.templates/readme.template.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Graphify report](../../../graphify-out/GRAPH_REPORT.md)
