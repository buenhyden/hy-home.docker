# [SPEC-INFRA-04] System Optimization & Hardening Specification

## 0. Pre-Implementation Checklist

- [x] Traceability: PRD-OPT-01 and ARD-OPT-01 references.
- [x] Security: 100% no-new-privileges coverage.
- [x] Performance: Resource reservations.

## 1. Technical Overview

This specification details the implementation of performance and security optimizations across the repository. It focuses on the inheritance of the "common-optimizations" layer and the enforcement of the hardened container standard.

## 2. Coded Requirements

| Req ID | Requirement Description | Priority |
| --- | --- | --- |
| **SPEC-OPT-01** | All production-like tiers MUST utilize `resource-med` or higher. | P0 |
| **SPEC-OPT-02** | Security hardening (`no-new-privileges: true`) is mandatory. | P0 |
| **SPEC-OPT-03** | Use of `init: true` is mandatory for correct signal handling. | P1 |
| **SPEC-OPT-04** | Root filesystems SHOULD be `read_only: true` where state is externalized. | P1 |

## 5. Component Breakdown

### 5.1 Common Optimization Layer

- **Templates**: `resource-low`, `resource-med`, `resource-high`.
- **Logic**: Centralized in `infra/common-optimizations.yml`.

### 5.2 Security Hardening

- **Directives**: `cap_drop: [ALL]`, `security_opt: [no-new-privileges:true]`, `init: true`.
- **Statelessness**: Mandatory `read_only: true` for exporters and UI proxies.

## 7. Verification Plan

- **Audit-01**: verify `docker stats` reflects limits defined in templates.
- **Audit-02**: verify image sizes in registry/local cache.

## 11. Related Documents

- **PRD Reference**: [[PRD-OPT-01] System Optimization PRD](../../docs/prd/system-optimization-prd.md)
- **Architecture Reference**: [[ARD-OPT-01] Optimized Infrastructure Reference Document](../../docs/ard/system-optimization-ard.md)
