# Implementation Plan: Agent Governance Refactor & Optimization (March 2026)

Analyze and refactor the project's agent governance infrastructure to align with the March 2026 standards for token efficiency, JIT context loading, and documentation taxonomy.

## User Review Required

> [!IMPORTANT]
> - Root files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) will be truncated to minimal shims (<40 lines).
> - Detailed governance is being consolidated into `docs/00.agent-governance/`.
> - Generic directory links in `persona-matrix.md` will be updated to point to specific governance-authoritative files within `.agent/rules/` where appropriate, or moved to `docs/00.agent-governance/` if they represent core project standards.

## Proposed Changes

### Root Instruction Shims
Consolidate redundant information and implement strict JIT redirection.

#### [MODIFY] [AGENTS.md](../../../AGENTS.md)
- Remove redundant language policy sections.
- Focus on the "Universal Contract" and "Entry Point".
- Use `[LOAD:RULES:BOOTSTRAP]` as the primary JIT trigger.

#### [MODIFY] [CLAUDE.md](../../../CLAUDE.md)
- Optimize for Claude Code specific features (thinking process, tool use).
- Link to specialized Claude configuration in `docs/00.agent-governance/claude-provider.md`.

#### [MODIFY] [GEMINI.md](../../../GEMINI.md)
- Optimize for Gemini CLI specific patterns (reasoning summaries).
- Link to specialized Gemini configuration in `docs/00.agent-governance/gemini-provider.md`.

---

### Agent Governance Hub (`docs/00.agent-governance/`)
Enhance the central hub to act as a high-performance dispatcher.

#### [MODIFY] [docs/00.agent-governance/README.md](../00.agent-governance/README.md)
- Standardize the "Dispatcher Table" for all `docs/01-11` layers.
- Ensure 100% English content for token efficiency.

#### [MODIFY] [docs/00.agent-governance/rules/persona-matrix.md](../00.agent-governance/rules/persona-matrix.md)
- Fix generic directory links to point to specific pillar files in `.agent/rules/` (e.g., `.agent/rules/1900-Architecture_Patterns/1901-architecture-rules.md`).

#### [NEW] [docs/00.agent-governance/rules/git-workflow.md](../00.agent-governance/rules/git-workflow.md)
- Offload git-related instructions from `AGENTS.md` to this specialized rule file.

## Verification Plan

### Automated Tests
- Run `markdownlint` (via `.markdownlint-cli2.yaml` configuration) to ensure no broken links or formatting issues.
- Use `grep` to verify no Korean remains in `docs/00.agent-governance/` (except allowed quotes).

### Manual Verification
- Verify link integrity by clicking through the root shims to the governance hub in the IDE.
- Test JIT markers in a fresh session to ensure the Agent correctly identifies the dispatcher logic.
