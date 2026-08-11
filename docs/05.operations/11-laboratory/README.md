# Operations — 11 Laboratory

> Laboratory management and experimental-service operations grouped by stable subject and role.

## Overview

This domain co-locates the existing Dashboard, Dozzle, Open Notebook,
optimization-hardening, Portainer, and RedisInsight roles under frozen
`ops-0071` through `ops-0076` identities. The catalog does not add a role that
is absent from the migration ledger.

## Audience

- Operators, SREs, platform engineers, developers, and AI agents.

## Scope

- Existing service context, access and hardening controls, validation,
  recovery, rollback boundaries, and escalation.
- No Runtime mutation, Docker-socket privilege change, credential access, or
  production promotion is authorized by this index.

## Structure

| Subject | Available documents |
| --- | --- |
| [Dashboard](./ops-0071-dashboard/guide.md) | [Guide](./ops-0071-dashboard/guide.md), [Policy](./ops-0071-dashboard/policy.md), [Runbook](./ops-0071-dashboard/runbook.md) |
| [Dozzle](./ops-0072-dozzle/guide.md) | [Guide](./ops-0072-dozzle/guide.md), [Policy](./ops-0072-dozzle/policy.md), [Runbook](./ops-0072-dozzle/runbook.md) |
| [Open Notebook](./ops-0073-open-notebook/guide.md) | [Guide](./ops-0073-open-notebook/guide.md), [Policy](./ops-0073-open-notebook/policy.md), [Runbook](./ops-0073-open-notebook/runbook.md) |
| [Optimization hardening](./ops-0074-optimization-hardening/guide.md) | [Guide](./ops-0074-optimization-hardening/guide.md), [Policy](./ops-0074-optimization-hardening/policy.md), [Runbook](./ops-0074-optimization-hardening/runbook.md) |
| [Portainer](./ops-0075-portainer/guide.md) | [Guide](./ops-0075-portainer/guide.md), [Policy](./ops-0075-portainer/policy.md), [Runbook](./ops-0075-portainer/runbook.md) |
| [RedisInsight](./ops-0076-redisinsight/guide.md) | [Guide](./ops-0076-redisinsight/guide.md), [Policy](./ops-0076-redisinsight/policy.md), [Runbook](./ops-0076-redisinsight/runbook.md) |

## How to Work in This Area

Use guides for routine context, policies for access and control boundaries,
and runbooks for existing ordered recovery procedures. Follow each role's
safety, evidence, rollback or recovery, and escalation limits.

## Related Documents

- [Operations index](../README.md)
- [Laboratory infrastructure](../../../infra/11-laboratory/README.md)
- [Incident records](../incidents/README.md)
- [Release records](../releases/README.md)
