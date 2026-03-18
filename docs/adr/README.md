---
layer: core
---

# Architecture Decision Records (ADR)

**Overview (KR):** 이 디렉토리는 프로젝트의 주요 아키텍처 결정 사항을 기록한 ADR(Architecture Decision Record) 문서들을 포함합니다. 각 ADR은 결정의 배경, 대안, 결과 및 영향을 상세히 기술합니다.

## Index of ADRs

| Number | Title | Status | Date |
| ------ | ----- | ------ | ---- |
| [ADR-0001](0001-root-orchestration-include.md) | Root Orchestration via `include` | Accepted | 2026-02-26 |
| [ADR-0002](0002-secrets-first-management.md) | Secrets-First Management Policy | Accepted | 2026-02-26 |
| [ADR-0003](0003-spec-driven-development.md) | Spec-Driven Development (SDD) | Accepted | 2026-02-26 |
| [ADR-0004](0004-tiered-directory-structure.md) | Tiered Directory Structure | Accepted | 2026-02-26 |
| [ADR-0005](0005-sidecar-resource-initialization.md) | Sidecar-Driven Resource Initialization | Accepted | 2026-02-26 |
| [ADR-0006](0006-project-net-external-network.md) | External `project_net` Convention | Accepted | 2026-02-26 |
| [ADR-0007](0007-mandatory-resource-limits.md) | Mandatory Resource Limits | Accepted | 2026-02-26 |
| [ADR-0008](0008-removing-static-docker-ips.md) | Removing Static Docker IPs | Accepted | 2026-02-23 |
| [ADR-0009](0009-strict-docker-secrets.md) | Strict Docker Secrets Adoption | Accepted | 2026-02-27 |
| [ADR-0011](0011-multi-stage-build-standard.md) | Multi-Stage Build Standard | Accepted | 2026-02-27 |
| [ADR-0012](0012-standardized-init-process.md) | Standardized Init Process | Accepted | 2026-02-27 |
| [ADR-0013](0013-configuration-deduplication.md) | Configuration Deduplication Strategy | Accepted | 2026-02-27 |
| [ADR-0014](0014-optimization-strategies.md) | System Optimization & Hardening | Accepted | 2026-02-27 |
| [ADR-0015](0015-infrastructure-directive-standard.md) | Infrastructure Directive Standard | Accepted | 2026-02-27 |
| [ADR-0016](0016-doc-taxonomy.md) | Standardized Documentation Taxonomy | Accepted | 2026-03-15 |
| [ADR-0017](0017-flat-documentation-taxonomy.md) | Flat Documentation Taxonomy | Accepted | 2026-03-15 |
| [ADR-0018](0018-lazy-loading-protocol.md) | Lazy-Loading Protocol for AI Agents | Accepted | 2026-03-15 |
| [ADR-0020](0020-intent-based-triggers.md) | Intent-Based Rule Triggers | Accepted | 2026-03-15 |
| [ADR-0021](0021-2026-march-agentic-standard.md) | March 2026 Agentic Standard Adoption | Accepted | 2026-03-15 |
| [ADR-0022](0022-cycle-2-doc-taxonomy.md) | Strict Enforcement of Plural Execution Paths | Accepted | 2026-03-15 |
| [ADR-0023](0023-plural-plans-path.md) | Adoption of Plural plans Path | Accepted | 2026-03-16 |
| [ADR-0024](0024-lazy-loading-agent-rules.md) | Lazy-Loading Agent Rules | Accepted | 2026-03-15 |
| [ADR-0025](0025-intent-based-lazy-loading.md) | Intent-Based Lazy Loading for Agent Rules | Accepted | 2026-03-16 |

---
> [!NOTE]
> All ADRs must be generated using [`../../templates/adr-template.md`](../../templates/adr-template.md).
