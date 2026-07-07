---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/agent-catalog-audit.md -->

# Reference: AI Agent Catalog and Instruction Audit

## Overview

This audit evaluates the instruction completeness of local AI agents, compares local configurations with `msitarzewski/agency-agents`, and details the specifications of three proposed agent roles.

## Purpose

Verify that local agent instructions define clear execution boundaries and select optimal roles to coordinate multi-agent operations.

## Repository Role

This document is an audit reference. It does not replace or modify active agent definitions or provider-specific configuration files.

## Scope

### In Scope

- Audit of agent instruction layouts (purpose, covers/excludes, metadata)
- Comparison of local agent scope against community persona catalogs
- Detailed specification of three proposed specialized agent roles

### Out of Scope

- Modifying active subagent structures or protocols
- Rewriting provider configuration adapters
- Installing community scripts or agents directly

## Definitions / Facts

- **Agent Instruction Layouts**:
  - *Status*: The 15 local agents define clear scopes (Covers/Excludes) to enforce single-task focuses and prevent overlapping operations.
  - *Gaps*: Instructions are maintained manually; they lack compilers to automatically synchronize markdown specifications with provider runtime files.
- **agency-agents Comparison**:
  - *Status*: Compared local agents against the 140+ community personas.
  - *Gaps*: Local agents lack granular domain expertise, and interaction checklists for failure-handling scenarios are missing.
- **Proposed Specialized Agents Specifications**:
  - **Performance Optimizer**: Manages container resource settings, execution profile checks, and file processing performance.
  - **Dependency Vulnerability Guardian**: Manages SBOM validation, package vulnerability audits, and CVE fix recommendations.
  - **Prompt/Context Refiner**: Manages JIT context window pruning, history compression, and prompt optimization.

## Sources

- [Agent catalog directory](../../../00.agent-governance/agents/README.md) - Local agent metadata catalog
- [Subagent protocol specification](../../../00.agent-governance/subagent-protocol.md) - Model tier assignment rules
- [agency-agents github](https://github.com/msitarzewski/agency-agents) - Community agent persona repository

## Maintenance

- **Owner**: Workspace Agent Architect
- **Review Cadence**: Review when new subagent protocols are drafted or when new roles are introduced
- **Update Trigger**: Update when agent instructions are updated or upstream persona catalogs change

## Related Documents

- [README.md](./README.md)
- [implementation-overview.md](./implementation-overview.md)
- [harness-loop-audit.md](./harness-loop-audit.md)
- [sdlc-qa-security-audit.md](./sdlc-qa-security-audit.md)
- [../../research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md](../../research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md)
