---
title: "Storybook Build and Delivery"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0219"
parent_ids:
- "REQ-0027"
- "AD-0031"
created: "2026-10-09"
---

# Storybook Build and Delivery

## Overview

`projects/storybook/nextjs` and `infra/13-experience/storybook` serve shared UI
documentation to other workspaces: a static Storybook behind Traefik and
administrator SSO, and the same build's manifests through `@storybook/mcp`.
Before this package the Compose pin named an image that no procedure built,
the shared UI was the create-storybook Button with example Header and Page in
the manifest, the docs MCP ran only on the HOME loopback, and nothing defined
what may be sent to Claude Design. This package makes the image reproducible
from one commit, proves the ingress and authorization paths in isolation,
turns the UI into a token-based package with tested states, serves the docs
MCP remotely to authenticated clients, and bounds the design export.

## Scope

In scope: the Storybook workspace and its UI package, the Dockerfile, the
image build and verification script, the Compose services and routes, the
remote docs MCP and its token checks, the design export,
the rehearsal and unit tests, and the operations documents. Out of scope:
creating the Keycloak client on HOME, starting the `experience` profile on
HOME, signing into Claude Design, changing other workspaces' files, and the
TypeScript 7 upgrade, which waits for `typescript-eslint` support, and a
`DESIGN.md`, which is separate later work.

## Contracts

1. Build input. An image is built only from `git archive` of the commit that
   last changed the Storybook source, with `npm ci` against its lockfile. The
   Dockerfile refuses a build without a 40-character commit. The static and
   MCP images carry that commit as their OCI revision label and in
   `revision.json`, with the lockfile SHA-256, the UI package name and version
   and the manifest SHA-256 values. No secret enters a build argument, layer or
   static file.
2. Delivery. A local preload loads both images; the registry path pushes them
   to the local registry with SBOM and max provenance attestations. Compose
   pins `hy-home/storybook:<commit>` and `hy-home/storybook-mcp:<commit>` to
   the same commit with `pull_policy: never`, so a missing image fails the
   start. HOME never selects the `experience` profile.
3. Static origin. The origin stays unprivileged, read-only, on the internal
   `experience_ingress_net`, behind `req-rate-limit`, `gateway-standard-chain`
   and `sso-auth`. Anonymous and non-administrator requests to the index,
   iframe, assets and manifests get a 302 to Keycloak or a 401, never content
   or a login page with 200; administrators get them with `no-store` and
   `frame-ancestors 'self'`.
4. Shared UI. The package CSS defines the `--hy-*` tokens. `Button` and `AsyncState` cover default, focus, disabled,
   loading, empty, error, 403, timeout and retry states, keyboard use, reduced
   motion and a 320px width, each proven by a story test with the
   accessibility addon failing on violations. Only these components reach the
   manifest. Consumers install a reviewed tarball.
5. Remote docs MCP. `storybook-mcp` serves only `docs-list`, `docs-show` and
   `docs-show-story` at `https://storybook-mcp.${DEFAULT_URL}/mcp`. It accepts a
   bearer token only when the RS256 signature, the Keycloak issuer, the audience
   equal to its own URL, the lifetime and the `/admins` group all hold; it
   answers 401 with protected resource metadata or 403 otherwise. Traefik
   forwards only `/mcp` and the metadata path. Browser cookies never
   authorize it. The loopback `mcp:docs` stays a development path.
6. Design export. Claude Design receives only a bundle of the committed files
   in `design-export.allowlist.json` and a hash manifest; the allowlist has no
   globs, parent paths, environment, secret or key files, and secret-shaped
   content stops the export.
7. Dependencies. The workspace uses the latest stable releases compatible with
   TypeScript 6.0.3; the TypeScript 7 conditions are recorded.

## Acceptance Criteria

1. A clean build from a commit yields both images whose labels, revision
   files, lockfile, package and manifest hashes match the commit, and the
   registry copies carry SBOM and provenance with the same digests.
2. The isolated rehearsal shows the static and MCP authorization results of
   contracts 3 and 5 with real Traefik, OAuth2 Proxy and Keycloak.
3. Story, accessibility, artifact, MCP, lint, type and build checks pass.
4. The design export contains exactly the allowlist and no secret-shaped data.
5. Operations documents, the gate contract and the service catalog match, and
   the changed gate passes. HOME, Keycloak and live client steps are recorded
   as not run.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-storybook-build-and-delivery.md)
- [Storybook policy](../../05.operations/policies/0101-storybook.md)
