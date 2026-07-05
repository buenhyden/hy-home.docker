---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md -->

# Task: 04-Data Optimization Hardening

## Overview

This document tracks the `04-data` optimization and hardening implementation tasks. It manages compose consistency improvements, hardening validation automation, and documentation traceability synchronization as task units.

## Inputs

- **Parent Spec**: [../../03.specs/04-data/spec.md](../../03.specs/04-data/spec.md)
- **Parent Plan**: [../plans/2026-03-28-04-data-optimization-hardening-plan.md](../plans/2026-03-28-04-data-optimization-hardening-plan.md)

## Working Rules

- 04-data hardening starts with immediately applicable items according to catalog priority.
- Every compose change leaves static validation (`docker compose config`) and script evidence.
- Documentation changes maintain PRD-to-Runbook cross-links.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-DATA-001 | Add healthchecks for core `supabase` services | impl | 04-data/spec.md / Contracts | PLN-DATA-001 | `docker compose ...supabase... config` | DevOps | Done |
| T-DATA-002 | Align the Valkey exporter secret path | impl | 04-data/spec.md / Contracts | PLN-DATA-002 | No `rg mng_valkey_password` matches | DevOps | Done |
| T-DATA-003 | Remove SeaweedFS expose typos | impl | 04-data/spec.md / Contracts | PLN-DATA-003 | No `rg ':-19333}]\|:-18085}]\|:-18888}]'` matches | DevOps | Done |
| T-DATA-004 | Normalize the ksql tier label | impl | 04-data/spec.md / Contracts | PLN-DATA-004 | Confirm `hy-home.tier: data` | DevOps | Done |
| T-DATA-005 | Create `check-all-hardening.sh 04-data` | ops | 04-data/spec.md / Governance | PLN-DATA-005 | `bash scripts/hardening/check-all-hardening.sh 04-data` | DevOps | Done |
| T-DATA-006 | Add the CI `infrastructure-hardening` job | ops | 04-data/spec.md / Governance | PLN-DATA-006 | Confirm workflow changes | DevOps | Done |
| T-DATA-007 | Refresh the scripts README index/examples | doc | 04-data/spec.md / Related Docs | PLN-DATA-007 | Confirm README entries | Docs | Done |
| T-DATA-008 | Reflect PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook docs | doc | 04-data/spec.md / Related Docs | PLN-DATA-008 | Confirm document links/indexes | Docs | Done |
| T-DATA-009 | Run static validation and record results | test | 04-data/spec.md / Verification | PLN-DATA-001~008 | Check compose + hardening + traceability | DevOps | Done |
| T-DATA-010 | Collect runtime validation evidence where available | test | 04-data/spec.md / Verification | PLN-DATA-001~008 | Live service health evidence is collected only in an approved runtime session | DevOps | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-DATA-001
- [x] T-DATA-002
- [x] T-DATA-003
- [x] T-DATA-004
- [x] T-DATA-005
- [x] T-DATA-006

### Phase 2

- [x] T-DATA-007
- [x] T-DATA-008
- [x] T-DATA-009
- [x] T-DATA-010 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config`
  - `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config`
  - `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config`
  - `docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config`
  - `bash scripts/hardening/check-all-hardening.sh 04-data`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local validation logs + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-DATA-010 is outside the static implementation pass and requires approved live services.

## Related Documents

- **PRD**: [../01.requirements/016-data-optimization-hardening.md](../../01.requirements/016-data-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0019-data-optimization-hardening-architecture.md](../../02.architecture/requirements/0019-data-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-04-data-optimization-hardening-plan.md](../plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/04-data/optimization/optimization-hardening.md](../../05.operations/guides/04-data/optimization/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/04-data/optimization/optimization-hardening.md](../../05.operations/policies/04-data/optimization/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/04-data/optimization/optimization-hardening.md](../../05.operations/runbooks/04-data/optimization/optimization-hardening.md)
