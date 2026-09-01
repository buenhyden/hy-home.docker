---
status: active
---

# Audit Packages

## Overview

Point-in-time gap, implementation, and conformance assessments. Audit packages are evidence, not approval gates.

The Stage 90 authority boundary and package lifecycle rules are defined by the [References index](../README.md) and Stage 99 Registry.

SPEC-0158 retires this category. The current tree defines the Stage 90 package
set: a package exists because its README is present and satisfies its Stage 99
profile, and it is retired by deleting it in the same change that migrates its
needed meaning to a canonical owner, updates every inbound consumer, and
removes its row below. No archive ledger decides membership, so retiring a
package is no longer a Stage 99 amendment.

Stage 99 identity is still consumed once. A retired package's `AUD-` number is
never reissued, because `identity-history-regression` forbids it.

A cross-stage audit belongs in a Task under its governing Spec, where `task` is
a `package-member` profile and so allocates no global identity.

## Packages

| Stable ID | Package | Status |
| :--- | :--- | :--- |
| [AUD-0019](./0019-readme/README.md) | Reference: Agentic Engineering Implementation Audit References | active |
| [AUD-0020](./0020-agent-instructions-catalog-vibe-models/README.md) | Reference: Agent Instructions, Catalog, Vibe Coding, and Model Routing | active |
| [AUD-0021](./0021-automation-candidates/README.md) | Reference: Agentic Engineering Automation Candidates | active |
| [AUD-0022](./0022-compose-infrastructure-operations-readiness/README.md) | Reference: Compose, Infrastructure, and Operations Readiness | active |
| [AUD-0023](./0023-frontmatter-semantic-inventory/README.md) | Reference: Frontmatter Semantic Inventory | active |
| [AUD-0024](./0024-frontmatter-template-readme-implementation/README.md) | Reference: Frontmatter, Template, and README Implementation Audit | active |
| [AUD-0025](./0025-harness-engineering-implementation/README.md) | Reference: Harness Engineering Implementation | active |
| [AUD-0026](./0026-implementation-overview/README.md) | Reference: Agentic Engineering Implementation Overview | active |
| [AUD-0027](./0027-loop-engineering-implementation/README.md) | Reference: Loop Engineering Implementation | active |
| [AUD-0028](./0028-provider-harness-loop-implementation/README.md) | Reference: Provider Harness and Loop Implementation | active |
| [AUD-0029](./0029-sdlc-document-contracts-implementation/README.md) | Reference: SDLC and Document Contracts Implementation Audit | active |
| [AUD-0030](./0030-sdlc-quality-formatting-implementation/README.md) | Reference: SDLC Quality Formatting Implementation | active |
| [AUD-0031](./0031-security-framework-maturity/README.md) | Reference: Security Framework Maturity Coverage | active |
| [AUD-0032](./0032-workspace-rules-environment-implementation/README.md) | Reference: Workspace Rules and Environment Implementation | active |
| [AUD-0033](./0033-readme/README.md) | Reference: Agentic Engineering Implementation Audit Pack (2026-07-07 Update) | superseded |

## Canonical Current Audit

The [implementation audit index](0019-readme/README.md) routes the current
criterion reports and their [implementation overview](0026-implementation-overview/README.md).
These reports remain point-in-time evidence, not policy authority.

## Dated Historical Snapshots

The [superseded audit snapshot](0033-readme/README.md) retains its observation
date in metadata; current package paths remain date-free.

## Supersession Ledgers

The snapshot and current audit index record reciprocal stable-ID supersession.
[Migration 0003](../../98.archive/migrations/0003-workspace-governance-simplification.md)
records historical path recovery.

## Authoring

Create packages only under `audits/####-<slug>/` and use the matching Stage 99 template. Preserve observation dates, citations, provenance, and active-owner Traceability.

## Related Documents

- [References index](../README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
