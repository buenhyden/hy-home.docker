---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md -->

# Task: 08-AI Optimization Hardening

## Overview

This document tracks the `08-ai` optimization and hardening execution tasks. It manages compose hardening, CI gates, documentation traceability, and catalog expansion policies (model promotion, access separation, and log masking) as task units.

## Inputs

- **Parent Spec**: [../../03.specs/08-ai/spec.md](../../03.specs/08-ai/spec.md)
- **Parent Plan**: [../plans/2026-03-28-08-ai-optimization-hardening-plan.md](../plans/2026-03-28-08-ai-optimization-hardening-plan.md)

## Working Rules

- AI configuration changes leave compose static validation plus hardening script results.
- Changes that affect gateway/auth record the security-boundary impact.
- Documentation changes update PRD-to-Runbook links and README indexes together.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AI-001 | Align Ollama/Open WebUI middleware with the gateway+SSO chain | impl | Contracts / Config | PLN-AI-001 | Confirm compose labels | DevOps | Done |
| T-AI-002 | Add environment variables for Ollama concurrency/queue limits | impl | Contracts / Config | PLN-AI-002 | Confirm env contract | DevOps | Done |
| T-AI-003 | Align the Open WebUI stateful template | impl | Contracts / Config | PLN-AI-003 | Confirm template | DevOps | Done |
| T-AI-004 | Add exporter health-gated dependency and healthcheck | impl | Contracts / Config | PLN-AI-004 | Confirm dependency/healthcheck | DevOps | Done |
| T-AI-005 | Add/update the AI hardening script | ops | Governance Contract | PLN-AI-005 | `bash scripts/hardening/check-all-hardening.sh 08-ai` | DevOps | Done |
| T-AI-006 | Add the CI `infrastructure-hardening` job | ops | Governance Contract | PLN-AI-005 | Confirm workflow job | DevOps | Done |
| T-AI-007 | Refresh scripts inventory/usage README | doc | Related Docs | PLN-AI-005 | Reflect README entries | Docs | Done |
| T-AI-008 | Create PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook docs | doc | Related Docs | PLN-AI-006 | Synchronize links/indexes | Docs | Done |
| T-AI-009 | Define Ollama model promotion procedures (experiment -> production) | doc | Catalog-aligned Expansion | PLN-AI-007 | Reflect operations/tasks updates | AI Owner | Done |
| T-AI-010 | Define Open WebUI model access separation criteria | doc | Catalog-aligned Expansion | PLN-AI-007 | Reflect operations/tasks updates | AI Owner | Done |
| T-AI-011 | Define Open WebUI conversation log retention/masking policy | doc | Catalog-aligned Expansion | PLN-AI-007 | Reflect operations/tasks updates | Security/AI Owner | Done |
| T-AI-012 | Run static validation and record results | test | Verification | PLN-AI-001~007 | Check compose/script/baseline/traceability | DevOps | Done |
| T-AI-013 | Collect runtime startup rehearsal and performance tuning evidence | test | Verification | PLN-AI-001~007 | Live health/latency/GPU metrics require an approved runtime rehearsal | DevOps | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-AI-001
- [x] T-AI-002
- [x] T-AI-003
- [x] T-AI-004
- [x] T-AI-005
- [x] T-AI-006
- [x] T-AI-007

### Phase 2

- [x] T-AI-008
- [x] T-AI-009
- [x] T-AI-010
- [x] T-AI-011
- [x] T-AI-012
- [x] T-AI-013 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `bash scripts/hardening/check-all-hardening.sh 08-ai`
  - `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local validation logs + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-AI-013 remains a live rehearsal item, not an unimplemented static hardening task.

## Related Documents

- **PRD**: [../01.requirements/020-ai-optimization-hardening.md](../../01.requirements/020-ai-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0023-ai-optimization-hardening-architecture.md](../../02.architecture/requirements/0023-ai-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-08-ai-optimization-hardening-plan.md](../plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/08-ai/optimization-hardening.md](../../05.operations/guides/08-ai/optimization-hardening.md)
- **Operation**: [../../05.operations/policies/08-ai/optimization-hardening.md](../../05.operations/policies/08-ai/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/08-ai/optimization-hardening.md](../../05.operations/runbooks/08-ai/optimization-hardening.md)
