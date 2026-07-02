---
layer: agentic
---

# Memory: Execution Stage Legacy Debt

- Date: 2026-05-18
- Layer: docs
- Status: superseded
- Applies To: `docs/04.execution/`, plan/task templates, execution-stage remediation
- Tags: #docs #execution #template-drift
- Retrieval Keywords: docs/04 execution legacy debt, plan task pseudo-links, execution stage remediation, bounded normalization
- Last Verified: 2026-05-26

## Problem

`docs/04.execution` contained historical plan and task artifacts that predated
the current template contract. That 2026-05-18 finding is superseded by the
2026-05-22 full-stage normalization baseline. This note remains as historical
context for why future execution edits should stay evidence-preserving.

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

- `docs/90.references/data/kubernetes/docker-compose-to-k3s-migration.md` (migrated from `docs/04.execution/plans/2026-03-29-k8s-migration-strategy.md`)
- `docs/04.execution/plans/2026-03-26-02-auth-standardization.md`
- `docs/04.execution/tasks/2026-03-26-10-communication-tasks.md`
- `docs/04.execution/tasks/2026-04-01-standardize-infra-net.md`

The 2026-05-22 bounded re-audit found the repository contract clean at that
time:

- `target_stage_docs_total=465`
- `normalized_target_stage_docs_total=465`
- `legacy_target_stage_docs_skipped=0`

The current 2026-05-26 repository contract baseline is also clean after later
stage-doc additions:

- `target_stage_docs_total=492`
- `normalized_target_stage_docs_total=492`
- `legacy_target_stage_docs_skipped=0`

That does not mean old execution history should be rewritten for style. It means
the current validator no longer sees these files as legacy-shape debt.

## Resolution

The 2026-05-22 remediation and bounded re-audit closed the legacy-shape debt.
Historical 2026-03 and 2026-04 artifacts remain audit evidence, not style
rewrite targets.

## Prevention

- New execution-stage documents must start from `docs/99.templates/templates/sdlc/plan.template.md`
  or `docs/99.templates/templates/sdlc/task.template.md`.
- New plan/task documents must include status frontmatter, a `Target:` comment,
  required template sections, and clickable Related Documents links.
- If future drift appears, use repository validators and a scoped execution plan
  before editing historical evidence.

## Evidence

- Custom 2026-05-18 section/frontmatter/target scan over `docs/04.execution`.
- Custom 2026-05-18 pseudo-link scan over `docs/04.execution`.
- `docs/04.execution/plans/2026-05-18-execution-stage-remediation.md`
- `docs/04.execution/tasks/2026-05-18-execution-stage-remediation.md`
- `bash scripts/validation/check-repo-contracts.sh` on 2026-05-26:
  `target_stage_docs_total=492`, `normalized_target_stage_docs_total=492`,
  and `legacy_target_stage_docs_skipped=0`
- Historical 2026-05-22 contract metrics were 465/465 normalized target-stage
  docs with `legacy_target_stage_docs_skipped=0`.
- [Workspace governance bounded re-audit task](../../04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md)

## Related Documents

- [Execution README](../../04.execution/README.md)
- [Execution plans README](../../04.execution/plans/README.md)
- [Execution tasks README](../../04.execution/tasks/README.md)
- [Execution stage remediation plan](../../04.execution/plans/2026-05-18-execution-stage-remediation.md)
- [Execution stage remediation task](../../04.execution/tasks/2026-05-18-execution-stage-remediation.md)
- [Plan template](../../99.templates/templates/sdlc/plan.template.md)
- [Task template](../../99.templates/templates/sdlc/task.template.md)
- [Progress log](./progress.md)
- [Workspace governance bounded re-audit task](../../04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md)
