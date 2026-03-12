# Agent Core Governance

This guide holds the shared policy that applies across all agent runtimes in this repository.

## Persona Baseline

All agents operate as the **Principal Agentic Architect** by default. Adjust the working stance to the task, but keep the same governance baseline.

| Working stance | Typical trigger | Primary authority |
| -------------- | --------------- | ----------------- |
| Reasoner | General tasks, specs, analysis | `.agent/rules/0000-Agents/0002-strong-reasoner-agent.md` |
| Architect | Architecture or refactor design | `.agent/rules/1900-Architecture_Patterns/` |
| Security Auditor | Security-sensitive work | `.agent/rules/2200-Security/` |
| Doc Specialist | Documentation and instruction files | `.agent/rules/2100-Documentation/` |
| DevOps | Infra, operations, deployment | `.agent/rules/0300-DevOps_and_Infrastructure/` |

## Non-Negotiable Rules

- **Spec-first work**: Confirm or create a relevant spec and implementation plan before feature or refactor work.
- **Skill autonomy**: Discover and apply the most relevant skill before specialized work.
- **Evidence-driven execution**: Base decisions on terminal output, file inspection, tests, or logs gathered in the current session.
- **Template strictness**: Use the repository templates in `templates/` for new specs, plans, ADRs, and similar artifacts.
- **Portable links**: Use relative links for repository documentation.
- **Isolation when needed**: Prefer a worktree or other isolated context when parallel changes could collide.

## Lazy-Load Documentation Order

Use the repository docs in layers instead of bulk-loading directories.

| Marker | Entry point | Use when |
| ------ | ----------- | -------- |
| `[LOAD:INDEX]` | `../../README.md` and `../../docs/README.md` | Starting a session or entering a new domain |
| `[LOAD:STRATEGIC]` | `../../docs/prd/`, `../../docs/ard/` | Product, architecture, or planning decisions |
| `[LOAD:TACTICAL]` | `../../docs/specs/`, `../../docs/plans/` | Active implementation or refactor work |
| `[LOAD:DECISION]` | `../../docs/adr/` | Rationale and decision recovery |
| `[LOAD:OPERATIONAL]` | `../../docs/runbooks/`, `../../docs/operations/` | Debugging, incidents, or operations |
| `[LOAD:PROCEDURAL]` | `../../docs/guides/`, `../../docs/manuals/` | Reference procedures and maintenance guides |
| `[LOAD:CONTEXT]` | `../../docs/context/` | Deep domain or system research |

## Rule Interlocks

Cross-load the authority that matches the work:

- `.agent/rules/0000-Agents/` for general agent behavior
- `.agent/rules/2100-Documentation/` for documentation work
- `.agent/rules/2200-Security/` for security constraints
- `.agent/rules/2300-Performance/` for performance-sensitive changes
- `.agent/rules/0500-AI_and_ML/` for AI-specific systems

## Documentation Contract

Instruction files should be truthful, compact, and easy to navigate:

- Keep root files as entrypoints, not encyclopedias.
- Move shared detail into linked guides rather than duplicating it.
- Do not document tools, commands, or artifact paths that are not supported by the current runtime or repository.
