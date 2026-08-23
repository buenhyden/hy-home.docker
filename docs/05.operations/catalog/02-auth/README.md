# Operations — 02 Auth

> Authentication guidance, controls, and recovery procedures grouped by stable subject.

## Overview

The authentication domain preserves the existing Keycloak and OAuth2 Proxy
roles in domain-first `ops-` subject folders; no new role is inferred.

## Audience

- Operators, SREs, developers, and AI agents responsible for authentication.

## Scope

- Keycloak and OAuth2 Proxy usage context, controls, and validated procedures.
- No credential value, runtime, or deployment mutation.

## Structure

| Subject | Available documents |
| --- | --- |
| [Keycloak](0014-keycloak/guide.md) | [Guide](0014-keycloak/guide.md), [Policy](0014-keycloak/policy.md), [Runbook](0014-keycloak/runbook.md) |
| [OAuth2 Proxy](0015-oauth2-proxy/guide.md) | [Guide](0015-oauth2-proxy/guide.md), [Policy](0015-oauth2-proxy/policy.md), [Runbook](0015-oauth2-proxy/runbook.md) |

## How to Work in This Area

Use the existing guide, policy, and runbook for their distinct purposes. A
runbook's commands, evidence, rollback, and escalation remain in its source
document and are not expanded by this index.

## Related Documents

- [Operations index](../../README.md)
- [Auth infrastructure](../../../../infra/02-auth/README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
