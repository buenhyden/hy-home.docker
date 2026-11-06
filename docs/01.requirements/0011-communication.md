---
title: "Communication Tier (10-communication) Requirements"
version: "1.3.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "requirements"
artifact_id: "REQ-0011"
created: "2026-03-26"
---

# Communication Tier (10-communication) Requirements

## Overview

Mail sending is fragmented, and a development environment can send real mail
by mistake. This package states the mail needs of the platform: a development
SMTP sandbox (Mailpit) that captures every test message, and a full mail
server (Stalwart) kept as an optional, isolated experiment capability. Stalwart
is not a HOME service: it rejects relaying, joins no HOME network and publishes
only its admin interface on the local host. Production delivery, public
protocol exposure and DNS/TLS deliverability are promotion requirements, not
current runtime claims.

## Scope

- **In scope**: SMTP capture, the experimental mail server, mail protocol
  security, admin access control, and capture history.
- **Out of scope**: groupware and messenger clients (a webmail UI may be a
  separate tier); marketing automation.
- **Non-goals**: replacing public email services.

### Assumptions

- No LAB is promoted until the owner decides it; until then no HOME container
  delivers mail through Stalwart.
- The shared SSO (Keycloak) and the gateway TLS boundary are available for the
  sandbox UI.

### Risks

- After a promotion, outbound delivery stops if the mail server IP is
  blacklisted.
- The sandbox accepts any SMTP credential, so it must stay unreachable from
  outside the host and its peers.

## Requirements

### Functional Requirements

- **REQ-0011-FR-0001**: Provide a development SMTP capture service (Mailpit)
  that keeps every received message inside the platform.
- **REQ-0011-FR-0002**: Provide an IMAP/SMTP/JMAP mail server (Stalwart) as an
  optional, isolated experiment capability that rejects relaying and serves no
  HOME container until a separately approved requirement adds a delivery path.
- **REQ-0011-FR-0003**: Support UI viewing and search of captured mail.
- **REQ-0011-FR-0004**: Mail retrieval and every browser access that leaves the
  host must use an encrypted channel. The experimental admin interface stays
  local-host only, and public submission over TLS is a promotion requirement.
- **REQ-0011-FR-0005**: The sandbox UI requires the shared SSO (Keycloak). The
  experimental mail server's admin interface is reachable only from the local
  host and uses its own administrator credential until a promotion adds SSO.

### Stakeholders and User Needs

- **Developer**: checks mail sent during development in the sandbox UI instead
  of a real inbox.
- **Admin**: evaluates the mail server, and after a promotion manages
  deliverability and anti-spam policy (SPF, DKIM) centrally.
- **Security officer**: requires encrypted mail channels and authenticated
  administration.

### Non-functional Requirements

No numbered non-functional requirement is issued.

### Interface Requirements

No numbered interface requirement is issued.

## Acceptance Criteria

- **REQ-0011-FR-0001**: No message leaves the development environment; the
  sandbox publishes its ports only on the local host.
- **REQ-0011-FR-0002**: The mail server renders on its own, selects no HOME
  service, joins only its isolated network, and its applied configuration
  rejects relaying.
- **REQ-0011-FR-0003**: A captured test message is listed and found by search
  in the sandbox UI.
- **REQ-0011-FR-0004**: IMAP is offered only with implicit TLS, and the sandbox
  UI route is served over gateway TLS. External delivery success, TLS version
  and DNS deliverability are verified as separate evidence at promotion.
- **REQ-0011-FR-0005**: An unauthenticated request to the sandbox UI route is
  redirected to SSO, and the mail server admin port is bound only to the LAB
  host address.

## Related Documents

- **Architecture Description**: [0010-communication-architecture.md](../02.architecture/descriptions/0010-communication-architecture.md)
- **ADR**: [0010-communication-services.md](../02.architecture/decisions/0010-communication-services.md)
- **Spec**: [SPEC-0262 LAB migration](../03.specs/0262-analytics-labs-migration/spec.md)
  and [SPEC-0263 LAB promotion contract](../03.specs/0263-lab-promotion-contract/spec.md)
- **Retired domain Spec SPEC-0011** (communication): replaced by the
  communication guides, policies and runbooks in the operations catalog under
  `docs/05.operations/`.
