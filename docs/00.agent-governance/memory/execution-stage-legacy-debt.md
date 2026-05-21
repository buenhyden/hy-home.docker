---
layer: agentic
---

# Memory: Execution Stage Legacy Debt

- Date: 2026-05-18
- Layer: docs
- Status: active
- Applies To: `docs/04.execution/`, plan/task templates, execution-stage remediation
- Tags: #docs #execution #template-drift
- Retrieval Keywords: docs/04 execution legacy debt, plan task pseudo-links, execution stage remediation, bounded normalization
- Last Verified: 2026-05-18

## Problem

`docs/04.execution` contains historical plan and task artifacts that predate the
current template contract. A full rewrite would risk changing execution evidence,
so remediation should stay bounded unless the user explicitly approves a legacy
normalization pass.

## Context

The 2026-05-18 bounded audit found:

- 65 Markdown files under `docs/04.execution` after adding the remediation plan
  and task artifacts.
- 34 plan documents, with 11 still missing one or more current plan-template
  sections.
- 28 task documents, with 4 still missing one or more current task-template
  sections.
- 76 backticked pseudo-links, all remaining in historical execution artifacts.
- 25 historical plan documents and 23 historical task documents still without
  status frontmatter.
- 16 historical plan documents and 15 historical task documents still without
  `Target:` comments.

Representative deferred files:

- `docs/90.references/kubernetes/docker-compose-to-k3s-migration.md` (migrated from `docs/04.execution/plans/2026-03-29-k8s-migration-strategy.md`)
- `docs/04.execution/plans/2026-03-26-02-auth-standardization.md`
- `docs/04.execution/tasks/2026-03-26-10-communication-tasks.md`
- `docs/04.execution/tasks/2026-04-01-standardize-infra-net.md`

## Resolution

The bounded remediation updates entrypoint READMEs, plan/task templates, current
2026-05 execution artifacts, and a new 2026-05-18 plan/task pair. Historical
2026-03 and 2026-04 artifacts remain as audit evidence unless a later task
explicitly scopes a legacy normalization pass.

## Prevention

- New execution-stage documents must start from `docs/99.templates/plan.template.md`
  or `docs/99.templates/task.template.md`.
- New plan/task documents must include status frontmatter, a `Target:` comment,
  required template sections, and clickable Related Documents links.
- Do not turn broad legacy drift into a repository-contract failure until the
  migration scope and exemptions are explicitly approved.

## Evidence

- Custom 2026-05-18 section/frontmatter/target scan over `docs/04.execution`.
- Custom 2026-05-18 pseudo-link scan over `docs/04.execution`.
- `docs/04.execution/plans/2026-05-18-execution-stage-remediation.md`
- `docs/04.execution/tasks/2026-05-18-execution-stage-remediation.md`

## Related Documents

- [Execution README](../../04.execution/README.md)
- [Execution plans README](../../04.execution/plans/README.md)
- [Execution tasks README](../../04.execution/tasks/README.md)
- [Execution stage remediation plan](../../04.execution/plans/2026-05-18-execution-stage-remediation.md)
- [Execution stage remediation task](../../04.execution/tasks/2026-05-18-execution-stage-remediation.md)
- [Plan template](../../99.templates/plan.template.md)
- [Task template](../../99.templates/task.template.md)
- [Progress log](./progress.md)
