---
status: completed
---
<!-- Target: docs/03.specs/095-infra-secrets-docs-refresh/spec.md -->

# Infra / Secrets / Docs Refresh Specification

## Overview

This document specifies how to refresh operations documents and READMEs based on the actual file contents under `infra/`, `secrets/`, `docs/05.operations/guides/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/`, and `docs/90.references/`. The goal is to strengthen implementation elements and operations documents so they follow the `docs/99.templates/` contract without changing Docker Compose runtime behavior or secret value files.

Current baseline structural validation is passing. `infra/` contains 48 Compose variant files and 40 Compose service directories, with 0 missing service READMEs. Root Compose has 17 active includes, so owned Compose files and root-active Compose files are documented separately. `secrets/` has 95 secret/cert filenames excluding Markdown registry/README documents, 70 root Compose declarations, and 0 missing declared secrets; values are not read. The target README audit scope is currently 134 README files, and the stage audit scope is currently 217 non-README Markdown files.

## Strategic Boundaries & Non-goals

This specification owns documentation structure, README contracts, stage document template compliance, and infra/secrets inventory analysis. Docker Compose service behavior changes, secret value reads, certificate regeneration, agent runtime catalog changes, deployments, and migration execution are out of scope.

## Related Inputs

- **PRD**: No explicit PRD. This work strengthens operations documentation consistency.
- **ARD**: No explicit ARD. It follows the existing layered `infra/` structure and stage docs taxonomy.
- **Related ADRs**: No explicit new ADR. No decision record is added because runtime structure does not change.

## Contracts

- **Config Contract**: `infra/**/docker-compose*.yml`, config files, and the root `docker-compose.yml` are analysis targets and are not modified by default.
- **Data / Interface Contract**: `secrets/**/*.txt` values are not read. Only filenames, directories, READMEs, and `.example` files are used as documentation inputs.
- **Governance Contract**: new stage documents follow the matching templates. READMEs follow the base structure in `docs/99.templates/templates/common/readme.template.md`.

## Current Baseline

| Area                  | Baseline                                                                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Infra inventory       | 48 Compose variant files, 40 Compose service directories, 0 missing service README files                                                                     |
| Root include state    | 17 active include files; commented optional and standalone files are not treated as active runtime                                                           |
| Secret inventory      | 69 root Compose declarations, 94 value/cert filenames, 0 missing declared files                                                                              |
| Secret classification | `compose-declared`, `bind-mounted-cert`, `registry/local-only`, `private-registry`, `example-registry`                                                       |
| README audit          | 134 README files, heading gaps 0                                                                                                                             |
| Stage audit           | 217 non-README docs under `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, `docs/90.references`, heading gaps 0    |
| Semantic QA           | Duplicate legacy/template blocks, non-link references, secret-value wording, and shell-history-sensitive examples are reviewed separately from heading audit |

## Core Design

- **Component Boundary**: documentation strengthening is limited to `README.md`, `docs/03.specs`, `docs/04.execution/plans`, `docs/04.execution/tasks`, `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, and `docs/90.references`.
- **Key Dependencies**: `docs/99.templates/`, `docs/00.agent-governance/rules/documentation-protocol.md`, `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/validate-docker-compose.sh`.
- **Tech Stack**: Markdown, Docker Compose, Bash validation scripts.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: no separate data store is created. Analysis results are stored in this spec, plan, task documents, and existing README/stage documents.
- **Migration / Transition Plan**: strengthen missing template sections without deleting existing document content. For older documents, add template alignment sections below the existing body when needed.

## Interfaces & Data Structures

### Core Interfaces

```text
README base headings:
- Overview
- Audience
- Scope
- Structure
- How to Work in This Area
- Related Documents

Stage document template families:
- docs/05.operations/guides -> guide.template.md
- docs/05.operations/policies -> policy.template.md
- docs/05.operations/runbooks -> runbook.template.md
- docs/90.references -> reference.template.md
```

## API Contract (If Applicable)

Not applicable. This work does not provide external APIs.

- **API Spec**: N/A
- **Policy**: do not create a new API Spec.
- **Machine-readable Contract**: N/A

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation Specialist with Infra/Ops analysis.
- **Inputs**: templates, READMEs, stage docs, infra compose/config paths, secret filenames, and example/registry documents.
- **Outputs**: template-aligned documents, analysis spec/plan/task, and verification results.
- **Success Definition**: repo checks and documentation heading audit pass, and the work completes without reading secret value files.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `find`, `python3`-based documentation audit, repository validation scripts.
- **Permission Boundary**: modify only documentation files inside the workspace. Do not modify secret value files, Docker Compose runtime files, or agent runtime files.
- **Failure Handling**: when validation fails, record failing files and missing sections in task evidence and resolve them with minimal documentation strengthening.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: user instructions granted permission to modify stage documents, so this is treated as an exception to the default read-only policy for `docs/01`~`docs/10`, `docs/90`, and `docs/99`.
- **Policy Constraints**: new active stage documents live only under the allowed taxonomy. Secret values are not exposed in responses, documents, or logs.
- **Versioning Rule**: date-based documents follow the `2026-05-09-*` format.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: preserve investigated file counts, README gaps, and stage template gaps from this run in task evidence.
- **Long-term Memory**: do not update a separate memory file.
- **Retrieval Boundary**: prioritize repo-local files and the provided user plan.

## Guardrails (If Applicable)

- **Input Guardrails**: do not read `secrets/**/*.txt` values.
- **Output Guardrails**: do not write secret values, tokens, private keys, or raw certificate contents into documents.
- **Blocked Conditions**: stop and request separate approval if secret value checks, external network lookup, or Docker runtime changes are needed.
- **Escalation Rule**: if compose/runtime changes become necessary beyond the documentation scope, update the plan and split them behind user approval.

## Evaluation (If Applicable)

- **Eval Types**: structural heading audit, repository contract checks, traceability checks, compose config validation.
- **Metrics**: README missing heading count 0, stage missing heading count 0, repository checks pass, semantic QA findings resolved without runtime or secret value changes.
- **Datasets / Fixtures**: live repository files under target paths.
- **How to Run**: run the Verification commands below and the documentation audit.

## Edge Cases & Error Handling

- **When a README has an existing custom structure**: preserve existing content and add only the missing base headings.
- **When document names and infra directory names differ**: record aliases in the README without renaming. `ksql` infra and `ksqldb` documents follow this rule.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: template strengthening changes the meaning of existing documents.
- **Fallback**: keep the existing body unchanged and add only a separate strengthening section.
- **Human Escalation**: request separate approval if compose file changes, secret value regeneration, or documentation taxonomy changes are needed.

## Verification

```bash
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-quickwin-baseline.sh
bash scripts/hardening/check-all-hardening.sh
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: new stage documents include the required sections from the matching templates.
- **VAL-SPC-002**: target READMEs include base headings.
- **VAL-SPC-003**: non-README Markdown under `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, and `docs/90.references` includes the matching template headings.
- **VAL-SPC-004**: secret value files are not read or modified.
- **VAL-SPC-005**: repository validation scripts pass.
- **VAL-SPC-006**: documents do not confuse root-active, optional, standalone, and variant Compose states.
- **VAL-SPC-007**: examples that encourage secret value checks or can leave sensitive values in shell history are removed or safely rephrased.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md](../../04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md)
- **Tasks**: [../../04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md](../../04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md)
- **Guide**: [../../05.operations/guides/README.md](../../05.operations/guides/README.md)
- **Policy**: [../../05.operations/policies/README.md](../../05.operations/policies/README.md)
- **Runbook**: [../../05.operations/runbooks/README.md](../../05.operations/runbooks/README.md)
- **References**: [../../90.references/README.md](../../90.references/README.md)
