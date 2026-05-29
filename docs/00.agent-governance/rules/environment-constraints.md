---
layer: agentic
---

# Environment Constraints

Detailed execution boundaries, verification rules, and Graphify behaviors for the `hy-home.docker` workspace.

## 1. Hard Constraints

- Root instruction files stay thin; detailed policy lives in `docs/00.agent-governance/`.
- `docs/01` to `docs/99` are read-only by default; modify only with explicit user instruction.
- Active stage artifacts belong only under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates`.
- Run checks listed by the active rules and primary scope before declaring completion.
- Most-specific in-scope instruction file wins when multiple repository instructions apply.
- System, developer, and direct user instructions always override repository instruction files.
- Use in-place refactors only; do not create parallel replacement files for canonical docs.
- Never write plaintext secrets; use Docker Secrets or `secrets/` mounts.

## 2. Verification

- For infra changes, run `bash scripts/validation/validate-docker-compose.sh`.
- For governance/root changes, run `bash scripts/validation/check-doc-traceability.sh` and link/stale-reference checks for edited files.
- Lint and format are managed by `.pre-commit-config.yaml`; do not run `pre-commit` manually.
- Run the completion checklist in `docs/00.agent-governance/rules/task-checklists.md` before declaring done.

## 3. Graphify

This project has a graphify knowledge graph at `graphify-out/`.

- Before architecture or codebase answers, read `graphify-out/GRAPH_REPORT.md`.
- If `graphify-out/wiki/index.md` exists, prefer it over raw-file browsing.
- Use Graphify as a navigation aid only when corpus health is clean.
- If Graphify output includes `volumes/`, gitlink/submodule content, minified/generated artifacts, meaningless god nodes, or unrelated cross-root inferred edges, treat it as advisory only.
- Corroborate architecture and codebase conclusions against tracked source files, `docs/00.agent-governance/`, and active stage docs.
- After modifying code files, run `graphify update .` when the CLI is available; if `graphify` is unavailable, report that graph refresh was skipped.

## Related Documents

- `../README.md`
- `agentic.md`
- `github-governance.md`
- `quality-standards.md`
