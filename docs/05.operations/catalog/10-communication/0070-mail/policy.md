---
title: "Stalwart Mail Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0070"
parent_ids:
- "AD-0010"
created: "2026-05-17"
---

# Stalwart Mail Operations Policy

## Overview

Stalwart is an OPTIONAL internal mail service. Its protocol listeners, relay
rule and mailbox data require controls beyond the management UI route.

## Policy Scope

Activation, DNS/TLS, protocol authentication/relay, mailbox/config data,
retention, backup/restore, license/upgrade, and removal.

## Controls

- **Activation:** use only `mail-server`; do not substitute Stalwart for Mailpit
  development capture or include it in HOME without a new accepted requirement.
- **Network/auth:** no host port; SMTP and IMAP are reachable only on
  `mail_net`. The tracked plan owns the listener set (reconciled) and keeps
  `allowRelaying = false`; a listener or relay change is a reviewed plan
  change, never a UI edit. Gateway SSO covers only the web UI.
- **Secrets/data:** keep admin, mailbox, DKIM, TLS, and backend credentials out of
  source/logs; the recovery admin comes only from the `stalwart_password`
  secret file. Treat mailbox content and metadata as sensitive personal data.
- **Retention:** record the configured backend and retention/expunge schedule.
  Do not claim Enterprise deleted-item recovery unless an applicable license and
  configuration are verified.
- **Backup/recovery:** capture config objects, every configured data/blob/search
  backend, certificate/key custody, and DNS/DKIM state. Restore with outbound
  delivery blocked and synthetic validation.
- **Resources:** measure queue, storage growth, indexing, and protocol load before
  changing the stateful-medium baseline.
- **Upgrade/license:** verify the chosen upstream license and release/storage
  migrations; test backup restore and listeners before promotion.
- **Removal:** export mailboxes/config, revoke DNS/routes/keys in a controlled
  sequence, and separately approve deletion of the bind directory.

## Exceptions

No exception may create an open relay, weaken protocol TLS without a bounded
migration, or discard mailbox data without explicit disposition.

## Verification

SMTP port health is partial. Acceptance covers authenticated submission, IMAP,
TLS certificates, DNS, relay denial, synthetic delivery, and restore where claimed.

## Review Cadence

Review before activation and on listener, DNS, backend, retention, image, or
license changes.

## Traceability

- [Guide](guide.md) (`GDE-0070`)
- [Runbook](runbook.md) (`RUN-0070`)
- [Communication architecture](../../../../02.architecture/descriptions/0010-communication-architecture.md)

## Related Documents

- [Stalwart server settings](https://stalw.art/docs/server/)
- [Stalwart storage](https://stalw.art/docs/storage/)
- [Stalwart licensing](https://github.com/stalwartlabs/stalwart/blob/main/README.md#license)
- [Stalwart Compose source](../../../../../infra/10-communication/stalwart/docker-compose.yml) and [derived version projection](../../../../../infra/tech-stack.versions.json)
