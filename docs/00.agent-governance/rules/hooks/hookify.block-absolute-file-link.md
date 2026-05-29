---
name: block-absolute-file-link
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.md$
  - field: new_text
    operator: regex_match
    pattern: \]\(file://|href=["']file://
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

🚫 **절대 file:// 링크 차단됨 (프로젝트 규칙)**

`docs/00.agent-governance/rules/documentation-protocol.md` — Documentation Standards:

> "Use only relative links; never use absolute `file://` links."

**왜 금지인가요?**

- `file://` 링크는 특정 로컬 머신에서만 작동합니다
- CI, 다른 개발자, GitHub 렌더링에서 링크가 깨집니다
- SSoT(단일 진실 원천) 추적 가능성을 파괴합니다

**올바른 링크 형식:**

```markdown
<!-- ❌ 절대 경로 - 금지 -->
[문서 링크](file:///home/hy/project-infra/hy-home.docker/docs/01.requirements/prd.md)

<!-- ✅ 상대 경로 - 사용 -->
[문서 링크](../01.requirements/prd.md)
[문서 링크](../../docs/01.requirements/prd.md)
```

현재 파일 위치를 기준으로 상대 경로를 계산하세요.

## Related Documents

- `docs/00.agent-governance/README.md`
