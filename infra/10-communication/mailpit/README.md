---
title: "Mailpit Implementation"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
---

# Mailpit

## Overview

Captures development SMTP traffic. UI and SMTP host ports bind to loopback and the UI is routed through authenticated Traefik. MAILPIT_UI_PORT and MAILPIT_SMTP_PORT own container listeners; HOST_PORT variants own publication. mailpit-data persists /data/mailpit.db. Test SMTP accepts arbitrary authentication and must not be exposed externally.

## Audience

Operators and developers reviewing service configuration.

## Scope

Lifecycle: **DEV**. Operational controls and recovery belong to `OPS-0084` through the [documentation index](../../../docs/README.md).

## Structure

[Compose](docker-compose.yml) owns the service, mounts, network grants and entrypoint.

## Tech Stack

Runtime pins belong to [Compose](docker-compose.yml); [version registry](../../../infra/tech-stack.versions.json) is a derived Compose image projection, not a deployment manifest.

## Configuration

Profiles: `mail-dev / local / dev`. Root Compose includes this definition; inclusion alone does not start a service. Network is `infra_net`. Review [public environment keys](../../../.env.example) and [secret references](../../../secrets/README.md) without printing private values.

## Validation

From the repository root, select the documented profile and run `scripts/validation/validate-docker-compose.sh`. Use the owning Runbook for runtime checks; config validation does not prove a successful maintenance run or SMTP capture.

## How to Work in This Area

Preserve data and credentials during changes. Review exact runtime targets before deployment. Keep operational procedures in the existing operations subject.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
