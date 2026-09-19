---
title: "Gatus Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0087"
parent_ids:
- "AD-0031"
created: "2026-09-19"
---

# Gatus Policy

## Overview

Keep availability monitoring part of the HOME baseline without exposing operational status publicly.

## Policy Scope

Service `gatus`, its local image build, read-only configuration, persistent SQLite database and authenticated gateway route.

## Controls

Keep direct host ports unpublished, root filesystem read-only and gateway authentication enabled. Preserve the configured non-root identity and writable data mount. Treat probe URLs and stored results as operational data; record sanitized status evidence only. Build and inspect the declared Dockerfile before deploying its local image.

## Exceptions

Owner @buenhyden records scope, risk, expiry and exit condition before changing exposure or persistence. A container health result does not prove endpoint coverage or successful restore.

## Verification

Validate selected profiles and source contracts, then collect the runbook's runtime checks only within the authorized scope. Test restore on isolated data before any production replacement.

## Review Cadence

Review monthly and whenever probe targets, image sources, authentication or storage change.

[Compose](../../../../../infra/06-observability/docker-compose.yml) owns activation, mounts and routing. [Dockerfile](../../../../../infra/06-observability/gatus/Dockerfile) owns upstream build pins; the local image name is not an upstream version.

## Traceability

- [AD-0031](../../../../02.architecture/descriptions/0031-home-development-host.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Official Gatus configuration, storage and authentication](https://github.com/TwiN/gatus)
