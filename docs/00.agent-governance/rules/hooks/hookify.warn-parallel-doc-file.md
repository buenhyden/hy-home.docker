---
name: warn-parallel-doc-file
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: docs/.*(-new|-v\d+|-updated|-revised|-backup|-copy|-old|-draft|-temp|-tmp)\.md$
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

⚠️ **병렬 대체 문서 파일 생성 감지됨 (프로젝트 규칙)**

`AGENTS.md` — Hard Constraints 정책 위반:

> "Use in-place refactors only; do not create parallel replacement files for canonical docs."

**금지된 파일 패턴:**

- `*-new.md`, `*-v2.md`, `*-updated.md`
- `*-revised.md`, `*-backup.md`, `*-copy.md`
- `*-old.md`, `*-draft.md`, `*-temp.md`

**올바른 방법:**

기존 파일을 직접 수정(in-place edit)하세요.

```bash
# ❌ 금지
docs/03.specs/service-spec-new.md   ← 생성하지 마세요

# ✅ 허용
docs/03.specs/service-spec.md       ← 이 파일을 직접 수정
```

파일을 생성하기 전, 기존 canonical 문서가 있는지 확인하고 해당 파일을 직접 편집하세요.
Git 히스토리가 변경 이력을 보존합니다.

## Related Documents

- `docs/00.agent-governance/README.md`
