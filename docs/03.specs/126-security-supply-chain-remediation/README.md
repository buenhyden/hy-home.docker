# Security Supply-Chain Remediation

> Active technical contract for sample-service vulnerability scanning, SBOM, provenance, signing, verification, and reviewed security-health signals.

## Overview

This folder owns the security supply-chain follow-up created from the canonical
quality and security audits. It selects a local-isolated sample-service evidence
chain while leaving exact tool pins and commands to the approved Plan and active
Task. Registry publication, keyless identity, and remote mutation remain out of
scope.

## Audience

- Security and QA maintainers
- Build, artifact, and registry owners
- Release/deployment reviewers
- Human approvers for signing identity and remote security work
- AI agents implementing a separately approved future task

## Scope

### In Scope

- Broader dependency and container-image scanning policy.
- SBOM generation, association, retention, and consumption.
- Build provenance/attestation and artifact signing/verification.
- Advisory OpenSSF Scorecard execution with reviewed findings.

### Out of Scope

- Tool execution or workflow/runtime changes without an approved Plan and active Task.
- Deployment promotion ownership.
- Secret values, signing credentials, tokens, raw findings, or remote mutation.

## Structure

```text
126-security-supply-chain-remediation/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Read [spec.md](./spec.md) for the six owned audit gaps.
2. Use PRD 025, ARD 0028, and ADR 0028 as the approved artifact, identity,
   trust, and evidence boundary.
3. Keep promotion enforcement as a dependency consumed by Spec 127.
4. Require a separate approved Stage 04 task before any scan, build, signing,
   verification, secret access, registry operation, or remote query.

## Related Documents

- [Technical specification](./spec.md)
- [Operational readiness PRD](../../01.requirements/025-operational-readiness-closure.md)
- [Operational readiness ARD](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [Local-isolated evidence ADR](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Draft implementation plan](../../04.execution/plans/2026-07-11-security-supply-chain-remediation.md)
- [Umbrella audit specification](../123-agentic-engineering-audit-remediation/spec.md)
- [Canonical security audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
- [Canonical quality audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md)
