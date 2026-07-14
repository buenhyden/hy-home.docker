---
status: draft
artifact_id: spec:124-compose-runtime-readiness-remediation
artifact_type: spec
parent_ids:
  - spec:123-agentic-engineering-audit-remediation
---

# Compose Runtime Readiness Remediation Technical Specification (Spec)

## Overview

This draft defines the future contract for proving that an explicitly bounded
Compose service set can start, become ready, recover from approved failure
scenarios, and tear down without unapproved data or secret exposure. It owns
three canonical audit gaps and does not authorize service startup, runtime
mutation, secret access, or remote action.

Spec 123 is the approved audit lineage and typed parent. Its approval authorizes
this documentation follow-up only; it is not runtime authorization. Activation
requires the unresolved Stage 01/02 predecessors and every approval gate below.

## Strategic Boundaries & Non-goals

- Own startup, observed readiness, bounded failure recovery, teardown, and the
  evidence envelope for a later runtime task.
- Do not own upgrade, migration, backup, or restore contracts; Spec 125 owns
  those stateful operations.
- Do not own supply-chain verification or promotion; Specs 126 and 127 own
  those decisions.
- Do not infer runtime health from Compose rendering, healthcheck YAML, or
  documentation presence.
- Do not select services, profiles, hosts, credentials, or failure-injection
  methods in this draft.

## Boundaries and Inputs

- **PRD**: Unresolved prerequisite. A Stage 01 owner must define approved
  runtime-readiness value, bounded service/profile scope, acceptable disruption,
  and acceptance criteria.
- **ARD**: Unresolved prerequisite. A Stage 02 architecture owner must define
  the isolated test topology, dependency boundary, state/secret boundary,
  observability surface, and teardown guarantees.
- **Related ADRs**: Unresolved prerequisites for runtime isolation strategy,
  readiness evidence source, and permitted failure-injection/cleanup approach.
- **Audit lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
  authorizes this draft only.

Architecture-changing runtime harness, topology, network, volume, healthcheck,
or initialization changes are blocked until the required PRD, ARD, and ADRs
exist and are approved. This specification does not create or claim them.

## Canonical Gap Ownership

The following matrix is authoritative for this specification. `Owned` means
the gap appears as a requirement only here. Sibling references are dependency
links and never duplicate ownership.

| Audit gap | Disposition | Requirement owner | Reason |
| --- | --- | --- | --- |
| `CIO-01`–`CIO-04` | Not routed: already implemented static evidence | Existing Compose inventory/render/hardening/version owners | These controls are prerequisites and regression evidence, not runtime gaps. |
| `CIO-05` | Not routed: non-runtime documentation adequacy | Stage 05 operations owners | Procedure presence/quality requires operations review, not a runtime requirement here. |
| `CIO-06` | Owned | `CRR-001` | Startup and initialization execution evidence. |
| `CIO-07` | Owned | `CRR-002` | Observed live readiness evidence. |
| `CIO-08` | Owned | `CRR-003` | Bounded failure recovery and escalation evidence; state restoration is a Spec 125 dependency. |

Owned gap count: **3**.

## Contracts

### Runtime Evidence Contract

| Requirement | Target behavior | Required evidence |
| --- | --- | --- |
| `CRR-001` | Start only an approved service/profile set in an approved isolated target; dependencies and initialization complete within declared bounds; teardown is deterministic. | Dated target/profile/service inventory, command class, initialization result, duration, teardown result, and non-secret failure summary. |
| `CRR-002` | Observe container and service-specific endpoint readiness after startup; distinguish ready, degraded, failed, and timed-out states. | Dated container/endpoint observations, service acceptance criteria, elapsed time, failure disposition, and evidence-source identity. |
| `CRR-003` | Rehearse only approved failure scenarios with bounded blast radius; record recovery time, state impact, stop conditions, and escalation. | Scenario ID, injection boundary, recovery steps, observed outcome, recovery-time observation, state classification, stop/escalation result, and teardown confirmation. |

### Configuration Contract

- A future active contract must name exact Compose files, profiles, services,
  target host class, resource limits, timeouts, and teardown commands.
- Test-only overlays or healthcheck/initialization changes are architecture or
  runtime changes and require predecessor approval plus scoped review.
- No unbounded `up`, default-profile expansion, production target, or implicit
  host selection is permitted.

### Data / Interface Contract

The future evidence record must contain stable scenario, service, target-class,
start/end time, observed state, recovery/teardown result, and approval/task
references. It must contain no secret value, raw environment dump, raw service
log, auth token, credential, or private endpoint payload.

### Governance Contract

- Audit and umbrella approval permit drafting only.
- Runtime execution requires a separately approved Stage 04 task naming the
  exact surface, approval source, commands, validation, recovery, and redaction.
- Unexpected service/profile expansion, state damage, secret exposure, or
  inability to tear down is a stop-and-escalate condition.

## Current Evidence

At the 2026-07-11 canonical audit baseline, the tracked Compose inventory
contained 49 files, 169 service entries, and 25 profiles. Static core rendering
passed with five services and all eleven hardening tiers passed. Healthcheck,
dependency, initialization, observability, and recovery documentation exists,
but no service startup, observed live health, or recovery drill was authorized
or recorded. These static results are prerequisites only.

## Core Design

- **Component Boundary**: A future bounded runtime evidence harness around a
  separately approved Compose target; no harness is selected here.
- **Key Dependencies**: Spec 125 for stateful recovery; Spec 126 for artifact
  verification inputs; Spec 127 for promoted artifact/config identity.
- **Tech Stack**: Unresolved. Compose and repository validators are candidates,
  not approved runtime commands.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Store concise, redacted task evidence with one
  record per approved scenario and service acceptance set. Keep raw runtime
  diagnostics outside tracked documentation and handle them under the future
  task's approved evidence boundary.
- **Migration / Transition Plan**: Draft -> predecessor approval -> active spec
  approval -> approved Stage 04 plan/task -> isolated rehearsal -> reviewed
  evidence. Existing Compose defaults remain unchanged until that sequence
  completes.

## Interfaces and Data

### Core Interfaces

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Approved runtime scope | Human/architecture approval | Future runtime task | Exact target, files, profiles, services, duration, and teardown. |
| Readiness result | Approved observation mechanism | QA/SRE review | Service criteria plus ready/degraded/failed/timed-out result. |
| Recovery result | Approved scenario executor | Operations/security review | Scenario, data impact, recovery time, stop/escalation, and cleanup. |
| Stateful recovery handoff | Spec 125 implementation | This workstream | Approved restore/rollback boundary; no duplicated requirement. |

## API Contract (If Applicable)

Not applicable. This draft defines runtime evidence and approval contracts and
does not expose an external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: A future `infra-implementer` may execute only a separately
  approved task; `iac-reviewer`, `security-auditor`, and `qa-engineer` review.
- **Inputs**: Approved predecessors, active spec/plan/task, exact runtime scope,
  redaction rules, and rollback/teardown criteria.
- **Outputs**: Concise evidence records and no unapproved runtime persistence.
- **Success Definition**: All scoped scenarios pass or stop safely with complete
  redacted evidence and independent review.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Unresolved until the future task names exact Compose and
  observation command classes.
- **Permission Boundary**: Documentation and static validation only under this
  draft; no service command is permitted.
- **Failure Handling**: Stop on scope drift, secret exposure, target ambiguity,
  resource exhaustion, state corruption, or teardown failure.

## Prompt / Policy Contract (If Applicable)

- Instructions must repeat the exact approved target/profile/service set and
  prohibited surfaces.
- No agent may infer runtime approval from Spec 123, this draft, or a static
  validation pass.
- Model/provider selection is outside this specification.

## Memory & Context Strategy (If Applicable)

Use canonical specs/plans/tasks and concise Stage 04 evidence. Do not persist
raw logs, runtime dumps, secrets, or credentials in memory or documentation.

## Guardrails (If Applicable)

- **Input Guardrails**: Validate exact target identity, worktree/revision,
  Compose files, profiles, services, approvals, timeouts, and teardown before
  execution.
- **Output Guardrails**: Redact secret-bearing fields and record bounded
  summaries only.
- **Blocked Conditions**: Missing predecessors, ambiguous target, no teardown,
  unapproved stateful service, missing secret approval, or missing recovery path.
- **Escalation Rule**: Stop immediately and obtain new human/runtime approval
  when any protected boundary changes.

## Approval Gates

| Gate | Unresolved approval required before activation/execution | Evidence required |
| --- | --- | --- |
| Architecture | Approved PRD, ARD, and relevant ADRs for topology, isolation, evidence, and failure injection | Canonical paths/IDs and approval state. |
| Human | Named owner approves scenario scope, blast radius, maintenance window, stop criteria, and residual risk | Approval reference in a future Stage 04 task. |
| Runtime | Exact target, Compose files, profiles, services, commands, timeouts, teardown, and recovery | Before-state/static render plus approved task contract. |
| Secret | Named secret IDs/paths and permitted metadata only; values remain prohibited | Redaction plan and reviewer; no secret material in evidence. |
| Remote | Any remote host, registry, observability, or GitHub query/mutation is separately approved | Repository/target identity, command class, before/after evidence, and rollback. |

## Edge Cases & Error Handling

- A declared healthcheck passes while the service endpoint fails: record
  degraded/failed, do not promote readiness.
- Dependency initialization exceeds the bound: stop, capture a concise
  non-secret summary, and tear down.
- Failure recovery crosses into data restore: stop and hand off to Spec 125.
- Teardown leaves services/networks/volumes unexpectedly active: treat as a
  runtime incident boundary and escalate; do not auto-delete state.

## Failure Modes and Guardrails

- **Failure Mode**: Startup, readiness, recovery, or teardown violates the
  approved envelope.
- **Fallback**: Stop new actions, preserve redacted evidence, use only the
  approved teardown/recovery path, and leave state intact when cleanup is
  uncertain.
- **Human Escalation**: Runtime owner and security/operations reviewers decide
  whether to recover, revise the contract, or abandon the scenario.

## Migration, Rollback, and Recovery

- Introduce the smallest approved isolated scenario first; expand only after
  reviewed evidence.
- Keep existing Compose declarations/default activation unchanged unless a
  later architecture decision and task explicitly authorize changes.
- Roll back test-only configuration by the future task's reviewed commit or
  override removal; never rewrite persistent data as configuration rollback.
- Use the Spec 125 recovery contract for state restoration. Configuration
  rollback and data recovery remain distinct.

## Verification

Documentation-phase checks:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 4937ae999825391963149cb285c686808dbb394b
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Runtime commands are intentionally absent. A future active task must define
them after approvals and must include one negative/stop-path check.

## Success Criteria & Verification Plan

- **VAL-CRR-001**: The three owned audit gaps appear exactly once across Specs
  124-127 and map to `CRR-001` through `CRR-003`.
- **VAL-CRR-002**: Static evidence remains labeled static; no runtime result is
  claimed.
- **VAL-CRR-003**: Every future scenario has approved scope, readiness criteria,
  teardown, redaction, recovery, and independent review evidence.
- **VAL-CRR-004**: Architecture, human, runtime, secret, and remote gates are
  resolved before any service command.

## Related Documents

- **Plan**: [Compose runtime-readiness draft plan](../../04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md)
- **Umbrella lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
- **Compose audit**: [Compose, infrastructure, and operations readiness](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md)
- **Research**: [Compose and infrastructure research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md)
- **Infrastructure dependency**: [Spec 125](../125-infrastructure-operations-readiness-remediation/spec.md)
- **Security dependency**: [Spec 126](../126-security-supply-chain-remediation/spec.md)
- **Deployment dependency**: [Spec 127](../127-deployment-release-engineering-remediation/spec.md)
