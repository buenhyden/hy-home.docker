# Shared Agent Workflow

This file describes the shared execution loop for work in `hy-home.docker`.

## Default Loop

1. Load [../docs/agent-instructions.md](../docs/agent-instructions.md) to discover current specs, ADRs, and runbooks.
2. Discover the current state from repo files, docs, rules, and command output.
3. Confirm or create the required spec and plan for complex work.
4. Apply the relevant persona and skills.
5. Execute the smallest correct change.
6. Verify with repo-local commands.
7. Update durable docs when behavior, structure, or operational guidance changes.

## Which Docs To Load

- Agent session entrypoint: [../docs/agent-instructions.md](../docs/agent-instructions.md)
- Infrastructure behavior and stack usage: [../README.md](../README.md), [../ARCHITECTURE.md](../ARCHITECTURE.md)
- Tactical implementation: [../docs/specs/README.md](../docs/specs/README.md), [../docs/plans/README.md](../docs/plans/README.md)
- Runbooks for “what to type”: [../docs/runbooks/README.md](../docs/runbooks/README.md)
- Incident history and RCA: [../docs/operations/README.md](../docs/operations/README.md), [../docs/operations/incidents/README.md](../docs/operations/incidents/README.md)
- Technical blueprints: [../docs/context/README.md](../docs/context/README.md)

## Specs And Plans

- For non-trivial work, verify that a matching spec and plan already exist under `../docs/specs/` and `../docs/plans/`.
- If they do not exist and the task is complex, create them using the repository templates before implementation.
- Current refactor contract:
  - [../docs/specs/agent-instructions/spec.md](../docs/specs/agent-instructions/spec.md)
  - [../docs/plans/2026-03-12-agent-instruction-refactor.md](../docs/plans/2026-03-12-agent-instruction-refactor.md)

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
- Shared detail goes in `.claude/*.md`, not repeated in every root file.

## Anti-Patterns

- Treating `README.md` as the only source of truth for agent behavior
- Duplicating the same policy in all three root files
- Linking directly to raw directories when an index README exists
- Leaving outdated template paths or absolute filesystem links in docs
