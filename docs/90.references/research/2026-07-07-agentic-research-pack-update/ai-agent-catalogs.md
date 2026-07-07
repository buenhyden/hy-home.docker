---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md -->

# Reference: AI Agent Catalogs and Comparative Persona Analysis

## Overview

This reference compares the large-scale community agent persona library, `msitarzewski/agency-agents`, against the curated, governance-first local agent catalog in `hy-home.docker`.

## Purpose

Assess the role definitions and instruction structures of workspace agents and evaluate potential opportunities for new specialized agent roles.

## Repository Role

This document is a comparative reference. It does not replace or modify active agent files under `docs/00.agent-governance/agents/` or their provider-specific projections.

## Scope

### In Scope

- Structuring standard AI Agent instruction templates
- Comparing `msitarzewski/agency-agents` against the local curated catalog
- Proposing new specialized agent profiles for performance, security, and context pruning

### Out of Scope

- Installing external untrusted agent files into runtime directories
- Modifying subagent protocol model assignments
- Endorsing community catalogs as adopted workspace tools

## Definitions / Facts

- **Local Agent Instruction Structure**: Enforces standard headers: Overview/Purpose, Scope (Covers/Excludes), Structure, Skills/Functions, and Usage/Artifacts.
- **Catalog Model Comparison**:
  - `agency-agents` contains 140+ personas across 16 corporate divisions, focusing on scenario-based prompts and multi-tool conversion scripts.
  - `hy-home.docker` curates a team of 15 agents tightly bound to the workspace's Docker Compose infrastructure, local validators, and approval boundaries.
- **Identified Gaps**:
  - The local catalog lack granular domain specialists (e.g., database or frontend styling experts) and detailed interaction guidelines for failure scenarios.
- **Proposed Specialized Agents**:
  - **Performance Optimizer**: Focuses on container resource limits, runtime execution speed, and file rendering performance.
  - **Dependency Vulnerability Guardian**: Focuses on SBOM scanning, vulnerability auditing (`npm audit`), and CVE remediation recommendations.
  - **Prompt/Context Refiner**: Focuses on context window pruning, history optimization, and JIT instruction compression (e.g., using `caveman` skill).

## Sources

- [agency-agents repository](https://github.com/msitarzewski/agency-agents) - Community agent persona library SSoT
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) - Claude subagent routing guidelines
- [Codex subagents](https://developers.openai.com/codex/subagents) - Codex TOML-based subagent schema

## Maintenance

- **Owner**: Workspace Agent Architect
- **Review Cadence**: Review when new subagent protocols or agent roles are introduced
- **Update Trigger**: Update when local roles are restructured or when upstream community catalog models change

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [provider-implementation-comparison.md](./provider-implementation-comparison.md)
- [../../../../00.agent-governance/agents/README.md](../../../00.agent-governance/agents/README.md)
