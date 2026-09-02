---
title: Operations — 07 Workflow
version: 1.0.0
type: operation/domain-readme
layer: operations
owner: "@buenhyden"
---

# Operations — 07 Workflow

> Workflow operations documents grouped by stable Airflow, n8n, and hardening subjects.

## Overview

This domain co-locates each existing guide, policy, and runbook under its
current four-digit subject directory without changing operational behavior.

## Audience

- Operators, SREs, workflow platform engineers, developers, and AI agents.

## Scope

- Existing workflow usage, DAG controls, approved deployment boundaries, and
  recovery procedures.
- No workflow execution, DAG deployment, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [Airflow](0050-airflow/guide.md) | [Guide](0050-airflow/guide.md), [Policy](0050-airflow/policy.md), [Runbook](0050-airflow/runbook.md) |
| [Airflow DAG basics](0051-airflow-dag-lifecycle/guide.md) | [Guide](0051-airflow-dag-lifecycle/guide.md) |
| [DAG deployment](0051-airflow-dag-lifecycle/policy.md) | [Policy](0051-airflow-dag-lifecycle/policy.md) |
| [n8n](0053-n8n/guide.md) | [Guide](0053-n8n/guide.md), [Policy](0053-n8n/policy.md), [Runbook](0053-n8n/runbook.md) |
| [Optimization hardening](0054-optimization-hardening/guide.md) | [Guide](0054-optimization-hardening/guide.md), [Policy](0054-optimization-hardening/policy.md), [Runbook](0054-optimization-hardening/runbook.md) |

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../../README.md)
- [Workflow infrastructure](../../../../infra/07-workflow/README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
- [Incident records](../../incidents/README.md)
