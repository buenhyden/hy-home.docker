---
title: "Narrow Native Grants and Visible Post-Edit Lint"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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

Focused RED: two tests failed with three expected assertions (two absent lint
messages and the five retained grants). GREEN: 2/2 PASS in 0.301s.
Final H: 48/48 PASS in 20.605s; N: 45/45 PASS in 1.975s, both exit 0.
Independent reviewer reran three focused tests: PASS, including installed lint
failure exit 37. Bash syntax, settings JSON, diff hygiene and renderer check
PASS; renderer providers=2 drift=0. Provider metadata selected=2 violations=0.
Executable mode remains 100755 for the hook; no mode changes.
Ruff/shellcheck availability remains an environment limitation; no installation
or native runtime observation was performed. Final lifecycle check: selected=4, violations=0, legacy_exceptions=0,
transition_overrides=0 against ad6281fe5.
Remove only Docker Compose config/logs, Docker inspect, and the two broad
/tmp/claude-* Write/Edit allow entries. Preserve the other approved settings.
Missing optional lint must print SKIPPED; installed failing lint stays nonzero.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R04/R10/R15/R16/R20/R31/R37 | W8 | Local implementation and H/N PASS; native observation NOT_RUN | Existing native controls, output adapters and post-edit hook |

## Review Evidence

Independent exact-seven-file code/security review: CLEAR; no findings. Static settings and payload
fixtures cannot prove actual native prompting, hook delivery or editor behavior.

## Commit Ledger

Actual predecessors: draft 837e05b7a, ready f6895e011, in-progress 2b965c99f;
each transition passed metadata validation. The seven implementation files,
Plan checklist and completed Task form one logical commit; Git owns its hash.

## Rulings

- Removing an automatic allow is not a new allow or a runtime invocation.
- Keep native event identities, existing payload normalization and W6 prompt route.
- Required final validation remains required even when optional post-edit lint
  is visibly skipped. Preserve executable mode and installed-linter exit codes.
- No global configuration, trust change, installation, credentials or live action.

## Deferred Items

W9 owns evaluation migration. W10 owns full branch and native/hosted/editor
acceptance; local payload fixtures do not close those observations.
