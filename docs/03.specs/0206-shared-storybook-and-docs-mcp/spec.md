---
title: "Shared Storybook and Documentation MCP Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0206"
parent_ids:
- "REQ-0027"
- "AD-0031"
- "SPEC-0201"
created: "2026-10-03"
---

# Shared Storybook and Documentation MCP Specification

## Overview

Make the existing `projects/storybook/nextjs` a shared UI reference with a static image, restricted browser route, reusable component contract, and local read-only documentation MCP. Baseline main/origin-main is `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; the isolated dependency prerequisite is `fbbea9123751c13588022cdb76213fd8b5a14b6e` on `feat/0205-storybook-dependency-refresh`. That prerequisite retains an unresolved high `braces` advisory and the user's remote-merge hold.

## Boundaries and Inputs

The shared UI stays in `projects/storybook/nextjs`; no business app is added here. SPEC-0205 owns the preceding npm refresh. Browser access initially retains Keycloak `/admins` through OAuth2 Proxy. A reviewer group and remote MCP OIDC audience/client are unapproved. No HOME rollout, DNS, secret issuance, external design upload, push, PR, merge, or user-global client configuration is included. The current Button/Header/Page are scaffold examples; only reviewed components with a package consumer test enter the export surface. No repository LICENSE file is tracked, so the package contract defaults to private internal use with no public npm publication until the owner assigns a distribution license.

## Behavior Contract

1. A lockfile-based multi-stage image builds Storybook static output. Context excludes `.env`, secrets, caches and unrelated paths. A non-root read-only origin uses an internal port, bounded resources, tmpfs and healthcheck; it opens no host 80/443.
2. An optional static Storybook service is root-included under a registered profile. Traefik terminates HTTPS and protects index, iframe, assets, manifests and deep links with the existing admin-only browser path. A dedicated internal ingress network joins only Traefik and Storybook so shared-network peers cannot bypass that path. Cache, 404, CSP/frame and logout behavior are verified.
3. A component artifact declares exports, TypeScript types, CSS/tokens, React peers, license, version and upgrade rules. A synthetic external consumer imports it; static URL and manifest are documentation, not code distribution.
4. Storybook's preview components/docs manifests are built from the same source revision as static output and checked against source exports and revision.
5. A separate task-local MCP process, absent from root Compose, serves only documentation tools from the manifests. Protocol tests cover initialize, tools/list, component/docs reads, unsupported and forbidden tools, reconnect and stale manifests. The static origin is not an MCP server.
6. Remote MCP remains disabled until machine-compatible issuer, audience, client, token validation and reader authorization are approved and tested. Browser-cookie ForwardAuth alone is insufficient.
7. Codex/Claude Code examples remain scoped and do not write user-global config. Claude Design guidance distinguishes official capability from installed-client execution; only approved UI code, tokens and synthetic screens may be shared.
8. Korean README and operations docs, derived image projection and path-aware checks agree with source. No 07/08 app, microphone, real audio or external bootstrap is added.

## Technical Approach

Define and test the package, manifests and local MCP; then build and check the image; finally integrate Compose/Traefik and operations docs. One integration Task exclusively writes root Compose, profile policy and Registry; no MCP port or service is added there. Reuse the shared Compose hardening and Traefik middleware. A 13-experience tier is created only if the real shared service justifies it.

## Interfaces and Data

Inputs: tracked npm manifest/lock, reviewed components/stories/MDX, public environment keys, existing gateway/identity contracts, synthetic fixtures and official documentation. Outputs: `storybook-static`, component package artifact, `components.json`/`docs.json`, local docs MCP and a disabled remote-auth contract. The revision marker must identify the exact source commit. No secret, HOME data, user session or design-tool upload is an input.

## Failure Modes and Guardrails

Reject context leakage, authentication HTML in assets/MCP, stale manifests, exposed development/testing tools, missing audience validation, absent package CSS/types, insecure runtime, second gateway and unregistered profile. Missing Docker or resource allowance blocks only isolated runtime evidence. The `braces` finding remains a merge blocker.

## Acceptance Contract

1. Package/lock/source inventory, official support, advisory, image architecture/digest and license are current and traceable.
2. Static image build, context hygiene, runtime hardening, internal port, health and isolated HTTP/browser paths pass with revision evidence.
3. Root Compose/profile/tier/Traefik renders safely, retains admin-only access, and adds no host 80/443 or external app source include.
4. Synthetic external consumer imports a package with tested exports/types/CSS/peers/license/version.
5. Manifests match source revision and local docs-only MCP passes positive/negative protocol checks; remote MCP stays disabled.
6. Codex/Claude instructions distinguish official support, installed-client evidence and unexecuted external actions.
7. README, Guide/Policy/Runbook, derived projection, inventory, focused gates, review and rollback agree with source.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [SPEC-0201](../0201-home-infrastructure-diagnosis-and-work-design/spec.md)
- [SPEC-0205](../0205-storybook-dependency-refresh/spec.md)

## Open Questions

A reviewer group needs a separate owner decision; none is approved. No remote MCP OIDC audience/client is approved. Exact image pins/digests and package compatibility need implementation-time official verification. Stage 99 operations-subject allocation is stale at next 0100 while GDE/POL/RUN-0100 are already issued; reconcile it before allocating Storybook subject 0101. REQ-0027 and AD-0031 remain drafts and are not treated as approval.

## Operational Impact

The service is optional and does not join the current HOME named selection. Docker tests require context, port, network, volume, resource and cleanup preflight. Real DNS/TLS/identity, reviewer access, remote MCP, rollout and credentials require separate exact approval and evidence.
