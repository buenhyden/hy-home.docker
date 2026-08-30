---
profile_id: spec
status: active
artifact_id: SPEC-0093
artifact_type: spec
parent_ids:
  - AD-0027
created: 2026-07-05
updated: 2026-08-11
---
# Docs Taxonomy and AI Agent-first Contract Migration Specification

## Overview

This specification defines the migration of the `hy-home.docker` documentation taxonomy into the new canonical structure from `01.requirements` through `05.operations`, and aligns the AI Agent-first Engineering contract with the same path system.

## Strategic Boundaries & Non-goals

- This specification covers documentation paths, governance routing, validator contracts, and runtime catalog terminology.
- It does not change Docker Compose runtime behavior, secret values, credentials, or deployment procedures.
- It does not create legacy path redirect documents.

## Related Inputs

- **Requirements**: [../../01.requirements/README.md](../../01.requirements/README.md)
- **Architecture**: [../../02.architecture/README.md](../../02.architecture/README.md)
- **Operations Stage**: [../../05.operations/README.md](../../05.operations/README.md)

## Contracts

- **Docs Taxonomy Contract**: Active stage documents may live only under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates`. `docs/04.execution` was removed from this set on 2026-08-29: the stage no longer exists, and Plans and Tasks are co-located in their owning `docs/03.specs/{number:4}-{slug}/` package.
- **Operations Contract**: Guide, Policy, and Runbook leaves share prefixless subject packages under `docs/05.operations/catalog/<domain>/<####-subject>/`; Incident packets remain the sibling `docs/05.operations/incidents/<year>/inc-####-<slug>/` topology.
- **Agent Governance Contract**: Root shims stay thin, with detailed policy kept in `docs/00.agent-governance/` and the runtime mirror.
- **Validation Contract**: the registered public validation suites, run by `scripts/validation/run-ci-gate.py`, and `check-document-links.py --mode traceability` enforce the new taxonomy and runtime agent/function catalog. Corrected 2026-08-29: `check-repo-contracts.sh` was deleted by `1c620dd0` when validation was routed through the public suites.

## Core Design

- Existing stage files move to the new paths.
- Legacy consolidated operations documents are split into `guides`, `policies`, and `runbooks` according to their consumption purpose.
- `docs/README.md` is the new taxonomy SSoT, and old paths are described only in the migration map.
- `docs/99.templates` keeps the existing template filenames while updating target examples to the new paths.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Stage taxonomy is represented by canonical folder paths and README indexes, not by a runtime database.
  - Template-to-folder mapping lives in `docs/99.templates/README.md` and governance rules.
- **Migration / Transition Plan**:
  - Move active artifacts into canonical stage paths.
  - Rewrite active references to canonical paths.
  - Keep legacy path names only in explicit migration maps and historical evidence.

## Interfaces & Data Structures

### Canonical Stage Path Contract

```text
docs/01.requirements/
docs/02.architecture/descriptions/
docs/02.architecture/decisions/
docs/03.specs/
docs/03.specs/{number:4}-{slug}/plan.md
docs/03.specs/{number:4}-{slug}/tasks/
docs/05.operations/
docs/90.references/
docs/99.templates/
```

## Guardrails

- Secret values, private keys, tokens, auth files, shell history, credential logs are out of scope.
- Graphify remains advisory when contaminated or unavailable.
- `.claude/settings.json` remains team config; `.claude/settings.local.json` remains personal-only.
- GitHub-native instruction layers remain out of scope.

## Verification

```bash
bash -n scripts/**/*.sh .claude/hooks/*.sh
python3 -m json.tool .claude/settings.json
python3 -m json.tool .codex/hooks.json
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/check-document-links.py --mode traceability
bash scripts/validation/validate-docker-compose.sh
bash scripts/knowledge/report-graphify-health.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: old active taxonomy references are absent except the explicit migration map in `docs/README.md`.
- **VAL-SPC-002**: repository contract and doc traceability gates pass under the new taxonomy.
- **VAL-SPC-003**: Docker Compose validation remains unchanged and passes.
- **VAL-SPC-004**: Graphify health is reported as advisory when contaminated, not promoted to a hard gate.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: co-located at `plan.md` in this package when one is written.
- **Tasks**: co-located under `tasks/` in this package when execution begins.
- **Operations Policy**: [../../05.operations/policies/00-workspace/harness-agent-first-engineering.md](../../05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/policy.md)

## Boundaries and Inputs

The preserved ownership boundaries, dependencies, and inputs above remain authoritative.

## Behavior Contract

The behaviors and invariants already specified above remain the package behavior contract.

## Technical Approach

The implementation and component design recorded above remain the technical approach.

## Interfaces and Data

The interfaces, configuration, and data shapes recorded above remain authoritative.

## Failure Modes and Guardrails

The safety, validation, and operational constraints above remain the package guardrails.

## Acceptance Contract

The verification and success conditions above remain the acceptance contract.

## Traceability

The requirement, architecture, operations, and evidence links above provide traceability.
