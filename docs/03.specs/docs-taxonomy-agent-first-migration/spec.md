---
status: completed
---
<!-- Target: docs/03.specs/docs-taxonomy-agent-first-migration/spec.md -->

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

- **Docs Taxonomy Contract**: Active stage documents may live only under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates`.
- **Operations Contract**: Guide, policy, runbook, and incident documents are separated under `docs/05.operations/{guides,policies,runbooks,incidents}`.
- **Agent Governance Contract**: Root shims stay thin, with detailed policy kept in `docs/00.agent-governance/` and the runtime mirror.
- **Validation Contract**: `check-repo-contracts.sh` and `check-doc-traceability.sh` enforce the new taxonomy and runtime agent/function catalog.

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
docs/02.architecture/requirements/
docs/02.architecture/decisions/
docs/03.specs/
docs/04.execution/plans/
docs/04.execution/tasks/
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
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
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

- **Plan**: [../../04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md)
- **Tasks**: [../../04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md)
- **Operations Policy**: [../../05.operations/policies/00-workspace/harness-agent-first-engineering.md](../../05.operations/policies/00-workspace/harness-agent-first-engineering.md)
