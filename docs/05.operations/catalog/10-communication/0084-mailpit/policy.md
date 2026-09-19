---
title: "Mailpit Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0084"
parent_ids:
- "AD-0010"
created: "2026-09-19"
---

# Mailpit Policy

## Overview

DEV mail capture; not a production mailbox or external relay.

## Policy Scope

`infra/10-communication/mailpit` and services `mailpit` under profiles `mail-dev / local / dev`.

## Controls

The test SMTP listener deliberately accepts arbitrary authentication and insecure transport. Keep direct host ports on loopback, UI behind gateway authentication and real mail credentials out of test traffic. Apply retention to captured message contents.

[Implementation](../../../../../infra/10-communication/mailpit/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Exceptions

Owner @buenhyden must record scope, risk, expiry and exit condition before any deviation. Static configuration is not evidence of live backup or recovery.

## Verification

Compose/profile validation and the [runbook](runbook.md) provide separate static and runtime evidence. Stop on unexpected service, mount, authentication or readiness state.

## Review Cadence

Review monthly and before image, persistence, authentication or exposure changes.

## Traceability

- Governing architecture: [AD-0010](../../../../02.architecture/descriptions/0010-communication-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://mailpit.axllent.org/docs/configuration/runtime-options/)
