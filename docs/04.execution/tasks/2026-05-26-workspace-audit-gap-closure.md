---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-05-26-workspace-audit-gap-closure.md -->

# Task: Workspace Audit Gap Closure

## Overview (KR)

이 문서는 2026-05-26 워크스페이스 감사(2차 세션)의 갭 클로저 작업 목록이다. 6개 저위험 갭의 구현 증거와 2개 deferred 항목의 기록을 추적한다.

## Inputs

- **Parent Plan**: [2026-05-26-workspace-audit-gap-closure plan](../plans/2026-05-26-workspace-audit-gap-closure.md)
- **Previous Audit Task**: [2026-05-26-workspace-audit](./2026-05-26-workspace-audit.md)

## Working Rules

- 저위험 변경만 즉시 구현; 중간/고위험은 deferred 기록
- 시크릿 값, .env 값 출력 금지
- Docker volume/network/port 변경 금지

## Task Table

| Task ID          | Description                                                       | Type | Parent Plan | Validation / Evidence                                     | Status   |
| ---------------- | ----------------------------------------------------------------- | ---- | ----------- | --------------------------------------------------------- | -------- |
| T-001            | `infra/tech-stack.versions.json` 드리프트 16개 컴포넌트 정정      | ops  | PLN-005     | `check-repo-contracts.sh` failures=0                      | Done     |
| T-002            | `docs/90.references/llm-wiki/index.md` 재생성 (928 paths)         | ops  | PLN-006     | `check-repo-contracts.sh` failures=0                      | Done     |
| T-003            | `.codex/hooks.json` `UserPromptSubmit` 이벤트 추가                | impl | PLN-001     | `jq '.hooks \| keys'` 7개 키 확인                         | Done     |
| T-004            | `AGENTS.md` 섹션 3 `.claude/skills/` 스킬 카운트 명시 (18 skills) | doc  | PLN-002     | `grep "18 skills" AGENTS.md`                              | Done     |
| T-005            | `stage-authoring-matrix.md` Section 4 Agent Skills by Stage 추가  | doc  | PLN-003     | Section 4 존재, 7개 스킬 행                               | Done     |
| T-006            | `docs/90.references/README.md` Stage Handoff 섹션 추가            | doc  | PLN-004     | "Stage Handoff" heading 존재                              | Done     |
| T-007 (BLOCKED)  | `.claude/CLAUDE.md` line 20 "11 functions" → "18 skills"          | doc  | PLN-007     | 런타임 자기-수정 차단 — 사용자 수동 수정 필요             | Blocked  |
| T-008 (DEFERRED) | ops 고아 파일 15개 tier 분류 기준 문서화                          | doc  | N/A         | 중위험: 파일 재분류가 다른 ops 문서 참조를 깨뜨릴 수 있음 | Deferred |
| T-009 (DEFERRED) | pre-commit에 5개 검증 스크립트 통합                               | impl | N/A         | 중위험: pre-commit hook 변경이 모든 개발자 환경에 영향    | Deferred |

## Phase View

### Phase A: 드리프트 클로저 (완료)

- [x] T-001 tech-stack.versions.json 16개 컴포넌트 버전 업데이트
- [x] T-002 LLM Wiki 인덱스 재생성

### Phase B: Hook Parity (완료)

- [x] T-003 .codex/hooks.json UserPromptSubmit 추가

### Phase C: 거버넌스 문서 보강 (완료)

- [x] T-004 AGENTS.md 스킬 카운트 명시
- [x] T-005 stage-authoring-matrix.md Section 4 추가
- [x] T-006 docs/90.references/README.md Stage Handoff 섹션 추가

### Phase D: 차단/지연 기록

- [ ] T-007 (BLOCKED) .claude/CLAUDE.md 수동 수정 요청
- [ ] T-008 (DEFERRED) ops 고아 파일 분류
- [ ] T-009 (DEFERRED) pre-commit 통합

## Verification Summary

- **Test Commands**:
  - `bash scripts/validation/check-repo-contracts.sh` → failures=0
  - `bash scripts/validation/check-doc-traceability.sh` → failures=0
  - `bash scripts/validation/validate-docker-compose.sh` → no errors
  - `jq '.hooks | keys' .codex/hooks.json` → 7개 이벤트 확인
- **Eval Commands**: N/A
- **Logs / Evidence Location**: `docs/00.agent-governance/memory/progress.md`

## Related Documents

- **Parent Plan**: [2026-05-26-workspace-audit-gap-closure plan](../plans/2026-05-26-workspace-audit-gap-closure.md)
- **Previous Audit Plan**: [2026-05-26-workspace-audit plan](../plans/2026-05-26-workspace-audit.md)
- **Previous Audit Task**: [2026-05-26-workspace-audit task](./2026-05-26-workspace-audit.md)
- **Reference**: [90.references Stage Handoff](../../90.references/README.md)
