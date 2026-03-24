---
layer: agentic
---

# Infrastructure Lifecycle Rule

This rule defines the mandatory lifecycle steps for any infrastructure or service modification.

## Lifecycle Phases

1. **Discover** — Load `docs/00.agent/gateway.md`; find existing specs, ADRs, runbooks.
2. **Specify** — If no spec exists, create `docs/04.specs/<name>.md` from `docs/99.templates/spec.template.md`.
3. **Plan** — Verify or create `docs/05.plans/<name>.md` from `docs/99.templates/plan.template.md`.
4. **Implement** — Apply the smallest correct change. `docker compose config` must pass before any `up`.
5. **Verify** — Run `bash scripts/validate-docker-compose.sh && bash scripts/preflight-compose.sh`.
6. **Document** — Update runbooks, ADRs, and operations history whenever behavior or structure changes.

## Compliance

- **Spec-Driven**: Never skip the specification phase for non-trivial work.
- **Traceability**: Link ADRs, Specs, and Plans reciprocally.
