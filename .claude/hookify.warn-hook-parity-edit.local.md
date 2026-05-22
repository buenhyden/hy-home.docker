---
name: warn-hook-parity-edit
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (\.claude/settings\.json|\.codex/hooks\.json)$
action: warn
---

⚠️ **Hook 파일 편집 감지됨 — 패리티 계약 확인 필요 (프로젝트 규칙)**

`docs/00.agent-governance/providers/claude.md` — Hook Parity Contract:

> "Claude hook events must stay behaviorally aligned with Codex hook events where both runtimes support the event."

**변경 시 반드시 확인:**

| 확인 항목 | Claude | Codex |
|----------|--------|-------|
| 설정 파일 | `.claude/settings.json` | `.codex/hooks.json` |
| 이벤트 커버리지 | SessionStart, PreToolUse, PostToolUse, SessionEnd, Stop, PreCompact | 동일 |
| 파일 편집 매처 | `Write\|Edit\|MultiEdit\|apply_patch\|ApplyPatch` | 동일 |
| 공유 디스패처 | `scripts/hooks/agent-event-hook.sh` | 동일 |

**패리티 체크리스트:**
- [ ] 이벤트 추가/제거 → 다른 파일에서도 동일하게 반영
- [ ] 타임아웃 변경 → 양쪽 파일에서 동일하게 조정
- [ ] 새 이벤트 매처 → `agent-event-hook.sh`에도 핸들러 추가
- [ ] `.codex/README.md` — Current Hook Contract 업데이트

**완료 후 검증:**
```bash
bash scripts/validation/check-repo-contracts.sh
python3 -m json.tool .claude/settings.json >/dev/null && echo "Claude JSON valid"
python3 -m json.tool .codex/hooks.json >/dev/null && echo "Codex JSON valid"
```
