---
name: "style-validation"
description: "Use when changed authored files need scoped deterministic formatting, lint, syntax, and metadata checks while preserving generated ownership. Reach for it when someone says the files they just changed need a style or lint pass, asks which checks apply to a change, asks whether an all-files run is allowed, or wants to be sure a formatter has not rewritten a generated file. Do NOT use it to judge whether the code is correct, to review a design, or to decide whether a change should ship; those are review questions, not style ones."
metadata:
  title: "style-validation"
  version: "1.3.0"
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
- `scripts/classify-changed-files.sh`, which this skill owns, for the bucket
  split the procedure below reads.

## Procedure

1. Run `scripts/classify-changed-files.sh` and read its buckets. Classification
   is mechanical, so it is fixed in that script rather than re-derived by
   whoever is looking; the `generated` bucket is the one that matters most,
   because a formatter that rewrites a generated file produces a diff its owner
   never made.
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
