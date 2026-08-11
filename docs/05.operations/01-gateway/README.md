# Operations — 01 Gateway

> Gateway guidance, controls, and recovery procedures grouped by stable subject.

## Overview

The gateway domain keeps each existing Nginx, setup, and Traefik document in
one `ops-` subject folder. Roles remain separate and no missing role is added.

## Audience

- Operators, SREs, developers, and AI agents working on gateway operations.

## Scope

- Nginx profile-only routing, root-active Traefik routing, and gateway setup.
- No runtime configuration, secret, or deployment mutation.

## Structure

| Subject | Available documents |
| --- | --- |
| [Nginx](./ops-0011-nginx/guide.md) | [Guide](./ops-0011-nginx/guide.md), [Policy](./ops-0011-nginx/policy.md), [Runbook](./ops-0011-nginx/runbook.md) |
| [setup](./ops-0012-setup/guide.md) | Guide |
| [Traefik](./ops-0013-traefik/guide.md) | [Guide](./ops-0013-traefik/guide.md), [Policy](./ops-0013-traefik/policy.md), [Runbook](./ops-0013-traefik/runbook.md) |

## How to Work in This Area

Use a guide for normal configuration context, a policy for controls, and a
runbook only for its existing ordered procedure and recovery boundary.

## Related Documents

- [Operations index](../README.md)
- [Gateway infrastructure](../../../infra/01-gateway/README.md)
- [Guides index](../README.md)
- [Policies index](../README.md)
- [Runbooks index](../README.md)
