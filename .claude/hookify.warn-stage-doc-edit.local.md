---
name: warn-stage-doc-edit
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (^|/)docs/(0[1-9]|[1-9][0-9])\.
action: warn
---

⚠️ **스테이지 문서 편집 감지됨 (프로젝트 규칙)**

`docs/01` ~ `docs/99` 디렉토리는 기본적으로 **읽기 전용**입니다.

**AGENTS.md 정책:**
> `docs/01` to `docs/99` are read-only by default; modify only with explicit user instruction.

**편집 전 확인사항:**

- [ ] 사용자로부터 명시적인 수정 지시를 받았나요?
- [ ] 활성 스테이지 아티팩트 디렉토리(`docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`) 내의 파일인가요?
- [ ] 인플레이스 수정인가요? (병렬 대체 파일 생성 금지)
- [ ] 상대 경로(`docs/...`)와 절대 경로(`/.../docs/...`) 어느 형태로 들어와도 이 규칙이 적용됩니다.

**수정 후 검증:**

```bash
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh
```
