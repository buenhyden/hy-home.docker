---
title: "Mailpit in HOME and Stalwart as a LAB"
version: "0.2.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0054"
parent_ids:
- "AD-0010"
created: "2026-11-06"
---

# ADR-0054: Mailpit in HOME and Stalwart as a LAB

## Context

### Problem and Drivers

Development mail must never reach a real recipient. The HOME SMTP trap is
Mailpit (`infra/11-quality/mailpit/`, root-included). Stalwart is a
standalone LAB (`labs/stalwart/`, SPEC-0262) and is not root-included.
`infra/10-communication/` holds only a README. No production mail server is
deployed.

- Captured development mail must stay local.
- A real mail server needs DNS, a fixed address and deliverability evidence the
  home host does not provide today.
- HOME should hold only services that run every day.

### Decision Scope

This decision covers the development SMTP trap, the Stalwart LAB and the
`10-communication` tier name. No production mail server is selected.

## Decision

### Chosen Option

1. Mailpit in `11-quality` is the HOME SMTP trap. It captures mail without
   relaying it, and its UI sits behind
   `gateway-standard-chain`, `sso-errors` and `sso-auth`.
2. Stalwart stays a LAB in `labs/stalwart/`. It refuses relaying, and its
   hardening check runs against the LAB source.
3. No production mail server is selected. Promoting Stalwart follows the LAB
   promotion policy (POL-0107) and needs TLS, DNS (SPF, DKIM) and
   deliverability evidence first.
4. `10-communication` keeps its tier name and README only; it owns no HOME
   service.

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval
record is linked. Effective from 2026-11-06.

## Alternatives

### Considered Options

- Keep MailHog: rejected; the tree runs Mailpit, the maintained successor with
  the same capture model.
- Promote Stalwart into HOME now: rejected; no deliverability evidence and no
  consumer needs outbound mail.
- Mailpit in HOME, Stalwart as a LAB until promoted: selected.

### Trade-offs

- Trade-off: no real outbound or inbound mail exists until Stalwart is
  promoted.

## Consequences

### Impacts

- Positive: development mail cannot leave the host.
- Positive: HOME carries no mail server to secure or monitor.

### Follow-up

Communication requirement and description text that still names MailHog or a
production Stalwart is reconciled by its owners.

#### Compliance

`check_11_quality` and the Stalwart checks in
`scripts/hardening/check-all-hardening.sh` guard both boundaries.

## Traceability

### Sources

Evidence is the current repository configuration and
`scripts/hardening/check-all-hardening.sh`, which checks
`labs/stalwart/docker-compose.yml` and its relay refusal; no runtime state is
claimed.

- [REQ-0011 Communication](../../01.requirements/0011-communication.md)
- [AD-0010 Communication architecture](../descriptions/0010-communication-architecture.md)
- [POL-0107 LAB promotion](../../05.operations/policies/15-labs/0107-lab-promotion.md)

### Supersession

This record replaces ADR-0010, deleted in the same change (ADR-0051); ADR-0010
is historical and non-authoritative. ADR-0010
selected MailHog as the development SMTP trap (in-memory, no external relay,
port 1025) and Stalwart as the production mail server under
`10-communication` (Rust single binary; JMAP, IMAP and SMTP; ports
25/465/587/993; persistent mail store; web UIs behind the Traefik SSO chain;
TLS and DNS deliverability verified before production). It named no rejected
candidates. The trap is now Mailpit, and Stalwart is an unpromoted LAB.
