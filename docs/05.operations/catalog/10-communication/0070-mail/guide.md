---
title: "Stalwart Mail Server Guide"
version: "2.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0070"
parent_ids:
- "POL-0070"
implementation_services:
  infra/10-communication/stalwart/docker-compose.yml:
  - stalwart
  - stalwart-config
created: "2026-05-10"
---

# Stalwart Mail Server Guide

## Usage

### Purpose and classification

Stalwart is the OPTIONAL internal mail server. It is selected only by
`mail-server` and is distinct from Mailpit capture. It has no host port: only
containers on `mail_net` submit mail, and the web admin and JMAP are routed by
Traefik behind SSO. It relays nothing: recipients outside the configured domain
are refused.

### Current implementation

- [Stalwart Compose](../../../../../infra/10-communication/stalwart/docker-compose.yml)
  runs the image as its own user (UID 2000) with a read-only root, `cap_drop:
  ALL` plus `NET_BIND_SERVICE` (the binary's file capability), and no host
  port.
- `config/config.json` names only the datastore (RocksDB in
  `/var/lib/stalwart`, bound from `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`).
  Everything else lives in the datastore.
- `stalwart-config` applies [config/plan.ndjson](../../../../../infra/10-communication/stalwart/config/plan.ndjson)
  with the pinned `stalwart-cli`: the domain `${DEFAULT_URL}`, host name
  `mail.${DEFAULT_URL}`, exactly four listeners (SMTP 25, submission 587, IMAPS
  993, HTTP 8080) and `allowRelaying = false`. It upserts, updates and
  reconciles, so a re-run converges; listener changes take effect on the next
  Stalwart restart.
- `stalwart_password` (COMM-006) becomes the recovery admin inside the server
  and job processes only; the Compose file carries no credential.
- TLS on 587/993 uses Stalwart's default certificate until a Certificate
  object is configured; clients on `mail_net` must trust it explicitly.
- The healthcheck reads `/healthz/live` on 8080, which is process liveness, not
  delivery readiness.
- The image is dual-licensed upstream under AGPL-3.0 or the Stalwart Enterprise
  License. No tracked license key proves Enterprise features; do not rely on them.

### Normal use and prerequisites

1. Create `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` empty; Docker gives it
   the image user's ownership on first start.
2. `docker compose --profile mail-server up -d stalwart`, then
   `docker compose --profile mail-server run --rm stalwart-config`, then
   `docker compose --profile mail-server restart stalwart`.
3. Create accounts through the admin UI or a further plan; use synthetic mail
   and never record bodies or credentials in evidence.
4. External delivery needs a new accepted requirement (DNS, SPF, DKIM, DMARC,
   reputation) and a reviewed change to the relay rule.

### Backup and upgrade

Use a version-supported Stalwart CLI snapshot/export for configuration objects
when available, plus the native backup method for each configured data/blob/
search backend. If the deployment uses only the local bind-backed stores and no
online-consistent export exists, stop Stalwart and copy the complete
`/var/lib/stalwart` tree with metadata (`stalwart --export` is the native
export). Preserve certificate/private-key custody and DNS/DKIM records
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
- [Stalwart CLI apply](https://stalw.art/docs/management/cli/apply)
- [Stalwart Compose source](../../../../../infra/10-communication/stalwart/docker-compose.yml) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [Stalwart storage model](https://stalw.art/docs/storage/)
- [Stalwart TLS](https://stalw.art/docs/server/tls/)
- [Stalwart CLI snapshot](https://stalw.art/docs/management/cli/)
- [Stalwart licensing](https://github.com/stalwartlabs/stalwart/blob/main/README.md#license)
