---
layer: agentic
---

# AGENTS.md

Universal entry shim for agent execution in `hy-home.docker`.

## §1 Bootstrap Sequence

1. Load `[LOAD:RULES:BOOTSTRAP]` from `docs/00.agent-governance/rules/bootstrap.md`.
2. Load `[LOAD:RULES:PERSONA]` from `docs/00.agent-governance/rules/persona.md`.
3. Load `[LOAD:RULES:CHECKLISTS]` from `docs/00.agent-governance/rules/task-checklists.md`.
4. Resolve task layer → load exactly one primary scope from `docs/00.agent-governance/scopes/`.
5. For documentation workflows, load `[LOAD:RULES:STAGE-MATRIX]` from `docs/00.agent-governance/rules/stage-authoring-matrix.md`.
6. JIT-load stage docs (`docs/01`–`docs/11`, `docs/90`, `docs/99`) only when required by the active task.

## §2 Hard Constraints

- Root instruction files must stay thin; detailed policy lives in `docs/00.agent-governance/`.
- `docs/01`–`docs/99` are read-only by default; modify only with explicit user instruction.
- Active stage artifacts may be created only under `docs/01`–`docs/11`, `docs/90`, and `docs/99`; non-stage `docs/*` paths must not hold active specs or plans.
- Run all checks listed by active rules and scope before declaring completion.
- Most-specific in-scope instruction file wins when multiple apply.
- System, developer, and direct user instructions always override repository instruction files.
- **In-place refactor only** — do not create parallel files; edit the canonical file.
- **Secrets** — never write plaintext; use Docker Secrets / `secrets/` mounts only.

## §3 Agent Catalog

| Agent                 | File                                    | Scope Import         | Role                                                         |
| --------------------- | --------------------------------------- | -------------------- | ------------------------------------------------------------ |
| `workflow-supervisor` | `.claude/agents/workflow-supervisor.md` | `scopes/agentic.md`  | Opus orchestration, routing, and synthesis                   |
| `infra-implementer`   | `.claude/agents/infra-implementer.md`   | `scopes/infra.md`    | Immutable IaC, blast-radius-aware                            |
| `drift-detector`      | `.claude/agents/drift-detector.md`      | `scopes/infra.md`    | Container config drift detection and policy compliance (r/o) |
| `iac-reviewer`        | `.claude/agents/iac-reviewer.md`        | `scopes/infra.md`    | Drift + performance validator (r/o)                          |
| `security-auditor`    | `.claude/agents/security-auditor.md`    | `scopes/security.md` | CVSS container auditor (r/o)                                 |
| `incident-responder`  | `.claude/agents/incident-responder.md`  | `scopes/ops.md`      | MTTD/MTTR timeline & RCA                                     |
| `code-reviewer`       | `.claude/agents/code-reviewer.md`       | `scopes/common.md`   | Style + security + arch review (r/o)                         |
| `doc-writer`          | `.claude/agents/doc-writer.md`          | `scopes/docs.md`     | Tech writer + ops manual authoring                           |

Each agent `@imports` its scope file for project-specific constraints (SLO, network policy, secrets rules).

Model policy: subagents use `sonnet`; the supervising/orchestrating agent uses `opus`.

**Skills** (orchestration — all agents may invoke):

| Skill                       | File                                                | Purpose                                                                |
| --------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------- |
| `infra-validate`            | `.claude/skills/infra-validate/skill.md`            | Pre/post-flight Compose validation pipeline                            |
| `infra-cross-validate`      | `.claude/skills/infra-cross-validate/skill.md`      | security-auditor → iac-reviewer cross-validation                       |
| `incident-response`         | `.claude/skills/incident-response/skill.md`         | Timeline reconstruction → RCA → MTTD/MTTR measurement                  |
| `code-reviewer`             | `.claude/skills/code-reviewer/skill.md`             | Style, security, performance, and architecture review orchestration    |
| `security-audit`            | `.claude/skills/security-audit/skill.md`            | Threat-model-first security audit orchestration                        |
| `docker-compose-patterns`   | `.claude/skills/docker-compose-patterns/skill.md`   | Rolling, Blue-Green, Canary deployment patterns for Docker Compose     |
| `container-threat-modeling` | `.claude/skills/container-threat-modeling/skill.md` | STRIDE/DREAD threat modeling for Docker container trust boundaries     |
| `code-review-dimensions`    | `.claude/skills/code-review-dimensions/skill.md`    | OWASP/CWE/SOLID/complexity reference patterns for code-reviewer        |
| `adr-writing`               | `.claude/skills/adr-writing/skill.md`               | MADR format, CAP theorem, ATAM, and quality attribute scoring for ADRs |
| `ci-cd-patterns`            | `.claude/skills/ci-cd-patterns/skill.md`            | CI/CD deployment strategies, security gates, and DORA metrics          |

## §4 Orchestration Protocol

```
validate → change → verify
```

1. `bash scripts/validate-docker-compose.sh` — BEFORE any infra change.
2. Apply change (in-place).
3. `docker compose ps` — AFTER change to confirm service health.
4. Run postflight: `docs/00.agent-governance/rules/postflight-checklist.md`.

## §5 Documentation

- Protocol: `docs/00.agent-governance/rules/documentation-protocol.md`
- Templates: `docs/99.templates/<type>.template.md`
- **DOCS 3 RULES (HALT):**
  - R1: Read template → fill → `status:draft`. Infra trigger: service→ARD, network→ADR, prod→OPER first.
  - R2: Folder change → README updated. BLOCKED until done.
  - R3: `## Related Documents` required in every doc. INCOMPLETE without upstream links.

## §6 Lint

- All lint/format managed by `.pre-commit-config.yaml` — never run manually.

## §7 Settings

| File                          | Purpose                                            | Git Tracked         |
| ----------------------------- | -------------------------------------------------- | ------------------- |
| `.claude/settings.json`       | Team-shared permissions, hooks, denied MCP servers | ✅ Yes              |
| `.claude/settings.local.json` | Personal overrides only                            | ❌ No (.gitignored) |

**No duplication** — team settings must not appear in `settings.local.json`.

## §8 Role Separation

- **`scopes/*.md`** = policy SSOT (boundaries, permissions, SLOs, file ownership)
- **`.claude/agents/*.md`** = runtime bridge (`@import` scope + role-specific capabilities)
- Agents must not embed policy directly; they delegate to their imported scope.

## Related Documents

- Hub: `docs/00.agent-governance/README.md`
- Shared standards: `docs/00.agent-governance/rules/standards.md`
- Quality gate: `docs/00.agent-governance/rules/quality-standards.md`
- Git workflow: `docs/00.agent-governance/rules/git-workflow.md`
- Subagent protocol: `docs/00.agent-governance/subagent-protocol.md`

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

@RTK.md
