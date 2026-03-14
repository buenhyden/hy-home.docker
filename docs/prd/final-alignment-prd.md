---
title: 'PRD: Final Mandatory Path and Rule Alignment'
status: 'Approved'
owner: 'buenhyden'
layer: 'product'
---

# PRD: Final Mandatory Path and Rule Alignment

**Overview (KR):** 에이전트 지침 및 라이브러리 구조를 사용자의 최신 "필수 사항"(`docs/plans/` 등)에 맞춰 최종 정렬하고, 2026년 3월 기준의 에이전틱 표준을 완성합니다.

## Requirements

- **[REQ-PATH-01] Implementation Plans Root**: All implementation plans must reside in `docs/plans/` (plural).
- **[REQ-RULE-01] Lazy Loading Integration**: Root files (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) must trigger rule discovery from `docs/agentic/`.
- **[REQ-SKILL-01] Skill Autonomy**: Explicitly state that agents have full autonomy to use any available skill.
- **[REQ-META-01] Layer Metadata**: All management documents must include `layer:` metadata.

## Success Criteria

- `docs/plans/` renamed to `docs/plans/`.
- All repository internal links point to `docs/plans/`.
- Root entrypoints contain `[LOAD:RULES:*]` triggers.
