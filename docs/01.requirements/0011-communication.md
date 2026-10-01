---
title: "Communication Tier (10-communication) Product Requirements"
version: "1.0.3"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "requirements"
artifact_id: "REQ-0011"
parent_ids: []
created: "2026-03-26"
---
# Communication Tier (10-communication) Product Requirements

## Problem and Goals

This document retains mail requirements across Stalwart in `10-communication` and the development SMTP sandbox Mailpit in `11-quality`. Current Stalwart is optional and internal-only: no host ports are published, and the tracked configuration rejects relaying. Production delivery, public protocol exposure and DNS/TLS acceptance remain separate promotion requirements, not implemented runtime claims.

### Problem Statement

Mail sending logic is currently fragmented, and inconsistent performance and security policy make it hard to guarantee reliability under large-scale notification load. There is also a risk that development environments send real production mail.

## Stakeholders and User Needs

Provide an intelligent communication hub that handles all notification and communication data safely under security guidelines and eliminates misdirected sends caused by mistakes during development.

### Personas

- **Developer**: wants to immediately check mail sent from the server in a local sandbox during development, instead of a real inbox.
- **Admin**: wants to increase the deliverability of the production mail server and manage anti-spam policy (SPF, DKIM) centrally.
- **Security Officer**: wants to ensure all external communication is encrypted and only authenticated users can send mail.

### Key Use Cases

- **STORY-01**: A developer confirms via the Mailpit UI that test mail is captured correctly instead of leaving the system.
- **STORY-02**: The system sends user sign-up welcome mail over an encrypted channel via Stalwart.
- **STORY-03**: An admin applies SPF/DKIM settings on Stalwart so mail sent to external services is not classified as spam.

## Functional Requirements

- **REQ-0011-FR-0001**: Provide a development SMTP trap service (Mailpit).
- **REQ-0011-FR-0002**: Provide a high-performance production IMAP/SMTP/JMAP mail server (Stalwart).
- **REQ-0011-FR-0003**: Support real-time UI monitoring and search of mail transmission data.
- **REQ-0011-FR-0004**: Guarantee secure communication through TLS encryption.
- **REQ-0011-FR-0005**: Control access to the admin UI based on system SSO (Keycloak).

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0011-FR-0001**: Zero accidental production mail sends from the development environment.
- **REQ-0011-FR-0002**: The optional mail compose passes hardening verification with valid network membership, Docker Secret references, and an SSO-protected UI route.
- **REQ-0011-FR-0003**: External delivery success rate, TLS version, and DNS deliverability metrics are verified as separate evidence at production promotion, and are not treated as completion criteria for the current optional compose.

## Constraints

- **In Scope**:
  - SMTP trapping and production mail service.
  - Mail protocol security and authentication policy.
  - Delivery history and data persistence management.
- **Out of Scope**:
  - Groupware or messenger clients (a webmail UI may be considered as a separate tier).
  - Marketing automation tools.
- **Non-goals**:
  - Fully replacing public email services (Gmail, etc.).

### AI Agent Requirements

N/A

## Risks

- **Risks**: risk of outbound delivery stopping if the mail server IP is blacklisted.
- **Dependencies**: `02-auth` (SSO authentication), `secrets/certs` (TLS certificates).

## Traceability

- **Architecture Description**: [0010-communication-architecture.md](../02.architecture/descriptions/0010-communication-architecture.md)
- **Spec**: [011-communication/spec.md](../02.architecture/descriptions/0010-communication-architecture.md)
- **Plan**: 2026-03-26-10-communication-standardization.md
- **ADR**: [0010-communication-services.md](../02.architecture/decisions/0010-communication-services.md)
