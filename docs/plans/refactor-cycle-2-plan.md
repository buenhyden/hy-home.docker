# Plan: Cycle 2 Documentation & Agentic Refactor Implementation

- **Status**: Ready
- **Scope**: master
- **layer:** architecture
- **Specification Reference**: `[../specs/refactor-cycle-2-spec.md]`

**Overview (KR):** 분석된 내용을 바탕으로 실제 파일 시스템 가공과 AI Agent 엔트리포인트 고도화를 수행하는 실행 계획입니다.

## 1. Phase 1: File System Cleanup

- [ ] Move `docs/plans/plan_tmp/*` to `docs/plans/`.
- [ ] Remove empty `docs/plans/plan_tmp/` directory.

## 2. Phase 2: Root Implementation

- [ ] Refactor `AGENTS.md` to be a pure metadata shim.
- [ ] Refactor `CLAUDE.md` and `GEMINI.md` for trigger-only loading.

## 3. Phase 3: Instructions & Gateway

- [ ] Update `docs/agentic/gateway.md` mapping to reflect consolidated paths.
- [ ] Inject skill autonomy guidance into `docs/agentic/instructions.md`.

## 4. Phase 4: Global Link Audit

- [ ] Iterate over `ARCHITECTURE.md`, `README.md`, `OPERATIONS.md` to fix stale links.

## 5. Phase 5: Metadata Completion

- [ ] Audit every `.md` file for `layer:` presence.
