---
name: block-direct-main-push
enabled: true
event: bash
pattern: git\s+push\s+\w[\w.-]*\s+(HEAD:)?main\s*$
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

🚫 **main 브랜치 직접 푸시 차단됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/github-governance.md` — Repository Protection Contract:

> "Agents must treat `main` as a protected branch: no direct pushes, no force pushes, no bypass of required checks."

> "No exceptions is mandatory agent behavior even when GitHub admin enforcement does not fully enforce the same boundary."

**올바른 워크플로우:**

```bash
# ❌ 금지 — main 직접 푸시
git push origin main
git push origin HEAD:main

# ✅ 허용 — feature 브랜치에서 PR
git push origin feat/42-my-feature
git push origin fix/17-bug-fix
# → GitHub에서 PR 생성 후 리뷰/머지
```

**PR 완료 게이트 (`github-governance.md` — Completion Gate):**

1. 모든 required status checks 통과
2. 모든 required reviews 승인
3. BLOCK 수준 소견 없음
4. CODEOWNERS 리뷰어 통보 완료
5. 시크릿/미핀 액션 없음

## Related Documents

- `docs/00.agent-governance/README.md`
