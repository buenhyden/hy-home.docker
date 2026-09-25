---
title: "Mailpit Guide"
version: "0.2.1"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0084"
parent_ids:
- "POL-0084"
implementation_services:
  infra/10-communication/mailpit/docker-compose.yml:
  - mailpit
created: "2026-09-19"
---

# Mailpit Guide

## Usage

### Purpose and classification

Mailpit is a DEV mail-capture service for application and integration tests. It
is not a delivery MTA and does not replace optional Stalwart. It belongs to
`dev`, `local`, and `mail-dev`; it is excluded from HOME. The UI and SMTP host
ports are bound to `127.0.0.1`, while the UI is also routed through Traefik.

### Current implementation

- [Mailpit Compose](../../../infra/10-communication/mailpit/docker-compose.yml)
  owns the image, profiles, ports, environment, healthcheck, and volume.
- SMTP listens inside `edge_net` and on loopback host port
  `${MAILPIT_SMTP_HOST_PORT:-1025}`. The UI uses loopback
  `${MAILPIT_UI_HOST_PORT:-8025}` and `mailpit.${DEFAULT_URL}` through the
  gateway middleware chain.
- `${DEFAULT_COMMUNICATION_DIR}/mailpit/data` is bind-backed at `/data` and
  `MP_DATABASE=/data/mailpit.db` selects persistent SQLite. `MP_MAX_MESSAGES=5000`
  prunes older messages by count.
- `MP_SMTP_AUTH_ACCEPT_ANY=1` and `MP_SMTP_AUTH_ALLOW_INSECURE=1` deliberately
  accept arbitrary credentials over plaintext SMTP for test compatibility. Do
  not publish this listener or route it to external mail.
- The `/mailpit readyz` healthcheck proves process readiness, not message capture,
  UI authorization, retention, or restoration.

### Normal use

1. Validate from the root with `docker compose --profile mail-dev config --quiet`.
2. Configure a development application to send to `mailpit:${MAILPIT_SMTP_PORT:-1025}`
   on `edge_net`; host tools use the loopback host port.
3. Send only synthetic or approved test mail. The database contains bodies,
   headers, addresses, and attachments and must be treated as sensitive test data.
4. Verify capture through the authenticated UI or a bounded API query, then
   delete/expire test data under the retention policy.

### Backup and upgrade

Mailpit supports live message export with `mailpit dump` and restore-style
ingestion with `mailpit ingest`. Prefer a live HTTP dump over copying an active
SQLite/WAL file. If copying the database, stop Mailpit and copy the database
plus SQLite sidecars consistently. Before an image upgrade, export messages,
record the database checksum, recreate only Mailpit, and verify capture and
message count. Restore first into an isolated Mailpit instance. These procedures
are documented but were not executed by this task.

## Common Checks

- `docker compose --profile mail-dev config --quiet`
- `docker compose --profile mail-dev config --services`
- `bash scripts/hardening/check-all-hardening.sh 10-communication`

## Runbook Handoff

Use the [runbook](../runbooks/0084-mailpit.md) for capture failures, consistent export/restore,
retention incidents, and image upgrades.

## Traceability

- [Policy](../policies/0084-mailpit.md) (`POL-0084`)
- [Runbook](../runbooks/0084-mailpit.md) (`RUN-0084`)
- [Communication architecture](../../02.architecture/descriptions/0010-communication-architecture.md)

## Related Documents

- [Mailpit email storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [Mailpit SMTP security](https://mailpit.axllent.org/docs/configuration/smtp/)
- [Mailpit import and export](https://mailpit.axllent.org/docs/usage/import-export/)
- [Operations index](../README.md)
