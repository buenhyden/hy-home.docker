---
name: warn-conventional-commit
enabled: true
event: bash
pattern: git\s+commit\s+(?!.*--amend|.*-C[\s=]).*-m\s+["'](?!(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]*\))?!?:[ \t]|Merge\s|Revert\s|Initial commit)
action: warn
---

⚠️ **Conventional Commit 형식 미준수 감지됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/git-workflow.md §1` 커밋 표준을 따르지 않는 메시지입니다.

**필수 형식:**
```
<type>[(scope)][!]: <description>
```

**허용된 type:**

| type | 용도 |
|------|------|
| `feat` | 새 기능 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 |
| `style` | 포맷 변경 (동작 변경 없음) |
| `refactor` | 리팩터 (기능/버그 변경 없음) |
| `perf` | 성능 개선 |
| `test` | 테스트 추가/수정 |
| `build` | 빌드 시스템 변경 |
| `ci` | CI 설정 변경 |
| `chore` | 기타 유지보수 |
| `revert` | 커밋 되돌리기 |

**올바른 예:**
```bash
git commit -m "feat(nginx): add rate limiting config"
git commit -m "fix(compose): correct volume mount path"
git commit -m "docs(readme): update service list"
git commit -m "chore!: drop support for legacy volume names"
```

**이 규칙이 감지하는 경우:**
- `"Update something"`, `"Fix the bug"`, `"Add feature"` — type prefix 없음
- `"feat something"` — 콜론(`:`) 구분자 없음
- `"FEAT: something"` — 대문자 type

**제외 조건:** `--amend`, `-C` (메시지 재사용), `Merge`, `Revert`, `Initial commit`

issue ID, ADR ID, 또는 plan/task ID가 있으면 footer에 참조하세요.
