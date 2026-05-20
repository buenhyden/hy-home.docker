---
name: block-git-no-verify
enabled: true
event: bash
pattern: git\s+commit\s+.*(--no-verify|-n\s+-m|-n\s+['"]|-n$)
action: block
---

🚫 **git commit --no-verify 차단됨 (프로젝트 규칙)**

전역 Claude Code 정책 및 `docs/00.agent-governance/rules/git-workflow.md §5`:

> "Changes that bypass checks or violate secret safety must not be merged."

`AGENTS.md §4`:

> "Lint and format are managed by `.pre-commit-config.yaml`; do not run `pre-commit` manually."

**이 프로젝트의 pre-commit 훅이 수행하는 작업:**
- 린트 / 포맷 검증
- 플레인텍스트 시크릿 감지
- 파일 형식 및 크기 검사

**왜 BLOCK인가요?**
- pre-commit 훅 우회는 품질/보안 게이트를 건너뜁니다
- 시크릿이 실수로 커밋될 위험이 높아집니다
- CI에서 lint 실패로 PR이 차단될 수 있습니다

**올바른 접근:**

```bash
# ❌ 금지
git commit --no-verify -m "fix: something"
git commit -n -m "fix: something"

# ✅ 훅이 실패하면 근본 원인을 수정
# 린트 오류 → 해당 파일 직접 수정
# 포맷 오류 → 포맷터 적용 후 변경사항 스테이지
git add -p
git commit -m "fix(scope): actual fix"
```
