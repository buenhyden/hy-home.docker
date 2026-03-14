---
layer: core
---

# Agent Instructions — hy-home.docker

Docker Compose infrastructure workspace.

## Core Discovery

All agents MUST start their session by loading the gateway:

- **Gateway**: [docs/agentic/gateway.md](docs/agentic/gateway.md)

## Intent-Based Rule Selection

Identify your current task and load the corresponding rule set.

| **Refactoring** | `[LOAD:RULES:REFACTOR]` | Doc restructuring and plural migration |
| **Documentation** | `[LOAD:RULES:DOCS]` | Maintaining or creating management docs |
| **Lifecycle** | `[LOAD:RULES:INFRA]` | Service bring-up and teardown |
| **Governance** | `[LOAD:RULES:OPS]` | Architecture review and code standards |

## Skill Autonomy

Proactively discover and apply any relevant skill from your toolkit. There are no restricted skills in this repository; use purpose-fit tools for every task (e.g., `agent-md-refactor`, `docker-expert`).
