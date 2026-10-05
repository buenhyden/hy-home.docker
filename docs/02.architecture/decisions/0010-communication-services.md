---
title: "Communication Services Selection and Configuration"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0010"
parent_ids:
- "AD-0010"
created: "2026-03-26"
---
# ADR-0010: Communication Services Selection and Configuration

## Context

This document is the ADR that tracks the background, choices, and outcomes of this architecture decision. This alignment section does not change the existing decision content.

The `10-communication` layer handles the system's email-based notifications and message sending/receiving. During development, incidents where mail is sent to real users must be prevented, and in operation, a mail server with high deliverability and security is needed. For this, a lightweight sandbox and a modern, high-performance mail server solution must be selected.

### Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision

The following service stack is selected as the standard tooling for `10-communication`.

1. **SMTP Trap (Dev)**: **MailHog**
   - Reason: simple to configure, captured mail can be checked immediately through the web UI, and it is safe because it operates only in memory with no external relay.
2. **Mail Server (Prod)**: **Stalwart**
   - Reason: written in Rust with excellent memory efficiency and performance, and supports modern protocols such as JMAP, IMAP, and SMTP. It is also easy to maintain since it can be operated as a single binary.

### Rationale

- **Isolation policy**: the dev `mailhog` uses internal SMTP port 1025 and the prod `stalwart` uses the standard 25/465/587/993 ports, keeping them logically and clearly separated.
- **Security protocol**: the Stalwart and MailHog web UIs are protected by the Traefik SSO middleware chain. TLS/DNS deliverability evidence is verified separately before promotion to production.
- **Data reliability**: Stalwart's mail store is managed as a persistent volume, retaining data across system restarts.

### Decision Record

Accepted (2026-03-26)

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

Existing alternatives, rationale, or rejected options in this ADR remain the alternative analysis. This alignment section does not add new alternatives.

## Consequences

- **Positive**:
  - Completely removes the risk of misdirected mail during development.
  - A standardized mail server configuration lets anti-spam policy promotion criteria such as SPF/DKIM be applied consistently.
- **Negative**:
  - Stalwart's initial setup (domain verification, etc.) can be somewhat complex.
  - Operating a mail server involves managing a fixed IP and DNS records.

### Explicit Non-goals

- This ADR does not change runtime behavior.
- This ADR does not rewrite historical decision evidence.
- Implementation details remain in linked specs, plans, and tasks.

## Related Documents

- [Communication PRD](../../01.requirements/0011-communication.md)
- [Communication Architecture Description](../descriptions/0010-communication-architecture.md)
- [Communication spec](../descriptions/0010-communication-architecture.md)
- Communication standardization plan
