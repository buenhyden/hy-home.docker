---
layer: architecture
---

# Implementation Plan: Documentation Refactor

## Phase 1: Preparation

- [x] Analyze root files and existing taxonomy.
- [x] Draft PRD and Spec.

## Phase 2: Metadata Enforce

- [ ] Add `layer` key to all missing root files (`CODE_OF_CONDUCT.md`, etc.).
- [ ] Audit `docs/` subdirectories for metadata consistency.

## Phase 3: Agentic Instruction Move

- [ ] Create `docs/agentic/instructions.md`.
- [ ] Update `docs/agentic/gateway.md` with new markers.
- [ ] Simplify `AGENTS.md` and `GEMINI.md`.

## Phase 4: Verification

- [ ] Run link check script.
- [ ] Validate metadata coverage.
