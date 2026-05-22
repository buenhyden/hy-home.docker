---
name: infra-cross-validate
description: >
  Cross-validation orchestrator after infra changes: security-auditor first, then
  iac-reviewer. Use after infra-implementer applies a change and post-flight validation
  succeeds. If a critical finding appears, halt and roll back.
---

# infra-cross-validate

Cross-validation pipeline after infrastructure changes.
Invoke only after `infra-validate` completes and the post-flight check passes.

## Execution Flow

```text
infra-implementer change complete
        │
        ▼
Phase 1 — security-auditor audit
Phase 2 — iac-reviewer drift + performance validation
Phase 3 — infra-implementer records and reports results
```

### Phase 1 — Security Audit

`infra-implementer` sends:

```text
"audit-request: <changed file list>"
```

`security-auditor` actions:

- audit Compose and infra artifacts against OWASP Top 10 and ASVS L2
- review workflow files using the GitHub Actions security baseline when applicable
- check image tags with `docker image ls <image>`
- detect plaintext secret exposure patterns

If a critical issue is found:

```text
security-auditor → infra-implementer: "BLOCK: <reason>"
```

The pipeline halts. `infra-implementer` rolls back and escalates to the user.

If no critical issue is found:

```text
security-auditor → iac-reviewer: "validate-request: <file list>"
```

### Phase 2 — Drift and Performance Review

`iac-reviewer` checks:

- network assignment to `infra_net`
- `no-new-privileges: true`
- Docker Secrets usage
- volume naming conventions
- health checks, restart policy, and resource limits
- gateway and stateful-service performance guardrails carried forward from the workspace performance patterns

Record results in `_workspace/cross-validate_<YYYY-MM-DD>.md`, then send:

```text
iac-reviewer → infra-implementer: "validate-complete: PASS|WARN <summary>"
```

### Phase 3 — Result Recording

`infra-implementer` must:

1. read `_workspace/cross-validate_<YYYY-MM-DD>.md`
2. record the result in `docs/00.agent-governance/memory/progress.md`
3. notify the user if warnings remain

## Error Handling

| Situation | Action |
| --- | --- |
| Critical issue in Phase 1 | Halt immediately, roll back, escalate |
| Warning in Phase 2 | Continue, record, notify |
| Missing agent response | Record the gap in `_workspace/`, escalate to the user |

## Relationship to infra-validate

| Skill | Purpose | Timing |
| --- | --- | --- |
| `infra-validate` | Single-agent validation gate | Before and after changes |
| `infra-cross-validate` | Independent security and drift/performance review | After post-flight success |

Full sequence:

```text
infra-validate(pre) → apply change → infra-validate(post) → infra-cross-validate
```

## Related Documents

- `docs/00.agent-governance/scopes/infra.md`
- `docs/00.agent-governance/scopes/security.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `.claude/agents/infra-implementer.md`
- `.claude/agents/security-auditor.md`
- `.claude/agents/iac-reviewer.md`
- `.claude/skills/infra-validate/skill.md`
