---
title: "Tooling Services Selection and Configuration"
version: "2.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0009"
parent_ids:
- "AD-0009"
created: "2026-03-26"
---
# ADR-0009: Tooling Services Selection and Configuration

## Context

This document is the ADR that tracks the background, choices, and outcomes of this architecture decision. The 2026-09-19 correction reflects the removed Syncthing obligation and the current OpenTofu execution owner; the original decision is preserved in Git history.

The `09-tooling` layer includes auxiliary tools for maximizing development and operational efficiency. Proven open-source solutions must be selected and integrated to satisfy various needs such as infrastructure automation (IaC), code quality analysis, performance testing, and internal image storage.

## Decision

The following service stack is selected as the standard tooling for `09-tooling`.

1. **IaC Automation**: **OpenTofu / Terrakube**
   - Reason: the current CLI helper is OpenTofu, and Terrakube manages workspace state and execution. The existing Terraform workspace state/provider contract is reviewed in the migration handoff.
2. **Code Quality**: **SonarQube**
   - Reason: multi-language support and precise static analysis capability let it centrally manage the project's overall code quality and security vulnerabilities.
3. **Performance Testing**: **Locust**
   - Reason: Python-based scenario definitions make it easy to extend, and a distributed architecture can generate large-scale load.
4. **OCI Registry**: **OCI Distribution Registry**
   - Reason: provides a lightweight private image store for internal service deployment.
5. **Withdrawn selection**: the Syncthing runtime and its file-synchronization obligation have been removed. This item is a record of the withdrawal of a past selection, not a requirement replaced by a current service or another feature.

### Rationale

- **Integration**: the SonarQube/Terrakube admin UI uses the declared gateway+SSO boundary. It does not assume the same browser SSO boundary applies to CLI operations, the load generator, and the registry protocol.
- **Persistence**: IaC state information and analysis data are kept in the declared backend. Single-host persistence is not an independent backup, and it does not guarantee data-loss prevention or recovery success without verified backup/recovery evidence.
- **Standardization**: each service is deployed consistently through Docker Compose and predefined environment variables.

### Decision Record

Accepted (2026-03-26). Amended on 2026-09-19 to withdraw Syncthing and align the CLI helper with OpenTofu; no runtime deployment or recovery success is asserted.

## Consequences

- **Positive**:
  - Infrastructure change history is managed transparently.
  - Code quality gates block deployment of defective code beforehand.
  - Performance bottlenecks can be identified with data.
- **Negative**:
  - Maintenance resource (memory, CPU) usage increases from operating various tools.
  - Complex network permission configuration between tools is required.

### Explicit Non-goals

- This ADR does not change runtime behavior.
- This ADR does not rewrite historical decision evidence.
- Implementation details remain in linked specs, plans, and tasks.

## Options Considered

Existing alternatives, rationale, or rejected options in this ADR remain the alternative analysis. This alignment section does not add new alternatives.

## Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- [Tooling PRD](../../01.requirements/0010-tooling.md)
- [Tooling Architecture Description](../descriptions/0009-tooling-architecture.md)
- [Current convergence Spec](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md)
- [OpenTofu operations](../../05.operations/guides/0082-opentofu.md)
- [Terraform migration handoff](../../05.operations/guides/0068-terraform.md)
