---
title: "HashiCorp Vault as Centralized Secrets Manager"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0003"
parent_ids:
- "AD-0003"
created: "2026-03-26"
---
# ADR-0003: HashiCorp Vault as Centralized Secrets Manager

## Context

A dedicated secrets management solution is needed to manage sensitive information (passwords, API keys, certificates, etc.) across the platform. As the decision, HashiCorp Vault is adopted, and this document records the concrete reasons and alternatives.

- Existing hardcoded configuration or `.env` file approaches have high security vulnerability and risk exposing secrets.
- Docker Secrets has limited functionality, and complex secret rotation or fine-grained access control (ACL) is difficult.
- In a cloud-native environment, dynamic secret injection is required based on trust relationships between services.

### Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision

**HashiCorp Vault** is adopted as the platform's standard secrets management tool.

1. **Raft Storage**: operates integrated storage without an external DB; currently a single node, with HA expansion possible in the future through an approved procedure.
2. **AppRole Mechanism**: provides an authentication method optimized for container-based services.
3. **Template Support**: smooth integration with existing applications via Vault Agent.
4. **Encryption-as-a-Service**: can provide a data encryption API beyond simple storage.

### Decision Record

- **Proposed**: 2026-03-26
- **Accepted**: 2026-03-26

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

1. **Docker Secrets**: simple to use, but lacks functionality and has low flexibility.
2. **SOPS**: good for file-based encryption, but dynamic injection and API-based management are difficult.
3. **AWS/GCP Secrets Manager**: creates cloud dependency, with cost and availability issues in an on-premises/Docker environment.

## Consequences

### Positive

- Centralizes and encrypts all secret information at storage.
- Strengthens compliance through detailed audit logs.
- Allows infrastructure code to be safely stored in a shared repository without exposing secrets.

### Negative

- Increased operational complexity, such as the Vault server's initial unseal.
- A Vault server failure can become a single point of failure for the whole service, so an HA configuration is essential.

### Explicit Non-goals

- This ADR does not change runtime behavior.
- This ADR does not rewrite historical decision evidence.
- Implementation details remain in linked specs, plans, and tasks.

## Related Documents

- [Security PRD](../../01.requirements/0003-security.md)
- [Security Architecture Description](../descriptions/0003-security-architecture.md)
- [Security spec](../descriptions/0003-security-architecture.md)
- Security standardization plan
