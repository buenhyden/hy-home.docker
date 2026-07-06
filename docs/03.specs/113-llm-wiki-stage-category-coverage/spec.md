---
status: completed
---

<!-- Target: docs/03.specs/113-llm-wiki-stage-category-coverage/spec.md -->

# LLM Wiki Stage Category Coverage Technical Specification

## Overview

This specification defines a generated Stage 90 coverage snapshot for the
repo-local LLM Wiki. The snapshot groups safe tracked source paths by source
bucket, LLM Wiki category, and lightweight path role so audit consumers can see
coverage shape without scanning the full generated index.

## Strategic Boundaries & Non-goals

This feature is generated reference data only. It does not publish a public
wiki, export full document contents, change runtime behavior, call external
models, or rewrite canonical source files.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the LLM Wiki
  freshness row in the agentic engineering automation candidates reference.
- **ARD**: No dedicated ARD exists; the implementation stays within the
  existing LLM Wiki and Stage 90 reference-data boundaries.
- **Related ADRs**: No new ADR is required because this is a small generated
  reference-data report.

## Contracts

- **Config Contract**: `scripts/knowledge/generate-llm-wiki-coverage.sh`
  generates
  `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`.
- **Data / Interface Contract**: The generator uses `git ls-files`, applies the
  same safe-path exclusion model as the LLM Wiki index, and excludes generated
  coverage/index outputs from counts.
- **Governance Contract**: `scripts/validation/check-repo-contracts.sh` must run
  `generate-llm-wiki-coverage.sh --check` so generated coverage cannot drift.

## Core Design

- **Component Boundary**: A Bash wrapper invokes an embedded Python renderer,
  matching the existing LLM Wiki index generator pattern.
- **Key Dependencies**: Git tracked-path metadata, Stage 90 data category,
  existing LLM Wiki safe-source boundary.
- **Tech Stack**: Bash and Python 3 standard library.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each safe path is classified into source bucket,
  LLM Wiki category, and path role. The generated Markdown stores counts and
  representative links, not full path contents.
- **Migration / Transition Plan**: Add the generator, generated data reference,
  freshness gate, script inventory, Stage 03/04 evidence, and automation
  candidate closure.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Wiki Curator / Documentation Specialist.
- **Inputs**: Safe tracked repository paths and existing LLM Wiki category
  rules.
- **Outputs**: Generated coverage snapshot under Stage 90 data.
- **Success Definition**: Audit consumers can inspect source-bucket/category
  coverage without reading every generated-index row.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Git, Bash, Python 3, repo-contract validator.
- **Permission Boundary**: Read tracked path metadata and write only the
  generated coverage snapshot.
- **Failure Handling**: `--check` fails when generated output is missing or
  stale.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat the generated snapshot as
  coverage/navigation evidence, not runtime truth.
- **Policy Constraints**: Do not include secret content paths, `graphify-out/`,
  `volumes/`, dependency trees, generated/minified artifacts, or lockfiles.
- **Versioning Rule**: Generator, generated output, contracts, and evidence are
  committed as one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records generation and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  closure of the LLM Wiki grouping follow-up.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked source files and Stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Use path metadata only; do not read or print secret
  values.
- **Output Guardrails**: Store counts, labels, and representative links only.
- **Blocked Conditions**: Full-content exports, public publishing, external
  model calls, runtime mutation, remote GitHub changes, or secret-bearing path
  inclusion.
- **Escalation Rule**: CI publication or public wiki generation requires a
  separate approved Stage 03/04 plan.

## Evaluation (If Applicable)

- **Eval Types**: Generator write/check, shell syntax, generated-output
  exclusion scan, repo-contract freshness gate, documentation validation.
- **Metrics**: safe paths, source buckets, categories, roles, zero stale
  generated-output failures.
- **Datasets / Fixtures**: Current tracked repository path set from
  `git ls-files`.
- **How to Run**: Use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **New untracked documents during implementation**: Stage or otherwise include
  approved in-progress paths before final generation.
- **Generated self-reference**: Exclude the generated coverage file and the
  generated LLM Wiki index from coverage counts.
- **Secret policy path**: Count only `secrets/README.md` as policy context.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Coverage output becomes stale after tracked path changes.
- **Fallback**: Regenerate with `bash scripts/knowledge/generate-llm-wiki-coverage.sh`.
- **Human Escalation**: Required before expanding allowed paths to secret,
  generated, volume, dependency, or public-publishing surfaces.

## Verification

```bash
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash -n scripts/knowledge/generate-llm-wiki-coverage.sh scripts/validation/check-repo-contracts.sh
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-LWC-001**: Generated coverage snapshot exists under
  `docs/90.references/data/knowledge/`.
- **VAL-LWC-002**: Snapshot groups safe paths by source bucket, LLM Wiki
  category, and path role.
- **VAL-LWC-003**: Repo contracts check snapshot freshness.
- **VAL-LWC-004**: Stage 03/04 evidence and automation candidate closure are in
  sync.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md](../../04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md](../../04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- **Generated coverage**: [../../90.references/data/knowledge/llm-wiki-stage-category-coverage.md](../../90.references/data/knowledge/llm-wiki-stage-category-coverage.md)
