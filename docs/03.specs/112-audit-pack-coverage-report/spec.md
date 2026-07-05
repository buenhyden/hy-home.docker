---
status: active
---

<!-- Target: docs/03.specs/112-audit-pack-coverage-report/spec.md -->

# Audit Pack Coverage Report Technical Specification

## Overview

This specification defines a read-only coverage report for the agentic
engineering implementation audit pack. The report parses implementation-status
tables, summarizes normalized and raw status values, and verifies that the
overview keeps the required top-level categories.

## Strategic Boundaries & Non-goals

This feature is intentionally non-mutating. It does not rewrite audit reports,
refresh implementation conclusions, change CI workflow behavior, alter
provider/runtime configuration, or claim new security maturity.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the repository
  contracts row in the agentic engineering automation candidates reference.
- **ARD**: No dedicated ARD exists; the design stays within the existing
  validation-script and Stage 90 audit-pack boundaries.
- **Related ADRs**: No new ADR is required because this is a small reporting
  validator over existing Markdown evidence.

## Contracts

- **Config Contract**: `scripts/validation/report-audit-pack-coverage.sh`
  defaults to
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack`.
- **Data / Interface Contract**: The report reads Markdown tables with status
  columns named `Status`, `Current Status`, `Claude`, `Codex`, or `Gemini`.
- **Governance Contract**: `scripts/validation/check-repo-contracts.sh` must run
  the report in `--check` mode and fail when required reports or overview
  categories are missing.

## Core Design

- **Component Boundary**: A Bash wrapper invokes an embedded Python parser,
  matching existing repository validation-script patterns.
- **Key Dependencies**: Git repository root detection, tracked Stage 90 audit
  Markdown files, and Python standard library only.
- **Tech Stack**: Bash and Python 3 standard library.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Parsed status cells are modeled as report path,
  row label, status-column header, raw status, and normalized status.
- **Migration / Transition Plan**: Add the script, wire repo contracts, update
  script inventory, add Stage 03/04 evidence, and close the audit candidate.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/validation/report-audit-pack-coverage.sh
bash scripts/validation/report-audit-pack-coverage.sh --check
bash scripts/validation/report-audit-pack-coverage.sh --pack <audit-pack-dir>
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: QA Engineer / Documentation Specialist.
- **Inputs**: Stage 90 audit pack Markdown reports.
- **Outputs**: Implementation-status coverage summary and `coverage_check=pass`
  marker in `--check` mode.
- **Success Definition**: Agents can see whether audit-pack categories are
  covered without manually scanning every status matrix.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Bash, Python 3, repo-contract validator.
- **Permission Boundary**: Read-only file access to tracked Markdown and script
  files; no runtime, remote, provider, credential, secret, raw-log,
  shell-history, or `.env` access.
- **Failure Handling**: Missing required reports, missing overview categories,
  or unparseable status cells fail `--check`.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat report output as audit navigation,
  not as refreshed implementation truth.
- **Policy Constraints**: Do not rewrite Stage 90 reports from this script.
- **Versioning Rule**: Script, contract, and evidence updates are committed as
  one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records validation output.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  closure of the audit-pack coverage follow-up.
- **Retrieval Boundary**: Graphify remains advisory; implementation claims are
  corroborated against tracked Stage 90 reports and validation scripts.

## Guardrails (If Applicable)

- **Input Guardrails**: Only parse tracked audit-pack Markdown reports.
- **Output Guardrails**: Print counts and labels only; do not print secret
  values, raw logs, shell history, or local auth files.
- **Blocked Conditions**: Runtime mutation, CI job changes, provider adapter
  changes, remote GitHub changes, or automatic audit conclusion rewrites.
- **Escalation Rule**: Any workflow publication, generated audit rewrite, or
  security-gate adoption requires separate Stage 03/04 work.

## Evaluation (If Applicable)

- **Eval Types**: Parser fixture against the current audit pack, shell syntax,
  repo-contract integration, documentation validation.
- **Metrics**: Required reports checked, status cells parsed, overview
  categories found, and zero repo-contract failures.
- **Datasets / Fixtures**: Current
  `2026-07-05-agentic-engineering-implementation-audit-pack` reports.
- **How to Run**: Use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **Provider comparison table**: Treat Claude, Codex, and Gemini columns as
  status columns.
- **Security framework tables**: Treat each `Status` column as reportable
  implementation-status evidence even when the heading is framework-specific.
- **Hybrid statuses**: Preserve raw status values and map them to normalized
  buckets for counting.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A report is renamed or loses its status matrix.
- **Fallback**: `--check` fails and repo-contract output identifies the missing
  report or category.
- **Human Escalation**: Required before changing the canonical category list or
  using output as an implementation-status rewrite.

## Verification

```bash
bash scripts/validation/report-audit-pack-coverage.sh --check
bash -n scripts/validation/report-audit-pack-coverage.sh scripts/validation/check-repo-contracts.sh
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-APC-001**: The report checks all required audit-pack reports.
- **VAL-APC-002**: The report finds all required overview categories.
- **VAL-APC-003**: Repo contracts run the report in `--check` mode.
- **VAL-APC-004**: Script inventory and Stage 03/04 evidence stay in sync.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-05-audit-pack-coverage-report.md](../../04.execution/plans/2026-07-05-audit-pack-coverage-report.md)
- **Tasks**: [../../04.execution/tasks/2026-07-05-audit-pack-coverage-report.md](../../04.execution/tasks/2026-07-05-audit-pack-coverage-report.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- **Scripts README**: [../../../scripts/README.md](../../../scripts/README.md)
