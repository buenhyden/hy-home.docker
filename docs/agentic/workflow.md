---
layer: agentic
---

# Shared Agent Workflow

This file describes the shared execution loop for work in `hy-home.docker`.

## Default Loop

1. Load [gateway.md](gateway.md) to discover current specs, ADRs, and runbooks.
2. Discover the current state from repo files, docs, rules, and command output.
3. Confirm or create the required spec and plan for complex work.
4. Apply the relevant persona and skills.
5. Execute the smallest correct change.
6. Verify with repo-local commands.
7. Update durable docs when behavior, structure, or operational guidance changes.

## Which Docs To Load

- Agent session entrypoint: [gateway.md](gateway.md)
- Infrastructure behavior: [../../README.md](../../README.md), [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
- Tactical implementation: [../specs/README.md](../specs/README.md), [../plans/README.md](../plans/README.md)
- Procedures: [../runbooks/README.md](../runbooks/README.md)
- Operations History: [../operations/README.md](../operations/README.md)
- Technical Context: [../context/README.md](../context/README.md)

## Specs And Plans

- For non-trivial work, verify that a matching spec and plan already exist under `../specs/` and `../plan/`.
- Current refactor contract:
  - [../specs/2026-03-alignment-spec.md](../specs/2026-03-alignment-spec.md)
  - [../plan/2026-03-alignment-plan.md](../plan/2026-03-alignment-plan.md)

## Runbooks Vs Operations History

- `docs/runbooks/`: executable recovery and maintenance procedures
- `docs/operations/`: historical incidents, postmortems, and anomaly records
- `docs/operations/incidents/README.md`: incident log entrypoint

## Repo-Local Validation Commands

```bash
bash scripts/validate-docker-compose.sh
bash scripts/preflight-compose.sh
docker compose config
docker compose up -d
rg -n 'file://|templates/(architecture|product|operations)/|\]\(/specs/' AGENTS.md CLAUDE.md GEMINI.md .claude docs
```

## Root-File Maintenance Rules

- `AGENTS.md` is the canonical cross-agent entrypoint.
- `CLAUDE.md` stays thin and uses `@` imports for shared guidance.
- `GEMINI.md` stays thin and links to shared guidance without duplicating it.
- Shared detail goes in `docs/agentic/*.md`, not repeated in every root file.

## Anti-Patterns

- Treating `README.md` as the only source of truth for agent behavior
- Duplicating the same policy in all three root files
- Linking directly to raw directories when an index README exists
- Leaving outdated template paths or absolute filesystem links in docs
