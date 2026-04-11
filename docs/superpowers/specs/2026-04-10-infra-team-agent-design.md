---
title: Infra Team Agent Cross-Validation Design
date: 2026-04-10
status: approved
---

# Infra Team Agent Cross-Validation Design

## 1. Context and Objective

This spec defines the implementation of a **Pipeline Team Agent** pattern for
`hy-home.docker` that auto-triggers cross-validation between `infra-implementer`
and `security-auditor` on every infrastructure change, integrates performance checks
(Performance) into `iac-reviewer`, and performs a full audit of `settings.json`
permissions.

## 2. Architecture

### 2.1 Pipeline Flow

```text
[Infrastructure Change]
        │
        ▼
infra-implementer
  ① infra-validate skill (pre-flight)
  ② Apply change (in-place)
  ③ Post-flight check
  ④ SendMessage → security-auditor ("audit-request: <file-list>")
        │
        ▼
security-auditor
  ① Security audit (OWASP/ASVS L2 + GitHub Actions §4)
  ② CRIT found → SendMessage → infra-implementer ("BLOCK: <reason>") → HALT
  ③ CRIT clear  → SendMessage → iac-reviewer ("validate-request: <file-list>")
        │
        ▼
iac-reviewer (drift checks + performance checks integrated)
  ① Drift detection (existing)
  ② Performance checks (new): SLO · resource limits · health-check gaps
  ③ Write _workspace/cross-validate_<date>.md
  ④ SendMessage → infra-implementer ("validate-complete: PASS|WARN <summary>")
        │
        ▼
infra-implementer
  ① Receive result → record to memory/progress.md
  ② BLOCK (from security-auditor) → roll back change → escalate to user
  ③ WARN (from iac-reviewer) → record findings → optional user notification
```

### 2.2 Skill Relationships

| Skill                        | Purpose                                | Trigger                        |
| ---------------------------- | -------------------------------------- | ------------------------------ |
| `infra-validate`             | Single-agent pre/post-flight           | Before and after every change  |
| `infra-cross-validate` (new) | Team orchestrator for cross-validation | After infra-validate completes |

Execution order: `infra-validate` → apply change → `infra-cross-validate`

## 3. Agent Changes

### 3.1 `infra-implementer.md`

Add `## Team Communication Protocol` section:

- **Sends to**: `security-auditor` — `"audit-request: <file-list>"` after change applied
- **Receives from**: `security-auditor` — `"BLOCK: <reason>"` or `"audit-complete"`
- **Receives from**: `iac-reviewer` — `"validate-complete: PASS|WARN <summary>"`
- **On BLOCK**: roll back change → escalate to user

### 3.2 `security-auditor.md`

Add `## Team Communication Protocol` section:

- **Receives from**: `infra-implementer` — `"audit-request: <file-list>"`
- **Sends (CRIT)**: `infra-implementer` — `"BLOCK: <reason>"` → pipeline halts
- **Sends (PASS)**: `iac-reviewer` — `"validate-request: <file-list>"`

Add image audit checklist item to Task Principles (required for `docker image ls` permission):

- **Image audit**: for changed services, run `docker image ls <image>` to confirm pinned digest
  or known tag; flag unpinned `latest` as WARN.

### 3.3 `iac-reviewer.md`

Update frontmatter `pattern` from `'26-infra-as-code/drift-detector'` to `'26+29'`.
Update `AGENTS.md` catalog row for `iac-reviewer` to show `drift + performance checks`.

Add `## Team Communication Protocol` section + performance checks Performance Check extension:

- **Receives from**: `security-auditor` — `"validate-request: <file-list>"`
- **Sends to**: `infra-implementer` — `"validate-complete: PASS|WARN <summary>"`

Performance checklist additions (performance checks):

- `LATENCY_SLO < 200ms` — flag services missing health-check definition
- `mem_limit` / `cpus` undeclared → WARN
- `restart` policy unset → WARN
- Resource ceiling absent on stateful services → WARN

## 4. New Skill: `infra-cross-validate`

File: `.claude/skills/infra-cross-validate.md`

**Phases:**

| Phase | Actor             | Action                    | Exit                        |
| ----- | ----------------- | ------------------------- | --------------------------- |
| 1     | security-auditor  | Security audit            | CRIT → HALT, PASS → Phase 2 |
| 2     | iac-reviewer      | Drift + performance check | WARN collected → Phase 3    |
| 3     | infra-implementer | Consolidate results       | Write workspace + progress  |

**Error handling:**

| Condition         | Action                                                     |
| ----------------- | ---------------------------------------------------------- |
| Phase 1 CRIT      | Immediate HALT + rollback instruction to infra-implementer |
| Phase 2 WARN      | Continue; include in summary report                        |
| Agent unreachable | Note in report; escalate to user                           |

**Output:** `_workspace/cross-validate_<YYYY-MM-DD>.md` + append to `memory/progress.md`

## 5. settings.json Permission Audit

### 5.1 Additions

| Permission                                                 | Rationale                                                          |
| ---------------------------------------------------------- | ------------------------------------------------------------------ |
| `Bash(docker compose config:*)`                            | infra-validate Phase 2 static check                                |
| `Bash(docker compose logs:*)`                              | infra-validate Phase 5 post-flight                                 |
| `Bash(bash scripts/check-all-hardening.sh:*)`              | security-auditor security audit checks                                           |
| `Bash(bash scripts/check-doc-traceability.sh:*)`           | CI/CD CI/CD checks                                                      |
| `Bash(bash scripts/check-template-security-baseline.sh:*)` | CI/CD CI/CD checks                                                      |
| `Bash(docker inspect:*)`                                   | iac-reviewer drift detection                                       |
| `Bash(docker image ls:*)`                                  | security-auditor image audit (see §3.2 image-audit checklist item) |

**Retained (already present, not removed):**

| Permission                  | Used by                                                    |
| --------------------------- | ---------------------------------------------------------- |
| `Bash(python3:*)`           | infra-validate Phase 3 drift parse                         |
| `Bash(grep:*)`              | infra-validate secrets guard pattern                       |
| `Bash(docker compose ps:*)` | infra-validate Phase 3+5 (wildcard covers `--format json`) |
| `Bash(docker ps:*)`         | iac-reviewer live container snapshot comparison            |

### 5.2 Removals

| Permission    | Reason                  |
| ------------- | ----------------------- |
| `Bash(cat:*)` | Replaced by `Read` tool |
| `Bash(ls:*)`  | Replaced by `Glob` tool |

### 5.3 Deny List Additions

| Deny                          | Reason                                       |
| ----------------------------- | -------------------------------------------- |
| `Bash(docker compose down:*)` | Destructive — requires explicit user consent |
| `Bash(docker volume rm:*)`    | Destructive — requires explicit user consent |

## 6. Constraints

- No plaintext secrets under any circumstance.
- `validate-docker-compose.sh` must run before every infra change; result recorded in `memory/progress.md`.
- Lint/format checks are managed by `.pre-commit-config.yaml` — never invoked manually by agents.
  Runtime validation scripts (`validate-docker-compose.sh`, `check-all-hardening.sh`, etc.) are
  invoked directly by agents as part of infra-validate and infra-cross-validate workflows.
- Domain policy for all infra-layer agents sourced from `scopes/infra.md` via `@import`.

## 7. Files Changed

| File                                          | Action                                                                                           |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `.claude/agents/infra-implementer.md`         | Add team communication protocol section                                                          |
| `.claude/agents/security-auditor.md`          | Add team communication protocol section                                                          |
| `.claude/agents/iac-reviewer.md`              | Add team protocol + performance checks performance checklist; update frontmatter to `pattern: '26+29'` |
| `AGENTS.md`                                   | Update `iac-reviewer` catalog row to `drift + performance checks`                                                |
| `.claude/skills/infra-cross-validate.md`      | Create (pipeline orchestrator)                                                                   |
| `.claude/settings.json`                       | Full permission audit and reconstruct                                                            |
| `docs/00.agent-governance/memory/progress.md` | Append P5 alignment record                                                                       |

## Related Documents

- `docs/00.agent-governance/scopes/infra.md`
- `docs/00.agent-governance/scopes/security.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `.claude/skills/infra-validate.md`
- `docs/00.agent-governance/memory/progress.md`
