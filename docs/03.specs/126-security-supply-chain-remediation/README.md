<!-- Target: docs/03.specs/126-security-supply-chain-remediation/README.md -->

# Security Supply-Chain Remediation

> Draft technical contract for broader vulnerability scanning, SBOMs, provenance, signing, verification, and reviewed security-health signals.

## Overview

This folder owns the security supply-chain follow-up created from the canonical
quality and security audits. It defines a later-approvable producer/consumer
trust contract without selecting tools, generating artifacts, reading secrets,
or changing workflows, registries, or remote settings.

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

- Tool adoption or workflow/runtime changes under this draft.
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
2. Resolve artifact-boundary, trust, retention, and identity predecessors before
   selecting tools or activating this draft.
3. Keep promotion enforcement as a dependency consumed by Spec 127.
4. Require a separate approved Stage 04 task before any scan, build, signing,
   verification, secret access, registry operation, or remote query.

## Related Documents

- [Technical specification](./spec.md)
- [Draft implementation plan](../../04.execution/plans/2026-07-11-security-supply-chain-remediation.md)
- [Umbrella audit specification](../123-agentic-engineering-audit-remediation/spec.md)
- [Canonical security audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
- [Canonical quality audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md)
