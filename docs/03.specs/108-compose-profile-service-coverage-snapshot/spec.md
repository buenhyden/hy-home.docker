---
status: active
---

<!-- Target: docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md -->

# Compose Profile Service Coverage Snapshot Technical Specification

## Overview

This specification defines a deterministic generator and repository-contract
gate for a Docker Compose profile/service coverage reference. The generated
reference supports Stage 90 audits and documentation reviews that need profile
coverage facts without copying Compose service details by hand.

## Strategic Boundaries & Non-goals

This spec owns static inventory generation only. It does not evaluate whether a
profile should exist, run `docker compose config`, resolve runtime includes,
start containers, inspect health, or change service declarations.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the completed
  agentic engineering implementation audit candidate `AEA-AUTO-005`.
- **ARD**: No dedicated ARD exists; the architecture boundary is the existing
  Docker Compose infrastructure source of truth under `infra/`.
- **Related ADRs**: No new ADR is required because this implements a generated
  reference and validation gate without changing runtime architecture.

## Contracts

- **Config Contract**: `scripts/operations/generate-compose-profile-service-coverage.sh`
  must read tracked Compose files only and write
  `docs/90.references/data/docker/compose-profile-service-coverage.md`.
- **Data / Interface Contract**: The generated reference must expose snapshot
  summary, profile coverage, stage coverage, and Compose file coverage sections.
  Services without a Compose `profiles` key must be represented as `default`.
- **Governance Contract**: `scripts/validation/check-repo-contracts.sh` must
  reject stale generated profile coverage output through the generator `--check`
  mode.

## Core Design

- **Component Boundary**: Generation lives in
  `scripts/operations/generate-compose-profile-service-coverage.sh`; freshness
  enforcement lives in `scripts/validation/check-repo-contracts.sh`; published
  reference output lives in Stage 90 data.
- **Key Dependencies**: tracked root `docker-compose.yml`, tracked
  `infra/**/docker-compose*.yml` / `.yaml` files, PyYAML, and `git ls-files`.
- **Tech Stack**: Bash wrapper with embedded Python for YAML parsing and
  deterministic Markdown rendering.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each service record contains service name,
  source Compose file path, inferred infrastructure stage, and normalized
  profile list.
- **Migration / Transition Plan**: Generate the Stage 90 reference once, add it
  to data indexes, then require the generator `--check` in repository contracts.

## Interfaces & Data Structures

### Core Interfaces

```text
tracked_compose_files = git ls-files filtered to root docker-compose.yml and infra/**/docker-compose*.yml|yaml
service_record = {service, path, stage, profiles}
profiles = service.profiles if present else ["default"]
output = docs/90.references/data/docker/compose-profile-service-coverage.md
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Infra/DevOps Engineer / Documentation Specialist / QA
  Engineer.
- **Inputs**: Tracked Compose files, Stage 90 data indexes, script inventory,
  and automation candidate audit evidence.
- **Outputs**: Generated Compose profile coverage reference, script inventory
  updates, repo-contract freshness gate, and Stage 04 evidence.
- **Success Definition**: The generated reference is fresh, indexed, and
  enforced by repo contracts without runtime or secret inspection.

## Tools & Tool Contract (If Applicable)

- **Tool List**: shell, `git`, PyYAML, repository validation scripts.
- **Permission Boundary**: The generator reads tracked repository files and
  writes only the governed Stage 90 reference output. It must not read local
  `.env`, secret, auth, token, shell-history, or runtime log files.
- **Failure Handling**: If the freshness check fails, run
  `bash scripts/operations/generate-compose-profile-service-coverage.sh` and
  inspect the tracked Compose diff that changed the generated output.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: The reference is derived inventory, not
  active operational policy or deployment procedure.
- **Policy Constraints**: No container lifecycle, remote state, credential,
  secret, CI workflow, or Compose behavior changes.
- **Versioning Rule**: Changes are recorded through Stage 04 evidence and a
  logical commit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records generator and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  the completed automation candidate closure.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked Compose files and active stage documents.

## Guardrails (If Applicable)

- **Input Guardrails**: Use `git ls-files`; ignore untracked runtime artifacts.
- **Output Guardrails**: Emit service names, paths, profiles, stage counts, and
  source links only.
- **Blocked Conditions**: Missing PyYAML, YAML parse failures, missing generated
  output in `--check` mode, or stale generated output.
- **Escalation Rule**: Stop before runtime execution, secret reads, or remote
  changes.

## Evaluation (If Applicable)

- **Eval Types**: Generated-output freshness, shell syntax, repo-contract
  validation, documentation traceability, and implementation alignment.
- **Metrics**: zero generator freshness failures; zero repo-contract failures.
- **Datasets / Fixtures**: Current tracked root and `infra/**` Compose files.
- **How to Run**: use the verification commands below and the linked task
  evidence.

## Edge Cases & Error Handling

- **Service without `profiles`**: classify as `default`.
- **Single string profile**: normalize to a one-item profile list.
- **Invalid or non-map Compose file**: treat non-map input as empty; fail on
  YAML parse errors.
- **Duplicate service names across files**: preserve each file-scoped service
  record; do not collapse across Compose files.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Generated reference is stale after Compose service/profile
  changes.
- **Fallback**: Regenerate the reference, review the diff, and rerun repo
  contracts.
- **Human Escalation**: Required only if the desired fix would change Compose
  behavior, CI workflows, runtime state, or secret handling.

## Verification

```bash
bash scripts/operations/generate-compose-profile-service-coverage.sh
bash scripts/operations/generate-compose-profile-service-coverage.sh --check
bash -n scripts/operations/generate-compose-profile-service-coverage.sh scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-CPC-001**: Generated reference exists under Stage 90 Docker data and
  includes snapshot summary, profile coverage, stage coverage, and file
  coverage.
- **VAL-CPC-002**: Generator `--check` fails on stale output and passes on the
  current generated output.
- **VAL-CPC-003**: Script inventory lists the generator under Operations.
- **VAL-CPC-004**: Full repo contracts pass with `failures=0`.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md](../../04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md)
- **Tasks**: [../../04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md](../../04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md)
- **Generated reference**: [../../90.references/data/docker/compose-profile-service-coverage.md](../../90.references/data/docker/compose-profile-service-coverage.md)
- **Docker data index**: [../../90.references/data/docker/README.md](../../90.references/data/docker/README.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
