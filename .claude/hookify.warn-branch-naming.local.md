---
name: warn-branch-naming
enabled: true
event: bash
pattern: git\s+(checkout\s+-b|switch\s+-c)\s+(?!(feat|fix|hotfix|docs|style|refactor|perf|test|build|ci|chore|revert|dependabot|codex)/)
action: warn
---

⚠️ **브랜치 이름 규칙 위반 감지됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/git-workflow.md`의 Branching Strategy를 따르지 않는 브랜치 이름입니다.

**허용된 prefix:**

| prefix | 용도 |
|--------|------|
| `feat/<issue-id>-<description>` | 새 기능 |
| `fix/<issue-id>-<description>` | 버그 수정 |
| `hotfix/<issue-id>-<description>` | 긴급 프로덕션 수정 |
| `docs/`, `style/`, `refactor/` | 문서·스타일·리팩터 |
| `perf/`, `test/`, `build/`, `ci/`, `chore/`, `revert/` | 기타 타입 |
| `dependabot/**`, `codex/**` | 자동화 도구 전용 |

**올바른 예:**
```bash
git checkout -b feat/42-add-nginx-service
git checkout -b fix/17-fix-volume-mount
git checkout -b hotfix/99-patch-secret-leak
```

`main` 브랜치를 직접 사용하지 마세요. 항상 feature/fix 브랜치에서 시작하세요.
