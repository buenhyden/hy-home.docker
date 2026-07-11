<!-- Target: docs/03.specs/124-compose-runtime-readiness-remediation/README.md -->

# Compose Runtime Readiness Remediation

> Draft technical contract for bounded Compose startup, observed readiness, and failure-recovery evidence.

## Overview

This folder owns the Compose runtime-readiness follow-up created from the
canonical agentic engineering audit. It converts static Compose evidence gaps
into a later-approvable contract without starting services or authorizing any
runtime change.

The folder is one of four sibling runtime follow-ups. Infrastructure state
recovery, security supply chain, and deployment/release engineering remain
separately owned and are dependencies only where their outputs are consumed.

## Audience

- Infrastructure and Compose maintainers
- Operations/SRE and security reviewers
- QA engineers designing bounded runtime evidence
- Human approvers for protected runtime work
- AI agents implementing a separately approved future task

## Scope

### In Scope

- Compose startup and dependency-initialization acceptance criteria.
- Live container and endpoint readiness evidence.
- Bounded failure-recovery scenarios, teardown, and escalation.
- Explicit architecture, runtime, secret, remote, and human approval gates.

### Out of Scope

- Runtime execution under this draft.
- Upgrade, migration, backup, or restore ownership.
- Supply-chain tooling and deployment automation.
- Secret values, credentials, live diagnostics, or remote mutations.

## Structure

```text
124-compose-runtime-readiness-remediation/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Read [spec.md](./spec.md) for the owned audit gaps and blocked prerequisites.
2. Treat Spec 123 as audit lineage only; it is not runtime authorization.
3. Resolve and approve the named Stage 01/02 predecessors before activating
   this draft or creating runtime task evidence.
4. Keep recovery dependencies as links to sibling owners rather than copying
   their requirements.
5. Require a separate Stage 04 task with bounded profiles, teardown, redaction,
   and rollback evidence before any service command runs.

## Related Documents

- [Technical specification](./spec.md)
- [Draft implementation plan](../../04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md)
- [Umbrella audit specification](../123-agentic-engineering-audit-remediation/spec.md)
- [Canonical Compose and operations audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md)
- [Compose and infrastructure research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md)
