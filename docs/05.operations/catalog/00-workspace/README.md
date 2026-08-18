# Operations — 00 Workspace

> Workspace-wide operational guidance, controls, and repeatable procedures.

## Overview

This domain groups existing workspace subjects by stable `ops-` identity. Each
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
| [common optimization exceptions](ops-0001-common-optimizations-template-exceptions/policy.md) | Policy |
| [developer environment](ops-0002-developer-environment/guide.md) | Guide |
| [environment-key comparison](ops-0003-env-key-comparison/guide.md) | Guide |
| [harness engineering](ops-0004-harness-agent-first-engineering/guide.md) | [Guide](ops-0004-harness-agent-first-engineering/guide.md), [Policy](ops-0004-harness-agent-first-engineering/policy.md), [Runbook](ops-0004-harness-agent-first-engineering/runbook.md) |
| [infrastructure optimization governance](ops-0006-infrastructure-optimization-governance/policy.md) | Policy |
| [LLM Wiki maintenance](ops-0007-llm-wiki-maintenance/guide.md) | [Guide](ops-0007-llm-wiki-maintenance/guide.md), [Policy](ops-0007-llm-wiki-maintenance/policy.md), [Runbook](ops-0007-llm-wiki-maintenance/runbook.md) |
| [new-service onboarding](ops-0008-new-service-onboarding/guide.md) | Guide |
| [release management](ops-0009-release-management/runbook.md) | Runbook |
| [sensitive environment comparison](ops-0010-sensitive-env-vars-comparison/guide.md) | Guide |

## How to Work in This Area

Follow a subject's guide for normal use, policy for control boundaries, and
runbook for executable recovery or validation. Do not infer a missing role.

## Related Documents

- [Operations index](../../README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
