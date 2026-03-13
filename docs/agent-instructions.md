# Agent Instructions Gateway

Agent-specific context entrypoint for the `hy-home.docker` infrastructure workspace. Load this file at session start to discover relevant documentation families before doing any work.

**See also:** [README.md](README.md) for the general documentation hub.

## Discovery Protocol

- `[GATE-AGT-01]` Load this file first in any agent session involving documentation or infrastructure work.
- `[GATE-AGT-02]` Use the lazy-loading map below — never raw directory scans.
- `[GATE-AGT-03]` All links are relative; do not introduce absolute paths.
- `[GATE-AGT-04]` Load only the doc families relevant to the current task.

## Lazy-Loading Map

| Marker | Entry Point | Load when |
| --- | --- | --- |
| `[LOAD:ADR]` | [adr/README.md](adr/README.md) | Reviewing or creating architecture decisions |
| `[LOAD:ARD]` | [ard/README.md](ard/README.md) | Reviewing or creating technical architecture requirements |
| `[LOAD:PRD]` | [prd/README.md](prd/README.md) | Reviewing product scope or feature requirements |
| `[LOAD:SPEC]` | [specs/README.md](specs/README.md) | Implementing or verifying against active specifications |
| `[LOAD:PLAN]` | [plans/README.md](plans/README.md) | Executing or tracking implementation plans |
| `[LOAD:RUNBOOK]` | [runbooks/README.md](runbooks/README.md) | Performing operational procedures or incident response |
| `[LOAD:INCIDENTS]` | [operations/incidents/README.md](operations/incidents/README.md) | Investigating or declaring incidents |
| `[LOAD:HISTORY]` | [operations/README.md](operations/README.md) | Reviewing historical operational records, RCAs, postmortems |
| `[LOAD:CONTEXT]` | [context/README.md](context/README.md) | Deep service blueprints and platform technical context |
| `[LOAD:GUIDES]` | [guides/README.md](guides/README.md) | Lifecycle guides and operational guides |
| `[LOAD:MANUALS]` | [manuals/README.md](manuals/README.md) | Team collaboration and workflow manuals |

## Template Contracts

When creating new artifacts, use the repository templates:

| Artifact | Template |
| --- | --- |
| PRD | [../templates/prd-template.md](../templates/prd-template.md) |
| ARD | [../templates/ard-template.md](../templates/ard-template.md) |
| ADR | [../templates/adr-template.md](../templates/adr-template.md) |
| Spec | [../templates/spec-template.md](../templates/spec-template.md) |
| Plan | [../templates/plan-template.md](../templates/plan-template.md) |
| Runbook | [../templates/runbook-template.md](../templates/runbook-template.md) |
| Incident | [../templates/incident-template.md](../templates/incident-template.md) |
| Postmortem | [../templates/postmortem-template.md](../templates/postmortem-template.md) |

## Validation Commands

```bash
# Verify Docker Compose syntax
docker compose config

# Full infrastructure pre-flight check
bash scripts/validate-docker-compose.sh
bash scripts/preflight-compose.sh

# Check for stale or broken links in instruction files
rg -n 'file://|templates/(architecture|product|operations)/|\]\(/specs/' AGENTS.md CLAUDE.md GEMINI.md .claude docs
```

## Related Policy

- [../AGENTS.md](../AGENTS.md) — Canonical cross-agent entrypoint
- [../CLAUDE.md](../CLAUDE.md) — Claude-specific shim
- [../GEMINI.md](../GEMINI.md) — Gemini-specific shim
- [../.claude/core-governance.md](../.claude/core-governance.md) — Persona matrix, rule-loading, template contracts
- [../.claude/workflow.md](../.claude/workflow.md) — Execution loop and validation commands
