---
layer: agentic
---

# Agent Bootstrap Governance

Universal bootstrap protocol for all agents in `hy-home.docker`.

## 1. Core Principles

- Spec-anchored: implementation decisions must map to `docs/01.prd/` and `docs/04.specs/`.
- Stage-gate discipline: use `docs/01` to `docs/11` as lifecycle SSoT.
- JIT loading: load only required rules, scopes, and stage docs.
- Deterministic routing: resolve persona and layer before mutation.

## 2. Mandatory Taxonomy (SSoT Paths)

| Stage | Path                        | Purpose                            |
| :---- | :-------------------------- | :--------------------------------- |
| 00    | `docs/00.agent-governance/` | Agent governance and routing rules |
| 01    | `docs/01.prd/`              | Product requirements               |
| 02    | `docs/02.ard/`              | Architecture reference             |
| 03    | `docs/03.adr/`              | Architecture decisions             |
| 04    | `docs/04.specs/`            | Technical specifications           |
| 05    | `docs/05.plans/`            | Implementation plans               |
| 06    | `docs/06.tasks/`            | Task execution evidence            |
| 07    | `docs/07.guides/`           | Human guides                       |
| 08    | `docs/08.operations/`       | Operations policy                  |
| 09    | `docs/09.runbooks/`         | Operational procedures             |
| 10    | `docs/10.incidents/`        | Incident records                   |
| 11    | `docs/11.postmortems/`      | Post-incident learning             |
| 90    | `docs/90.references/`       | Stable references                  |
| 99    | `docs/99.templates/`        | Document templates                 |

## 3. Bootstrap Loading Sequence

1. Load `[LOAD:RULES:PERSONA]` from `rules/persona.md`.
2. Load `[LOAD:RULES:CHECKLISTS]` from `rules/task-checklists.md`.
3. Resolve task layer and load one primary scope from `scopes/<layer>.md`.
4. For docs authoring work, load `[LOAD:RULES:STAGE-MATRIX]` from `rules/stage-authoring-matrix.md`.
5. Load stage docs JIT only when required by the active task.

## 4. Hard Constraints

- `docs/00.agent-governance/` must stay English-only.
- `docs/01` to `docs/99` are read-only by default unless the user explicitly allows mutation.
- Root shim files must remain concise and delegate details to this hub.
- **In-place refactor only** — edit the canonical file directly; do not create parallel or renamed copies.
- **Settings SSOT** — team settings in `settings.json` (git tracked); personal overrides in `settings.local.json` only; no duplication across both files.
- **Secrets** — never write plaintext credentials; use Docker Secrets or `secrets/` bind-mounts exclusively.

## 5. Verification Gate

For structural or cross-cutting changes:

1. Run applicable repository checks (for infra, include `bash scripts/validate-docker-compose.sh`).
2. Validate link integrity for changed governance/root files.
3. Confirm policy text matches current workspace reality.
4. Record out-of-scope breakages in `docs/00.agent-governance/memory/`.
