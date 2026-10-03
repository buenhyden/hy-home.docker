---
title: "Shared Experience Integration Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0206-TSK-0002"
parent_ids:
- "SPEC-0206"
- "SPEC-0206-PLAN-0001"
created: "2026-10-03"
---

# Shared Experience Integration Task

## Objective

Register the tested Storybook static origin in root Compose with restricted browser access, coherent operations contracts and generated metadata.

## Inputs

Approved SPEC-0206 and Plan W3-W4; TSK-0001 artifacts are required before integration; current root/Traefik/OAuth2 Proxy source; admin-only decision from the user; no remote MCP audience/client.

## Work Log

| Current -> target | Exact writer files | Regression / rollback |
| --- | --- | --- |
| No shared experience tier -> optional Storybook static origin | NEW `infra/13-experience/README.md`, `infra/13-experience/storybook/README.md`, `infra/13-experience/storybook/docker-compose.yml`; `docker-compose.yml`, `infra/README.md` | Root/profile render, no host 80/443, network/health/resource checks; revert only new tier and root include. |
| Browser route unavailable -> admin-only Traefik HTTPS | New leaf Compose labels; read-only existing `infra/01-gateway/traefik/dynamic/middleware.yml` and `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg` | RouteAuth, asset auth, TLS/render and deny checks; no OAuth2 Proxy group widening. |
| Profile/public metadata absent -> registered optional profile and source projection | `docs/05.operations/policies/0078-compose-profile-vocabulary.md`; generated `infra/tech-stack.versions.json`; `docs/99.templates/registry.json`; `docs/03.specs/README.md` | Profile vocabulary, image projection generator/check, registry and document contracts; revert logical metadata commit. No new public or secret environment key is required for the static origin; existing `DEFAULT_URL` is consumed without reading its value. The real `.env` is untouched. |
| No current operating contract -> Storybook subject 0101 | NEW `docs/05.operations/guides/0101-storybook.md`, `docs/05.operations/policies/0101-storybook.md`, `docs/05.operations/runbooks/0101-storybook.md`; `docs/05.operations/README.md`, `docs/05.operations/guides/README.md`, `docs/05.operations/policies/README.md`, `docs/05.operations/runbooks/README.md` | Operations catalog, links, metadata, exact service binding; revert only this subject/index rows. |
| Codex/Claude Design usage -> verified instructions | `projects/storybook/nextjs/README.md` is TSK-0001 writer; this Task writes the new GDE-0101 usage section and reads that README | Official-source URL and installed-client availability review; revert guide section. |

The root Compose, profile policy, Stage 99 Registry and image projection have exactly one writer: this Task. TSK-0001 consumes their planned contracts and does not edit them. If the current research inventory projection requires an update, amend this Task with the exact generated path and preserve historical prose before writing.

## Verification Evidence

`NOT_RUN`: integration awaits TSK-0001 artifact handoff, not another source approval. Existing profile/operations catalog checks are baseline inputs, not new service evidence.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 3 | W3 | NOT_RUN: root render/auth checks | Compose and POL-0078 |
| 6 | W4 | NOT_RUN: official/installed client guide | GDE-0101 |
| 7 | W3-W4 | NOT_RUN: operations/registry/projection and review | Stage 05 subject, README, this Task |

## Review Evidence

Pending independent source, security and document review of the exact integration diff.

## Commit Ledger

Baseline main/origin-main `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; dependent source base `fbbea9123751c13588022cdb76213fd8b5a14b6e`. No integration commit.

## Rulings

Use existing `/admins` ForwardAuth for browser traffic. MCP is a task-local process outside root Compose until approved machine authentication exists. Reconcile already issued operations subject 0100 before reserving 0101; do not reuse or relabel 0100.

## Deferred Items

Reviewer group, remote MCP OIDC, HOME activation, DNS/TLS observations, external design account use, push/PR/merge and data migration.
