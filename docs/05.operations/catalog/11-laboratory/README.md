---
title: "Operations — 11 Laboratory"
version: "1.0.0"
type: "operation/domain-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
---

# Operations — 11 Laboratory

> Laboratory management and experimental-service operations grouped by stable subject and role.

## Overview

This domain co-locates the current Dozzle, Open Notebook,
optimization-hardening, RedisInsight, SurrealDB, MLflow and JupyterLab roles under
stable four-digit subject identities. Dozzle uses `admin`/`admin-logs`,
RedisInsight uses `admin`/`admin-data`, Open Notebook plus SurrealDB use
`notebook`/`surrealdb` (not `admin`), MLflow uses `mlops`/`data-science`, and
JupyterLab uses `data-science`. There is no current laboratory `dev` profile or
Metabase service.

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
| [Dozzle](0072-dozzle/guide.md) | [Guide](0072-dozzle/guide.md), [Policy](0072-dozzle/policy.md), [Runbook](0072-dozzle/runbook.md) |
| [Open Notebook](0073-open-notebook/guide.md) | [Guide](0073-open-notebook/guide.md), [Policy](0073-open-notebook/policy.md), [Runbook](0073-open-notebook/runbook.md) |
| [Optimization hardening](0074-optimization-hardening/guide.md) | [Guide](0074-optimization-hardening/guide.md), [Policy](0074-optimization-hardening/policy.md), [Runbook](0074-optimization-hardening/runbook.md) |
| [RedisInsight](0076-redisinsight/guide.md) | [Guide](0076-redisinsight/guide.md), [Policy](0076-redisinsight/policy.md), [Runbook](0076-redisinsight/runbook.md) |
| [SurrealDB](0080-surrealdb/guide.md) | [Guide](0080-surrealdb/guide.md), [Policy](0080-surrealdb/policy.md), [Runbook](0080-surrealdb/runbook.md) |
| [MLflow](0088-mlflow/guide.md) | [Guide](0088-mlflow/guide.md), [Policy](0088-mlflow/policy.md), [Runbook](0088-mlflow/runbook.md) |
| [JupyterLab](0089-jupyterlab/guide.md) | [Guide](0089-jupyterlab/guide.md), [Policy](0089-jupyterlab/policy.md), [Runbook](0089-jupyterlab/runbook.md) |

## How to Work in This Area

Use guides for routine context, policies for access and control boundaries,
and runbooks for existing ordered recovery procedures. Follow each role's
safety, evidence, rollback or recovery, and escalation limits.

## Related Documents

- [Operations index](../../README.md)
- [Laboratory infrastructure](../../../../infra/11-laboratory/README.md)
- [Incident records](../../incidents/README.md)
