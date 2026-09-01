---
profile_id: operations-domain-readme
---

# Operations — 11 Laboratory

> Laboratory management and experimental-service operations grouped by stable subject and role.

## Overview

This domain co-locates the current Dashboard, Dozzle, Open Notebook,
optimization-hardening, Portainer, and RedisInsight roles under stable
four-digit subject identities. Role membership follows the current tree.

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
| [Dashboard](0071-homer-dashboard/guide.md) | [Guide](0071-homer-dashboard/guide.md), [Policy](0071-homer-dashboard/policy.md), [Runbook](0071-homer-dashboard/runbook.md) |
| [Dozzle](0072-dozzle/guide.md) | [Guide](0072-dozzle/guide.md), [Policy](0072-dozzle/policy.md), [Runbook](0072-dozzle/runbook.md) |
| [Open Notebook](0073-open-notebook/guide.md) | [Guide](0073-open-notebook/guide.md), [Policy](0073-open-notebook/policy.md), [Runbook](0073-open-notebook/runbook.md) |
| [Optimization hardening](0074-optimization-hardening/guide.md) | [Guide](0074-optimization-hardening/guide.md), [Policy](0074-optimization-hardening/policy.md), [Runbook](0074-optimization-hardening/runbook.md) |
| [Portainer](0075-portainer/guide.md) | [Guide](0075-portainer/guide.md), [Policy](0075-portainer/policy.md), [Runbook](0075-portainer/runbook.md) |
| [RedisInsight](0076-redisinsight/guide.md) | [Guide](0076-redisinsight/guide.md), [Policy](0076-redisinsight/policy.md), [Runbook](0076-redisinsight/runbook.md) |

## How to Work in This Area

Use guides for routine context, policies for access and control boundaries,
and runbooks for existing ordered recovery procedures. Follow each role's
safety, evidence, rollback or recovery, and escalation limits.

## Related Documents

- [Operations index](../../README.md)
- [Laboratory infrastructure](../../../../infra/11-laboratory/README.md)
- [Incident records](../../incidents/README.md)
