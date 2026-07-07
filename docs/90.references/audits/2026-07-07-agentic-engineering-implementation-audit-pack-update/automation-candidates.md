---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/automation-candidates.md -->

# Reference: Automation Candidates and Implementation Roadmap

## Overview

This reference identifies 14 automation candidates and proposes an implementation roadmap to enhance harness validation, loop pipelines, and agent orchestration.

## Purpose

Define actionable roadmap goals to reduce manual steps and enforce consistent validation constraints across all agent runtimes.

## Repository Role

This document is a roadmap reference. It does not replace or modify active validation scripts, CI workflows, or tool configurations.

## Scope

### In Scope

- Listing 14 automation candidates across pipelines, workflows, and tools
- Structuring priority recommendations and immediate action items

### Out of Scope

- Directly implementing proposed automation codes or scripts
- Deploying new third-party pipeline integrations
- Modifying live branch protection rules

## Definitions / Facts

- **14 Automation Candidates**:
  - `AEA-AUTO-014` (CVE Scan), `AEA-AUTO-015` (Multi-agent Orchestrator), `AEA-AUTO-016` (Semantic Eval CI Integration), `AEA-AUTO-017` (Universal CLI Wrapper), `AEA-AUTO-018` (SBOM Generator), `AEA-AUTO-019` (attestation signing), `AEA-AUTO-020` (Instruction TOML Compiler), `AEA-AUTO-021` (Link integrity daemon), `AEA-AUTO-022` (eslint-disable abuse checker), `AEA-AUTO-023` (Git Hook Graphify integration), `AEA-AUTO-024` (Developer tool version check), `AEA-AUTO-025` (Template migration utilities), `AEA-AUTO-026` (check log validation parser), `AEA-AUTO-027` (release notes automation).
- **Roadmap Priorities**:
  - *High*: `AEA-AUTO-016` (Semantic Eval) and `AEA-AUTO-017` (Universal CLI Wrapper) to automate meaning-level code reviews and enforce consistent post-tool validation.
  - *Medium*: `AEA-AUTO-020` (Instruction Compiler) and `AEA-AUTO-023` (Git Hook Graphify) to maintain parity between agent instructions and knowledge graphs.

## Sources

- [QA scope](../../../00.agent-governance/scopes/qa.md) - QA/CI automation guidelines
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - Local automation script SSoT
- [Scripts contract README](../../../../scripts/README.md) - Script inventory definitions

## Maintenance

- **Owner**: DevOps & Workflow Specialist
- **Review Cadence**: Review when local pipelines or build chains are updated
- **Update Trigger**: Update when new automation features are proposed or integrated

## Related Documents

- [README.md](./README.md)
- [implementation-overview.md](./implementation-overview.md)
- [harness-loop-audit.md](./harness-loop-audit.md)
- [sdlc-qa-security-audit.md](./sdlc-qa-security-audit.md)
