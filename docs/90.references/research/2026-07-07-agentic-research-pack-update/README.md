---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/README.md -->

# Agentic Engineering Research Pack (2026-07-07 Update)

> Detailed research pack index analyzing harness engineering, loop engineering, multi-provider implementations, and agent catalog frameworks.

## Overview

This research pack provides a comparative study of AI agent sandboxing, tool routing, feedback loops, provider integrations, and multi-agent persona catalogs for the `hy-home.docker` workspace. It evaluates the differences between Claude, Codex, and Gemini, and contrasts the local non-root worker model against the `msitarzewski/agency-agents` framework.

## Category Role

`docs/90.references/research/2026-07-07-agentic-research-pack-update/` serves as a dedicated, point-in-time research category analyzing agent-first engineering infrastructure. The files herein are references and do not represent active policies or plans.

## Audience

The primary audience of this research pack includes:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Analysis of local workspace baseline configuration (SDLC, SDD, CI/CD, QA, formatting, security).
- Comparative review of Harness Engineering elements (sandboxing, tool permissions, JIT context) across Claude, Codex, and Gemini.
- Multi-tier feedback loops (Inner, Outer, CI, and Human-in-the-loop) and automated Diagnostic Parsers.
- Architectural design for universal CLI wrapper and agent adapters.
- Analysis of community agent personas from `msitarzewski/agency-agents` vs. local workers.

### Out of Scope

- Active policy changes in `docs/00.agent-governance/`.
- Executable configurations or runtime Docker Compose changes.
- Incident records or postmortems.
- Sensitive credentials, secrets, or tokens.

## Structure

```text
2026-07-07-agentic-research-pack-update/
├── README.md                              # This index file
├── workspace-baseline.md                  # Workspace baseline environment, SDLC, QA, formatting, and security
├── harness-engineering.md                 # Sandbox isolation, tool permissions, JIT context, and wrapper design
├── loop-engineering.md                    # Multi-tier feedback loops and diagnostic parser models
├── provider-implementation-comparison.md # Detailed comparison matrix and adapters for Claude, Codex, and Gemini
└── ai-agent-catalogs.md                   # Persona analysis vs. agency-agents and proposal for new agents
```

## How to Work in This Area

1. These are living references, not active policy or plans. Improve or supplement them in place when analysis reveals gaps, drift, or incorrect facts; preserve the reference boundary and record any change that would alter another stage as a gap rather than editing that stage from here.
2. Ensure target-relative links use relative Markdown syntax rather than absolute paths or `file://` schemes.
3. Validate changes against repository contracts by running `./scripts/validation/check-repo-contracts.sh`.

## Related Documents

- [Research Category README](../README.md)
- [References Root README](../../README.md)
- [Documentation Protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [Agent Governance Hub](../../../00.agent-governance/README.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
