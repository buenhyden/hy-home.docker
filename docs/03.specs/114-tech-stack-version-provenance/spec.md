---
status: completed
---

<!-- Target: docs/03.specs/114-tech-stack-version-provenance/spec.md -->

# Tech-Stack Version Provenance Technical Specification

## Overview

This specification defines a generated Stage 90 provenance snapshot for the
curated tech-stack version registry. The snapshot groups registry images by
drift severity, declaration status, infrastructure tier, and Compose source
line so reviewers can inspect registry-to-Compose parity without manually
reading every Compose file.

## Strategic Boundaries & Non-goals

This feature is generated reference data only. It does not change Docker
Compose files, update image versions, run registry network lookups, scan
vulnerabilities, generate SBOMs, mutate runtime state, or read local `.env`
values.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the tech-stack
  version sync row in the agentic engineering automation candidates reference.
- **ARD**: No dedicated ARD exists; the implementation stays within the
  existing Docker reference-data and infra registry boundaries.
- **Related ADRs**: No new ADR is required because this is a small generated
  reference-data report.

## Contracts

- **Config Contract**:
  `scripts/operations/generate-tech-stack-version-provenance.sh` generates
  `docs/90.references/data/docker/tech-stack-version-provenance.md`.
- **Data / Interface Contract**: The generator reads
  `infra/tech-stack.versions.json`, listed Compose files, and
  `infra/image-tag-policy.exceptions.json`; it records image declaration source
  paths and line numbers only.
- **Governance Contract**: `scripts/validation/check-repo-contracts.sh` must run
  the generator in `--check` mode so generated provenance cannot drift.

## Core Design

- **Component Boundary**: A Bash wrapper invokes an embedded Python renderer,
  matching existing generated Docker data patterns.
- **Key Dependencies**: Curated tech-stack registry, floating image exception
  registry, tracked Compose image declarations, repo-contract validator.
- **Tech Stack**: Bash and Python 3 standard library.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each registry image is classified as
  `declared-pinned`, `floating-exception`, `floating-without-exception`,
  `registry-image-not-declared`, or `missing-compose-file`, then mapped to
  severity `none`, `advisory`, `high`, or `critical`.
- **Migration / Transition Plan**: Add the generator, generated data reference,
  freshness gate, script inventory, Stage 03/04 evidence, and automation
  candidate closure.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/operations/generate-tech-stack-version-provenance.sh
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
bash scripts/operations/generate-tech-stack-version-provenance.sh --dry-run
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Infra/DevOps Engineer / Documentation Specialist.
- **Inputs**: Curated registry JSON, floating image exception JSON, and tracked
  Compose image declarations.
- **Outputs**: Generated provenance snapshot under Stage 90 Docker data.
- **Success Definition**: Audit consumers can see whether registry images are
  pinned, approved floating exceptions, missing, or blocked by source drift.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Git, Bash, Python 3, repo-contract validator.
- **Permission Boundary**: Read tracked registry and Compose source files;
  write only the generated Stage 90 snapshot and related docs/evidence.
- **Failure Handling**: `--check` fails when generated output is missing or
  stale.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat the generated snapshot as audit
  context, not runtime truth or a security attestation.
- **Policy Constraints**: Do not include secret values, `.env` values, live
  container state, registry network output, SBOM output, or vulnerability scan
  findings.
- **Versioning Rule**: Generator, generated output, contracts, and evidence are
  committed as one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records generation and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  closure of the tech-stack provenance follow-up.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked source files and Stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Parse only tracked registry and Compose files listed in
  the registry; do not read local `.env`, secrets, logs, or runtime state.
- **Output Guardrails**: Store image names, status/severity labels, source file
  paths, line numbers, and exception ownership metadata only.
- **Blocked Conditions**: Image upgrades, Compose rewrites, external registry
  calls, vulnerability gating, SBOM/provenance attestation, CI workflow changes,
  runtime mutation, or secret-bearing evidence.
- **Escalation Rule**: Security tooling, SBOM, attestation, or CI publication
  requires a separate approved Stage 03/04 plan.

## Evaluation (If Applicable)

- **Eval Types**: Generator write/check, shell syntax, generated-output literal
  checks, repo-contract freshness gate, documentation validation.
- **Metrics**: registry image count, severity counts, status counts, tier
  coverage, missing compose references.
- **Datasets / Fixtures**: Current tracked registry and listed Compose files.
- **How to Run**: Use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **Environment-default image declarations**: Treat `${VAR:-image:tag}` default
  values as source provenance with `env-default` mode.
- **Floating image exceptions**: Classify approved exceptions as `advisory`, not
  pass/fail errors.
- **Missing registry source file**: Classify missing listed Compose files as
  `critical` in generated output and rely on repo contracts to fail the gate.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Provenance output becomes stale after registry, exception,
  or Compose image changes.
- **Fallback**: Regenerate with
  `bash scripts/operations/generate-tech-stack-version-provenance.sh`.
- **Human Escalation**: Required before broadening this report into external
  registry checks, SBOM/provenance attestation, vulnerability gates, CI
  publication, or runtime image changes.

## Verification

```bash
bash scripts/operations/generate-tech-stack-version-provenance.sh
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
bash -n scripts/operations/generate-tech-stack-version-provenance.sh scripts/validation/check-repo-contracts.sh
git diff --check
bash scripts/operations/sync-tech-stack-versions.sh --check
bash scripts/operations/generate-compose-profile-service-coverage.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-TSV-001**: Generated provenance snapshot exists under
  `docs/90.references/data/docker/`.
- **VAL-TSV-002**: Snapshot reports registry image status/severity and Compose
  source provenance.
- **VAL-TSV-003**: Repo contracts check snapshot freshness.
- **VAL-TSV-004**: Stage 03/04 evidence, Docker data indexes, script inventory,
  and automation candidate closure are in sync.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-06-tech-stack-version-provenance.md](../../04.execution/plans/2026-07-06-tech-stack-version-provenance.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-tech-stack-version-provenance.md](../../04.execution/tasks/2026-07-06-tech-stack-version-provenance.md)
- **Generated provenance**: [../../90.references/data/docker/tech-stack-version-provenance.md](../../90.references/data/docker/tech-stack-version-provenance.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
