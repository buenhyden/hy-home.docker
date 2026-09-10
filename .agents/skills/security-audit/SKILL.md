---
name: "security-audit"
description: "Use when an exact change needs read-only analysis of trust boundaries, exposed inputs, privileges, dependencies, and plausible security findings. Reach for it when someone asks whether a change has a security problem, wants exposed inputs or privilege paths examined, or asks whether a new dependency is safe to take. Do NOT use it to exploit a finding, to call an external system, to read or rotate a secret, or to sign off a release; it describes a mechanism and its evidence and changes nothing."
metadata:
  title: "security-audit"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "security-audit"
  scope: "security"
  owner_agent: "security-auditor"
---

# security-audit

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The exact change boundary, security contract, trust assumptions, and read-only authorization must be known.

## Inputs

- Exact change boundary and security contract.
- Threat model, dependency/workflow metadata, secret boundaries, and validation evidence.
- `references/analysis-axes.md`, which this skill owns, for what to look at on
  each axis and the mistake that makes each one look finished too early.

## Procedure

1. Trace exposed inputs, privileges, credentials, data flows, dependencies, and execution sinks affected by the change.
2. Reproduce plausible weaknesses using safe static or approved local checks and distinguish exploit paths from policy hardening.
3. Rank findings by impact and reachability, cite evidence, and assign remediation or residual-risk ownership.

## Outputs

- A read-only analysis in the shape of `assets/findings.md`. Every axis gets a
  row even when it found nothing, and `not-assessable` is recorded as a result
  rather than as a pass.

## Gates

- Every finding cites exact evidence.
- Secret values and prohibited sensitive payloads are absent from output.

## Failure Handling

Stop and redact on accidental sensitive-data exposure; escalate Critical risk or missing authorization without probing external systems.

## Related Documents

- [Security auditor](../../roles/security-auditor.md)
- [Container threat modeling](../container-threat-modeling/SKILL.md)
- [Security scope](../../governance/quality-standards.md)
