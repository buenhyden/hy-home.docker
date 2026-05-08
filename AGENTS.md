---
layer: agentic
---

# AGENTS.md

Universal entry shim for agent execution in `hy-home.docker`.

## 1. Bootstrap Sequence

1. Load `[LOAD:RULES:BOOTSTRAP]` from `docs/00.agent-governance/rules/bootstrap.md`.
2. Load `[LOAD:RULES:PERSONA]` from `docs/00.agent-governance/rules/persona.md`.
3. Load `[LOAD:RULES:CHECKLISTS]` from `docs/00.agent-governance/rules/task-checklists.md`.
4. Load `[LOAD:RULES:AGENTIC]` from `docs/00.agent-governance/rules/agentic.md`.
5. Resolve task layer and load exactly one primary scope from `docs/00.agent-governance/scopes/`.
6. For documentation workflows, load `[LOAD:RULES:STAGE-MATRIX]`.
7. For PR, merge, review, or workflow tasks, load `[LOAD:RULES:GITHUB]`.
8. JIT-load stage docs only when required by the active task.

## 2. Hard Constraints

- Root instruction files stay thin; detailed policy lives in `docs/00.agent-governance/`.
- `docs/01` to `docs/99` are read-only by default; modify only with explicit user instruction.
- Active stage artifacts belong only under `docs/01` to `docs/10`, `docs/90`, and `docs/99`.
- Run checks listed by the active rules and primary scope before declaring completion.
- Most-specific in-scope instruction file wins when multiple repository instructions apply.
- System, developer, and direct user instructions always override repository instruction files.
- Use in-place refactors only; do not create parallel replacement files for canonical docs.
- Never write plaintext secrets; use Docker Secrets or `secrets/` mounts.

## 3. Runtime Surfaces

- Governance SSOT: `docs/00.agent-governance/`
- Provider-neutral entry: `AGENTS.md`
- Provider shims: `CLAUDE.md`, `GEMINI.md`
- Provider overlays: `docs/00.agent-governance/providers/`
- Claude runtime: `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, `.claude/skills/`
- Codex runtime hooks: `.codex/hooks.json`
- Agent/function catalog: `docs/00.agent-governance/agents/`
- Delegation protocol: `docs/00.agent-governance/subagent-protocol.md`

## 4. Verification

- For infra changes, run `bash scripts/validate-docker-compose.sh`.
- For governance/root changes, run `bash scripts/check-doc-traceability.sh` and link/stale-reference checks for edited files.
- Lint and format are managed by `.pre-commit-config.yaml`; do not run `pre-commit` manually.
- Run the completion checklist in `docs/00.agent-governance/rules/task-checklists.md` before declaring done.

## 5. Graphify

This project has a graphify knowledge graph at `graphify-out/`.

- Before architecture or codebase answers, read `graphify-out/GRAPH_REPORT.md`.
- If `graphify-out/wiki/index.md` exists, prefer it over raw-file browsing.
- After modifying code files, run `graphify update .` when the CLI is available; if `graphify` is unavailable, report that graph refresh was skipped.

## Related Documents

- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `.claude/CLAUDE.md`
- `.codex/README.md`
