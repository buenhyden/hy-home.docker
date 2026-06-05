---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md -->

# Infra / Secrets / Docs Refresh Plan

## Overview

This document is the implementation plan for updating README and stage documents to match templates based on analysis of `infra`, `secrets`, `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, and `docs/90.references`.

## Context

The current repository has layered Docker Compose infrastructure and a stage-based docs taxonomy, and repository contract validation passes. README and stage heading audits also currently show gap 0. This work is a documentation-focused refresh that strengthens root-active Compose scope, secret classification, and semantic QA results in the documents so heading-pass status is not mistaken for full quality completion.

## Goals & In-Scope

- **Goals**:
  - Record implementation elements, compose/config/related files, and documentation gaps for target paths in official stage documents.
  - Align READMEs with the `readme.template.md` base structure.
  - Strengthen `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, and `docs/90.references` documents so they include required sections from their matching templates.
  - Distinguish root-active, optional, standalone, and variant Compose states.
  - Classify root Compose declarations, bind-mounted certs, registry files, and local-only files without reading secret values.
  - Verify heading audit and semantic QA separately.
  - Connect root `README.md` and `docs/README.md` to the latest analysis scope.
- **In Scope**:
  - Document and README updates
  - Parent README link updates
  - Validation command execution and task evidence recording

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Changing Docker Compose service behavior
  - Reading or regenerating secret value files
  - Changing the agent runtime catalog
- **Out of Scope**:
  - Creating new PRDs, ARDs, ADRs, or incidents
  - Querying external networks
  - Deployments, migrations, or certificate reissuance

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create analysis spec/plan/task | `docs/03.specs`, `docs/04.execution/plans`, `docs/04.execution/tasks` | REQ-DOC-001 | Required template sections exist |
| PLN-002 | Refresh root/docs/secrets READMEs | `README.md`, `docs/README.md`, `secrets/README.md` | REQ-RDM-001 | README base heading audit passes |
| PLN-003 | Strengthen infra and docs stage READMEs | `infra/**/README.md`, `docs/05.operations/{guides,policies,runbooks}/**/README.md`, `docs/90.references/**/README.md` | REQ-RDM-002 | 0 missing headings and non-link references cleaned up |
| PLN-004 | Strengthen guide/operation/runbook/reference documents | `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, `docs/90.references` | REQ-STG-001 | Stage heading audit passes and semantic QA passes |
| PLN-005 | Refresh validation and evidence | `docs/04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md` | REQ-VAL-001 | Validation command results recorded |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Confirm repository contract | `bash scripts/validation/check-repo-contracts.sh` | failures=0 |
| VAL-PLN-002 | Structural | Confirm docs traceability | `bash scripts/validation/check-doc-traceability.sh` | failures=0 |
| VAL-PLN-003 | Runtime config | Confirm Compose config | `bash scripts/validation/validate-docker-compose.sh` | service count > 0 |
| VAL-PLN-004 | Security baseline | Confirm template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | pass |
| VAL-PLN-005 | Hardening | Confirm baseline hardening | `bash scripts/validation/check-quickwin-baseline.sh` and `bash scripts/hardening/check-all-hardening.sh` | pass |
| VAL-PLN-006 | Docs template | README/stage heading audit | local `python3` audit | missing=0 |
| VAL-PLN-007 | Diff hygiene | Confirm Markdown whitespace | `git diff --check` | no errors |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Meaning changes while older documents are aligned to templates | Medium | Preserve existing body content and strengthen only missing sections |
| Secret values are exposed in documents | High | Do not read `secrets/**/*.txt`; use only paths and examples |
| Documentation strengthening scope becomes too broad | Medium | Exclude runtime, compose, and governance changes; focus on template alignment |
| `ksql`/`ksqldb` naming differences are mistaken for omissions | Low | Explain aliases in README and do not rename files |
| Held Compose files are confused with root-active Compose | Medium | Document `root-active`, `root-commented-optional`, `standalone-only`, and `dev/cluster variant` states |
| Validation results read like all profiles passed | Medium | Record the default `core` profile scope and temporary-file behavior of `validate-docker-compose.sh` in evidence |
| Heading audit pass is mistaken for document quality completion | Medium | Record semantic QA items separately in task evidence and README |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: README/stage heading audit must have missing=0.
- **Sandbox / Canary Rollout**: Not applied; this is a docs-only change.
- **Human Approval Gate**: Separate approval is required if runtime, secret value, or compose changes become necessary.
- **Rollback Trigger**: Revert the affected document change and record the cause if validation failure or secret value exposure is found.
- **Prompt / Model Promotion Criteria**: Not applied.

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **PRD**: No explicit PRD
- **ARD**: No explicit ARD
- **Spec**: [../03.specs/infra-secrets-docs-refresh/spec.md](../../03.specs/infra-secrets-docs-refresh/spec.md)
- **ADR**: No explicit ADR
- **Task**: [../04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md](../tasks/2026-05-09-infra-secrets-docs-refresh.md)
- **Operation**: [../05.operations/README.md](../../05.operations/README.md)
- **Runbook**: [../05.operations/README.md](../../05.operations/README.md)
