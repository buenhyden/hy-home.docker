---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/harness-loop-audit.md -->

# Reference: Harness and Loop Engineering Audit

## Overview

This audit evaluates the implementation maturity of Harness Engineering and Loop Engineering within the `hy-home.docker` workspace, analyzing multi-provider (Claude, Codex, Gemini) runtimes and common rules.

## Purpose

Assess local testbed constraints and self-correcting agent loops to prevent policy drift and improve execution predictability.

## Repository Role

This document is an audit reference. It does not replace or modify active validation scripts, Git hooks, or provider configurations.

## Scope

### In Scope

- Audit of Harness Engineering components (validators, post-tool sanitizers)
- Audit of Loop Engineering systems (inner loops, outer gates, human feedback)
- Comparison of Claude, Codex, Gemini integrations and common workspace setups

### Out of Scope

- Modifying active hook codes or validation wrappers
- Changing Docker network or compose files
- Mutating environment variables or secrets

## Definitions / Facts

- **Harness Engineering Audit**:
  - *Status*: Enforced by `harness-implementation-map.md`, `check-repo-contracts.sh` for metadata SSoT, and `post-tool-validate.sh` for auto-normalisation of code.
  - *Gaps*: Sandbox limits are inconsistent (Gemini lacks native tool execution gates), and updating the `graphify` knowledge graph is currently manual.
- **Loop Engineering Audit**:
  - *Status*: Clear workflow loops (plan approval -> task execution -> validation evidence) are in place, supported by self-healing local error parsing.
  - *Gaps*: Semantic evaluation of agent code and design choices is missing from CI/CD, remaining local-only (advisory).
- **Multi-provider & Common Setup**:
  - Claude and Codex support mature automated post-tool validation, whereas Gemini relies on prompt instructions, leading to loop execution variance.
  - An instruction compiler (markdown SSoT to TOML/MDC) and a Universal Exec CLI wrapper are missing.

## Sources

- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - Local harness configuration SSoT
- [Post tool validate hook](../../../../scripts/hooks/post-tool-validate.sh) - Normalisation hook code
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - Model routing policies
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - Multi-provider capability table

## Maintenance

- **Owner**: Platform Infrastructure Lead
- **Review Cadence**: Review when local hooks or sandbox permission scopes change
- **Update Trigger**: Update when provider runtimes are updated or new validation scripts are integrated

## Related Documents

- [README.md](./README.md)
- [implementation-overview.md](./implementation-overview.md)
- [sdlc-qa-security-audit.md](./sdlc-qa-security-audit.md)
- [agent-catalog-audit.md](./agent-catalog-audit.md)
- [../../research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md](../../research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md)
