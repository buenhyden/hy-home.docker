# [SPEC-INFRA-01] Infrastructure Global Baseline Specification

## 0. Pre-Implementation Checklist

- [x] Traceability: PRD-BASE-01 and ARD-BASE-01 references.
- [x] Security: Verified non-root UID (1000).
- [x] Design: global inheritance via common-optimizations.yml.

## 1. Technical Overview

This specification establishes the global technical invariants for all infrastructure services. It defines the mandatory inheritance model, least privilege access controls, and environment portability required across the Hy-Home service tiers.

## 2. Coded Requirements

| Req ID | Requirement Description | Priority |
| --- | --- | --- |
| **SPEC-GLOB-01** | All services MUST extend from `infra/common-optimizations.yml`. | P0 |
| **SPEC-GLOB-02** | services SHALL utilize `${DEFAULT_DATA_DIR}` for all bind mounts. | P0 |
| **SPEC-GLOB-03** | Runtime filesystems SHALL be `read_only: true` by default. | P1 |

## 4. Interfaces & Internal API

- **Logging Interface**: Loki driver with `hy-home.tier` and `job` labels.
- **Environment API**: Mandatory `.env` template defined in `.env.example`.

## 5. Component Breakdown

### 5.1 Common Optimizations

- **File**: `infra/common-optimizations.yml`
- **Templates**: `base-security`, `logging-loki`, `resource-med`.

### 5.2 Path Abstraction

- **Variable**: `DEFAULT_DATA_DIR`
- **Usage**: Mandatory for all database and log volumes.

## 6. Edge Cases & Failure Handling

- **Missing ENV**: Startup SHALL fail if `DEFAULT_DATA_DIR` is unbound.
- **Resource Exhaustion**: Services hitting mem_limit SHALL be restarted by the system.

## 7. Verification Plan

- **Audit-01**: Run `docker compose config` to verify template resolution.
- **Audit-02**: verify label searchability in Grafana Loki Explorer.

## 11. Related Documents

- **PRD Reference**: [[PRD-BASE-01] Infrastructure Baseline PRD](../../docs/prd/infra-baseline-prd.md)
- **Architecture Reference**: [[ARD-BASE-01] Infrastructure Baseline Reference Document](../../docs/ard/infra-baseline-ard.md)
