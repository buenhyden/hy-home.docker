---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/ci-qa-parser-graphify-decision.md -->

# Reference: CI, QA, Parser, and Graphify Decision

## Overview

This reference records the T-005 decision for `WDC-GAP-010`,
`WDC-GAP-011`, and `WDC-GAP-018`. It closes the decision gap without changing
GitHub workflows, validation scripts, pre-commit hooks, Graphify output, or
Markdown content.

## Evidence Snapshot Boundary

- **Evidence as of**: 2026-07-03
- **Current implementation route**: [canonical agentic implementation audit](../2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Citation rule**: Preserve the counts, findings, commands, and dispositions below as dated evidence. Do not cite them as the current workspace state without current tracked-source revalidation.

## Purpose

The document-contract remediation plan requires a decision before adding
dependency-audit gates, hardening Graphify freshness, or changing parser
behavior. This document records the current repository evidence and separates
documented no-change decisions from future protected implementation work.

## Repository Role

This reference supports Stage 04 task evidence and the document-contract gap
register. It is not active CI policy, not a workflow specification, not a
validator implementation, and not approval to mutate protected workflow or
script surfaces.

## Scope

### In Scope

- `WDC-GAP-010`: dependency vulnerability audit gate decision.
- `WDC-GAP-011`: Graphify advisory vs hard gate decision.
- `WDC-GAP-018`: fenced/comment-like heading parser decision.
- Repo-local evidence from tracked workflows, scripts, governance, and current
  command output.

### Out of Scope

- Editing `.github/workflows/**`, `scripts/validation/**`,
  `scripts/knowledge/**`, `.pre-commit-config.yaml`, or Graphify generated
  output.
- Running networked dependency audit commands.
- Reading secret values, `.env` values, credentials, tokens, certificates,
  private keys, raw logs, or shell history.
- Re-verifying remote branch protection or required-check state.

## Definitions / Facts

- **Dependency-audit hard gate**: an active CI, local QA, or pre-commit gate
  that runs `npm audit`, `pip audit`, or an equivalent vulnerability audit and
  fails on a defined policy threshold.
- **Documented coverage**: a decision that current Dependabot, lint/build,
  secret scanning, and contract gates are the active coverage for this batch.
- **Graphify advisory mode**: Graphify output can assist navigation, but claims
  must be corroborated against tracked source files and canonical docs.
- **Parser tooling gap**: a scan limitation where line-based heading detection
  sees Markdown-like lines inside comments or fenced code examples.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| CQA-001 | `bash scripts/validation/run-local-qa-gates.sh --list` | Local script-backed gates and remote-only responsibilities are already listed; dependency audit is not listed. | Confirms current QA surface. |
| CQA-002 | `rg -n 'npm audit\|pip audit' .github scripts --glob '*.yml' --glob '*.yaml' --glob '*.sh'` | No active workflow or script-backed `npm audit` / `pip audit` command was found. | Confirms WDC-GAP-010 evidence. |
| CQA-003 | `bash scripts/knowledge/report-graphify-health.sh` | Report returns `status=advisory`, `surprising_cross_root_inferred_edges=2`, and exits 0. | Confirms WDC-GAP-011 advisory posture. |
| CQA-004 | `rg -n '^# ' .github/PULL_REQUEST_TEMPLATE.md scripts/README.md secrets/README.md` | Matches include real H1 headings plus command comments and fenced examples. | Confirms WDC-GAP-018 is parser/tooling, not a content defect. |
| CQA-005 | Reads of `.github/workflows/ci-quality.yml`, `.github/dependabot.yml`, `.pre-commit-config.yaml`, and relevant governance docs | CI, Dependabot, pre-commit, secret scanning, repo contracts, and Graphify advisory rules are already defined. | Confirms protected mutation boundaries. |

## Decisions

| Gap | Decision | Current Evidence | Future Implementation Gate |
| --- | --- | --- | --- |
| WDC-GAP-010 dependency audit coverage | Document current coverage and do not add `npm audit` or `pip audit` hard gates in this batch. | Dependabot watches GitHub Actions, Docker, Docker Compose, and Storybook Next.js npm dependencies; pre-commit validates Dependabot config and runs `gitleaks`; CI runs frontend lint/typecheck/build and repository security contracts. | A future Security/QA batch may add audit gates only after approving workflow/script changes, severity thresholds, exception handling, package-manager scope, and Python dependency source. |
| WDC-GAP-011 Graphify enforcement | Keep Graphify advisory rather than hard-gated. | `AGENTS.md` requests `graphify update .` after code edits when available; `report-graphify-health.sh` exits 0 and currently reports advisory status because of two cross-root inferred edges. | A future knowledge-graph batch may harden Graphify only after the CLI is reliably available and generated graph health is clean enough for blocking use. |
| WDC-GAP-018 parser/content split | Treat fenced/comment-like heading matches as tooling evidence, not content drift. | The matched lines in PR template, scripts README, and secrets README are H1 headings or shell-comment examples inside code blocks. | A future audit-tooling batch may add a fenced-aware heading parser; no content edit is needed in this batch. |

## Findings

- No active workflow or script-backed dependency audit command exists today.
- The repository already has dependency update automation and related safety
  controls, but those are not the same as an audit hard gate.
- Adding `npm audit` or `pip audit` would be a protected workflow/script change
  and needs separate Security/QA policy decisions for thresholds and
  exceptions.
- Graphify is intentionally advisory in the current workspace because health
  can be advisory even when contamination is zero.
- WDC-GAP-018 does not justify editing PR template, scripts README, or secrets
  README content because the matched lines are valid examples or headings.

## Source Rules

- Prefer tracked workflow, script, and governance files over historical progress
  notes for current automation decisions.
- Do not introduce hard gates without an explicit protected-surface approval
  and rollback plan.
- Keep Graphify generated output and parser tooling changes separate from
  document-contract reference decisions.
- Do not run networked dependency-audit commands during a documentation-only
  decision batch.

## Sources

- [Automation coverage map](./automation-coverage-map.md) - Supplies the
  original automation gaps and protected-surface boundaries.
- [Gap register](./gap-register.md) - Supplies `WDC-GAP-010`,
  `WDC-GAP-011`, and `WDC-GAP-018`.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) -
  Current GitHub Actions QA gates.
- [Dependabot configuration](../../../../.github/dependabot.yml) - Dependency
  update automation.
- [Pre-commit configuration](../../../../.pre-commit-config.yaml) - Formatting,
  linting, actionlint, dependency-config validation, and secret scanning.
- [Local QA gate runner](../../../../scripts/validation/run-local-qa-gates.sh) -
  Local script-backed and remote-only QA responsibility list.
- [Graphify health reporter](../../../../scripts/knowledge/report-graphify-health.sh) -
  Advisory Graphify corpus health behavior.

## Maintenance

- **Owner**: Documentation Specialist / QA Engineer / Security Auditor.
- **Review Cadence**: Review before any workflow, validator, pre-commit,
  dependency-audit, or Graphify hard-gate change.
- **Update Trigger**: Update when dependency audit gates are implemented,
  Graphify becomes a hard freshness gate, or the heading inventory tooling
  becomes fenced-aware.

## Related Documents

- [Document contract audit references](./README.md)
- [Automation coverage map](./automation-coverage-map.md)
- [Gap register](./gap-register.md)
- [Document contract remediation task](../../../04.execution/tasks/2026-07-03-document-contract-remediation-batches.md)
