---
name: "style-validation"
description: "Use when changed authored files need scoped deterministic formatting, lint, syntax, and metadata checks while preserving generated ownership."
metadata:
  title: "style-validation"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-10"
  function_id: "style-validation"
  scope: "qa"
  owner_agent: "qa-engineer"
---

# style-validation

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Changed authored files and their language/document style contracts must be identified; generated files remain owned by their generators.

## Inputs

- Changed authored files and style contract.
- Existing formatters, linters, syntax checks, metadata validators, and exclusion rules.
- The [execution boundary](../../governance/quality-standards.md#4-execution-boundary),
  which owns which of these may be run locally and on what scope.

## Procedure

1. Classify changed files by formatter, linter, syntax, metadata, and generated-owner obligations.
2. Run the smallest deterministic checks, apply approved formatter changes, and inspect all hook-managed fallout.
3. Record commands, results, skipped/CI-only checks, and any remaining style finding without masking semantic defects.

## Outputs

- Style-validation evidence and approved deterministic formatting changes.

## Gates

- Formatting is deterministic and generated ownership is preserved.
- Linting is scoped to relevant authored files and does not rely on blanket suppression.

## Failure Handling

Stop on unexpected paths, formatter oscillation, or conflicting style authorities. Do not invoke `pre-commit run` directly, and do not delete content to satisfy lint.

A prohibition without its permitted counterpart is what makes a caller
improvise, so the counterpart is named here: the one approved all-files route is
`scripts/validation/run-agent-precommit-all-files.sh`. It is not a free
substitute. The [execution boundary](../../governance/quality-standards.md#4-execution-boundary)
owns the conditions it carries, and those conditions decide whether an all-files
pass is available at all. Read them before reaching for it; the normal answer to
a scoped change is the scoped check, not the whole tree.

## Related Documents

- [QA engineer](../../roles/qa-engineer.md)
- [Task checklists](../../governance/task-checklists.md)
- [Quality standards](../../governance/quality-standards.md)
