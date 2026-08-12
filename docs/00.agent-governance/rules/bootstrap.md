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
| Architecture descriptions | `docs/02.architecture/descriptions/` | Architecture Description |
| Architecture decisions | `docs/02.architecture/decisions/` | Architecture decisions |
| Specifications | `docs/03.specs/` | Technical specifications |
| Capability plans | `docs/03.specs/spec-*/plan.md` | Co-located implementation plans |
| Capability tasks | `docs/03.specs/spec-*/task.md` | Co-located task evidence |
| Operations | `docs/05.operations/` | Guides, policies, runbooks, incidents |
| References | `docs/90.references/` | Stable references |
| Templates | `docs/99.templates/` | Document templates |

## 3. Canonical Load Order

1. Enter through the active root shim and load this bootstrap, the matching
   provider overlay, `memory/README.md`, and `memory/current.md`.
2. Validate the current Task and verified commit before relying on the bounded
   memory handoff.
3. Load `[LOAD:RULES:PERSONA]` from `rules/persona.md` and resolve a registered
   agent identity and primary scope from `contracts/agent-catalog.yaml`.
4. Load `[LOAD:RULES:CHECKLISTS]` from `rules/task-checklists.md`.
5. Load `[LOAD:RULES:AGENTIC]` from `rules/agentic.md`.
6. Retrieve targeted Memory notes only when governance, docs, runtime, or
   repeated-failure context is relevant; corroborate them against live evidence.
7. For docs authoring work, load `[LOAD:RULES:STAGE-MATRIX]` from
   `rules/stage-authoring-matrix.md`.
8. For PR creation, merge, or review tasks, load `[LOAD:RULES:GITHUB]` from
   `rules/github-governance.md`.
9. Load stage docs JIT only when required by the active task.

Root shims and provider overlays point here; they do not define another load
sequence.

## 4. Hard Constraints

- Follow the document-role language authority in
  `rules/documentation-protocol.md#31-language-boundary-by-document-role`;
  Stage 00 remains English-only.
- `docs/01` to `docs/99` are read-only by default unless the user explicitly allows mutation.
- Root shim files must remain concise and delegate details to this hub.
- Provider-specific runtime behavior belongs in the matching provider overlay
  and native `.claude/`, `.codex/`, or `.gemini/` surface. `.agents/` is the
  compatibility and shared-skill projection.
- **Memory is advisory** — use `docs/00.agent-governance/memory/current.md`
  only for the bounded current handoff and use other Memory notes for durable
  findings and retrieval context. `progress.md` is append-preserved historical
  navigation only; active policy still belongs in rules, scopes, providers,
  and runtime files.
- **In-place refactor only** — edit the canonical file directly; do not create parallel or renamed copies.
- **Settings SSOT** — team settings in `settings.json` (git tracked); personal overrides in `settings.local.json` only; no duplication across both files.
- **Secrets** — never write plaintext credentials; use Docker Secrets or `secrets/` bind-mounts exclusively.

## 5. Verification Routing

Use the single completion contract in
`rules/task-checklists.md#3-completion-contract`. Structural and cross-cutting
changes add the applicable focused validators named by their typed authority;
they record results in the applicable co-located Task and do not define a
second completion checklist here.

## Related Documents

- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/scopes/docs.md`
- `docs/00.agent-governance/providers/codex.md`
