---
status: draft
---

# Harness / Agent-first Engineering Plan

## Overview (KR)

이 계획은 현재 `hy-home.docker`에 구현된 하네스 엔지니어링과 Agent-first Engineering 계약을 파일 내용 기준으로 분석하고, 새 런타임 확장 없이 공식 stage 문서로 정리하는 실행 계획이다.

## Context

최근 repository contract는 `.claude` runtime mirror, Codex boundary, source-label leak prevention, graphify fallback, `rg` discovery permission을 이미 검증한다. 따라서 구현 범위는 runtime mutation이 아니라 분석 결과를 template-compliant stage 문서와 README traceability로 남기는 것이다.

## Goals & In-Scope

- 워크스페이스 목적, 규칙, 환경을 관련 파일 기준으로 정리한다.
- 하네스 엔지니어링 구성 요소를 분석한다.
- Agent-first Engineering 구성 요소를 분석한다.
- 현재 gap이 없는 계약은 no-runtime-change로 명시한다.
- 새 stage docs와 parent README 링크를 생성한다.
- 지정 검증 명령으로 완료를 증명한다.

## Non-Goals & Out-of-Scope

- 새 agent catalog 또는 Codex delegated-agent catalog 생성.
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, `.codex/**` 정책 변경.
- `docs/01.prd`, `docs/02.ard`, `docs/03.adr`, `docs/10.incidents` 신규 산출물 생성.
- `pre-commit` 수동 실행.
- Docker stack 실행, 배포, 중지, 삭제.

## Work Breakdown

| Phase | Work | Output |
| --- | --- | --- |
| P1 | Root, docs, infra, scripts README 분석 | 워크스페이스 목적/환경 요약 |
| P2 | `AGENTS.md`, provider shims, governance rules 분석 | agent entry/rule contract 요약 |
| P3 | `.claude`, `.codex`, governance agent catalog 분석 | harness component와 runtime mirror 요약 |
| P4 | templates와 validators 분석 | Agent-first guardrail와 verification map 요약 |
| P5 | stage docs 작성 | Spec, Plan, Task, Guide, Operation, Runbook |
| P6 | parent README 갱신 | 새 문서 링크와 structure 동기화 |
| P7 | 검증 실행 | command evidence와 residual risk 보고 |

## Verification Plan

```bash
bash scripts/check-repo-contracts.sh
bash scripts/check-doc-traceability.sh
bash scripts/validate-docker-compose.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-quickwin-baseline.sh
bash scripts/check-all-hardening.sh
rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md GEMINI.md .claude .codex docs/00.agent-governance --glob '!docs/00.agent-governance/memory/**'
```

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Stage doc churn duplicates existing governance | Keep active policy in `docs/00.agent-governance/`; stage docs describe analysis and operation only. |
| README sync drift | Update each parent README in the same change as the new document. |
| Source-label regression | Run explicit source-label scan and rely on `check-repo-contracts.sh`. |
| Over-expanding runtime | Do not change `.claude`, `.codex`, or root shims unless a validator proves a specific gap. |

## Agent Rollout & Evaluation Gates (If Applicable)

- Agent persona: Agentic Workflow Specialist with Documentation Specialist behavior for stage artifacts.
- Evaluation gate: all commands in the verification plan pass.
- Runtime rollout: not applicable; this is documentation and traceability work.

## Completion Criteria

- New stage docs exist and contain `## Related Documents`.
- Parent README files reference the new docs.
- Repository contract, docs traceability, Compose, template/security, QuickWin, and hardening checks pass.
- Source-label scan returns no active runtime/governance matches.

## Related Documents

- [Specification](../04.specs/harness-agent-first-engineering/spec.md)
- [Task Evidence](../06.tasks/2026-05-09-harness-agent-first-engineering.md)
- [Guide](../07.guides/harness-agent-first-engineering.md)
- [Operations Policy](../08.operations/harness-agent-first-engineering.md)
- [Validation Runbook](../09.runbooks/harness-agent-first-engineering-validation.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
