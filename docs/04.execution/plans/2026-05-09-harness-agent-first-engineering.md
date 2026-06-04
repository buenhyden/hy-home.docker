---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-09-harness-agent-first-engineering.md -->

# Harness / Agent-first Engineering Plan

## Overview (KR)

이 계획은 현재 `hy-home.docker`에 구현된 하네스 엔지니어링과 Agent-first Engineering 계약을 파일 내용 기준으로 분석하고, 실제 gap을 최소 수정으로 보완하는 실행 계획이다.

## Context

최근 repository contract는 `.claude` runtime mirror, Codex boundary, source-label leak prevention, graphify fallback, `rg` discovery permission을 이미 검증한다. 이후 확인된 gap은 세 가지다: Claude hooks의 double-quoted Python block이 markdown backtick command substitution을 유발할 수 있음, HAFE evidence가 `core` profile과 supported hardening tiers 범위를 전체 workspace처럼 읽힐 수 있음, Graphify advisory output이 architecture authority처럼 오해될 수 있음.

## Goals & In-Scope

- 워크스페이스 목적, 규칙, 환경을 관련 파일 기준으로 정리한다.
- 하네스 엔지니어링 구성 요소를 분석한다.
- Agent-first Engineering 구성 요소를 분석한다.
- 현재 gap이 없는 agent/catalog 계약은 no-agent-catalog-change로 명시한다.
- Claude hook quoting gap을 heredoc/argv 방식으로 보완한다.
- 기존 stage docs와 parent README traceability를 유지하고, 이번 Graphify 보완은 existing stage docs in-place로 반영한다.
- Graphify health가 clean이 아니면 advisory context로 낮추는 규칙과 evidence command를 추가한다.
- `10-communication` Compose include/IP/network 문제는 별도 infra remediation으로 분리한다.
- 지정 검증 명령으로 완료를 증명한다.

## Non-Goals & Out-of-Scope

- 새 agent catalog 또는 Codex delegated-agent catalog 생성.
- Agent catalog, root shim, provider policy, `.codex` delegated-agent behavior 변경.
- `docs/01.requirements`, `docs/02.architecture/requirements`, `docs/02.architecture/decisions`, `docs/05.operations/incidents` 신규 산출물 생성.
- `graphify-out` generated artifact hand-edit 또는 regeneration.
- Graphify health report를 hard validation gate로 승격.
- `10-communication` root compose include, network, IP allocation, or hardening tier remediation.
- `pre-commit` 수동 실행.
- Docker stack 실행, 배포, 중지, 삭제.

## Work Breakdown

| Phase | Work | Output |
| --- | --- | --- |
| P1 | Root, docs, infra, scripts README 분석 | 워크스페이스 목적/환경 요약 |
| P2 | `AGENTS.md`, provider shims, governance rules 분석 | agent entry/rule contract 요약 |
| P3 | `.claude`, `.codex`, governance agent catalog 분석 | harness component와 runtime mirror 요약 |
| P4 | templates와 validators 분석 | Agent-first guardrail와 verification map 요약 |
| P5 | stage docs 작성/갱신 | Spec, Plan, Task, Guide, Policy, Runbook |
| P6 | parent README traceability 확인 | 문서 링크와 structure 동기화 유지 |
| P7 | Claude hook quoting 보완 | heredoc/argv 기반 JSON output과 payload simulation |
| P8 | Graphify/context-quality 및 evidence 범위 보완 | advisory health wording, scoped infra evidence, residual risk |
| P9 | 검증 실행 | command evidence와 residual risk 보고 |

## Verification Plan

```bash
python3 -m json.tool .codex/hooks.json >/dev/null
python3 -m json.tool .claude/settings.json >/dev/null
bash -n .claude/hooks/*.sh scripts/*.sh
printf '{"tool_input":{"file_path":"infra/10-communication/mail/docker-compose.yml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/docker-compose-pre.sh
CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh
printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/post-tool-validate.sh
bash scripts/knowledge/report-graphify-health.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-quickwin-baseline.sh
bash scripts/hardening/check-all-hardening.sh
! rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md GEMINI.md .claude .codex docs/00.agent-governance --glob '!docs/00.agent-governance/memory/**'
```

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Stage doc churn duplicates existing governance | Keep active policy in `docs/00.agent-governance/`; stage docs describe analysis and operation only. |
| README sync drift | Update each parent README in the same change as the new document. |
| Source-label regression | Run explicit source-label scan and rely on `check-repo-contracts.sh`. |
| Over-expanding runtime | Do not change agent catalogs, `.codex`, or root shims unless a validator proves a specific gap. |
| Polluted Graphify output is over-trusted | Keep Graphify readable but advisory when health reports contamination; corroborate with tracked source and canonical docs. |
| Hook payload breaks despite syntax checks | Add real `tool_input` payload simulation for Claude and Codex hook entrypoints. |
| `10-communication` validation gap expands scope | Record it as separate infra remediation; do not block HAFE completion. |

## Agent Rollout & Evaluation Gates (If Applicable)

- Agent persona: Agentic Workflow Specialist with Documentation Specialist behavior for stage artifacts.
- Evaluation gate: all commands in the verification plan pass.
- Runtime rollout: limited to shell-safe Claude hook invocation; no agent catalog or provider policy rollout is needed.

## Completion Criteria

- Stage docs exist and contain `## Related Documents`.
- Parent README files keep references to the stage docs.
- Claude hook payload simulations return JSON/system-message output without command substitution side effects.
- `bash scripts/knowledge/report-graphify-health.sh` exits 0 and reports clean or advisory without being treated as architecture authority when advisory.
- Repository contract, docs traceability, default/core Compose, template/security, QuickWin, and supported hardening checks pass.
- Source-label scan returns no active runtime/governance matches.
- `10-communication` remediation remains documented as out of scope for this pass.

## Related Documents

- [Specification](../../03.specs/harness-agent-first-engineering/spec.md)
- [Task Evidence](../tasks/2026-05-09-harness-agent-first-engineering.md)
- [Guide](../../05.operations/guides/00-workspace/harness-agent-first-engineering.md)
- [Operations Policy](../../05.operations/policies/00-workspace/harness-agent-first-engineering.md)
- [Validation Runbook](../../05.operations/runbooks/00-workspace/harness-agent-first-engineering-validation.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
