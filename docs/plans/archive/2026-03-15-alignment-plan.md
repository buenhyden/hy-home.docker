---
goal: 'Align repository with March 2026 agentic standards'
layer: agentic
---

# 2026-03 Alignment implementation Plan

**Overview (KR):** 2026년 3월 에이전틱 표준에 맞춘 리포지토리 전반의 정렬 실행 계획입니다.

## Tasks

| Task | Description | File |
| :--- | :--- | :--- |
| TASK-ALGN-01 | Fix `README.md` plans path | `README.md` |
| TASK-ALGN-02 | Synchronize `AGENTS.md` and `GEMINI.md` rule matrix | root files |
| TASK-ALGN-03 | Add skill autonomy clause to all shims | root files |
| TASK-ALGN-04 | Audit `docs/` for first-line metadata | `docs/**/*.md` |
| TASK-ALGN-05 | Create Incident/Postmortem | `docs/operations/` |

## Verification

- Run `grep -r "\[LOAD:RULES:" .`
- Run `ls docs/plan` (should fail)

## References

- [../prd/README.md]
- [../specs/README.md]
