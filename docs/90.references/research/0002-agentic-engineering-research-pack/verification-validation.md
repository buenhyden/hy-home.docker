---
status: draft
artifact_id: reference:agentic-engineering-research-draft:verification-validation
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Verification and Validation

## Overview

Verification and validation are distinct evidence disciplines. Verification
asks whether a named artifact conforms to a requirement, contract, or oracle;
validation asks whether a result is adequate for intended use and its stated
stakeholder or operational context.

## Purpose

Provide a small responsibility model that prevents the invalid inference that
a local test or CI pass automatically validates a system, accepts residual
risk, or authorizes release.

## Scope

This leaf maps retained V&V research and entry-HEAD validators to documentation
and delivery evidence. It excludes an actual product validation exercise,
stakeholder acceptance, hosted execution, deployment, incident evidence, and
remote authority.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `VV-001` | Tracked metadata and link validators, typed CI gates, tests, and review records provide verification mechanisms for declared artifacts and oracles. | tracked configuration | VERIFIED | `scripts/validation/`, `tests/validation/`, `.github/workflow-contract.yml` at `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | Record the candidate, oracle, environment, command, and raw result for each verification claim. |
| `VV-002` | Retained IEEE/NASA/NIST material distinguishes conformance-oriented verification from intended-use validation and identifies review, inspection, analysis, and testing as complementary evidence methods. | retained official observation | HISTORICAL VERIFIED | retained Task 0001 V&V ledger | A successful verification activity does not supply intended-use validation or acceptance authority. |
| `VV-003` | Independent review and acceptance require a named responsibility separate from the implementation command; this draft's terminal reviews remain external and the Task remains active. | tracked governance plus advisory synthesis | VERIFIED | Task 0004 and current draft execution contract | Keep authoring, checking, review, and acceptance evidence attributable to their respective owners. |

### Lifecycle evidence and independence

The minimum chain is expectation or requirement → identified candidate → method
and risk depth → environment/data/oracle → observation → defect disposition or
repeat evidence → acceptance decision and residual-risk authority → monitoring
and revalidation trigger. A missing link is `UNVERIFIED`, not a reason to
substitute a convenient check.

Apply independence in proportion to consequence: an author may run a focused
verification, but an independent reviewer evaluates the evidence range and a
named authority decides acceptance. Validation needs a representative intended
use, success criteria, and stakeholder or operational authority; none are
created by this Stage 90 research leaf. Revalidate after a change to the
candidate, requirement, design, oracle, data, environment, dependency, threat
model, defect disposition, or acceptance assumptions.

No observed validator proves a provider entitlement, runtime behavior, hosted
check, branch rule, deployment, rollback, security certification, or release
acceptance. `SDLCDOC-ADR-002` and `SDLCDOC-ADR-003` remain `UNVERIFIED`; this
leaf does not alter either ADR evidence state.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `VV-SRC-001` | `VV-001` | Validation scripts, tests, and workflow registry / workspace | [validation scripts](../../../../scripts/validation/), [validation tests](../../../../tests/validation/), [workflow registry](../../../../.github/workflow-contract.yml) | tracked configuration | `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | 2026-08-28 | Definitions and file presence do not prove a complete or hosted execution. |
| `VV-SRC-002` | `VV-002` | V&V guidance / IEEE, NASA, NIST | [IEEE 1012](https://standards.ieee.org/ieee/1012/7324/), [NASA Product Realization](https://www.nasa.gov/reference/5-0-product-realization/), [NISTIR 8397](https://www.nist.gov/publications/guidelines-minimum-standards-developer-verification-software) | retained official observation | Task 0001 dated V&V ledger | 2026-08-09T12:37:24Z | Public material supports only the retained high-level distinction; no clause-level conformance is claimed. |
| `VV-SRC-003` | `VV-003` | Current draft execution and task ledger / workspace | [Task 0004](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md), [plan](../../../03.specs/0137-agentic-research-pack-rebuild/plan.md) | tracked governance | `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | 2026-08-28 | This is a draft workflow boundary, not product or release acceptance. |

## Maintenance

Remeasure local validators and their contracts after any owner change. Reopen
retained V&V sources only with authorized access. For each future validation or
acceptance decision, preserve the candidate identity, intended use, authority,
evidence, residual risk, monitoring, and revalidation trigger.

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Define agent task success, tools, evidence, and handoff before validation. | Inspect Task and evidence contract. | Provider runtime is unobserved. |
| architecture | applies | Trace architecture decisions and quality attributes to an owner. | Inspect design/requirement evidence. | Conformance does not establish fitness. |
| common | applies | Maintain reusable contracts and independent review boundaries. | Inspect owner and reviewer records. | Shared checks need scope-specific oracles. |
| docs | applies | Verify metadata, links, and source support; validate reader utility separately. | Record validator and review evidence. | A link pass is not reader validation. |
| infra | applies | Define target, environment, health, rollback, and acceptance authority. | Inspect target-specific evidence. | No runtime target is observed. |
| ops | applies | Bind release and incident evidence to named operational authority. | Inspect runbook and event records. | No release or incident result is claimed. |
| qa | applies | Use risk-based methods and preserve oracle/defect evidence. | Inspect test/review results and disposition. | Tests alone do not accept residual risk. |
| security | applies | Include threat, control, scan, exception, and acceptance evidence. | Inspect security owner decision. | Scanner output is not certification. |

## Related Documents

- [Automation Pipeline Workflow](./automation-pipeline-workflow.md)
- [Quality CI and Formatting](./quality-ci-formatting.md)
