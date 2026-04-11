---
name: infra-cross-validate
description: >
  Cross-validation pipeline orchestrator after infra changes: security-auditor → iac-reviewer.
  Use immediately after infra-implementer applies changes to run security audit and
  drift + performance checks in sequence. If CRIT is found, halt and roll back.
---

# infra-cross-validate

Cross-validation pipeline orchestrator after infrastructure changes.
Invoke only after `infra-validate` (single-agent pre/post-flight) completes.

## Execution Flow

```text
infra-implementer change complete
        │
        ▼
Phase 1 — security-auditor audit
Phase 2 — iac-reviewer drift + performance validation
Phase 3 — results merge and recording
```

### Phase 1 — Security Audit (security-auditor)

`infra-implementer` sends to security-auditor:

```text
"audit-request: <changed file list>"
```

security-auditor actions:

- Container security audit based on OWASP Top 10 + ASVS L2
- If workflow files exist, apply `rules/github-governance.md` §4
- Verify image tags are pinned (`docker image ls <image>`)
- Detect secret exposure patterns

**If CRIT found → HALT:**

```text
security-auditor → infra-implementer: "BLOCK: <reason>"
```

infra-implementer must roll back immediately and escalate to the user. Do not proceed to Phase 2.

**If no CRIT → proceed to Phase 2:**

```text
security-auditor → iac-reviewer: "validate-request: <file list>"
```

### Phase 2 — Drift + Performance Check (iac-reviewer)

iac-reviewer checklist:

**Drift checks:**

- All services use `infra_net`
- `no-new-privileges: true` on every container
- Secrets referenced only via `secrets:` block
- Volume names follow `[Service]-[Data]-[Volume]`
- Health-checks defined
- Restart policy set
- Resource limits (`mem_limit` / `cpus`) declared

**Performance checks:**

- Missing health-checks on `LATENCY_SLO < 200ms` services → WARN
- Missing `mem_limit` / `cpus` → WARN
- Missing restart policy on stateful services → WARN
- Missing resource ceilings for PostgreSQL/Kafka/OpenSearch/MinIO → WARN

Record results in `_workspace/cross-validate_<YYYY-MM-DD>.md`, then:

```text
iac-reviewer → infra-implementer: "validate-complete: PASS|WARN <summary>"
```

### Phase 3 — Result Merge (infra-implementer)

infra-implementer must:

1. Read `_workspace/cross-validate_<YYYY-MM-DD>.md`
2. Record results in `docs/00.agent-governance/memory/progress.md`
3. Notify the user if WARN items exist (pipeline continues)
4. If no BLOCK items, complete the task

## Error Handling

| Situation               | Action                                                       |
| ----------------------- | ------------------------------------------------------------ |
| Phase 1 CRIT            | HALT immediately · send BLOCK · roll back change             |
| Phase 2 WARN            | Continue · record results · notify user                      |
| No agent response       | Record non-response in `_workspace/` · escalate to user      |

## Relationship to infra-validate

| Skill                 | Purpose                           | Timing                      |
| --------------------- | --------------------------------- | --------------------------- |
| `infra-validate`      | Single-agent pre/post-flight      | Before/after change         |
| `infra-cross-validate`| Team cross-validation orchestrator| After change (post-validate)|

Full sequence: `infra-validate(pre)` → apply change → `infra-validate(post)` → `infra-cross-validate`

## Test Scenarios

**Normal flow:**

1. infra-implementer sends audit-request after a service change
2. security-auditor: no CRIT → sends validate-request
3. iac-reviewer: WARN (missing mem_limit) → sends validate-complete WARN
4. infra-implementer: record in progress.md + notify user → complete

**CRIT stop flow:**

1. infra-implementer adds plaintext password in env
2. security-auditor detects CRIT → sends BLOCK
3. infra-implementer rolls back → escalates → pipeline halted

## References

- `docs/00.agent-governance/scopes/infra.md`
- `docs/00.agent-governance/scopes/security.md`
- `docs/00.agent-governance/rules/github-governance.md` §4
- `.claude/skills/infra-validate.md`
- `.claude/agents/infra-implementer.md`
- `.claude/agents/security-auditor.md`
- `.claude/agents/iac-reviewer.md`
