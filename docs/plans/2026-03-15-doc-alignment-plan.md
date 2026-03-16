---
layer: agentic
---
# Plan-0001: Documentation Taxonomy and Agentic Refactor Implementation
n**Overview (KR):** 리포지토리의 문서 분류 체계 및 에이전틱 리팩토링의 상세 구현 단계입니다.

- **Status**: In Progress
- **Scope**: master
- **layer:** architecture
- **Parent Master Plan**: N/A

**Overview (KR):** 분석된 내용을 바탕으로 실제 파일 이동, 링크 수정, 그리고 AI Agent 엔트리포인트 최적화를 수행하는 단계별 실행 계획입니다.

## 1. Execution Steps

1. **Directory Setup**: Ensure `plans`, `specs`, `runbooks` directories exist.
2. **File Migration**: Move singular docs to plural paths.
3. **Link Update**: Global search/replace for `docs/plan/` -> `docs/plans/` etc.
4. **Agent Optimization**: Update `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` to point to `docs/agentic/gateway.md`.
5. **Metadata Audit**: Add `layer:` to any file missing it.

## 2. Verification

| Task     | Files Affected | Target REQ | Validation Criteria  |
| -------- | -------------- | ---------- | -------------------- |
| MIG-01   | `docs/`        | REQ-FUN-01 | Dir structure is flat|
| AGT-01   | Root `.md`     | REQ-FUN-03 | Trigger-based loading|

## 3. Completion Criteria

- [ ] No broken links in root files.
- [ ] Every file has `layer:` metadata.
- [ ] Agents can load rules via triggers.
