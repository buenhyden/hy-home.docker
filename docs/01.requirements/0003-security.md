---
title: "Security Tier (03-security) Requirements"
version: "1.2.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "requirements"
artifact_id: "REQ-0003"
created: "2026-03-26"
---
# Security Tier (03-security) Requirements

## Overview

### Problem and Goals

The `03-security` tier manages eligible consumer secrets through OpenBao and
file-based rendering. Secrets must not appear in source or plaintext environment
values. Bootstrap, recovery and independent backup credentials keep their
separate custody under the current OpenBao policy; central storage must not make
recovery depend on the unavailable service being recovered.

### Problem Statement

When per-service secrets are scattered across files, environment variables, and manual procedures, exposure risk and audit gaps grow. `03-security` must integrate secret storage, access control, injection, and audit logging around OpenBao so that every service follows the same trust boundary.

## Scope

### Stakeholders and User Needs

- **Security**: Encrypted storage of eligible consumer secrets, independent recovery custody and least-privilege access control.
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

## Requirements

### Functional Requirements

| ID    | Requirement           | Priority                                           |
| ----- | --------------------- | -------------------------------------------------- |
| REQ-0003-FR-0001 | Raft Storage          | Currently uses single-node Raft integrated storage, with HA expansion prepared as a separate transition procedure. |
| REQ-0003-FR-0002 | Authorized TLS Access | Route authorized operator UI/API access through Traefik and preserve validated TLS on native consumer paths. This grants no new public endpoint. |
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

### Quality Measurement

These measures apply the product-quality, measurement and requirement concepts
of ISO/IEC 25010, 25023 and 25030. They are local acceptance measures, not an ISO
certification or a claim to have reviewed the paid standards' full text.

| Requirement | Characteristic and measure | Environment and baseline | Acceptance and owner |
| --- | --- | --- | --- |
| REQ-0003-FR-0001 | Configuration correctness: failed declared Compose selections and invalid port/storage overlaps, in counts | Public source render with synthetic inputs; record the exact source and Compose version in the owning Task | Zero failures across selected declared profiles and HOME. Static render never proves live health; QA owns source acceptance. |
| REQ-0003-FR-0003 | Access safety: unauthorized token, issuer, custody and restore actions admitted, in counts | Bounded positive/negative fixtures with isolated source and no real credentials; each changed trust boundary selects its existing regression | Zero unauthorized actions admitted; security review and the owning Task judge evidence. |
| REQ-0003-FR-0004 | Audit reliability: required rotation/scrape failure detections and missing observations, in counts | Named deployed target and safe operational observations; source declarations and live observations remain separate | Required detections succeed; unobserved rotation remains pending in the service Task. |
| REQ-0003-NFR-0005 | Recoverability: successful isolated restoration and elapsed recovery time, in seconds | Exact image, snapshot identity and empty storage target; live recovery baseline is not measured by source tests | Operator defines the recovery-time target before the authorized run and verifies restored state. A synthetic PASS cannot accept HOME recovery. |
| REQ-0003-NFR-0007 | Performance: secret lookup latency distribution, in milliseconds | Named load, sample count and tool; baseline not measured | The consumer owner sets the latency threshold from the intended workload before measurement; no invented global threshold or caching guarantee. |

## Acceptance Criteria

- **REQ-0003-FR-0001**: The current OpenBao/Agent compose and documentation are managed under the root `security`/`core` profile validation and hardening gate.
- **REQ-0003-FR-0002**: Service containers do not need to know secrets directly and start successfully after receiving them via the OpenBao Agent.
- **REQ-0003-FR-0003**: Unseal and recovery procedures retain the approved custody and authorization boundaries; no new rekey or credential issuance is inferred.
- **REQ-0003-FR-0004**: Audit log/remote audit enhancements are rolled out in stages after policy approval, with actual rotation and failure observations kept in the service Task.

## Related Documents

### Traceability

- **Architecture Description**: [Security architecture descriptions](../02.architecture/descriptions/0003-security-architecture.md)
- **Change owner**: [Service integration and security](../03.specs/0204-service-integration-security-and-operations/spec.md)
- **Custody policy**: [OpenBao policy](../05.operations/policies/04-security-and-secrets/0085-openbao.md)
- **Recovery procedure**: [OpenBao runbook](../05.operations/runbooks/04-security-and-secrets/0085-openbao.md)
- **Quality references**: [ISO/IEC 25010](https://www.iso.org/standard/78176.html), [ISO/IEC 25023](https://www.iso.org/standard/35747.html), [ISO/IEC 25030](https://www.iso.org/standard/72116.html).
- **Historical ADR**: [Central secrets manager decision](../02.architecture/decisions/0003-vault-as-secrets-manager.md)
