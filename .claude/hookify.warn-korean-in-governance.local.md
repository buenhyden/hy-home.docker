---
name: warn-korean-in-governance
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: docs/00\.agent-governance/.*\.md$
  - field: new_text
    operator: regex_match
    pattern: "[가-힣ㄱ-ㅎㅏ-ㅣ]"
action: warn
---

⚠️ **거버넌스 문서에 한국어 감지됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/standards.md §2` — 언어 정책 위반:

> "Governance and provider policy files in `docs/00.agent-governance/` must be English."

**언어 정책 요약:**

| 영역 | 언어 |
|------|------|
| `docs/00.agent-governance/` | **영어 전용** |
| 사용자 대면 응답 | 한국어 우선 |
| 인간 대상 저장소 가이드 | 한국어 |
| 기술 식별자, 코드 | 원본 형식 유지 |

**올바른 접근:**
- 거버넌스 정책 설명 → 영어로 작성
- 한국어 설명이 필요하다면 `docs/01` ~ `docs/99`의 인간 대상 문서에 작성
- 코드 블록 내 주석은 영어 사용 권장

거버넌스 문서(`docs/00.agent-governance/`)는 모든 AI 에이전트가 공통으로 읽는 정책 파일입니다.
영어로 작성해야 다중 제공자(Claude, Gemini, Codex) 환경에서 일관성이 유지됩니다.
