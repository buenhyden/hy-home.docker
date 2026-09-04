---
title: "Operations — 00 Workspace"
version: "1.0.0"
type: "operation/domain-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "operations"
---

# Operations — 00 Workspace

> Workspace-wide operational guidance, controls, and repeatable procedures.

## Overview

This domain groups existing workspace subjects by stable four-digit identity. Each
subject exposes only the roles it actually has: guide for routine context,
policy for controls, and runbook for ordered recovery or validation.

## Audience

- Operators, SREs, developers, and AI agents maintaining shared workspace flow.

## Scope

- Developer environment, environment-key comparisons, harness engineering, LLM Wiki
  maintenance, onboarding, release-management procedure, and approved policy
  controls.
- No secret values, deployment/runtime changes, or invented role documents.

## Structure

| Subject | Available documents |
| --- | --- |
| [common optimization exceptions](0001-common-optimizations-template-exceptions/policy.md) | Policy |
| [developer environment](0002-developer-environment/guide.md) | Guide |
| [environment-key comparison](0003-env-key-comparison/guide.md) | Guide |
| [harness engineering](0004-harness-agent-first-engineering/guide.md) | [Guide](0004-harness-agent-first-engineering/guide.md), [Policy](0004-harness-agent-first-engineering/policy.md), [Runbook](0004-harness-agent-first-engineering/runbook.md) |
| [infrastructure optimization governance](0006-infrastructure-optimization-governance/policy.md) | Policy |
| [LLM Wiki maintenance](0007-llm-wiki-maintenance/guide.md) | [Guide](0007-llm-wiki-maintenance/guide.md), [Policy](0007-llm-wiki-maintenance/policy.md), [Runbook](0007-llm-wiki-maintenance/runbook.md) |
| [new-service onboarding](0008-new-service-onboarding/guide.md) | Guide |
| [release management](0009-release-management/runbook.md) | Runbook |
| [sensitive environment comparison](0010-sensitive-env-vars-comparison/guide.md) | Guide |
| [Compose profile vocabulary](0078-compose-profile-vocabulary/policy.md) | Policy |

## How to Work in This Area

Follow a subject's guide for normal use, policy for control boundaries, and
runbook for executable recovery or validation. Do not infer a missing role.

## Related Documents

- [Operations index](../../README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
