---
layer: agentic
---

# Agent Bootstrap Governance

Universal entry point for all agents in `hy-home.docker`.

## 1. Core Principles

- **Spec-Anchored**: Implementation must map to `docs/01.prd/` and `docs/04.specs/`.
- **Stage-Gate Discipline**: Use `docs/01` to `docs/11` as execution lifecycle SSoT.
- **JIT Loading**: Load only required rules/scopes/stage docs.
- **Deterministic Routing**: Always resolve persona and layer before mutation.

## 2. Mandatory Taxonomy (SSoT Paths)

| Stage | Path | Purpose |
| :--- | :--- | :--- |
| **00** | `docs/00.agent-governance/` | Agent governance and routing rules |
| **01** | `docs/01.prd/` | Product requirements |
| **02** | `docs/02.ard/` | Architecture reference |
| **03** | `docs/03.adr/` | Architecture decisions |
| **04** | `docs/04.specs/` | Technical specifications |
| **05** | `docs/05.plans/` | Implementation plans |
| **06** | `docs/06.tasks/` | Task execution and evidence |
| **07** | `docs/07.guides/` | Human guides |
| **08** | `docs/08.operations/` | Operations policy |
| **09** | `docs/09.runbooks/` | Operational procedures |
| **10** | `docs/10.incidents/` | Incident records |
| **11** | `docs/11.postmortems/` | Post-incident learning |
| **90** | `docs/90.references/` | Stable references |
| **99** | `docs/99.templates/` | Document templates |

## 3. Layer Identification Protocol

Before performing any task:

1. Identify the target layer.
2. Load `rules/persona.md`.
3. Load one primary scope from `scopes/<layer>.md`.
4. Announce active persona/layer/rule.
5. Load required stage docs JIT.

## 4. Documentation Standards

- All files in `docs/00.agent-governance/` must be English-only.
- Every governance markdown file must include `layer` frontmatter.
- Keep root shim files minimal and delegate details to `rules/`, `scopes/`, and `providers/`.

## 5. Verification Gate

For infra or cross-cutting structural changes:

1. Run `bash scripts/validate-docker-compose.sh`.
2. Ensure secrets are not stored in plaintext files.
3. Validate link integrity for changed governance files.
4. Confirm updated guidance reflects current repository reality.
