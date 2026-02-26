# [PLAN-INFRA-01] Infrastructure Hardening & Optimization Implementation

- **Role**: DevOps Lead / Implementation Engineer
- **Status**: Completed
- **Reference Spec**: [[SPEC-INFRA-04] Infrastructure Hardening & Optimization](/specs/infra/system-optimization/spec.md)

## 1. Implementation Strategy

Every infrastructure modification SHALL follow the Spec-Driven Development (SDD) lifecycle:

1. **Audit**: Identification of redundant `security_opt` and legacy anchors.
2. **Refactor**: Transition to global `extends` pattern via `common-optimizations.yml`.
3. **Validate**: Verification of configuration integrity via `docker compose config`.

## 2. Key Components

### 2.1 Multi-Stage Builds [REQ-SPT-05]

- **Requirement**: Use multi-stage Dockerfiles to minimize leakage and optimize layer caching.
- **Action**: Refactor `n8n`, `OpenSearch`, and `Keycloak` Dockerfiles to utilize builder patterns.

### 2.2 Global Configuration Propagation

- **Requirement**: propagate security and resource invariants via the `extends` keyword.
- **Action**: Standardize all 10+ tiers to inherit from `base-security` and `base-resource-*`.

## 3. Verification & Compliance Checklist

- [x] **[AC-PLAN-01]**: `docker compose config` validates with zero unknown anchor errors.
- [x] **[AC-PLAN-02]**: Redundant security blocks removed from `minio`, `mongodb`, and `supabase`.
- [x] **[AC-PLAN-03]**: Keycloak image version hardcoded to `26.5.4` for stability.
