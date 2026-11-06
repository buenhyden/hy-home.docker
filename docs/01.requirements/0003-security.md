---
title: "Security Tier (03-security) Requirements"
version: "1.3.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "requirements"
artifact_id: "REQ-0003"
created: "2026-03-26"
---

# Security Tier (03-security) Requirements

## Overview

The `03-security` tier stores eligible consumer secrets centrally and delivers
them to services as rendered files. When secrets are scattered across files,
environment variables and manual steps, exposure risk and audit gaps grow.
Secrets must not appear in source or in plaintext environment values, every
access must be auditable, and recovery must not depend on the service being
recovered: bootstrap, recovery and independent backup credentials keep their
separate custody.

## Scope

- **In scope**: the secrets server and its storage, the delivery agent that
  renders secrets into files for consumers, access policies, unseal and recovery
  custody, and audit logging.
- **Out of scope**: managing the external identity provider (Auth tier) and
  issuing browser-facing certificates (Gateway tier).

### Assumptions

- Machine consumers authenticate with a role-scoped machine identity; operators
  authenticate through the central identity provider.
- Per-service secret paths and their access policies are declared in source and
  reviewed before change.

### Risks

- The server runs as a single node: if it is down or sealed, secret delivery to
  new or restarting consumers stops.
- A lost or wrongly held unseal share or recovery credential can make the
  stored secrets unrecoverable.

## Requirements

### Functional Requirements

- **REQ-0003-FR-0001**: Secrets must be kept in durable integrated storage. The
  current deployment is a single node; expanding to a replicated quorum is a
  separate, planned transition.
- **REQ-0003-FR-0002**: Operator user-interface and API access must pass through
  the gateway over TLS, and service-to-server paths must use validated TLS. No
  new public endpoint is granted.
- **REQ-0003-FR-0003**: Unsealing must be a manual, threshold-based operator
  procedure whose shares and recovery credentials stay in their approved
  separate custody.
- **REQ-0003-FR-0004**: Every request to the secrets server must be written to
  an audit log that does not contain secret values in plaintext.

### Stakeholders and User Needs

- **Security administrator**: sets fine-grained access policies, holds unseal
  custody and reviews audit logs.
- **Infrastructure engineer**: keeps the server available and grants each
  service only the secret paths it needs.
- **Service developer**: receives secrets as rendered files at startup instead
  of environment variables, with no secret-handling code in the service.

### Non-functional Requirements

- **REQ-0003-NFR-0005 — Recoverability**: the impact of a single-node failure
  must be detectable, and the stored secrets must be restorable from a snapshot
  into empty storage; measure: successful isolated restoration and elapsed
  recovery time in seconds, on the exact image and snapshot identity, against a
  recovery-time target the operator sets before the authorized run. A synthetic
  pass does not accept recovery of the home deployment.
- **REQ-0003-NFR-0006 — Confidentiality**: stored secrets must be encrypted at
  rest with an authenticated cipher of at least 256-bit key strength; measure:
  the server's documented storage encryption for the deployed version, checked
  at each version change.
- **REQ-0003-NFR-0007 — Performance**: secret lookup latency must suit each
  consumer's workload; measure: latency distribution in milliseconds under a
  named load, sample count and tool, against a threshold the consumer owner
  sets before measurement. No global threshold or caching guarantee is made;
  no baseline is recorded.

### Interface Requirements

No separately numbered solution-independent external interface requirement is
defined.

## Acceptance Criteria

These are local acceptance measures that apply ISO/IEC 25010, 25023 and 25030
concepts; they are not a certification claim.

- **REQ-0003-FR-0001**: The declared deployment renders with zero failures and
  zero storage or port overlaps across its selected profiles, using synthetic
  inputs. A static render never proves live health.
- **REQ-0003-FR-0002**: Consumers start with secrets delivered as files and
  need no secret in their own configuration; operator access reaches the server
  only through the gateway over TLS.
- **REQ-0003-FR-0003**: Bounded positive and negative checks without real
  credentials admit zero unauthorized token, issuer, custody or restore
  actions; no new rekey or credential issuance is inferred.
- **REQ-0003-FR-0004**: Audit logging is enabled on the deployed server and
  required rotation and failure detections succeed; a rotation not yet observed
  stays pending in the service Task.

## Related Documents

- [Security architecture description](../02.architecture/descriptions/0003-security-architecture.md)
- [ADR-0050: OpenBao as secrets manager](../02.architecture/decisions/0050-openbao-as-secrets-manager.md), which supersedes ADR-0003
- [SPEC-0204: Service integration and security](../03.specs/0204-service-integration-security-and-operations/spec.md)
- [OpenBao policy](../05.operations/policies/04-security-and-secrets/0085-openbao.md)
- [OpenBao runbook](../05.operations/runbooks/04-security-and-secrets/0085-openbao.md)
- Quality references: [ISO/IEC 25010](https://www.iso.org/standard/78176.html),
  [ISO/IEC 25023](https://www.iso.org/standard/35747.html),
  [ISO/IEC 25030](https://www.iso.org/standard/72116.html).
- Retired domain Spec SPEC-0003 (security): replaced by the security guides,
  policies and runbooks under `docs/05.operations/`.
- Retired requirement REQ-0015 (security optimization hardening): retired under
  SPEC-0169 because every clause named an implementation artifact; its
  implementation contract lives in the security operations policies and its
  documentation traceability clause moved to REQ-0026-FR-0011.
