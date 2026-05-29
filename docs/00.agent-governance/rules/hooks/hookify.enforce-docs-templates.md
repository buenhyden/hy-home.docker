---
name: enforce-docs-templates
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (^|/)docs/(0[1-5]|90)\.
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

⚠️ **템플릿 사용 강제화 (프로젝트 규칙)**

`docs/01` ~ `docs/05` 및 `docs/90` 디렉토리에 새로운 문서를 작성하거나 편집할 때는 반드시 `docs/99.templates`의 템플릿 양식을 준수해야 합니다.

**AGENTS.md 정책:**
> Use templates from `docs/99.templates/` for every new or modified target-stage document under `docs/01` to `docs/05`, and `docs/90`.

**준수해야 할 사항:**

1. 대상 문서 유형에 맞는 템플릿을 `docs/99.templates/`에서 먼저 확인하세요.
2. 템플릿의 필수 헤딩(Heading) 구조를 변경하거나 삭제하지 마세요.
3. 임시 플레이스홀더를 모두 제거한 후 저장하세요.
4. 모든 문서는 관련 문서(`## Related Documents`) 링크를 포함해야 합니다.

검증을 위해 완료 후 `bash scripts/validation/check-repo-contracts.sh` 스크립트를 실행하여 템플릿 형식이 유지되는지 확인하세요.
