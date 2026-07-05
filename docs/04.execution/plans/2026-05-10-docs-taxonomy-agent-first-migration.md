---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md -->

# Docs Taxonomy and AI Agent-first Contract Migration Plan

## Overview

This document is the implementation plan for migrating the documentation taxonomy and AI Agent-first contract to the new canonical paths. The goal is to align docs SSoT, validator, and runtime mirror terminology at once without changing the Docker runtime.

## Context

The previous repository contract pinned legacy requirements, execution, and operations stage names into documents, templates, validators, and runtime docs. The new contract uses shorter active stages and purpose-specific operations subfolders.

## Goals & In-Scope

- Move documentation files into the new taxonomy.
- Update governance, provider, runtime, template, and infra README links to the new paths.
- Update validators against the new taxonomy and the runtime agent/function catalog.
- Leave migration evidence inside the new taxonomy.

## Non-Goals & Out-of-Scope

- Docker Compose runtime behavior changes
- Secret value or credential file analysis
- Adding a GitHub-native instruction layer
- Promoting Graphify advisory status to a hard gate

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Move stage docs to the new taxonomy | `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations` | REQ-TAX-001 | top-level docs contract passes |
| PLN-002 | Split operations docs by purpose | `docs/05.operations/{guides,policies,runbooks,incidents}` | REQ-OPS-001 | service coverage and traceability pass |
| PLN-003 | Update governance and runtime references | `docs/00.agent-governance`, `.claude`, `.codex`, `.github`, `infra` | REQ-AGENT-001 | stale-reference scan passes |
| PLN-004 | Update validators | `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-traceability.sh` | REQ-VAL-001 | validators pass |
| PLN-005 | Record migration evidence | this plan, spec, task evidence | REQ-EVD-001 | evidence docs exist and link back |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Syntax | Bash and JSON syntax | `bash -n ...`; `python3 -m json.tool ...` | exit 0 |
| VAL-PLN-002 | Contract | Repository docs/runtime contract | `bash scripts/validation/check-repo-contracts.sh` | failures=0 |
| VAL-PLN-003 | Traceability | Execution to operations links | `bash scripts/validation/check-doc-traceability.sh` | failures=0 |
| VAL-PLN-004 | Runtime | Docker Compose config remains valid | `bash scripts/validation/validate-docker-compose.sh` | pass |
| VAL-PLN-005 | Advisory graph | Graphify state reported | `bash scripts/knowledge/report-graphify-health.sh` | status reported |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Relative links break during moves | High | Run stale-reference scans and validators after migration |
| Validator passes stale taxonomy | High | Update allowed docs, stale regex, coverage and traceability checks together |
| Operations split creates duplicate SSoT | Medium | Do not require every service to have all guide/policy/runbook documents |
| Graphify output is contaminated | Low | Keep Graphify advisory and corroborate against tracked files |

## Completion Criteria

- [x] Scoped migration completed
- [x] Validators pass under the new taxonomy
- [x] Docker Compose validation still passes
- [x] Graphify advisory status reported

## Related Documents

- **Spec**: [../../03.specs/093-docs-taxonomy-agent-first-migration/spec.md](../../03.specs/093-docs-taxonomy-agent-first-migration/spec.md)
- **Task Evidence**: [../tasks/2026-05-10-docs-taxonomy-agent-first-migration.md](../tasks/2026-05-10-docs-taxonomy-agent-first-migration.md)
- **Docs Index**: [../../README.md](../../README.md)
