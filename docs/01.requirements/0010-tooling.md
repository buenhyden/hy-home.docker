---
title: "Platform Operations and Software Verification Requirements"
version: "2.3.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "requirements"
artifact_id: "REQ-0010"
created: "2026-03-26"
---

# Platform Operations and Software Verification Requirements

## Overview

### Problem and Outcome

Manual infrastructure changes are hard to track, and fragmented code quality
and performance checks leave the platform's stability unverified. This package
states the tooling needs of two capability tiers: platform operations
(infrastructure as code, a private image registry, dependency updates and
backup) and software verification (static analysis, load testing, API mocking,
contract testing and policy checks; the SMTP sandbox is REQ-0011's). The goal is a supporting
toolset that removes manual work and gives data for engineering decisions.

### Stakeholders

- **DevOps engineer**: manages infrastructure consistently through IaC and has
  every infrastructure plan reviewed before it is applied (Terrakube).
- **Developer**: sees bugs, vulnerabilities and code smells for each change
  (SonarQube) and shares images through the internal registry.
- **QA or performance engineer**: runs load scenarios with k6 to find
  bottlenecks, and uses Locust only for comparison runs.

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

- Infrastructure automation and its orchestration, the private
  image registry, static code analysis, load testing, and the shared
  verification tools of the quality tier.

### Constraints and Exclusions

- **Out of scope**: servers that run business logic; service monitoring and
  logging, owned by the observability tier; mail capture requirements, owned by
  REQ-0011.
- **Non-goals**: general-purpose public cloud services.
- The file synchronization obligation of former REQ-0010-FR-0005 was withdrawn on
  2026-09-19 with the Syncthing runtime. It is not reallocated, and number 5
  stays reserved in the Registry `reserved_history`.

**Assumptions.**

- Infrastructure orchestration and static analysis use the shared management
  database and the shared authentication boundary.
- Static analysis and the alternative load tool are optional experiment
  capabilities outside the always-on HOME set; no LAB is promoted until the
  owner decides it.
- The acceptance criteria are verification targets, not evidence that they are
  met on the current host.

**Risks.**

- An orchestration API failure blocks infrastructure changes.
- The registry and the infrastructure-as-code helper keep state on the single
  host; preserving that host's storage alone is not backup or host-failure
  recovery.

## Requirements

### Functional Requirements

- **REQ-0010-FR-0001**: Provide an infrastructure-as-code command-line helper
  for execution and state management, plus a centralized orchestration service
  (Terrakube) whose browser and API routes require the shared SSO.
- **REQ-0010-FR-0002**: Provide multi-language static code analysis with quality
  gate enforcement (SonarQube) as an optional, isolated experiment capability.
  It reaches the shared management database only through an endpoint the
  operator approves, and is reachable only on the LAB host address
  (loopback by default) until promoted.
- **REQ-0010-FR-0003**: Provide k6 as the default load tool. Locust is an
  optional, isolated experiment capability for Python or protocol comparisons,
  not part of the always-on HOME set.
- **REQ-0010-FR-0004**: Provide a single-node private image registry for
  internal service deployment, reachable only from the local host.
- **REQ-0010-FR-0006**: Propose dependency and image updates automatically for
  review, and take scheduled encrypted backups with both a local and an
  offsite copy.
- **REQ-0010-FR-0007**: Provide shared verification tools: API mocking,
  consumer contract testing through a contract broker, and policy checks over
  tracked configuration.

## Acceptance Criteria

### Acceptance Conditions

- **REQ-0010-FR-0001**: Every tracked infrastructure change is applied through
  the IaC helper or the orchestration service, and an unauthenticated request
  to an orchestration route is redirected to SSO.
- **REQ-0010-FR-0002**: The static analysis capability renders on its own,
  selects no always-on HOME service, refuses to start without an approved
  database endpoint, and publishes nothing beyond the LAB host address
  (loopback by default).
- **REQ-0010-FR-0003**: The default load tool reports its pinned version from
  the root composition, and the alternative load tool renders only outside it.
- **REQ-0010-FR-0004**: The registry accepts a push and pull from the local host
  and publishes no port on a non-loopback address.
- **REQ-0010-FR-0006**: The update tool opens reviewable change requests and
  applies nothing itself, and a backup run leaves an encrypted snapshot in the
  local and the offsite repository.
- **REQ-0010-FR-0007**: The mock server, the contract broker and the policy
  checker each render in the quality tier, and the policy check runs as a
  registered CI gate.

### Verification Method

Render and policy conditions (REQ-0010-FR-0003, REQ-0010-FR-0007 and the port bindings in REQ-0010-FR-0002 and REQ-0010-FR-0004) are judged by reviewing the rendered root composition, the isolated LAB compositions and the registered CI policy gate. Behavior conditions need runtime observations: the SSO redirect of REQ-0010-FR-0001, the refusal to start without an approved database endpoint in REQ-0010-FR-0002, the registry push and pull in REQ-0010-FR-0004, and the encrypted local and offsite snapshot in REQ-0010-FR-0006. The criteria are verification targets, not evidence that they are met on the current host. SPEC-0262 cites REQ-0010, and its Task evidence rows record the results it produces; a later Spec records any runtime observation it makes in its own Task. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence and accepts the requirement once every condition is judged met.

## Traceability

### Source and Constraints

This package records the owner's requirements for the tooling tier; no upstream
document governs it.

### Downstream Links

- **Architecture Description**: [0009-tooling-architecture.md](../02.architecture/descriptions/0009-tooling-architecture.md)
- **Spec**: [SPEC-0262 LAB migration](../03.specs/0262-analytics-labs-migration/spec.md)
  and [SPEC-0263 LAB promotion contract](../03.specs/0263-lab-promotion-contract/spec.md)
- **ADR**: [ADR-0062 HOME Membership and Planned LABs](../02.architecture/decisions/0062-home-lab-membership.md)
- **Retired domain Spec SPEC-0010** (tooling): replaced by the tooling guides,
  policies and runbooks in the operations catalog under `docs/05.operations/`.
- **Retired requirement REQ-0021** (tooling optimization hardening): retired
  under SPEC-0169 because every clause named an implementation artifact; its
  contract lives in the tooling operations policy, and its documentation
  traceability clause moved to REQ-0026-FR-0011.
- **Retired Terraform operations documents**: retired when OpenTofu became the
  infrastructure-as-code tool.
