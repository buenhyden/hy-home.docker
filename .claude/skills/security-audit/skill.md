---
name: security-audit
description: >
  Workspace security audit orchestrator. Use for container, Compose, script, workflow,
  and code-security audits. Runs a threat-model-first review, secret exposure checks,
  image and dependency risk review, and remediation-oriented reporting.
---

# security-audit

Workspace security audit orchestration skill.
Adapt the selected harness logic to the current runtime inventory without creating extra runtime agent teams.

## Primary Actor

- `security-auditor` owns the audit
- `workflow-supervisor` coordinates when the audit crosses multiple domains
- `incident-responder` supports only when the audit is tied to an active or recent incident

## Workflow

### Phase 1 — Define Scope

Capture:

- target paths, services, or workflow files
- code, container, or operational audit boundary
- compliance or policy context if relevant

Save broad-scope input to `_workspace/00_input.md`.

### Phase 2 — Threat-Model-First Audit

`security-auditor` performs:

- lightweight threat modeling for new or changed services
- plaintext secret exposure checks
- container and Compose hardening review
- workflow security checks using the GitHub Actions baseline
- image tag and dependency risk review where evidence is available

### Phase 3 — Report and Remediation

Write `_workspace/security_audit_<date>.md` with:

- severity-tagged findings: `CRIT`, `HIGH`, `MED`, `LOW`
- evidence references
- remediation guidance

If the audit is incident-linked, add the incident reference to the report and notify `incident-responder`.

## Expected Audit Dimensions

1. **Secrets and credentials**
2. **Network and access exposure**
3. **Container and runtime hardening**
4. **Workflow and automation security**
5. **Code and dependency risk**

## Error Handling

| Situation | Action |
| --- | --- |
| Inaccessible artifact | Record the gap as a finding and continue |
| Ambiguous credential | Treat as critical until proven safe |
| Missing runtime evidence | Complete a static audit and state the limitation |

## Related Documents

- `docs/00.agent-governance/scopes/security.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/postflight-checklist.md`
- `.claude/agents/security-auditor.md`
- `.claude/agents/incident-responder.md`
- `.claude/agents/workflow-supervisor.md`
