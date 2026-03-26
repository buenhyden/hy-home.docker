---
layer: agentic
---

# Memory: Stage Docs Link Integrity Report (Read-Only Scope)

- Date: 2026-03-26
- Layer: docs
- Tags: #governance #link-integrity #read-only-scope

## Problem

While refactoring governance and root shim files, link integrity issues were discovered in `docs/01` to `docs/99`. Those stages were in read-only mode for this task, so direct fixes were deferred.

## Context

- Editable scope for this task:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `GEMINI.md`
  - `README.md`
  - `docs/00.agent-governance/**`
- Read-only scope for this task:
  - `docs/01` to `docs/99`
- Detection method:
  - Markdown link existence scan for stage docs.
  - `file://` URI pattern scan.

## Findings

### High Priority

1. `file://` links in stage docs violate documentation policy (`relative links only`).

| File | Reference | Recommended Fix |
| :--- | :--- | :--- |
| `docs/07.guides/06-observability/grafana.md` | `file:///home/hy/projects/hy-home.docker/docs/07.guides/02-auth/keycloak.md` | Replace with relative path to `../02-auth/keycloak.md`. |
| `docs/07.guides/06-observability/grafana.md` | `file:///home/hy/projects/hy-home.docker/infra/06-observability/grafana/provisioning/datasources/datasource.yml` | Replace with repository-relative markdown link. |
| `docs/08.operations/06-observability/grafana.md` | `file:///home/hy/projects/hy-home.docker/docs/07.guides/06-observability/grafana.md` | Replace with relative path to guide doc. |
| `docs/08.operations/06-observability/grafana.md` | `file:///home/hy/projects/hy-home.docker/docs/08.operations/06-observability/loki.md` | Replace with relative path to operations doc. |
| `docs/09.runbooks/06-observability/grafana.md` | `file:///home/hy/projects/hy-home.docker/docs/07.guides/06-observability/grafana.md` | Replace with relative path to guide doc. |
| `docs/09.runbooks/06-observability/grafana.md` | `file:///home/hy/projects/hy-home.docker/docs/09.runbooks/02-auth/keycloak.md` | Replace with relative path to runbook doc. |
| `docs/09.runbooks/06-observability/loki.md` | `file:///home/hy/projects/hy-home.docker/docs/07.guides/06-observability/loki.md` | Replace with relative path to guide doc. |

### Medium Priority

2. Template-local links in `docs/99.templates/readme.template.md` resolve as missing when parsed literally from template location.

| File | Reference | Recommended Fix |
| :--- | :--- | :--- |
| `docs/99.templates/readme.template.md` | `./AGENTS.md`, `./ARCHITECTURE.md`, `./docs/README.md`, and stage README relative links | Clarify these are placeholder links for generated README targets, or convert to explicit placeholder tokens (for example `<REPO_ROOT>/...`). |

## Resolution

- No changes were applied to `docs/01` to `docs/99` in this task.
- Findings were captured here to preserve policy compliance and handoff context.

## Prevention

- Add a stage-doc link hygiene task before future documentation releases.
- Keep `file://` URI prohibition explicit in `docs/00.agent-governance/rules/documentation-protocol.md`.
- When validating templates, exclude placeholder examples from strict path existence checks or mark them with explicit placeholders.
