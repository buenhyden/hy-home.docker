---
title: "Mailpit Policy"
version: "0.2.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0084"
parent_ids:
- "AD-0010"
created: "2026-09-19"
---

# Mailpit Policy

## Overview

Mailpit captures development email. Its intentionally permissive SMTP settings
are acceptable only with the current DEV classification and loopback/internal
network boundaries.

## Policy Scope

Activation, SMTP/UI access, captured message data, SQLite retention, backup,
upgrade, and removal for the `mailpit` service.

## Controls

- **Activation:** use `mail-dev`, `dev`, or `local`; do not add Mailpit to HOME
  or represent it as a production mailbox/delivery service.
- **Access:** preserve loopback host binds and authenticated gateway access.
  `ACCEPT_ANY` and insecure SMTP authentication forbid external publication.
- **Data:** captured bodies, headers, addresses, and attachments are sensitive.
  Use synthetic data where possible and retain at most the configured 5000
  messages unless a reviewed requirement changes that limit.
- **Backup:** prefer live HTTP export. A database-file copy requires Mailpit to
  be stopped and SQLite database/WAL sidecars to be captured consistently.
- **Restore:** ingest only into an isolated DEV instance, verify counts and
  samples without exposing message bodies, then authorize promotion if needed.
- **Resources:** preserve the stateful medium template and monitor database size;
  pruning/vacuum activity can consume CPU and disk.
- **Upgrade:** export first, review release/storage changes, recreate only
  Mailpit, and verify readyz, UI access, SMTP capture, and retained count.
- **Removal:** export or explicitly approve disposal of retained messages before
  deleting the bind directory. Stopping/removing the container is not data removal.

## Exceptions

External exposure, SMTP relay/forwarding, real mail, or relaxed retention needs
its own security and data approval. It cannot be approved as a routine exception.

## Verification

Static checks do not prove mail capture or restore. Runtime evidence must avoid
message content and record only synthetic identifiers/counts and final state.

## Review Cadence

Review when ports, auth, retention, database path, profiles, or image change.

## Traceability

- [Guide](guide.md) (`GDE-0084`)
- [Runbook](runbook.md) (`RUN-0084`)
- [Communication architecture](../../../../02.architecture/descriptions/0010-communication-architecture.md)

## Related Documents

- [Mailpit Compose source](../../../../../infra/10-communication/mailpit/docker-compose.yml)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
- [Mailpit storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [Mailpit runtime options](https://mailpit.axllent.org/docs/configuration/runtime-options/)
- [Operations index](../../../README.md)
