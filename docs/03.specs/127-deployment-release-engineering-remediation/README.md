# Deployment and Release Engineering Remediation

> Active technical contract for local sample-service promotion, health evidence, and rollback.

## Overview

This folder owns the deployment, release, and CD follow-up created from the
canonical quality, automation, Compose, and release evidence. It selects
separate local baseline and canary projects for verified-digest promotion and
rollback. It does not own observed execution or current lifecycle evidence;
those are owned by the exact
[domain Task](../../04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md)
and [Program Task](../../04.execution/tasks/2026-07-19-operational-readiness-closure-program.md).
It does not authorize workflow mutation, GitHub Environments/Releases,
publication, secret access, or remote deployment.

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
2. Use PRD 025, ARD 0028, ADR 0028, and Specs 124-126 as the approved local
   architecture and dependency chain.
3. Consume security/runtime/recovery evidence from sibling owners rather than
   duplicating their requirements.
4. Use the [domain Task](../../04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md)
   and [Program Task](../../04.execution/tasks/2026-07-19-operational-readiness-closure-program.md)
   as the sole owners of observed evidence and current lifecycle status;
   require a separate approved Stage 01-04 chain before any workflow, remote,
   environment, Release, secret, or production action.

## Related Documents

- [Technical specification](./spec.md)
- [Operational readiness PRD](../../01.requirements/025-operational-readiness-closure.md)
- [Operational readiness ARD](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [Local-isolated evidence ADR](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Active implementation plan](../../04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md)
- [Domain Task evidence owner](../../04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md)
- [Program Task evidence owner](../../04.execution/tasks/2026-07-19-operational-readiness-closure-program.md)
- [Umbrella audit specification](../123-agentic-engineering-audit-remediation/spec.md)
- [Canonical quality audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md)
- [Canonical automation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
