---
name: warn-pre-commit-manual
enabled: true
event: bash
pattern: pre-commit\s+run
action: warn
---

⚠️ **pre-commit 수동 실행 감지됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/postflight-checklist.md §5` — 정책 위반:

> "`.pre-commit-config.yaml` hooks will pass (never run manually)"

**이 프로젝트의 pre-commit 정책:**
- pre-commit 훅은 `git commit` 시 **자동으로** 실행됩니다
- 수동으로 실행하면 일관성이 깨질 수 있습니다
- CI에서 별도로 lint/format 검증을 수행합니다

**올바른 접근:**

```bash
# ❌ 수동 실행 금지
pre-commit run --all-files
pre-commit run --files myfile.py

# ✅ 커밋 시 자동 실행
git commit -m "feat(scope): my change"
# → pre-commit 훅이 자동으로 실행됨
```

린트/포맷 문제가 있다면 해당 파일을 직접 수정한 후 커밋하세요.
