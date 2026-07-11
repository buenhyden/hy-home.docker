<!-- Target: docs/03.specs/127-deployment-release-engineering-remediation/README.md -->

# Deployment and Release Engineering Remediation

> Draft technical contract for environments, promotion, approvals, release records, deployment evidence, and rollback.

## Overview

This folder owns the deployment, release, and CD follow-up created from the
canonical quality, automation, Compose, and release evidence. It remains a
documentation-only draft and does not authorize workflow changes, deployments,
GitHub Environments/Releases, registry operations, or remote mutations.

## Audience

- CI/CD, release, and operations maintainers
- Security and artifact owners
- Environment and change-approval authorities
- QA engineers designing promotion/rollback evidence
- AI agents implementing a separately approved future task

## Scope

### In Scope

- Environment and promotion contracts distinct from CI quality.
- Deployment approvals, evidence, and health gates.
- Release iteration records with tag, changelog, artifact, approval, and result.
- Config/application rollback and data-recovery handoffs.

### Out of Scope

- Workflow, environment, Release, registry, or deployment changes now.
- Supply-chain evidence production and data recovery ownership.
- Secrets, credentials, live diagnostics, or remote state mutation.

## Structure

```text
127-deployment-release-engineering-remediation/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Read [spec.md](./spec.md) for the five owned audit gaps.
2. Resolve environment, artifact, identity, and rollback architecture
   predecessors before activating the draft.
3. Consume security/runtime/recovery evidence from sibling owners rather than
   duplicating their requirements.
4. Require a separate approved Stage 04 task before any workflow, remote,
   deployment, environment, Release, secret, or runtime action.

## Related Documents

- [Technical specification](./spec.md)
- [Draft implementation plan](../../04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md)
- [Umbrella audit specification](../123-agentic-engineering-audit-remediation/spec.md)
- [Canonical quality audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md)
- [Canonical automation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
