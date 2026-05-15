---
layer: agentic
---

# Agent Bootstrap Governance

Universal bootstrap protocol for all agents in `hy-home.docker`.

## 1. Core Principles

- Spec-anchored: implementation decisions must map to `docs/01.requirements/` and `docs/03.specs/`.
- Stage-gate discipline: use `docs/01` to `docs/05` as lifecycle SSoT, plus `docs/90` and `docs/99`.
- JIT loading: load only required rules, scopes, and stage docs.
- Deterministic routing: resolve persona and layer before mutation.

## 2. Mandatory Taxonomy (SSoT Paths)

| Area | Path | Purpose |
| :--- | :--- | :--- |
| Agent governance | `docs/00.agent-governance/` | Agent governance and routing rules |
| Requirements | `docs/01.requirements/` | Product requirements |
| Architecture requirements | `docs/02.architecture/requirements/` | Architecture reference |
| Architecture decisions | `docs/02.architecture/decisions/` | Architecture decisions |
| Specifications | `docs/03.specs/` | Technical specifications |
| Execution plans | `docs/04.execution/plans/` | Implementation plans |
| Execution tasks | `docs/04.execution/tasks/` | Task execution evidence |
| Operations | `docs/05.operations/` | Guides, policies, runbooks, incidents |
| References | `docs/90.references/` | Stable references |
| Templates | `docs/99.templates/` | Document templates |

## 3. Bootstrap Loading Sequence

1. Load `[LOAD:RULES:PERSONA]` from `rules/persona.md`.
2. Load `[LOAD:RULES:CHECKLISTS]` from `rules/task-checklists.md`.
3. Load `[LOAD:RULES:AGENTIC]` from `rules/agentic.md`.
4. Review `[LOAD:MEMORY]` from `memory/README.md` and `memory/progress.md`; retrieve targeted memory notes when governance, docs, runtime, or repeated-failure context is relevant.
5. Resolve task layer and load one primary scope from `scopes/<layer>.md`.
6. For docs authoring work, load `[LOAD:RULES:STAGE-MATRIX]` from `rules/stage-authoring-matrix.md`.
7. For PR creation, merge, or review tasks, load `[LOAD:RULES:GITHUB]` from `rules/github-governance.md`.
8. Load stage docs JIT only when required by the active task.

## 4. Hard Constraints

- `docs/00.agent-governance/` must stay English-only.
- `docs/01` to `docs/99` are read-only by default unless the user explicitly allows mutation.
- Root shim files must remain concise and delegate details to this hub.
- Provider-specific runtime behavior belongs in `providers/claude.md`, `providers/gemini.md`, `providers/codex.md`, `.claude/`, or `.codex/`.
- **Memory is advisory** — use `docs/00.agent-governance/memory/` for durable findings, progress logging, and retrieval context only; active policy still belongs in rules, scopes, providers, and runtime files.
- **In-place refactor only** — edit the canonical file directly; do not create parallel or renamed copies.
- **Settings SSOT** — team settings in `settings.json` (git tracked); personal overrides in `settings.local.json` only; no duplication across both files.
- **Secrets** — never write plaintext credentials; use Docker Secrets or `secrets/` bind-mounts exclusively.

## 5. Verification Gate

For structural or cross-cutting changes:

1. Run applicable repository checks (for infra, include `bash scripts/validation/validate-docker-compose.sh`).
2. Validate link integrity for changed governance/root files.
3. Confirm policy text matches current workspace reality.
4. Update `docs/00.agent-governance/memory/progress.md` with progress, verification evidence, and durable memory pointers.
5. Record out-of-scope breakages in `docs/00.agent-governance/memory/` from `docs/99.templates/memory.template.md`.

## Related Documents

- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/scopes/docs.md`
- `docs/00.agent-governance/providers/codex.md`
