---
layer: agentic
---

# Shared Agent Workflow

**Overview (KR):** `hy-home.docker`에서 작업을 수행하기 위한 공유 실행 루프 및 검증 절차를 정의합니다.

## Default Loop

1. Load [gateway.md](gateway.md) to discover current specs, ADRs, and runbooks.
2. Discover the current state from repo files, docs, rules, and command output.
3. Confirm or create the required spec and plan for complex work.
4. Apply the relevant persona and skills.
5. Execute the smallest correct change.
6. Verify with repo-local commands.
7. Update durable docs when behavior, structure, or operational guidance changes.

## Which Docs To Load

## Related Navigation

- [Decisions Index](../adr/README.md)
- [Context Hub](../context/README.md)
- [Persona Standards](core-governance.md)
- [Agent Governance](../../AGENTS.md)

## Specs And Plans

- For non-trivial work, verify that a matching spec and plan already exist under `../specs/` and `../plan/`.
- Current refactor contract:
  - [../specs/2026-03-15-alignment-spec.md](../specs/2026-03-15-alignment-spec.md)
  - [../plans/2026-03-15-alignment-plan.md](../plans/2026-03-15-alignment-plan.md)

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
