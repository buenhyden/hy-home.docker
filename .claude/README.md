# Shared Agent Guidance

This directory stores the shared operational detail referenced by the root agent files.

## Files

- [core-governance.md](core-governance.md): Shared policy, persona loading, lazy-loading rules, and template contracts
- [workflow.md](workflow.md): Shared execution loop, command references, and document usage rules

## Consumer Files

- [../AGENTS.md](../AGENTS.md): Canonical cross-agent entrypoint
- [../CLAUDE.md](../CLAUDE.md): Claude-specific shim via `@` imports
- [../GEMINI.md](../GEMINI.md): Gemini-specific shim via links

## Maintenance Rule

Keep the root files concise. Add durable shared detail here instead of duplicating it across `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
