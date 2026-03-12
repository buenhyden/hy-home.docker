# Hy-Home Agent Guide

Canonical cross-agent entrypoint for `hy-home.docker`, a Docker Compose infrastructure repository for local and homelab multi-service stacks.

## Quick Start

- Bootstrap env: `cp .env.example .env`
- Generate local certs: `bash scripts/generate-local-certs.sh`
- Bootstrap secrets: `bash scripts/bootstrap-secrets.sh --env-file .env.example`
- Validate compose: `bash scripts/validate-docker-compose.sh`
- Optional runtime preflight: `bash scripts/preflight-compose.sh`
- Start stack: `docker compose up -d`

## Universal Rules

- Treat this file as the canonical cross-agent contract and keep provider roots thin.
- Shared durable policy lives in [.claude/README.md](.claude/README.md), not duplicated across root files.
- Load the **Principal Agentic Architect** baseline, then the matching persona from `.agent/rules/` for the task.
- Complex work is plan-first: confirm or create the relevant spec and plan before editing code or docs.
- Use the most relevant skill for the task; do not artificially restrict the skill set.
- Prefer repository-relative links and repo-local commands over generic advice.
- Treat [README.md](README.md) as the human overview, not the full agent contract.

## Shared Guides

- [Shared Guide Index](.claude/README.md)
- [Core Governance](.claude/core-governance.md)
- [Shared Workflow](.claude/workflow.md)

## Lazy-Load Docs

- `[LOAD:INDEX]` [docs/README.md](docs/README.md)
- `[LOAD:DECISION]` [docs/adr/README.md](docs/adr/README.md)
- `[LOAD:STRATEGIC]` [docs/prd/README.md](docs/prd/README.md), [docs/ard/README.md](docs/ard/README.md)
- `[LOAD:TACTICAL]` [docs/specs/README.md](docs/specs/README.md), [docs/plans/README.md](docs/plans/README.md)
- `[LOAD:RUNBOOK]` [docs/runbooks/README.md](docs/runbooks/README.md)
- `[LOAD:HISTORY]` [docs/operations/README.md](docs/operations/README.md), [docs/operations/incidents/README.md](docs/operations/incidents/README.md)
- `[LOAD:CONTEXT]` [docs/context/README.md](docs/context/README.md)
- `[LOAD:GUIDE]` [docs/guides/README.md](docs/guides/README.md), [docs/manuals/README.md](docs/manuals/README.md)

## Provider Roots

- Claude: [CLAUDE.md](CLAUDE.md)
- Gemini: [GEMINI.md](GEMINI.md)
