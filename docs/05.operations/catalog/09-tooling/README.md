# Operations — 09 Tooling

> Tooling operations documents grouped by stable infrastructure, testing, registry, quality, synchronization, and IaC subjects.

## Overview

This domain co-locates each existing tooling guide, policy, and runbook under
its frozen `ops-0060` through `ops-0069` identity without adding a role that
did not exist in the migration ledger.

## Audience

- Operators, SREs, platform engineers, developers, and AI agents.

## Scope

- Existing infrastructure-as-code controls, testing and quality tooling,
  registry operations, synchronization, and recovery procedures.
- No deployment, destructive test, registry mutation, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [IaC deployment policy](ops-0060-iac-deployment/policy.md) | [Policy](ops-0060-iac-deployment/policy.md) |
| [k6](ops-0061-k6/guide.md) | [Guide](ops-0061-k6/guide.md), [Policy](ops-0061-k6/policy.md), [Runbook](ops-0061-k6/runbook.md) |
| [Locust](ops-0062-locust/guide.md) | [Guide](ops-0062-locust/guide.md), [Policy](ops-0062-locust/policy.md), [Runbook](ops-0062-locust/runbook.md) |
| [Optimization hardening](ops-0063-optimization-hardening/guide.md) | [Guide](ops-0063-optimization-hardening/guide.md), [Policy](ops-0063-optimization-hardening/policy.md), [Runbook](ops-0063-optimization-hardening/runbook.md) |
| [Performance testing](ops-0064-performance-testing/guide.md) | [Guide](ops-0064-performance-testing/guide.md), [Policy](ops-0064-performance-testing/policy.md), [Runbook](ops-0064-performance-testing/runbook.md) |
| [Registry](ops-0065-registry/guide.md) | [Guide](ops-0065-registry/guide.md), [Policy](ops-0065-registry/policy.md), [Runbook](ops-0065-registry/runbook.md) |
| [SonarQube](ops-0066-sonarqube/guide.md) | [Guide](ops-0066-sonarqube/guide.md), [Policy](ops-0066-sonarqube/policy.md), [Runbook](ops-0066-sonarqube/runbook.md) |
| [Syncthing](ops-0067-syncthing/guide.md) | [Guide](ops-0067-syncthing/guide.md), [Policy](ops-0067-syncthing/policy.md), [Runbook](ops-0067-syncthing/runbook.md) |
| [Terraform](ops-0068-terraform/guide.md) | [Guide](ops-0068-terraform/guide.md), [Policy](ops-0068-terraform/policy.md), [Runbook](ops-0068-terraform/runbook.md) |
| [Terrakube](ops-0069-terrakube/guide.md) | [Guide](ops-0069-terrakube/guide.md), [Policy](ops-0069-terrakube/policy.md), [Runbook](ops-0069-terrakube/runbook.md) |

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../../README.md)
- [Tooling infrastructure](../../../../infra/09-tooling/README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
- [Incident records](../../incidents/README.md)
