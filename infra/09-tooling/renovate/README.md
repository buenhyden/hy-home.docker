---
title: "Renovate Implementation"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
---

# Renovate

## Overview

Explicit version-update job. The repository policy is renovate.json5; config/config.js owns the self-host command allowlist. renovate_token is mounted as a Docker Secret. The cache volume is disposable and no host port is published.

## Audience

Operators and developers reviewing service configuration.

## Scope

Lifecycle: **DEV maintenance job**. Operational controls and recovery belong to `OPS-0083` through the [documentation index](../../../docs/README.md).

## Structure

[Compose](docker-compose.yml) owns the service, mounts, network grants and entrypoint.

```
renovate/
├── config/
│   └── config.js          # self-host command allowlist
├── systemd/
│   ├── hyhome-renovate.service  # oneshot service unit
│   └── hyhome-renovate.timer   # weekly schedule trigger
└── docker-compose.yml
```

## Tech Stack

Runtime pins belong to [Compose](docker-compose.yml); [version registry](../../../infra/tech-stack.versions.json) is a derived Compose image projection, not a deployment manifest.

## Configuration

Profiles: `dependency-update`. Root Compose includes this definition; inclusion alone does not start a service. Network is `infra_net`. Review [public environment keys](../../../.env.example) and [secret references](../../../secrets/README.md) without printing private values.

## Validation

From the repository root, select the documented profile and run `scripts/validation/validate-docker-compose.sh`. Use the owning Runbook for runtime checks; config validation does not prove a successful maintenance run or remote repository update.

## How to Work in This Area

Preserve data and credentials during changes. Review exact runtime targets before deployment. Keep operational procedures in the existing operations subject.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
