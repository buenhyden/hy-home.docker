# Hy-Home Agent Guide

Agent entrypoint for `hy-home.docker`, a Docker Compose infrastructure repository for local and homelab multi-service stacks.

## Setup And Verification

- Bootstrap env: `cp .env.example .env`
- Generate local certs: `bash scripts/generate-local-certs.sh`
- Bootstrap secrets: `bash scripts/bootstrap-secrets.sh --env-file .env.example`
- Validate compose: `bash scripts/validate-docker-compose.sh`
- Optional runtime preflight: `bash scripts/preflight-compose.sh`
- Start stack: `docker compose up -d`

## Core Contract

- Use the **Principal Agentic Architect** baseline, then load the matching persona from `.agent/rules/`.
- Complex work is plan-first: confirm or create the relevant spec and plan before editing code or docs.
- Use the most relevant skill for the task. Do not artificially restrict which skill may be used.
- Treat `README.md` as the human overview and this file as the cross-agent working contract.
- Use repository-relative links only and prefer repo-local commands over generic advice.

## Persona Loading

- Reasoner: `.agent/rules/0000-Agents/0002-strong-reasoner-agent.md`
- Doc Specialist: `.agent/rules/2100-Documentation/2100-documentation-pillar.md`
- Architect: `.agent/rules/1900-Architecture_Patterns/`
- DevOps: `.agent/rules/0300-DevOps_and_Infrastructure/`
- Security: `.agent/rules/2200-Security/`

## Lazy-Load Docs

- `[LOAD:INDEX]` [docs/README.md](docs/README.md)
- `[LOAD:DECISION]` [docs/adr/README.md](docs/adr/README.md)
- `[LOAD:STRATEGIC]` [docs/prd/README.md](docs/prd/README.md), [docs/ard/README.md](docs/ard/README.md)
- `[LOAD:TACTICAL]` [docs/specs/README.md](docs/specs/README.md), [docs/plans/README.md](docs/plans/README.md)
- `[LOAD:RUNBOOK]` [docs/runbooks/README.md](docs/runbooks/README.md)
- `[LOAD:HISTORY]` [docs/operations/README.md](docs/operations/README.md), [docs/operations/incidents/README.md](docs/operations/incidents/README.md)
- `[LOAD:CONTEXT]` [docs/context/README.md](docs/context/README.md)
- `[LOAD:GUIDE]` [docs/guides/README.md](docs/guides/README.md), [docs/manuals/README.md](docs/manuals/README.md)

## Provider Files

- Claude: [CLAUDE.md](CLAUDE.md)
- Gemini: [GEMINI.md](GEMINI.md)
