---
status: active
---

<!-- Target: docs/03.specs/118-audit-implementation-matrix-snapshot/spec.md -->

# Audit Implementation Matrix Snapshot Technical Specification

## Overview

This specification defines a generated Stage 90 governance data snapshot for
the agentic engineering implementation audit pack. The snapshot summarizes
required audit report presence, implementation-overview category coverage,
automation candidate closure rows, generated evidence surfaces, and residual
gap signals without rewriting audit conclusions or changing protected state.

## Strategic Boundaries & Non-goals

This feature is a local evidence generator only. It does not rewrite audit
findings, change implementation-status conclusions, run model calls, run
security scanners, generate SBOMs, sign artifacts, attest builds, query remote
GitHub, mutate CI workflows, mutate provider runtime, mutate Docker Compose
runtime, change branch protection, read secrets, read raw logs, read shell
history, or read `.env` values.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the
  audit-maintenance automation gaps in the agentic engineering implementation
  audit pack.
- **ARD**: No dedicated ARD exists; the change stays within the existing
  validation-script and Stage 90 generated-reference boundaries.
- **Related ADRs**: No new ADR is required because this feature adds generated
  audit context, not an architecture decision.

## Contracts

- **Config Contract**:
  `scripts/validation/generate-audit-implementation-matrix.sh` supports default
  write mode, `--check`, `--dry-run`, and `--help`.
- **Data / Interface Contract**:
  The generator writes
  `docs/90.references/data/governance/audit-implementation-matrix.md` from
  tracked audit-pack and generated-evidence files.
- **Governance Contract**:
  `scripts/validation/check-repo-contracts.sh` must run the generator in
  `--check` mode so the generated audit implementation matrix cannot drift.

## Core Design

- **Component Boundary**: A Bash wrapper invokes embedded Python, matching the
  repository's generated reference pattern for security readiness and provider
  hook parity snapshots.
- **Key Dependencies**: Stage 90 implementation audit reports, Stage 90
  governance/data references, Stage 03/04 evidence links, generated reference
  scripts, and repo-contract validation.
- **Tech Stack**: Bash and Python 3 standard library.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: The generated reference records summary
  metrics, overview categories, report coverage, normalized status counts,
  raw status counts, automation candidate dispositions, generated evidence
  surfaces, and residual gap signals.
- **Migration / Transition Plan**: Add the generator, generate the Stage 90
  governance data reference, add repo-contract freshness coverage, update
  script and Stage 90 indexes, add Stage 04 evidence, and mark `AEA-AUTO-013`
  as implemented in the automation candidate report.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --dry-run
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation Specialist / QA Engineer.
- **Inputs**: tracked audit reports, generated-reference files, scripts, and
  Stage 03/04 evidence paths.
- **Outputs**: generated Stage 90 governance data snapshot.
- **Success Definition**: Maintainers can inspect audit-pack coverage,
  automation-candidate closure, and residual gap signals from one generated
  reference without changing underlying audit conclusions.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Bash, Python 3, repo-contract validator.
- **Permission Boundary**: Read tracked repository files only; do not read
  secrets, raw logs, shell history, `.env`, registry network data, model
  outputs, or live remote GitHub settings.
- **Failure Handling**: `--check` fails when the generated snapshot is missing
  or stale.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat the snapshot as consistency
  evidence, not active policy, runtime truth, a security certification, a
  vulnerability result, an SBOM, a signature, or an attestation.
- **Policy Constraints**: Route future CI gate, vulnerability gate, SBOM,
  signing, attestation, Scorecard, model-eval, or remote GitHub work through a
  separate approved Stage 03/04 plan.
- **Versioning Rule**: Generator, generated data, repo contract, and evidence
  updates are committed as one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records generation and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  completion and residual audit/security automation gaps.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked source files and stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Use tracked audit reports and repository files as
  source evidence; do not treat generated summary rows as canonical audit
  conclusions.
- **Output Guardrails**: Do not emit secret values, scan output, model-output
  payloads, `.env` values, raw logs, shell history, or live remote state.
- **Blocked Conditions**: Attempting to rewrite audit findings, change CI
  gates, run scanners, generate SBOMs, sign artifacts, attest builds, run model
  jobs, query registries, or mutate remote GitHub in this task.
- **Escalation Rule**: Any move from advisory matrix to enforced CI/security
  gate requires a separate approved spec, plan, and task.

## Evaluation (If Applicable)

- **Eval Types**: generator write/check, dry-run, shell syntax, repo-contract
  integration, docs traceability, docs implementation alignment.
- **Metrics**: required reports, overview categories, status cells,
  automation candidate rows, generated surface states, and freshness result.
- **Datasets / Fixtures**: tracked Stage 90 implementation audit pack and
  generated reference evidence surfaces.
- **How to Run**: Use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **Generated output self-reference**: The generator treats the output path as
  a generated evidence surface and uses filesystem presence while the file is
  being introduced.
- **Audit conclusion drift**: The generator parses table rows but does not
  normalize or rewrite underlying report conclusions.
- **Security and CI gaps**: Eval CI gates, vulnerability gates, SBOM,
  provenance, attestation, and Scorecard remain residual gap signals unless a
  separate approved implementation changes them.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Generated snapshot becomes stale after audit-pack,
  generated-reference, or automation-candidate changes.
- **Fallback**: Regenerate with
  `bash scripts/validation/generate-audit-implementation-matrix.sh`.
- **Human Escalation**: Required before turning advisory matrix gaps into CI,
  security, remote, or provider-runtime gates.

## Verification

```bash
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --dry-run
bash -n scripts/validation/generate-audit-implementation-matrix.sh scripts/validation/check-repo-contracts.sh
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-AIM-001**: Generated audit implementation matrix exists under
  `docs/90.references/data/governance/` and reports expected audit reports,
  overview categories, and automation candidates.
- **VAL-AIM-002**: `--check` mode reports the generated snapshot is fresh.
- **VAL-AIM-003**: Repo contracts include and pass the generated snapshot
  freshness check.
- **VAL-AIM-004**: Stage 03/04 evidence, Stage 90 indexes, scripts inventory,
  and audit references are synchronized.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md](../../04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md](../../04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md)
- **Generated reference**: [../../90.references/data/governance/audit-implementation-matrix.md](../../90.references/data/governance/audit-implementation-matrix.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
