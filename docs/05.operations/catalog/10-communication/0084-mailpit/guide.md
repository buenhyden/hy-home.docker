---
title: "Mailpit Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0084"
parent_ids:
- "POL-0084"
created: "2026-09-19"
---

# Mailpit Guide

## Usage

DEV mail capture; not a production mailbox or external relay.

Profiles: `mail-dev / local / dev`. Services: `mailpit`. Root Compose owns inclusion.

UI and SMTP listeners use MAILPIT_UI_PORT and MAILPIT_SMTP_PORT; HOST_PORT variants control loopback publication. The database is /data/mailpit.db on mailpit-data. Application containers use the service DNS name on infra_net.

[Implementation](../../../../../infra/10-communication/mailpit/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Common Checks

Compose declares the image-native `/mailpit readyz` check explicitly; it follows `MP_UI_BIND_ADDR`, including nondefault ports. SMTP capture still needs a separate synthetic delivery check.

Check selected services, declared mounts, published interfaces and container state before use. Readiness and data recovery remain unverified until the runbook evidence is collected.

## Runbook Handoff

[Runbook](runbook.md) owns commands, expected results and recovery. [Policy](policy.md) owns controls.

## Traceability

- Governing architecture: [AD-0010](../../../../02.architecture/descriptions/0010-communication-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://mailpit.axllent.org/docs/configuration/runtime-options/)
