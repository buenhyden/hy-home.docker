---
title: "Narrow Native Grants and Visible Post-Edit Lint"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0008"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Narrow Native Grants and Visible Post-Edit Lint

## Objective

Implement Plan W8: remove five broad native automatic grants and report missing
optional post-edit linters without hiding actual failures or required gates.

## Inputs

- [Approved Spec](../spec.md), [approved Plan](../plan.md), and
  [W7 evidence](tsk-0007-workflow-and-handoff.md).
- Approved local implementation, tests, review and logical commits only.
- Primary writer: hook-developer; independent code/security review is read-only.
  Root owns lifecycle, evidence and the index. W7 writers release their paths.
- Exact seven files: .claude/settings.json, .claude/provider.md,
  .codex/provider.md, .claude/output-styles/hy-home.md,
  scripts/hooks/post-tool-validate.sh,
  tests/validation/test_provider_native_payloads.py, and
  tests/validation/test_agent_governance_ci_routing.py.

## Work Log

Read-only preparation found five exact broad allow entries and two optional
linter branches that silently omit missing tools. Existing fake-PATH fixtures
can test visible absence and preserve available-tool failure propagation.
No new hook identity, payload schema, grant or scratch-path substitute is needed.

## Verification Evidence

NOT_RUN: focused H/N RED/GREEN, full H/N, Bash syntax, JSON parsing and review.
Remove only Docker Compose config/logs, Docker inspect, and the two broad
/tmp/claude-* Write/Edit allow entries. Preserve the other approved settings.
Missing optional lint must print SKIPPED; installed failing lint stays nonzero.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R04/R10/R15/R16/R20/R31/R37 | W8 | NOT_RUN | Existing native controls, output adapters and post-edit hook |

## Review Evidence

Independent exact-diff code/security review pending. Static settings and payload
fixtures cannot prove actual native prompting, hook delivery or editor behavior.

## Commit Ledger

Root validates and commits actual draft, ready and in-progress predecessors
before implementation GO. No W8 implementation commit yet.

## Rulings

- Removing an automatic allow is not a new allow or a runtime invocation.
- Keep native event identities, existing payload normalization and W6 prompt route.
- Required final validation remains required even when optional post-edit lint
  is visibly skipped. Preserve executable mode and installed-linter exit codes.
- No global configuration, trust change, installation, credentials or live action.

## Deferred Items

W9 owns evaluation migration. W10 owns full branch and native/hosted/editor
acceptance; local payload fixtures do not close those observations.
