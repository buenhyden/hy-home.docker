---
title: "Gatus Implementation"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
---

# Gatus

## Overview

Monitors configured endpoint availability and stores SQLite history on `gatus-data` at `/data/gatus.db`. The status UI uses authenticated Traefik without direct host publication. A healthy monitor does not prove every monitored application works.

## Audience

Operators and developers reviewing service configuration.

## Scope

Lifecycle: **HOME**. Operational controls and recovery belong to `OPS-0087` through the [documentation index](../../../docs/README.md).

## Structure

[Compose](../docker-compose.yml) owns the service, mounts, network grants and entrypoint.

## Tech Stack

Upstream build pins belong to [Dockerfile](Dockerfile); runtime configuration belongs to [Compose](../docker-compose.yml); [version registry](../../../infra/tech-stack.versions.json) is a curated projection, not a deployment manifest.

## Configuration

Profiles: `availability / obs / dev`. Root Compose includes this definition; inclusion alone does not start a service. Network is `infra_net`. Review [public environment keys](../../../.env.example) and [secret references](../../../secrets/README.md) without printing private values.

## Validation

From the repository root, select the documented profile and run `scripts/validation/validate-docker-compose.sh`. Use the owning Runbook for runtime checks; config validation does not prove a successful maintenance run or restored monitoring history.

## How to Work in This Area

Preserve data and credentials during changes. Review exact runtime targets before deployment. Keep operational procedures in the existing operations subject.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
