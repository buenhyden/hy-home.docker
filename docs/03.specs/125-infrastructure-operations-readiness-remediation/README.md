<!-- Target: docs/03.specs/125-infrastructure-operations-readiness-remediation/README.md -->

# Infrastructure Operations Readiness Remediation

> Draft technical contract for upgrades, migrations, backups, restores, and state-aware recovery evidence.

## Overview

This folder owns the infrastructure operations follow-up for representative
upgrade, migration, backup, and restore rehearsals. It remains documentation
only and does not authorize access to runtime state, backups, secrets, or
production targets.

## Audience

- Infrastructure and data-service maintainers
- Operations/SRE and security reviewers
- Data owners and recovery-approval authorities
- QA engineers designing representative-state verification
- AI agents implementing a separately approved future task

## Scope

### In Scope

- Compatibility and upgrade rehearsal contracts.
- Representative data/configuration migration and integrity checks.
- Stateful-service backup coverage, retention, ownership, and capture evidence.
- Restore drills with RTO/RPO observations and escalation.

### Out of Scope

- Starting any service or reading runtime state under this draft.
- Compose startup/readiness ownership, supply-chain tooling, or deployment/CD.
- Production data, secret values, credentials, or remote mutations.

## Structure

```text
125-infrastructure-operations-readiness-remediation/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Read [spec.md](./spec.md) for the four owned audit gaps.
2. Resolve the required Stage 01/02 data-protection and recovery predecessors.
3. Treat sibling specs as dependency owners; do not copy their requirements.
4. Create no runtime task until exact representative data, target, retention,
   rollback, redaction, and approval evidence is available.

## Related Documents

- [Technical specification](./spec.md)
- [Draft implementation plan](../../04.execution/plans/2026-07-11-infrastructure-operations-readiness-remediation.md)
- [Umbrella audit specification](../123-agentic-engineering-audit-remediation/spec.md)
- [Canonical Compose and operations audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md)
- [Compose and infrastructure research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md)
