---
status: completed
artifact_id: spec:124-compose-runtime-readiness-remediation
artifact_type: spec
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:123-agentic-engineering-audit-remediation
---

# Compose Runtime Readiness Remediation Technical Specification (Spec)

## Overview

This active specification defines the contract for proving that the exact
`core` five-service Compose set can start, become ready, recover from approved
failure scenarios, and tear down without unapproved data or secret exposure.
It owns three canonical audit gaps. PRD 025, ARD 0028, and ADR 0028 approve the
local-isolated architecture; the linked Plan and Task own command authorization
and observed evidence. Broader or remote execution requires a new Task.

## Strategic Boundaries & Non-goals

- Own startup, observed readiness, bounded failure recovery, teardown, and the
  evidence envelope for a later runtime task.
- Do not own upgrade, migration, backup, or restore contracts; Spec 125 owns
  those stateful operations.
- Do not own supply-chain verification or promotion; Specs 126 and 127 own
  those decisions.
- Do not infer runtime health from Compose rendering, healthcheck YAML, or
  documentation presence.
- Do not expand beyond the `core` profile services `keycloak`, `oauth2-proxy`,
  `traefik`, `vault`, and `vault-agent` without a new architecture decision and
  task approval.

## Boundaries and Inputs

- **PRD**: [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
  defines the bounded local value, exact representative scope, and acceptance
  intent.
- **ARD**: [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
  defines the isolated topology, evidence boundary, and cleanup guarantees.
- **ADR**: [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
  selects contract-first local-isolated vertical slices.
- **Audit lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
  remains the canonical audit lineage.

Architecture-changing runtime harness, topology, network, volume, healthcheck,
or initialization changes remain blocked until the Plan identifies the exact
test-only change and the active Task records protected-surface approval.

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

- The approved Plan and active Task must name exact Compose files, profiles, services,
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

This Spec defines the readiness contract; it does not own observed execution
evidence or lifecycle conclusions. Observed evidence and current status are
owned by the exact [domain Task](../../04.execution/tasks/2026-07-19-compose-runtime-readiness-remediation.md)
and [Program Task](../../04.execution/tasks/2026-07-19-operational-readiness-closure-program.md).

## Core Design

- **Component Boundary**: A task-scoped Compose runtime evidence harness using a
  unique project identity, synthetic configuration, explicit timeouts, owned
  resources, and deterministic teardown.
- **Key Dependencies and Consumers**: The tracked Compose source, ARD 0028,
  and ADR 0028 define the input boundary. Spec 125 consumes the recovery
  boundary and Spec 127 consumes the readiness verdict; neither is a prerequisite
  for the first bounded `core` rehearsal.
- **Tech Stack**: Docker Compose v2, repository validation scripts, service
  healthchecks, bounded endpoint probes, and shell wrappers with strict mode
  and trap-based cleanup. Exact commands belong in the approved Plan and Task.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Store concise, redacted task evidence with one
  record per approved scenario and service acceptance set. Keep raw runtime
  diagnostics outside tracked documentation and handle them under the future
  task's approved evidence boundary.
- **Migration / Transition Plan**: Approved Stage 04 Plan/Task -> isolated
  rehearsal -> independent review -> evidence and honest lifecycle
  reconciliation. Existing Compose defaults remain unchanged unless the Task
  explicitly approves a test-only overlay.

## Interfaces and Data

### Core Interfaces

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Approved runtime scope | Human/architecture approval | Future runtime task | Exact target, files, profiles, services, duration, and teardown. |
| Readiness result | Approved observation mechanism | QA/SRE review | Service criteria plus ready/degraded/failed/timed-out result. |
| Recovery result | Approved scenario executor | Operations/security review | Scenario, data impact, recovery time, stop/escalation, and cleanup. |
| Stateful recovery handoff | This workstream | Spec 125 implementation | Stop and hand off when a scenario crosses from service recovery into data restore. |

## API Contract (If Applicable)

Not applicable. This specification defines runtime evidence and approval contracts and
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

- **Tool List**: Docker Compose v2 plus repository-owned preflight, observation,
  timeout, evidence-summary, and cleanup wrappers defined by the future Plan.
- **Permission Boundary**: This active Spec approves the local-isolated design,
  not command execution. The active Task must authorize exact files, services,
  projects, resources, and commands.
- **Failure Handling**: Stop on scope drift, secret exposure, target ambiguity,
  resource exhaustion, state corruption, or teardown failure.

## Prompt / Policy Contract (If Applicable)

- Instructions must repeat the exact approved target/profile/service set and
  prohibited surfaces.
- No agent may infer runtime approval from Spec 123, this specification, or a static
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

| Gate | Remaining approval required before execution | Evidence required |
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

Runtime commands are intentionally absent from the Spec. The active Plan and
Task define them and include timeout, unhealthy dependency,
recovery, and cleanup negative paths.

## Success Criteria & Verification Plan

- **VAL-CRR-001**: The three owned audit gaps appear exactly once across Specs
  124-127 and map to `CRR-001` through `CRR-003`.
- **VAL-CRR-002**: Static evidence remains labeled static and distinct from
  Task-owned observed runtime evidence.
- **VAL-CRR-003**: Every future scenario has approved scope, readiness criteria,
  teardown, redaction, recovery, and independent review evidence.
- **VAL-CRR-004**: Architecture, human, runtime, secret, and remote gates are
  resolved before any service command.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Plan**: [Compose runtime-readiness plan](../../04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md)
- **Task**: [Compose runtime-readiness Task](../../04.execution/tasks/2026-07-19-compose-runtime-readiness-remediation.md)
- **Umbrella lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
- **Compose audit**: [Compose, infrastructure, and operations readiness](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md)
- **Research**: [Compose and infrastructure research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md)
- **Infrastructure dependency**: [Spec 125](../125-infrastructure-operations-readiness-remediation/spec.md)
- **Security dependency**: [Spec 126](../126-security-supply-chain-remediation/spec.md)
- **Deployment dependency**: [Spec 127](../127-deployment-release-engineering-remediation/spec.md)
