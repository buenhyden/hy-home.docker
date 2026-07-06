---
status: active
---

<!-- Target: docs/03.specs/117-security-automation-readiness-snapshot/spec.md -->

# Security Automation Readiness Snapshot Technical Specification

## Overview

This specification defines a generated Stage 90 security automation readiness
snapshot. The snapshot classifies repo-local evidence for workflow security,
secret scanning, Dependabot, hardening, vulnerability gates, SBOM generation,
provenance/attestation, and OpenSSF Scorecard automation without running
security scanners or changing CI behavior.

## Strategic Boundaries & Non-goals

This feature is a local evidence generator only. It does not run OSV, SCA,
SAST, container scanners, Scorecard, SBOM tools, signing, attestation, registry
lookups, remote GitHub checks, or runtime state checks. It does not change
workflow permissions, required checks, branch protection, release assets,
secrets, credentials, tokens, private keys, shell history, raw logs, `.env`
values, Docker Compose files, or provider/runtime state.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the security
  maturity gaps in the agentic engineering implementation audit pack.
- **ARD**: No dedicated ARD exists; the change stays within existing validation
  script and Stage 90 data boundaries.
- **Related ADRs**: No new ADR is required because this feature adds generated
  planning evidence, not an architecture decision.

## Contracts

- **Config Contract**:
  `scripts/validation/generate-security-automation-readiness.sh` supports
  default write mode, `--check`, `--dry-run`, and `--help`.
- **Data / Interface Contract**:
  The generator writes
  `docs/90.references/data/security/security-automation-readiness.md` and uses
  tracked files only.
- **Governance Contract**:
  `scripts/validation/check-repo-contracts.sh` must run the generator in
  `--check` mode so the generated readiness snapshot cannot drift.

## Core Design

- **Component Boundary**: A Bash wrapper invokes embedded Python, matching the
  repository's existing generated-reference script pattern.
- **Key Dependencies**: tracked `.github/**` workflow/security files,
  `.pre-commit-config.yaml`, `.gitleaks.toml`, `scripts/**`, tech-stack
  provenance data, and Stage 90 security audits.
- **Tech Stack**: Bash and Python 3 standard library.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each readiness control has an ID, control name,
  status, evidence, and gap or next-step text.
- **Migration / Transition Plan**: Add the generator, generate the Stage 90
  data reference, add category/index documentation, wire repo-contract
  freshness checks, add Stage 04 evidence, and update the audit pack's
  automation/security references.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --dry-run
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Security Reviewer / QA Engineer.
- **Inputs**: tracked workflow, script, governance, Dependabot, hardening, and
  generated-reference files.
- **Outputs**: generated Stage 90 security automation readiness snapshot.
- **Success Definition**: Maintainers can see which security automation
  surfaces are implemented, partial, or still gaps without running scanners or
  changing protected state.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Bash, Python 3, repo-contract validator.
- **Permission Boundary**: Read tracked repository files only; do not read
  secrets, raw logs, shell history, `.env`, registry network data, or live
  remote GitHub settings.
- **Failure Handling**: `--check` fails when the generated snapshot is missing
  or stale.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat the snapshot as planning evidence,
  not active security policy, certification, vulnerability result, SBOM,
  signature, or attestation.
- **Policy Constraints**: Route any future vulnerability gate, SBOM, signing,
  attestation, Scorecard, or remote GitHub work through a separate approved
  Stage 03/04 plan.
- **Versioning Rule**: Generator, generated data, repo contract, and evidence
  updates are committed as one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records generation and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  completion and residual security automation gaps.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked source files and stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Use `git ls-files` and tracked files only.
- **Output Guardrails**: Do not emit secret values, scan output, `.env` values,
  raw logs, shell history, or live remote state.
- **Blocked Conditions**: Attempting to run scanners, generate SBOMs, sign
  artifacts, attest builds, query registries, mutate CI, or mutate remote
  GitHub in this task.
- **Escalation Rule**: Security tooling adoption or CI gate changes require a
  separate approved security spec/plan/task.

## Evaluation (If Applicable)

- **Eval Types**: generator write/check, dry-run, shell syntax, repo-contract
  integration, docs traceability, docs implementation alignment.
- **Metrics**: total controls, status counts, freshness result, repo-contract
  failures.
- **Datasets / Fixtures**: tracked workflow/script/security evidence surfaces.
- **How to Run**: Use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **Self-scan false positives**: The generator excludes itself from scanned
  workflow/script surfaces so its explanatory text cannot satisfy readiness
  controls.
- **Remote-only controls**: Branch protection remains partial unless live
  remote GitHub state is re-verified in a dedicated task.
- **Security gaps**: Missing vulnerability/SBOM/attestation/Scorecard commands
  are reported as gaps, not failures.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Generated snapshot becomes stale after workflow, script, or
  security-surface changes.
- **Fallback**: Regenerate with
  `bash scripts/validation/generate-security-automation-readiness.sh`.
- **Human Escalation**: Required before turning readiness gaps into CI gates or
  remote security automation.

## Verification

```bash
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --dry-run
bash -n scripts/validation/generate-security-automation-readiness.sh scripts/validation/check-repo-contracts.sh
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-SAR-001**: Generated readiness snapshot exists under
  `docs/90.references/data/security/` and reports 11 controls.
- **VAL-SAR-002**: `--check` mode reports the generated snapshot is fresh.
- **VAL-SAR-003**: Repo contracts include and pass the generated snapshot
  freshness check.
- **VAL-SAR-004**: Stage 03/04 evidence, Stage 90 indexes, scripts inventory,
  and audit references are synchronized.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-06-security-automation-readiness-snapshot.md](../../04.execution/plans/2026-07-06-security-automation-readiness-snapshot.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md](../../04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md)
- **Generated reference**: [../../90.references/data/security/security-automation-readiness.md](../../90.references/data/security/security-automation-readiness.md)
- **Security maturity audit**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
