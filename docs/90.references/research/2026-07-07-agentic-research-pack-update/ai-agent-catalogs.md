---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md -->

# Reference: AI Agent Catalogs and Workspace Alignment

This document analyzes public agent repositories, compares open-source agent libraries with the workspace's agent architecture, and establishes patterns for scaling localized agent catalogs.

---

## Overview

AI Agent Catalogs are centralized registers of agent personas, specifications, capabilities, and execution contexts. By standardizing agent specifications, teams can configure and spawn subagents for specialized tasks (e.g. security audits, refactoring, code formatting) with predictable behaviors:
- **Public Agent Pools**: Open-source libraries like `msitarzewski/agency-agents` collect various agent personas. While useful for general brainstorming, they lack the strict constraints, sandbox requirements, and local validation hooks needed for secure production use.
- **Workspace Agent Catalogs**: Located in [docs/00.agent-governance/agents/](../../../00.agent-governance/agents/), the workspace uses a single source of truth (SSoT) to define local agent capabilities. Every agent has explicit boundaries, file permission controls, and target validation scripts.

## Purpose

This reference baseline studies the architecture of open-source agent catalogs to determine how to scale the local agent directory while maintaining security, compliance, and isolation boundaries.

## Repository Role

This document serves as an advisory reference for scaling agent directories. It does not replace the Stage 00 agent governance profiles or the execution instructions in [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md).

## Scope

### In Scope
- Analysis of public agent repositories (`msitarzewski/agency-agents`).
- Workspace agent catalog layout and synchronization mechanisms.
- Verification checks for agent profile integrity.
- Gaps in agent catalog governance (lack of profile linters, subagent trace logging).

### Out of Scope
- Creation of new executable subagent roles or modifications to model routing.
- Mutating active agent profiles under `docs/00.agent-governance/agents/`.
- Credentials, private keys, or API secrets.

## Definitions / Facts

### 1. Analysis of `msitarzewski/agency-agents`
`msitarzewski/agency-agents` is a structured repository grouping agents by agency roles (e.g., Tech Agency, Writing Agency, QA Agency):
- **Structure**: Uses YAML/Markdown definitions containing the agent's name, system instruction prompt, and a list of allowed tools.
- **Execution**: Employs a chat-centric orchestration wrapper where agents converse with each other to complete goals.
- **Parity Gap**: Lacks sandboxing, terminal-level hook attachments, and deterministic rollbacks, making it unsuitable for direct deployment in our isolated Docker Compose environments without wrapping.

### 2. Local Workspace Catalog Alignment
The workspace implements a structured, localized catalog in [docs/00.agent-governance/agents/](../../../00.agent-governance/agents/):
- **Specification Compliance**: Each profile defines specific `Covers` (files the agent is allowed to write) and `Excludes` (files the agent is blocked from modifying) to prevent credential leaks or unauthorized code alterations.
- **Subagent Spawning**: Managed by [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md). Spawning is triggered via programmatic tool calls (`invoke_subagent`), routing task inputs to dedicated agent instances.

### 3. Identified Gaps
- **Missing Instruction Linters**: The repository lacks static linters to verify that new agent profiles include all required safety fields (e.g., permission bounds, role descriptions).
- **Subagent Logging**: No centralized tracing exists for inter-agent communication, making auditing difficult. Message exchanges should be mirrored to `.agent-work/logs/`.

## Sources

- [msitarzewski/agency-agents Repository](https://github.com/msitarzewski/agency-agents) - Open-source agent persona library
- [Agent Catalog Overview](../../../00.agent-governance/agents/README.md) - SSOT for local agent catalogs
- [Subagent Protocol Specifications](../../../00.agent-governance/subagent-protocol.md) - Subagent execution and communication architectures

## Maintenance

- **Owner**: Workspace Platform Agent Governance Architect
- **Review Cadence**: Semi-annually, or upon approval of new agent roles.
- **Update Trigger**: Triggered by changes to the schema rules in the `docs/00.agent-governance/agents/` directory.

## Related Documents

- [Research Index README](./README.md)
- [References Category README](../README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [harness-engineering.md](./harness-engineering.md)
- [loop-engineering.md](./loop-engineering.md)
- [provider-implementation-comparison.md](./provider-implementation-comparison.md)
