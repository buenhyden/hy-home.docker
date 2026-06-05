---
status: draft
---
<!-- Target: docs/03.specs/<feature-id>/spec.md -->

# [Feature Name] Technical Specification (Spec)

> Use this template for `docs/03.specs/<feature-id>/spec.md`.
>
> Rules:
>
> - Every active spec must declare PRD and ARD references or make the absence explicit.
> - Verification is mandatory.
> - If this feature exposes an external API, link a dedicated API Spec.
> - Write this document in English. Preserve code identifiers, command names,
>   service names, environment variables, and quoted upstream terms exactly.
> - Keep one `Overview` summary near the top.
> - This document is the parent design doc; API contracts live in `api-spec.md` under the same feature directory.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.
> - Replace example links with real target-relative links, or delete unused examples before saving.
>
> Target-relative examples from `docs/03.specs/<feature-id>/spec.md`:
>
> - PRD: `../../01.requirements/YYYY-MM-DD-feature-or-system.md`
> - ARD: `../../02.architecture/requirements/####-system-or-domain-name.md`
> - ADR: `../../02.architecture/decisions/####-short-title.md`
> - Plan: `../../04.execution/plans/YYYY-MM-DD-feature.md`
> - Task: `../../04.execution/tasks/YYYY-MM-DD-feature-or-stream.md`
> - Same-directory API Spec: `./api-spec.md`
> - Operations direct target: `../../05.operations/guides/topic.md`
> - Operations domain target: `../../05.operations/guides/domain/topic.md`
> - Operations nested target: `../../05.operations/guides/domain/subdomain/topic.md`

---

## Overview

This document defines the technical design and implementation contract for
[feature name]. It turns PRD requirements into implementation-ready contracts
and verification criteria.

## Strategic Boundaries & Non-goals

[What this spec owns, and what it does not.]

## Related Inputs

- **PRD**: [../../01.requirements/YYYY-MM-DD-<feature-or-system>.md](../../01.requirements/YYYY-MM-DD-<feature-or-system>.md)
- **ARD**: [../../02.architecture/requirements/####-<system-or-domain-name>.md](../../02.architecture/requirements/####-<system-or-domain-name>.md)
- **Related ADRs**: [../../02.architecture/decisions/####-<short-title>.md](../../02.architecture/decisions/####-<short-title>.md)

## Contracts

- **Config Contract**:
- **Data / Interface Contract**:
- **Governance Contract**:

## Core Design

- **Component Boundary**:
- **Key Dependencies**:
- **Tech Stack**:

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
- **Migration / Transition Plan**:

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface ExampleContract {
  id: string;
  name: string;
}
```

## API Contract (If Applicable)

Contract-first rule: if this feature exposes an external API, define the
detailed API contract in a dedicated API Spec document.

- **API Spec**: [./api-spec.md](./api-spec.md)
- **Policy**: Keep the API Spec under the current feature directory, not under a
  separate top-level path such as `docs/api/`.
- **Machine-readable Contract**:
  - `./contracts/openapi.yaml`
  - `./contracts/service.proto`
  - `./contracts/schema.graphql`

## Agent Role & IO Contract (If Applicable)

- **Agent Role**:
- **Inputs**:
- **Outputs**:
- **Success Definition**:

## Tools & Tool Contract (If Applicable)

- **Tool List**:
- **Permission Boundary**:
- **Failure Handling**:

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**:
- **Policy Constraints**:
- **Versioning Rule**:

## Memory & Context Strategy (If Applicable)

- **Short-term Context**:
- **Long-term Memory**:
- **Retrieval Boundary**:

## Guardrails (If Applicable)

- **Input Guardrails**:
- **Output Guardrails**:
- **Blocked Conditions**:
- **Escalation Rule**:

## Evaluation (If Applicable)

- **Eval Types**:
- **Metrics**:
- **Datasets / Fixtures**:
- **How to Run**:

## Edge Cases & Error Handling

- **Error 1**:
- **Error 2**:

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**:
- **Fallback**:
- **Human Escalation**:

## Verification

List the commands, manual checks, or evidence capture steps. This section answers "how to run the checks."

```bash
[command 1]
[command 2]
pytest tests/[feature]_test.py
python evals/run_[feature]_eval.py
```

## Success Criteria & Verification Plan

Define what each verification step proves. This section answers "what must be true for the spec to be accepted."

- **VAL-SPC-001**:
- **VAL-SPC-002**:

## Related Documents

- **Plan**: [../../04.execution/plans/YYYY-MM-DD-<feature>.md](../../04.execution/plans/YYYY-MM-DD-<feature>.md)
- **Tasks**: [../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md](../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md)
- **Guide, direct operations target**: [../../05.operations/guides/<topic>.md](../../05.operations/guides/<topic>.md)
- **Guide, domain operations target**: [../../05.operations/guides/<domain>/<topic>.md](../../05.operations/guides/<domain>/<topic>.md)
- **Policy, direct operations target**: [../../05.operations/policies/<topic>.md](../../05.operations/policies/<topic>.md)
- **Policy, domain operations target**: [../../05.operations/policies/<domain>/<topic>.md](../../05.operations/policies/<domain>/<topic>.md)
- **Runbook, direct operations target**: [../../05.operations/runbooks/<topic>.md](../../05.operations/runbooks/<topic>.md)
- **Runbook, domain operations target**: [../../05.operations/runbooks/<domain>/<topic>.md](../../05.operations/runbooks/<domain>/<topic>.md)
- **Runbook, nested operations target**: [../../05.operations/runbooks/<domain>/<subdomain>/<topic>.md](../../05.operations/runbooks/<domain>/<subdomain>/<topic>.md)
