---
title: Document Lifecycle Convergence Task
version: 1.0.0
type: sdlc/task
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0169-TSK-0001
parent_ids: [SPEC-0169, SPEC-0169-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Document Lifecycle Convergence Task

## Objective

Execute the five phases of SPEC-0169 and record the evidence for each.

## Inputs

- `docs/99.templates/registry.json` section contracts and identity spaces.
- `scripts/lib/document_governance/metadata/heading.py` enforcement branch.
- The 349 stage documents measured in the survey below.
- REQ-0026, AD-0030, ADR-0030 as the retention owners to update in place.

## Work Log

### Survey baseline (2026-09-03, commit d129870f)

| Profile | Docs | Missing required | Unregistered headings |
| :--- | ---: | ---: | ---: |
| `guide` | 66 | 66 | 66 |
| `policy` | 64 | 64 | 64 |
| `runbook` | 62 | 62 | 62 |
| `spec` | 33 | 0 | 6 |
| `adr` | 27 | 0 | 23 |
| `requirements-package` | 26 | 0 | 23 |
| `architecture-description` | 26 | 0 | 20 |
| **Total** | **349** | **192** | **272** |

Enforcement gap proven by mutation on `docs/03.specs/0002-auth/spec.md`:
adding an unregistered `## Totally Unregistered Heading` passed the contract
check, and renaming the required `## Traceability` to `## Trace` also passed.
Cause: `validate_body_contract` enforces sections only where `template_id` is
`None` or the type is outside the typed target set.

## Verification Evidence

Recorded per phase as the work lands.

## Review Evidence

Recorded per phase as the work lands.

## Commit Ledger

| Commit | Phase |
| :--- | :--- |
| pending | Phase 1 declarations |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
