---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md -->

# Targeted Documentation Precision Remediation Plan

## Overview (KR)

이 문서는 `README.md`, `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`를 대상으로 한 정밀 문서 보정 계획이다. 범위는 validator가 통과한 이후에도 남을 수 있는 discoverability, target-relative link, stage ownership, current evidence drift에 한정한다.

## Context

최근 stage별 보정 작업과 bounded consistency audit으로 `check-repo-contracts.sh`와 `check-doc-traceability.sh`는 통과한다. 이번 작업은 broad rewrite가 아니라, 각 편집을 구체적인 failing condition에 묶어 불필요한 template churn을 막는 precision remediation이다.

## Goals & In-Scope

- **Goals**:
  - 각 편집을 evidence gate에 연결한다.
  - target-relative link mismatch와 reader-facing discoverability 문제를 고친다.
  - 새 실행 plan/task evidence를 canonical `docs/04.execution` stage에 남긴다.
  - 변경된 parent README와 generated path index를 필요한 경우에만 동기화한다.
- **In Scope**:
  - `README.md`
  - `docs/01.requirements/**`
  - `docs/02.architecture/**`
  - `docs/03.specs/**`
  - `docs/04.execution/**`
  - `docs/05.operations/**`
  - `docs/90.references/**`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Historical leaf documents를 current template 모양으로 일괄 재작성하지 않는다.
  - Style-only prose rewrite를 하지 않는다.
  - Runtime Docker Compose, service config, API behavior, secret structure를 바꾸지 않는다.
  - Graphify inferred edge를 새 remediation scope로 사용하지 않는다.
- **Out of Scope**:
  - secret 값, credential, token, 인증서 본문, shell history, raw logs 열람.
  - 기존 untracked `projects/storybook/mcp/`.
  - branch history cleanup, deployment, external publishing.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Record current precision remediation plan/task evidence | `docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md`, `docs/04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md` | DOC-PRECISION-001 | Plan/task use canonical paths, Target comments, and valid Related Documents |
| PLN-002 | Run evidence-gated drift scans | target docs set | DOC-PRECISION-002 | Missing Related Documents, placeholder, stale taxonomy, pseudo-link, and operations profile scans are classified |
| PLN-003 | Fix only concrete drift | affected docs only | DOC-PRECISION-003 | Every edit cites a failing condition in task evidence |
| PLN-004 | Sync parent README/index docs | `docs/04.execution/README.md`, plans/tasks README, generated LLM Wiki index if path set changes | DOC-PRECISION-004 | New plan/task paths are discoverable |
| PLN-005 | Verify reader smoke flows and validators | validation commands | DOC-PRECISION-005 | Focused scans, smoke flows, validators, and diff hygiene pass or have documented intentional exceptions |
| PLN-006 | Record final progress evidence | `docs/00.agent-governance/memory/progress.md` | DOC-PRECISION-006 | Progress log records concise final status and evidence only |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PRECISION-001 | Coverage | Check required related-doc sections | `rg --files-without-match "^## Related Documents$" README.md docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references -g '*.md'` | No actionable missing files |
| VAL-PRECISION-002 | Placeholder | Check real placeholders in non-template docs | focused `rg` placeholder scan | No actionable non-template placeholder remains |
| VAL-PRECISION-003 | Link hygiene | Check pseudo-links, stale taxonomy, absolute links, and `file://` usage | focused `rg` scans | Findings are fixed or documented as intentional command payloads |
| VAL-PRECISION-004 | Operations purpose | Check guide/policy/runbook heading separation | focused operations heading scan | No cross-profile heading drift in edited docs |
| VAL-PRECISION-005 | Smoke Flow | Validate root and operations navigation | manual README link path walk | Root README -> docs README -> stage README -> leaf doc works; operations README -> guide/policy/runbook works |
| VAL-PRECISION-006 | Repository Contract | Verify repository docs contracts | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-PRECISION-007 | Traceability | Verify execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-PRECISION-008 | LLM Wiki | Verify generated index freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS, regenerating only if tracked path set changed |
| VAL-PRECISION-009 | Diff Hygiene | Check whitespace and conflict markers | `git diff --check` | PASS |
| VAL-PRECISION-010 | Graphify | Refresh/report graph navigation after approved docs edits | `graphify update .` if available, then `bash scripts/knowledge/report-graphify-health.sh` | Clean or advisory-only for known inferred edges |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Precision pass becomes bulk rewrite | High | Require a failing condition before each edit |
| Historical task evidence meaning changes | High | Do not rewrite historical leaf plan/task content unless the failing condition is current and concrete |
| Secret data exposure | High | Count paths only; never open secret values or credential files |
| Generated index churn | Medium | Regenerate LLM Wiki only when tracked path inventory changes |
| Graphify inferred edges mislead remediation | Medium | Use Graphify as navigation/reporting evidence only |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Focused scans and repository validators must pass before completion.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only remediation.
- **Human Approval Gate**: User approved the plan before implementation.
- **Rollback Trigger**: Revert scoped docs changes only if validators cannot pass without broader rewrite.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Plan/task evidence is present and linked.
- [x] Each edited file maps to a failing condition.
- [x] Parent README/index files are synchronized for new paths.
- [x] Reader smoke flows pass.
- [x] Repository validators and diff hygiene pass.
- [x] Progress log records final evidence.

## Related Documents

- **Execution README**: [../README.md](../README.md)
- **Execution Task**: [../tasks/2026-05-18-targeted-docs-precision-remediation.md](../tasks/2026-05-18-targeted-docs-precision-remediation.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Root README**: [../../../README.md](../../../README.md)
