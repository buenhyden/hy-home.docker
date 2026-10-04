---
title: "Shared Storybook and Documentation MCP Plan"
version: "1.0.1"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0206-PLAN-0001"
parent_ids:
- "SPEC-0206"
created: "2026-10-03"
---

# Shared Storybook and Documentation MCP Plan

## Objective

Implement Prompt 05 on the isolated Storybook dependency branch after written Spec, Plan and Task approval, with local source and verification separated from HOME and remote action.

## Dependencies

- Latest main/origin-main: `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; dependent feature base: `fbbea9123751c13588022cdb76213fd8b5a14b6e`. Recheck both before source mutation.
- SPEC-0205 local package refresh and the later bounded audit handling in the canonical quality policy. This Plan changes no dependency-security exception.
- Existing OAuth2 Proxy allows only Keycloak `/admins`; reviewer access requires later approval. No remote MCP audience/client exists.
- Official Storybook 10.6 MCP/manifests preview contract; verify exact package version and published API at implementation. Static Storybook and self-hosted docs MCP are different runtimes.
- Stage 99 operations subject allocator is reconciled with already-issued 0100 before subject 0101 registration. Current REQ-0027 and AD-0031 draft status is preserved.

## Execution Sequence

1. W1: Source and package contract — TSK-0001 reviews existing demo components, adds only an exportable shared subset, CSS/types/peer/license contract and synthetic consumer test. Enable and build components/docs manifests, then implement a local docs-only MCP with negative protocol tests. Scope only Storybook-owned files and focused validator.
2. W2: Static origin — TSK-0001 creates a confined multi-stage image and static-server configuration. Verify lockfile, source revision, build context, static routes and browser behavior in a task-owned isolated environment after Docker preflight.
3. W3: Root integration — TSK-0002 is sole writer of new experience Compose, root include, profile policy, version projection, Stage 99 registry and Stage 05 subject. Use existing admin-only SSO and an internal ingress network joining only Traefik and Storybook; do not attach Storybook to shared edge_net. No MCP service, port or remote route enters root Compose. Recheck exact gateway/identity contracts before writing.
4. W4: Documentation and review — TSK-0002 updates Korean template-shaped READMEs, Guide/Policy/Runbook and Codex/Claude instructions. Run scoped Compose, hardening, operations catalog, doc and path-aware checks; inspect rendered delta. Independent reviewers judge source/security/docs. Record all exits and unsupported runtime claims.

## Risk and Rollback

| Risk | Control and rollback |
| --- | --- |
| Dependency audit handling | Use the canonical quality policy and gate contract; this Plan adds no blanket override or forced update. |
| Manifest/MCP preview API drift | Lock exact compatible versions; test protocol and rebuild from source; revert only TSK-0001 files. |
| Static asset or package data leak | Narrow Docker context, inspect built assets, use synthetic fixtures; stop and discard only task-owned outputs. |
| Browser/MCP auth confusion | Browser uses current admin SSO on a dedicated ingress network; remote machine MCP stays disabled pending approved issuer/audience/client. |
| Root profile or route conflict | Render scoped root profiles and service graph; revert only TSK-0002 configuration, not HOME containers/data. |
| Operations ID collision | Reconcile existing 0100 before allocating 0101; do not reuse an issued ID. |

## Verification

Run existing npm lint, typecheck, Next and Storybook builds, browser coverage, and Storybook contract checker; add one focused check for export/manifest/MCP behavior. For infrastructure, run the registered Compose/static helper, hardening and operations catalog plus changed-path gate. Before any container test, record Docker context, task project, ports, networks, volumes, resources and exact cleanup. HOME TLS/OIDC, remote MCP, Claude Design account and deployment remain Stage 05 operational follow-ups until separately approved and observed.

Completion evidence summary:

| Work unit | Completion evidence | Durable owner |
| --- | --- | --- |
| W1: source and package contract | PASS: TSK-0001 records reviewed UI package exports/types/CSS/peers/license/version, manifest generation, local docs-only MCP protocol checks, synthetic consumer and source review. | TSK-0001, UI package README |
| W2: static origin | PASS: TSK-0001 records exact-SHA image build, isolated HTTP/browser/a11y checks, context hygiene, runtime hardening and cleanup. No fresh image or HOME run is claimed by this completion receipt. | TSK-0001, Dockerfile |
| W3: root integration | PASS: TSK-0002 records optional `experience` profile, dedicated internal ingress, admin-only browser route, profile policy, version/inventory projections and focused Compose/quickwin gates. | TSK-0002, POL-0101 |
| W4: documentation and review | PASS: TSK-0002 records Stage 05 Guide/Policy/Runbook, Codex/Claude guidance, operations catalog, links, metadata and independent source/security/policy reviews. | GDE/POL/RUN-0101, TSK-0002 |

The remaining HOME TLS/OIDC/session, reviewer group, remote MCP audience/client, credential, DNS and external design-account actions are operational follow-ups with named Stage 05 owners and triggers, not unfinished work inside this source/static Plan. Fresh source/static batch evidence from 2026-10-04 reports Storybook contract, core/experience render, version92 and combined 25 unittests PASS; no Docker/HOME run is added here. No archive is created by this change; archival waits for a later protected SHA.

## Rulings

No new business app, speculative 07/08 UI, second gateway, user-global client install, external design upload or new reviewer group. Prefer official `@storybook/mcp` over a second custom MCP protocol implementation; the dev-only addon is not required for a self-hosted docs-only service. Do not count a static server as MCP success. The 13-experience tier becomes real only with built shared services and a registered optional profile.
