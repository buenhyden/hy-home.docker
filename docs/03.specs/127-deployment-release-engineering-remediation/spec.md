---
status: completed
artifact_id: spec:127-deployment-release-engineering-remediation
artifact_type: spec
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:123-agentic-engineering-audit-remediation
  - spec:124-compose-runtime-readiness-remediation
  - spec:125-infrastructure-operations-readiness-remediation
  - spec:126-security-supply-chain-remediation
---

# Deployment and Release Engineering Remediation Technical Specification (Spec)

## Overview

This active specification defines the bounded local contract for sample-service
baseline/canary environments, verified-digest promotion, health evidence, and
rollback. It owns five canonical audit gaps. The local design does not authorize
CI/CD workflow mutation, GitHub Environments/Releases, artifact publication,
remote deployment, secret access, or a real Release event.

## Strategic Boundaries & Non-goals

- Own CD environment/promotion/deployment/release and config/application
  rollback contracts distinct from CI quality.
- Consume verified artifact verdicts from Spec 126, readiness from Spec 124,
  and data recovery from Spec 125 without duplicating those requirements.
- Do not claim a release from a tag-string changelog check or deployment from a
  successful build.
- Do not infer production deployment or release readiness from the local
  baseline/canary rehearsal.

## Boundaries and Inputs

- **PRD**: [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
  defines local promotion/rollback value and remote non-goals.
- **ARD**: [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
  defines separate baseline/canary projects and upstream verdict boundaries.
- **ADR**: [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
  selects verified-artifact local canary, promotion, and previous-identity rollback.
- **Audit lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
  remains the canonical audit lineage.
- **Direct dependencies**: [Spec 124](../124-compose-runtime-readiness-remediation/spec.md),
  [Spec 125](../125-infrastructure-operations-readiness-remediation/spec.md), and
  [Spec 126](../126-security-supply-chain-remediation/spec.md) own readiness,
  recovery, and supply-chain verdicts.

Architecture-changing workflow, environment, target, identity, artifact,
network, promotion, or rollback work remains blocked until the approved Plan
and active Task identify the exact local surface and rollback.

## Canonical Gap Ownership

| Audit gap | Disposition | Requirement owner | Reason |
| --- | --- | --- | --- |
| `QAF-01`–`QAF-09`, `QAF-11` | Not routed: implemented/non-runtime QA | Existing QA/project owners | These are quality inputs, not CD runtime gaps. |
| `QAF-12` | Not routed: Task 9 ownership | Controlled agent pre-commit wrapper | Task 9 implemented and reviewed this boundary. |
| `QAF-13` | Not routed: implemented/Task 10 CI stewardship | Existing CI/governance owners | Task 10 updated the existing CI job; CI definition is not CD. |
| `QAF-14` | Not routed: remote revalidation | GitHub governance owner | Requires separately approved timestamped remote evidence. |
| `QAF-15` | Owned | `DRE-001` | Environment promotion, approval, deployment, and rollback as CD. |
| `QAF-16` | Owned | `DRE-002` | Actual release iteration record and outcome. |
| `AUT-01`–`AUT-02`, `AUT-04`–`AUT-08` | Not routed: implemented/non-runtime automation | Existing script/generator/eval owners | Local/advisory/generator automation remains outside CD ownership. |
| `AUT-03` | Not routed: implemented/Task 10 ownership | Provider synchronization owner | Task 10 synchronized provider surfaces; it is not deployment automation. |
| `AUT-09` | Not routed: Task 9 ownership | Controlled agent pre-commit wrapper | Task 9 implemented and reviewed this boundary. |
| `AUT-10` | Owned | `DRE-003` | Approved environment/promotion/deployment/rollback automation. |
| `AUT-11` | Not routed: remote revalidation | GitHub governance owner | Current remote enforcement/run state was not queried. |
| `CIO-13` | Owned | `DRE-001` | Promote tested artifacts/configuration through explicit environments. |
| `CIO-14` | Owned | `DRE-004` | Execute/verify config and application rollback with a data-recovery handoff. |

Owned gap count: **5 audit IDs** mapped to four requirements because `QAF-15`
and `CIO-13` are two canonical audit views of the same promotion contract.
Every `QAF` and `AUT` ID is classified exactly once across Specs 126-127.

## Contracts

### Delivery Evidence Contract

| Requirement | Target behavior | Required evidence |
| --- | --- | --- |
| `DRE-001` | Promote an immutable tested artifact/configuration through explicit environments with separation of duties, approvals, security/readiness gates, and deployment history. | Artifact/config identity, source/target environment, approver, gate verdicts, deployment identity, timestamps, outcome, and history reference. |
| `DRE-002` | Record a release iteration with tag/version, changelog entry, immutable artifact/digest, approval, security evidence, publication/deployment outcome, and rollback disposition. | Release record ID, tag/version, changelog reference, artifact/digest, approval, verification verdict, environment/result, timestamps, and final status. |
| `DRE-003` | Automate only an approved promotion/deployment path that fails closed on required gates and preserves auditable evidence. | Pinned workflow/action definition, environment protections, least-privilege identity, test/canary result, gate failures, approval path, and rollback result. |
| `DRE-004` | Execute and verify config/application rollback with post-rollback health; hand irreversible data recovery to Spec 125. | Trigger, decision owner, prior artifact/config identity, steps, health/readiness result, data-impact classification, recovery handoff, and outcome. |

### Configuration Contract

- Future active work names exact environments, targets, immutable artifacts,
  workflow/actions, identities/permissions, approvals, health/security gates,
  release record, timeouts, and rollback/recovery.
- CI quality jobs remain independent inputs and are not renamed or counted as
  deployment evidence.
- Remote required checks, rulesets, environments, and Release settings require
  current separately approved evidence before design assumptions become active.

### Data / Interface Contract

Promotion and release records bind source revision, immutable artifact/config
identity, verifier verdicts, environment, approvals, timestamps, outcome, and
rollback. Tracked evidence contains no credential, secret, OIDC token, raw log,
private endpoint payload, or unrestricted artifact URL.

For the bounded local rehearsal, Spec 127 consumes only Spec 126 verdict schema
v2 and pair schema/generation v3. The consumer uses the pair-bound deterministic
`local_image_ref`, proves its local `.Id` equals `runtime_image_id` before every
start boundary, starts Compose with `pull_policy: never`, `--pull never`, and
`--no-build`, and proves the running container `.Image` still equals that ID.
The strict rehearsal record is schema v4 and carries both roles' full portable
identity tuples together with exact upstream handoff hashes.

### Governance Contract

- A future Stage 04 task must name exact workflow/runtime/remote/secret
  surfaces, approval source, validation, rollback/recovery, and redaction.
- Human environment approval and deployment identity are mandatory and cannot
  be inferred from local repository definitions.
- Remote mutation, paid service, credential change, environment creation, or
  deployment needs explicit external-action approval.

## Current Evidence

This Spec defines the delivery contract; it does not own observed execution
evidence or lifecycle conclusions. Observed evidence and current status are
owned by the exact [domain Task](../../04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md)
and [Program Task](../../04.execution/tasks/2026-07-19-operational-readiness-closure-program.md).

## Core Design

- **Component Boundary**: Separate local baseline and canary Compose projects
  for `examples/sample-web-service`, started only from pair-bound deterministic
  local references and promoted only after exact runtime-ID, health, and
  previous-artifact rollback checks.
- **Key Dependencies**: Spec 126 verdict schema v2 and pair schema/generation
  v3; Spec 124 readiness; Spec 125 data recovery and state-aware rollback.
- **Tech Stack**: Docker image/build, Docker Compose, repository-owned health
  and promotion wrappers, and Spec 126 verification verdicts. No remote
  environment, registry, Release, or workflow provider is selected.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: One release/deployment record keyed by release
  ID/tag plus immutable artifact digest, environment, approval, verifier
  verdict, outcome, and rollback status. Future Release artifact/profile must
  use the repository's typed lifecycle contract.
- **Migration / Transition Plan**: Document environments/artifacts -> approve
  architecture/ADRs -> local/sandbox fixture -> canary/non-production ->
  reviewed promotion -> separately approved broader rollout. Existing CI and
  manual readiness remain unchanged until gates pass.

## Interfaces and Data

### Core Interfaces

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Immutable artifact/config | Approved build/release flow | Promotion/deployment | Source revision plus OCI manifest/config/archive identity, deterministic Docker-load archive, local reference, and observed runtime image ID/kind. |
| Security verdict pair | Spec 126 implementation | Promotion gate | Verdict schema v2 and pair schema/generation v3, exact verdict hashes and full role tuples, accepted/no-exception/redaction status. |
| Runtime readiness | Spec 124 implementation | Deployment health gate | Scoped ready/degraded/failed result and teardown/recovery boundary. |
| Data recovery handoff | Spec 125 implementation | Rollback decision | Approved restore point, integrity criteria, and recovery owner. |

## API Contract (If Applicable)

Not applicable. Any future provider/GitHub/registry API contract is deferred
until remote surface selection and approval.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Future implementation by `ci-cd-engineer` and
  `infra-implementer`; independent review by release, security, operations, and
  QA owners.
- **Inputs**: Approved predecessors/task, environments, artifact/config,
  verifier/readiness verdicts, identity, approvals, rollback/recovery.
- **Outputs**: Redacted release/deployment/rollback evidence.
- **Success Definition**: Only approved immutable artifacts reach approved
  environments; required gates fail closed and rollback/recovery is verified.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Local Docker build/image inspection, Docker Compose baseline
  and canary projects, endpoint health probes, verified-digest promotion, and
  rollback wrappers defined by the approved Plan.
- **Permission Boundary**: Task-owned local resources only. Workflow, registry,
  GitHub Environment/Release, identity, publication, and remote deployment
  remain prohibited.
- **Failure Handling**: Stop promotion/deployment on gate, approval, identity,
  target, health, or rollback ambiguity.

## Prompt / Policy Contract (If Applicable)

Future instructions must name exact repository, revision, artifact/config,
environment/target, workflow/action, identity/permissions, approvals, gates,
rollback/recovery, and redaction. Neither Spec 123 nor CI success authorizes CD.

## Memory & Context Strategy (If Applicable)

Use canonical release/deployment/task evidence with identifiers and concise
outcomes. Never persist raw remote output, logs, tokens, credentials, secrets,
or environment dumps in tracked docs or memory.

## Guardrails (If Applicable)

- **Input Guardrails**: Verify repository/revision, immutable artifact/config,
  environment, target, approval, identity/permissions, security/readiness, and
  rollback/recovery before promotion.
- **Output Guardrails**: Redact secrets and raw runtime/remote outputs; retain
  concise identifiers and outcomes.
- **Blocked Conditions**: Missing predecessors, immutable artifact, environment,
  approval, trusted identity, verifier/readiness gate, rollback, or data
  recovery handoff.
- **Escalation Rule**: Stop and obtain new human/runtime/secret/remote approval
  whenever environment, target, identity, permissions, artifact, or risk changes.

## Approval Gates

| Gate | Remaining approval required before execution | Evidence required |
| --- | --- | --- |
| Architecture | Approved PRD/ARD/ADRs for environments, artifact flow, identity, promotion, health, release record, and rollback/recovery | Canonical IDs/paths and approval state. |
| Human | Release/environment/change owners approve target, artifact, gates, window, rollback, and residual risk | Approval reference and named decision/recovery owners. |
| Runtime | Exact deployment target, commands/actions, canary/window, health, teardown/rollback, and recovery | Future Stage 04 task with before/after evidence plan. |
| Secret | Exact deployment/signing/OIDC/registry IDs/claims/paths and permitted metadata; no values | Identity/secret threat boundary, redaction, rotation/revocation, and reviewer. |
| Remote | Workflow, GitHub Environment/Release, registry, target, ruleset, or deployment query/mutation requires separate approval | Repository/target identity, permissions, command/action class, before/after evidence, rollback. |

## Edge Cases & Error Handling

- Build succeeds but verifier fails: do not promote.
- The bound local reference is missing, retargeted, built, pulled, or resolves
  to another runtime ID/role: fail before or during the affected start boundary.
- Environment approval is stale or for another artifact: do not deploy.
- Deployment health fails after partial rollout: stop expansion and use only
  approved rollback/recovery.
- Config/application rollback cannot reverse data migration: hand off to Spec
  125; do not claim full rollback.
- Release record exists without artifact/outcome evidence: mark incomplete.

## Failure Modes and Guardrails

- **Failure Mode**: Gate, approval, identity, target, deployment, record,
  health, rollback, or recovery failure.
- **Fallback**: Stop promotion, preserve redacted evidence, keep/restore the
  last approved artifact/config through the approved mechanism, and isolate
  uncertain data state.
- **Human Escalation**: Release/environment/security/operations owners decide
  rollback, data recovery, exception, redesign, or abandonment.

## Migration, Rollback, and Recovery

- Begin with a non-production/sandbox path and immutable test artifact, then a
  separately approved canary before broader promotion.
- Preserve current CI jobs and manual release readiness while the new delivery
  flow is advisory or incomplete.
- Roll back workflow/config changes by reviewed commit; roll back deployed
  application/config by previous immutable identity and verified health.
- Treat data recovery as Spec 125-owned and security identity revocation as
  Spec 126/security-owned dependencies.

## Verification

Documentation-phase checks:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 4937ae999825391963149cb285c686808dbb394b
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

No local delivery command is authorized until the Plan and active Task name the
exact artifact digest, projects, ports, gates, health criteria, failure
injection, cleanup, and rollback. Remote delivery commands remain out of scope.

## Success Criteria & Verification Plan

- **VAL-DRE-001**: Five owned audit IDs map exactly once to `DRE-001`–`DRE-004`.
- **VAL-DRE-002**: CI, build, release readiness, release record, deployment,
  promotion, and rollback evidence remain distinct.
- **VAL-DRE-003**: Security/readiness/data recovery inputs are dependencies and
  are not duplicated as requirements.
- **VAL-DRE-004**: Architecture, human, runtime, secret, and remote gates are
  resolved before any delivery action.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Plan**: [Deployment/release draft plan](../../04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md)
- **Task**: [Delivery rehearsal Task](../../04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md)
- **Umbrella lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
- **Quality audit**: [SDLC quality and formatting](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md)
- **Automation audit**: [Automation candidates](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- **Compose audit**: [Compose, infrastructure, and operations readiness](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md)
- **Research**: [Automation/pipeline/workflow research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md), [security research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md)
- **Runtime dependency**: [Spec 124](../124-compose-runtime-readiness-remediation/spec.md)
- **Recovery dependency**: [Spec 125](../125-infrastructure-operations-readiness-remediation/spec.md)
- **Security dependency**: [Spec 126](../126-security-supply-chain-remediation/spec.md)
