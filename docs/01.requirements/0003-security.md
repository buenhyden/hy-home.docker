---
title: "Security Tier (03-security) Product Requirements"
version: "1.0.2"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0003"
created: "2026-03-26"
---
# Security Tier (03-security) Product Requirements

## Overview

### Overview

### Problem and Goals

The `03-security` tier serves as the "root of trust" of the hy-home.docker platform, centrally managing and encrypting sensitive data (passwords, API keys, certificates, and so on) through OpenBao. It builds a security scheme in which no service exposes secrets directly in source code or environment variables; instead, every service receives them dynamically injected or referenced through OpenBao.

### Problem Statement

When per-service secrets are scattered across files, environment variables, and manual procedures, exposure risk and audit gaps grow. `03-security` must integrate secret storage, access control, injection, and audit logging around OpenBao so that every service follows the same trust boundary.

## Requirements

### Requirements

### Functional Requirements

| ID    | Requirement           | Priority                                           |
| ----- | --------------------- | -------------------------------------------------- |
| REQ-0003-FR-0001 | Raft Storage          | Currently uses single-node Raft integrated storage, with HA expansion prepared as a separate transition procedure. |
| REQ-0003-FR-0002 | Forward Proxy Support | Expose the OpenBao UI/API externally through Traefik with SSL applied. |
| REQ-0003-FR-0003 | Unseal Protocols      | Manual unseal procedure and policy.                |
| REQ-0003-FR-0004 | Audit Logging         | Enable and retain audit logs for all requests.     |

### Non-functional Requirements

| ID     | Requirement  | Description                                                            |
| ------ | ------------ | ---------------------------------------------------------------------- |
| REQ-0003-NFR-0005 | Availability | Clearly detect the impact of a single-node OpenBao failure, and maintain the operational procedure for future Raft quorum expansion. |
| REQ-0003-NFR-0006 | Reliability  | Keep secret encryption algorithms current (AES-256-GCM).              |
| REQ-0003-NFR-0007 | Performance  | Minimize secret lookup latency (local API caching).                   |

### Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0003-FR-0001**: The current OpenBao/Agent compose and documentation are managed under the root `security`/`core` profile validation and hardening gate.
- **REQ-0003-FR-0002**: Service containers do not need to know secrets directly and start successfully after receiving them via the OpenBao Agent.
- **REQ-0003-FR-0003**: Audit log/remote audit enhancements are rolled out in stages after policy approval.

## Scope

### Scope

### Stakeholders and User Needs

- **Security**: Encrypted storage of all secrets and automated access control.
- **Transparency**: Audit logs that capture who accessed which secret and when.
- **Convenience**: Minimize application changes through a sidecar pattern using the OpenBao Agent.

### Personas

| Persona        | Role                              | Needs                                                                 |
| -------------- | --------------------------------- | --------------------------------------------------------------------- |
| Security Admin | Establishes and audits security policy | Fine-grained ACL policy configuration, unseal key management, audit log monitoring. |
| Infra Engineer | Operates and manages the platform | Maintain OpenBao server high availability (Raft) and assign per-service access permissions. |
| App Developer  | Develops and deploys services     | A mechanism to receive secrets dynamically injected from OpenBao instead of environment variables. |

### Key Use Cases

| ID    | Case              | Description                                                                     |
| ----- | ----------------- | ------------------------------------------------------------------------------- |
| UC-01 | Secret Storage    | Store per-service secrets securely using the KV (key-value) engine.             |
| UC-02 | Sidecar Injection | Inject secrets into configuration files via templates through the OpenBao Agent at container startup. |
| UC-03 | Dynamic Access    | Enforce per-application/per-user permission-based access control via AppRole or Userpass. |

### Constraints

- **In Scope**: OpenBao Server (Raft), OpenBao Agent, ACL policies, KV engine.
- **Out of Scope**: Direct management of the external IdP (Keycloak), automated Let's Encrypt certificate issuance (owned by Gateway).
- **Non-goals**: Direct management of the external IdP (Keycloak), automated Let's Encrypt certificate issuance (owned by Gateway).

### AI Agent Requirements

N/A

### Risks

- **Risk**: If the OpenBao quorum or unseal procedure fails, secret injection may be interrupted.
- **Dependency**: Depends on Traefik-based external exposure and the Docker/OpenBao Agent sidecar pattern.
- **Assumption**: Per-service secret paths and ACL policy are managed through the OpenBao KV and AppRole/Userpass permission model.

## Related Documents

### Traceability

- **Architecture Description**: [Security architecture descriptions](../02.architecture/descriptions/0003-security-architecture.md)
- **Spec**: [Security technical specification](../02.architecture/descriptions/0003-security-architecture.md)
- **Plan**: Security standardization plan
- **ADR**: [Central secrets manager decision](../02.architecture/decisions/0003-vault-as-secrets-manager.md)
