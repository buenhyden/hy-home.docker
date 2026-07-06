---
status: completed
---

<!-- Target: docs/03.specs/109-gap-routing-recommendation/README.md -->

# Gap Routing Recommendation

> Stage 00 gap-to-stage routing advisory automation contract

## Overview

This folder defines the technical contract for the local advisory tool that
classifies audit, review, validation, and handoff gaps against the Stage 00
gap-to-stage routing table.

The recommender closes `AEA-AUTO-004` by making the manual routing contract
easier to apply before edits begin.

## Audience

This README is for:

- Documentation Specialists
- QA Engineers
- Agentic Workflow Specialists
- Repository Maintainers

## Scope

### In Scope

- Advisory text and path based gap classification.
- Stage 90 governance data reference for the routing contract.
- Repository-contract validation for representative recommender behavior.
- Stage 04 evidence for implementation and verification.

### Out of Scope

- Automatic edits to the recommended owner.
- Replacing human review for ambiguous findings.
- Runtime, remote, CI workflow, provider runtime, credential, secret, token, or
  deployment changes.

## Structure

```text
109-gap-routing-recommendation/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Use [spec.md](./spec.md) as the implementation contract.
2. Keep Stage 00 documentation protocol as the source of truth for routing
   categories.
3. Keep the recommender advisory and non-mutating.
4. Record execution evidence in the linked Stage 04 task.

## Related Documents

- [Spec](./spec.md)
- [Implementation plan](../../04.execution/plans/2026-07-05-gap-routing-recommendation.md)
- [Task evidence](../../04.execution/tasks/2026-07-05-gap-routing-recommendation.md)
- [Gap-to-stage routing reference](../../90.references/data/governance/gap-to-stage-routing.md)
- [Automation candidates](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
