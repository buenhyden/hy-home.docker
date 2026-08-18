---
status: active
artifact_id: spec-0004
artifact_type: spec
parent_ids:
  - ad-0019
created: 2026-07-05
updated: 2026-08-11
---
<!-- Target: docs/03.specs/spec-0004-data/spec.md -->

# 04-Data Optimization Hardening Specification

## Overview

This document defines the optimization/hardening implementation contract for the `infra/04-data` tier. It prioritizes immediately applicable compose consistency, healthchecks, secret path contracts, and verification automation, while connecting catalog-based expansion items to operations policy/runbook coverage.

## Strategic Boundaries & Non-goals

- This specification owns the 04-data infrastructure configuration hardening and verification contract.
- Large-scale per-engine topology expansion, such as multi-cluster migration, is deferred to a later phase.

## Related Inputs

- **PRD**: [../../01.requirements/prd-0016-data-optimization-hardening.md](../../01.requirements/prd-0016-data-optimization-hardening.md)
- **ARD**: [../../02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/adr-0004-postgresql-ha-patroni.md](../../02.architecture/decisions/adr-0004-postgresql-ha-patroni.md)
  - [../../02.architecture/decisions/adr-0019-04-data-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0019-04-data-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - 04-data compose keeps inheriting the `infra/common-optimizations.yml` template.
  - Core `supabase` services must provide healthchecks.
  - The `ksql` tier label uses `hy-home.tier: data`.
- **Data / Interface Contract**:
  - The `valkey-cluster-exporter` secret file path uses `/run/secrets/service_valkey_password`.
  - The `seaweedfs` expose definition allows only valid port tokens.
- **Governance Contract**:
  - Enforce `scripts/hardening/check-all-hardening.sh 04-data` through the CI `infrastructure-hardening` job.
  - Compose the operating gate together with `scripts/validation/check-template-security-baseline.sh` and `scripts/validation/check-document-links.py --mode traceability`.

## Core Design

- **Component Boundary**:
  - Target scope: `infra/04-data/{analytics,cache-and-kv,lake-and-object,nosql,operational,relational,specialized}`
  - Immediate hardening targets:
    - `operational/supabase`
    - `cache-and-kv/valkey-cluster`
    - `lake-and-object/seaweedfs`
    - `analytics/ksql`
- **Key Dependencies**:
  - `03-security` secret operating policy
  - `01-gateway` exposure/routing policy
  - `06-observability` monitoring policy
- **Tech Stack**:
  - Docker Compose
  - common optimization templates (`template-infra-*`, `template-stateful-*`)

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - service-specific data separation based on `${DEFAULT_DATA_DIR}`
- **Migration / Transition Plan**:
  - Phase 1: lock compose consistency and healthcheck contracts
  - Phase 2: formalize catalog expansion items (backup/retention/failover/reindex) as policy
  - Phase 3: execute approved per-service expansion

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface DataHardeningContract {
  composePath: string;
  templateInherited: true;
  hasHealthcheck: boolean;
  secretsPathPolicy: 'service_valkey_password';
  malformedExposeForbidden: true;
}
```

## Catalog-aligned Expansion Targets

- Analytics: retention tiering, schema compatibility gate, ISM/rollover, batch window governance
- Cache & KV: failover drill, eviction policy split, exporter standardization
- Lake & Object: lifecycle/versioning/KMS policy, quorum/recovery automation
- NoSQL: compaction/repair, shard/replica balance, election/backup drill
- Operational: DB baseline + slow-query gate, supabase exposure/resource review
- Relational: failover SLA, vacuum tuning, PITR drill
- Specialized: graph/query guardrail, vector indexing/reindex policy

## Edge Cases & Error Handling

- If a service depends on `service_healthy` but has no healthcheck configured, startup order can fail.
- Secret file path mismatches cause exporter authentication failure.
- Compose token typos (`]`) can cause static validation failure or runtime errors.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: abnormal dependency-service restart loop in the `supabase` stack
- **Fallback**: restore the healthcheck contract, then restart through `docker compose config` and runbook procedure
- **Human Escalation**: page Data Platform Operator and DevOps on-call together

## Verification

```bash
docker compose -f infra/04-data/operational/supabase/docker-compose.yml config
docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config
docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config
docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config
bash scripts/hardening/check-all-hardening.sh 04-data
bash scripts/validation/check-template-security-baseline.sh
python3 scripts/validation/check-document-links.py --mode traceability
```

Runtime verification where the environment allows:

```bash
docker compose -f infra/04-data/operational/supabase/docker-compose.yml up -d
docker inspect --format '{{json .State.Health}}' supabase-analytics
docker inspect --format '{{json .State.Health}}' supabase-db
docker inspect --format '{{json .State.Health}}' supabase-pooler
```

## Success Criteria & Verification Plan

- **VAL-SPC-DATA-001**: `check-all-hardening.sh 04-data` has zero failures.
- **VAL-SPC-DATA-002**: core `supabase` services have healthchecks.
- **VAL-SPC-DATA-003**: `valkey-cluster-exporter` secret path contract is aligned.
- **VAL-SPC-DATA-004**: `seaweedfs` expose token typo is removed.
- **VAL-SPC-DATA-005**: 04-data document-layer traceability links are synchronized.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: ../../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md
- **Tasks**: ../../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md
- **Guide**: [../../05.operations/guides/04-data/optimization/optimization-hardening.md](../../05.operations/catalog/04-data/ops-0030-optimization-optimization-hardening/guide.md)
- **Policy**: [../../05.operations/policies/04-data/optimization/optimization-hardening.md](../../05.operations/catalog/04-data/ops-0030-optimization-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/runbooks/04-data/optimization/optimization-hardening.md](../../05.operations/catalog/04-data/ops-0030-optimization-optimization-hardening/runbook.md)
