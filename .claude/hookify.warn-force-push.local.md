---
name: warn-force-push
enabled: true
event: bash
pattern: git\s+push\s+.*(--force\b|--force-with-lease\b|-f\s|-f$)
action: warn
---

⚠️ **Force Push 감지됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/github-governance.md §1`:

> "no direct pushes, no force pushes, no bypass of required checks"

**force push가 정당한 경우:**
- 자신의 feature 브랜치에서 rebase 후 history 재작성
- `--force-with-lease`를 사용해 원격 상태 보호

**절대 금지:**
- `main` 브랜치에 force push
- 다른 에이전트/개발자의 작업 중인 브랜치에 force push
- 이미 머지된 커밋 force push

**확인 체크리스트:**
- [ ] `main`이 아닌 본인 소유 브랜치인가?
- [ ] `--force-with-lease`를 사용하고 있는가? (`--force` 보다 안전)
- [ ] 팀원이 같은 브랜치에서 작업 중이 아닌가?

```bash
# ⚠️ 최소한 --force 대신 --force-with-lease 사용
git push --force-with-lease origin feat/42-my-feature
```
