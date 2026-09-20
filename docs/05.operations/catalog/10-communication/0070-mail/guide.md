---
title: "Stalwart Mail Server Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0070"
parent_ids:
- "POL-0070"
implementation_services:
  infra/10-communication/stalwart/docker-compose.yml:
  - stalwart
created: "2026-05-10"
---

# Stalwart Mail Server Guide

## Usage

### Purpose and classification

Stalwart is the OPTIONAL real mail server. It is selected only by `mail-server`
and is distinct from DEV-only Mailpit capture. Source declares SMTP, submission,
SMTPS, IMAPS, and ManageSieve host ports plus a Traefik management UI route; it
does not prove DNS, relay reputation, inbound delivery, mailbox auth, or backup readiness.

### Current implementation

- [Stalwart Compose](../../../../../infra/10-communication/stalwart/docker-compose.yml)
  owns ports, route, secret, certificate mount, healthcheck, and data volume.
- `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` is mounted at `/opt/stalwart` and
  contains runtime configuration plus mailbox/storage data selected through the
  Stalwart UI. The tracked repository does not reveal the configured data/blob/
  search/in-memory backends; inspect them through an approved admin session before backup.
- `${DEFAULT_CERT_DIR}` is mounted read-only at `/opt/stalwart/certs`.
  `stalwart_password` seeds the admin password. The Traefik middleware protects
  the web UI only; SMTP/IMAP authentication and TLS are Stalwart listener controls.
- The SMTP socket probe is process reachability, not delivery/auth/TLS readiness.
- The image is dual-licensed upstream under AGPL-3.0 or the Stalwart Enterprise
  License. No tracked license key proves Enterprise features; do not rely on them.

### Normal use and prerequisites

1. Validate `docker compose --profile mail-server config --quiet` from the root.
2. Before activation, verify domain ownership, A/AAAA/MX, reverse DNS, SPF, DKIM,
   DMARC, TLS certificates, listener authentication, relay policy, abuse controls,
   host firewall, storage backend, and recovery owner.
3. Start only `stalwart`. Verify the management UI separately from authenticated
   submission/IMAP and inbound/outbound test delivery. Use synthetic mail and
   never record bodies or credentials in evidence.
4. Record actual configured storage backends and retention. Do not assume the
   bind directory is a Maildir or a particular database solely from Compose.

### Backup and upgrade

Use a version-supported Stalwart CLI snapshot/export for configuration objects
when available, plus the native backup method for each configured data/blob/
search backend. If the deployment uses only the local bind-backed stores and no
online-consistent export exists, stop Stalwart and copy the complete `/opt/stalwart`
tree with metadata. Preserve certificate/private-key custody and DNS/DKIM records
separately. Restore on an isolated hostname with outbound SMTP blocked, verify
accounts/mailbox counts and synthetic retrieval, then approve cutover.

Before upgrade, take and test that backup, read release/storage/license notes,
pin a compatible image, and validate all listeners. No delivery, backup, restore,
or upgrade was executed by this documentation task.

## Common Checks

- `docker compose --profile mail-server config --quiet`
- `docker compose --profile mail-server config --services`
- `bash scripts/hardening/check-all-hardening.sh 10-communication`

## Runbook Handoff

Use the [runbook](runbook.md) for listener failures, data recovery, or upgrades.

## Traceability

- [Policy](policy.md) (`POL-0070`)
- [Runbook](runbook.md) (`RUN-0070`)
- [Communication architecture](../../../../02.architecture/descriptions/0010-communication-architecture.md)

## Related Documents

- [Stalwart Docker deployment](https://stalw.art/docs/install/platform/docker/)
- [Stalwart storage model](https://stalw.art/docs/storage/)
- [Stalwart TLS](https://stalw.art/docs/server/tls/)
- [Stalwart CLI snapshot](https://stalw.art/docs/management/cli/)
- [Stalwart licensing](https://github.com/stalwartlabs/stalwart/blob/main/README.md#license)
