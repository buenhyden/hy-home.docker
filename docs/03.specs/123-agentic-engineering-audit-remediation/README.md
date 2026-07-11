---
status: active
---

<!-- Target: docs/03.specs/123-agentic-engineering-audit-remediation/README.md -->

# Agentic Engineering Audit and Remediation

> Design contract for consolidating agentic research and audits, measuring workspace implementation depth, and applying approved governance and development-harness improvements in stages.

## Overview

This folder defines the staged program that extends the existing canonical
agentic research and implementation-audit packs. The program first refreshes
external criteria and performs a repository-wide audit, then introduces typed
document metadata, lifecycle validation, controlled full-repository
pre-commit execution, and synchronized provider and CI governance.

The program is active again after the postclosure whole-branch review found one
Important changed/new metadata defect: deleting a typed artifact could leave an
unchanged dependent relation unresolved without failing the gate. The focused
fix and affected local gates are being completed before a new exact-range
whole-branch review. The four runtime follow-up specifications and plans remain
`draft` and require separate approval.

Docker Compose services, infrastructure runtime, deployment state, secrets,
and remote GitHub settings are audit-only in this program. Their findings are
routed to independent specifications and plans for later approval.

## Audience

- Documentation and metadata maintainers
- Agentic workflow maintainers
- QA, CI/CD, security, and infrastructure reviewers
- Claude, Codex, and Gemini provider maintainers
- AI agents executing approved Stage 04 work

## Scope

### In Scope

- In-place expansion of the canonical 2026-07-05 research and audit packs.
- Supersession of the overlapping 2026-07-07 implementation audit pack.
- Repository-wide implementation-depth and semantic frontmatter audits.
- Typed metadata, lifecycle, traceability, provider, validator, QA-wrapper,
  and CI-workflow remediation.
- Independent follow-up specifications and plans for runtime findings.
- Subagent-driven implementation, independent reviews, and logical commits.

### Out of Scope

- Starting, stopping, deploying, or mutating Docker Compose services.
- Changing infrastructure runtime, secret values, credentials, or remote
  GitHub settings.
- Adopting a provider model without an exact model-ID approval and coupled
  validator update.
- Treating Stage 90 research or audit reports as active policy or runtime
  truth.

## Structure

```text
123-agentic-engineering-audit-remediation/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Read [spec.md](./spec.md) for the approved program boundaries, workstreams,
   metadata model, and verification contract.
2. Extend the existing canonical research and audit packs in place; do not
   create a third dated pack.
3. Keep audit findings separate from active-policy and runtime mutations.
4. Execute each approved implementation task with a fresh implementer and
   independent reviewers.
5. Record exact checks, deviations, and protected-surface decisions in Stage
   04 task evidence.
6. Keep the typed Spec/Plan/Task, canonical research, and canonical audit leaf
   chain internally resolvable; READMEs remain explicit metadata exceptions.

## Related Documents

- [Technical specification](./spec.md)
- [Implementation plan](../../04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md)
- [Task evidence](../../04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md)
- [Previous research consolidation specification](../122-agentic-research-pack-consolidation/spec.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
