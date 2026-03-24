---
layer: agentic
---

# CLAUDE.md

<contract>
Claude-specific operational triggers for `hy-home.docker`.

## 1. Session Initialization
ALWAYS load **[docs/00.agent/01.gateway.md](docs/00.agent/01.gateway.md)** at startup.

## 2. Operational XML Rules
<workflow>
- **Plan-First**: Create implementation plans in `docs/05.plans/` before any major changes.
- **SDD Compliance**: Ensure all changes are tracked via PRD -> Spec -> Plan -> Task.
- **Validation**: NEVER bypass `bash scripts/validate-docker-compose.sh`.
</workflow>

## 3. Technical Reference
<commands>
| Task | Command |
| --- | --- |
| **Validate** | `bash scripts/validate-docker-compose.sh` |
| **Deploy** | `docker compose up -d` |
| **Secrets** | `bash scripts/bootstrap-secrets.sh` |
| **Cert-Gen** | `bash scripts/generate-local-certs.sh` |
</commands>

## 4. Lazy-Loading Markers
Use these triggers to load specialized context:
- `[LOAD:RULES:REFACTOR]` -> Refactoring logic
- `[LOAD:RULES:DOCS]` -> Documentation standards
- `[LOAD:RULES:INFRA]` -> Infrastructure lifecycle
- `[LOAD:RULES:OPS]` -> Operations/Incidents
</contract>

