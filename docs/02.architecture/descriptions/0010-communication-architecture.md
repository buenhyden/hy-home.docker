---
title: "Communication Tier Architecture Description"
version: "1.1.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "architecture"
artifact_id: "AD-0010"
parent_ids:
- "REQ-0011"
created: "2026-03-26"
---

# Communication Tier Architecture Description

## Context and Stakeholders

The mail requirements separate development message capture in `11-quality/mailpit` from the optional internal mail server in `10-communication/stalwart`. Mailpit is a DEV SMTP sink/UI selected by `dev`, `local`, or
`mail-dev`. Stalwart is selected only by `mail-server` and requires mail-domain,
DNS, TLS, authentication, relay, abuse, and backup ownership before use.

## System Boundaries

- **Mailpit owns:** test-message capture in persistent SQLite
  `/data/mailpit.db`, loopback-published SMTP/UI ports, and a Traefik UI route.
  It accepts arbitrary SMTP authentication by design and must not be internet
  exposed or described as a delivery MTA.
- **Stalwart owns:** internal SMTP25/submission587, implicit-TLS IMAP993 and HTTP8080 listeners, a management UI, and `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`. No host port is published. Its helper reconciles the complete listener set from `config/plan.ndjson`, including relay denial. Both `edge_net` and `mail_net` peers can reach listeners bound to `[::]`; UI ForwardAuth does not secure direct mail/API access.
- **Declared versus observed:** tracked `config/plan.ndjson` supplies the domain, listeners and relay-denial intent. The actual datastore/backend state, successful plan application, users, DKIM keys and DNS provider state remain unverified. Operators must
  inspect the running configuration without exposing values before choosing a
  backend-specific export or snapshot.
- **Non-goals:** Mailpit does not replace Stalwart, and Stalwart is not an
  automatic HOME service.

## Components

Mailpit is the development SMTP/UI component backed by one SQLite database.
Stalwart is the optional mail-protocol and administration component backed by
the operator-selected storage configuration under its persistent mount.

## Data Flow

```mermaid
flowchart LR
  DevApp -->|SMTP test| Mailpit[(SQLite capture)]
  Browser -->|loopback/Traefik UI| Mailpit
  MailClient -->|authenticated mail protocols| Stalwart
  Stalwart -.->|external delivery requires separate promotion approval| Internet
  Stalwart --> Store[(configured data/blob/directory backends)]
```

## Deployment View

The root project includes both leaves. Profile choice determines activation:
`mail-dev`/`dev`/`local` select Mailpit and `mail-server` selects Stalwart plus `stalwart-config`. The helper uses its selected `config/Dockerfile` and existing reconciliation wrapper. A
currently running optional service may remain running when another profile is
rendered; profile rendering is not a stop operation.

## Quality Attributes

- **Isolation:** applications choose Mailpit explicitly for tests; no captured
  development message may be relayed externally.
- **Security:** current internal operation needs authenticated protocol and relay-denial evidence. Public delivery additionally requires DNS/SPF/DKIM/DMARC and TLS promotion acceptance. No public listener or internet-delivery success is inferred from current source; shared-network reachability remains broader than the browser route.
- **Recoverability:** Mailpit recovery preserves SQLite with its WAL or uses the
  official dump/ingest path. Stalwart recovery captures configuration, all active
  storage backends, keys/certificates, and DNS dependencies at one consistency
  point, then restores with outbound delivery disabled.
- **Licensing:** Stalwart upstream offers AGPL-3.0 and enterprise licensing;
  deployment documentation must not assume paid features or entitlement.

## Traceability

- [Mailpit operations](../../05.operations/guides/0084-mailpit.md)
- [Stalwart operations](../../05.operations/guides/0070-mail.md)

## Related Documents

- [Communication requirement](../../01.requirements/0011-communication.md)
- [Communication decision](../decisions/0010-communication-services.md)

Runtime pins are owned by Compose/Dockerfile declarations; the
[derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
