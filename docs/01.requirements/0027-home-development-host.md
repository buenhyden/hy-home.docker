---
title: "Home and Development Host Requirements"
version: "1.1.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "requirements"
artifact_id: "REQ-0027"
created: "2026-09-19"
---

# Home and Development Host Requirements

## Overview

### Problem and Outcome

Operate real HOME services and development work on a single Linux host.
Remove inconsistencies in implementation, operations documentation,
configuration, and version-update rules so one operator can explain each
service's necessity, access path, status, and recovery method. This
requirement records the full audit/redesign scope the user requested.
Authoring documents and implementation does not imply approval to deploy real
services or change data.

### Stakeholders

- A HOME user must be able to use the access/authentication foundation and
  AI/workflow features at all times.
- A developer must be able to select the development/experiment features
  they need and know the impact on HOME availability.
- An operator must align configuration without exposing values and verify
  state and recoverability before and after a change.

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

This package covers real HOME services and development work on a single Linux host, including the full audit and redesign scope the user requested, as stated in the Overview.

### Constraints and Exclusions

Targets a single physical host with real operational data. Multiple
containers or profiles on the same host do not provide physical failure
isolation. Secret rotation, destructive data operations, reboots, and
running-service changes follow a separate approval scope. Frozen historical
documents and the meaning of issued identifiers are preserved.

**Risks.**

Failures and resource contention on shared host, storage, and GPU affect
multiple HOME features. The user's requirement for always-on availability is
not a verification result that all concurrent workloads are possible on the
current hardware, so real resource measurement and recovery rehearsal are
needed.

## Requirements

### Functional Requirements

- **REQ-0027-FR-0001**: Every current service must be classified as HOME,
  DEV, OPTIONAL, LAB, REMOVE, or MIGRATE, describing its consumers, data,
  resources, and reason for retention.
- **REQ-0027-FR-0002**: HOME must provide AI/workflow and required dependent
  features at all times, while development, experimentation, and update work
  must be explicitly opted in.
- **REQ-0027-FR-0003**: The service selection vocabulary and dependency
  relationships must match the actual running configuration and describe
  mutually exclusive combinations and side effects.
- **REQ-0027-FR-0004**: Each retained service must have documentation for
  implementation discovery, normal use, operating rules, and failure
  recovery.
- **REQ-0027-FR-0005**: Public configuration and secret metadata must
  correspond to current consumers, and local sync must preserve existing
  values and unknown user entries.
- **REQ-0027-FR-0006**: The implementation declaration owns the exact
  running version, and each dependency area must have only one owner for
  update proposals.
- **REQ-0027-FR-0007**: Before deployment, present the concrete target,
  preconditions, verification, and recovery procedure, and execute only
  approved changes.
- **REQ-0027-FR-0008**: Approved execution verification must separate
  startup, status, authentication, persistence, resource, backup, and
  recovery results into actual evidence versus unverified items.
- **REQ-0027-FR-0009**: The optional `experience` profile must serve shared
  Storybook documentation and a read-only docs MCP only to authenticated
  administrators, both built from one source commit, and must stay outside
  the default HOME selection.

### Quality Requirements

- **REQ-0027-NFR-0001 — Confidentiality**: Passwords, tokens, keys, and
  local secret values must not appear in output, reports, model context, or
  version control; measure: scans of tracked files and reports find no secret value.
- **REQ-0027-NFR-0002 — Recoverability**: Distinguish configuration restore
  from data restore, and do not claim recoverability from an unverified
  backup; measure: each recoverability claim cites a verified restore.
- **REQ-0027-NFR-0003 — Maintainability**: Documentation must not duplicate
  ownership of the implementation's exact patch version, and any needed
  exception must state its reason and basis; measure: each exact version has one owning declaration.
- **REQ-0027-NFR-0004 — Verifiability**: Verification must run against the
  latest main, and unexecuted, failed, or blocked results must not be
  recorded as success; measure: every non-PASS result is recorded as such.

## Acceptance Criteria

### Acceptance Conditions

- **REQ-0027-FR-0001**: The classification of every service, with its
  consumers, data, resources and retention reason, can be confirmed in code and
  documentation.
- **REQ-0027-FR-0002**: HOME's required features and dependencies can be
  confirmed in code and documentation, and development, experimentation and
  update work start only when explicitly selected.
- **REQ-0027-FR-0003**: Missing entries and conflicts in the profile vocabulary
  and dependencies against the running configuration are checked automatically,
  and actual results are recorded.
- **REQ-0027-FR-0004**: Current documents for each retained service link to the
  implementation and authoritative basis and provide the required operations
  and recovery procedures.
- **REQ-0027-FR-0005**: Missing entries and conflicts in configuration and
  secret metadata are checked automatically with actual results recorded, and
  local sync is verified to preserve existing values and unknown user entries.
- **REQ-0027-FR-0006**: Missing entries and conflicts in version ownership are
  checked automatically with actual results recorded, and each dependency area
  has one update-proposal owner.
- **REQ-0027-FR-0007**: Deployment executes only after concrete approval of a
  presented target, preconditions, verification and recovery procedure.
- **REQ-0027-FR-0008**: A reviewable change history, verification results,
  residual risk and incomplete execution verification are provided, with
  startup, status, authentication, persistence, resource, backup and recovery
  results each marked verified or unverified.
- **REQ-0027-FR-0009**: The `experience` profile is outside the default HOME
  selection, its Storybook documentation and docs MCP reach only authenticated
  administrators, and both are built from one source commit.
- **REQ-0027-NFR-0001**: Scans of tracked files and reports find no secret
  value, and local sync verifies exposure prevention.
- **REQ-0027-NFR-0002**: Each recoverability claim cites a verified restore,
  with configuration restore and data restore reported separately.
- **REQ-0027-NFR-0003**: Each exact version has one owning declaration, and any
  exception states its reason and basis.
- **REQ-0027-NFR-0004**: Every non-PASS result is recorded as such, from a run
  against the latest main.

### Verification Method

Each condition is judged by running the checks against the latest main, with actual results recorded separately from unverified items and any non-PASS result recorded as such. The Spec Packages that list REQ-0027 as a parent, such as SPEC-0204, SPEC-0212 and SPEC-0218, record the results in their Task evidence rows. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

## Traceability

### Source and Constraints

No upstream policy or ADR is cited; the origin is the user's audit and redesign request stated in the Overview.

### Downstream Links

- [Home and Development Host Architecture](../02.architecture/descriptions/0031-home-development-host.md)
- [SPEC-0261 REQ-0027 Approval](../03.specs/0261-req-0027-approval/spec.md)
