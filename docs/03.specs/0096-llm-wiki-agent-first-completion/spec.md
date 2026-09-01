---
profile_id: spec
status: completed
artifact_id: SPEC-0096
artifact_type: spec
parent_ids:
  - AD-0027
created: 2026-07-05
updated: 2026-09-01
---
# LLM Wiki Completion Outcome

## Overview

This completed change made the repository LLM Wiki a generated, verifiable
navigation surface rather than a second policy or document authority.

## Boundaries and Inputs

The change covered the generator, tracked navigation output, freshness check,
and Operations maintenance procedure. It did not make generated text a
substitute for Stage 00 or Stage 99.

## Behavior Contract

- scripts/knowledge/generate-llm-wiki.py owns deterministic generation and
  freshness checking.
- llms.txt and generated indexes are navigation consumers of tracked sources.
- Missing or stale output fails its registered check.
- Generated navigation cannot override canonical document content.

## Technical Approach

The generator derives its source set from current tracked contracts, writes in
a stable order, and provides a check-only mode. Stage 05 owns the operator
procedure.

## Interfaces and Data

The public interfaces are the generator CLI, llms.txt, and the LLM Wiki
Operations subject. Generated data contains paths and summaries, not secrets.

## Failure Modes and Guardrails

Stale output, nondeterministic ordering, a missing source, or a generated policy
claim blocks acceptance. Historical data snapshots are not required for
current generation.

## Acceptance Contract

The generator check and its focused tests pass, the Operations procedure names
the current command, and generated navigation links resolve to current owners.

## Traceability

- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [LLM Wiki maintenance guide](../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md)
- [LLM Wiki maintenance runbook](../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/runbook.md)
- [Generator](../../../scripts/knowledge/generate-llm-wiki.py)
