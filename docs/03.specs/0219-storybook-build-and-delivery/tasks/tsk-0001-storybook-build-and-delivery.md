---
title: "Storybook Build and Delivery Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0219-TSK-0001"
parent_ids:
- "SPEC-0219-PLAN-0001"
created: "2026-10-09"
---

# Storybook Build and Delivery Task

## Objective

Make the Storybook images reproducible from one commit, prove the static and
MCP authorization paths in isolation, ship a token-based shared UI with tested
states, serve the docs MCP to other workspaces with Keycloak tokens, and bound
what reaches Claude Design.

## Inputs and Authorization

The current user request on 2026-10-09 asks to execute prompt 06 of the
analysis pack (Storybook build, Traefik and design tools) with per-unit
commits and a per-Spec PR merge. During the work the owner clarified that
Storybook and its MCP serve other workspaces, including clients on other
machines (remote MCP chosen), that `DEFAULT_URL` is `hy.home.arpa`, and that
dependencies move to their latest releases on TypeScript 6.0.3 with
TypeScript 7 kept in view. Baseline `main` `6011c9f4c` (SPEC-0218 merged).
Creating the Keycloak client, starting `experience` on HOME and signing into
Claude Design are not part of this request.

## Work Log

### Starting State

The Compose pin `hy-home/storybook:e811e159a` named an image that was not
present on HOME and that no tracked procedure built; the Dockerfile defaulted
the revision to `uncommitted`. The shared package exported the create-storybook
Button with a free `backgroundColor`, and the example Header, Page and
Configure pages reached the component and docs manifests. The a11y addon only
reported violations. The docs MCP ran on the HOME loopback only. Local
`node_modules` predated the UI workspace, so the build failed until `npm ci`.

### W1 Build Contract

`scripts/operations/storybook_image.py` exports the committed source with
`git archive`, builds with SBOM and max provenance, optionally pushes to the
local registry, and verifies label, `revision.json`, lockfile, UI package and
manifest hashes. `revision.json` now records the lockfile hash and the UI
package. The Dockerfile refuses anything but a 40-character commit (checked
in Alpine against empty, `uncommitted`, short and non-hex values). A trial on
the previous source commit built with a local attestation manifest and
`verify` correctly failed because that commit's revision file lacked the new
fields. Commit `cdbf5768a`.

### W2 Ingress Regression

The SSO rehearsal's stack became a mixin; a Storybook ingress rehearsal builds
its routers from the Compose labels and runs the pinned image read-only behind
real Traefik, OAuth2 Proxy and Keycloak. A static test pins the image to a
commit with `pull_policy: never` and keeps `experience` out of HOME. With the
old pin the rehearsal fails with the build command, as intended. Commit
`f1ae14eb0`.

### W3 Shared UI

Root `DESIGN.md` uses the Project-Template token vocabulary, and a test keeps
it equal to `styles.css`. Button 0.2.0 takes `variant`, `disabled` and
`loading`; `AsyncState` covers loading, empty, error, 403 (no retry), timeout
and ready. Fourteen story tests cover keyboard, focus ring, retry and 320px
wrapping with the a11y addon in `error` mode; lowering one text colour failed
four stories on `color-contrast`, then passed when restored. The examples
left the manifest, which now lists only `AsyncState` and `Button`. A synthetic
consumer installed the packed 0.2.0 tarball and rendered the components.
Project-Template `6b1c739` has no consumer. Commit `73beaa382`.

### W4 Dependencies

`next` and `eslint-config-next` 16.4.0, `vite` 8.3.4 and `playwright` 1.64.0;
Storybook and `@storybook/mcp` 10.6.1 are the latest stable (11.0.0 is
alpha). TypeScript 7.0.2 and `7.1.0-dev.20261008.1` (no 7.1 beta is on npm)
were tried: Storybook build, docgen, story tests, MCP tests and the Next build
pass with `experimental.useTypeScriptCli: true`, but `typescript-eslint` 8.71.1
(latest and canary, range below 6.1.0) stops with "does not support TS 7.0",
and without the Next setting the build fails for the missing compiler API.
TypeScript stays 6.0.3. With it all checks pass. Commit `943108232`.

### W5 Remote MCP, Design Export and Documents

`mcp/server.ts` gains a remote mode: RS256 tokens checked against the Keycloak
discovery JWKS, issuer, audience equal to its own URL, lifetime with 30 s skew
and the reader group; 401 with `scope` and `resource_metadata`, 403
`insufficient_scope`, and RFC 9728 metadata on both paths. Node tests cover
eleven refusal cases. `esbuild` bundles the server for the Dockerfile `mcp`
target. Compose adds `storybook-mcp` on `edge_net` with the root CA and a route
limited to `/mcp` and the metadata path, without `sso-auth`. The rehearsal
gained an HTTPS issuer (throwaway CA) and remote MCP checks. The design export
script and allowlist, the operations catalog bindings and POL/GDE/RUN-0101
follow. Before commit: lint, typecheck, Storybook build with 9 artifact and
MCP tests, 14 story tests, the bundle and 148 Python tests (2 contract tests
then registered the MCP route as `oauth-bearer` and its Grafana coverage row).
A live run of the local server answered `initialize`, listed exactly the three
tools, returned `ui-*` entries, refused an out-of-scope tool, a forged Origin
and a non-loopback Host. Codex loaded a project-scoped definition and Claude
Code reported it pending approval; those definitions were removed because the
consumers are other workspaces. Commit `f9977d135`.

### W6 Images and Rehearsal

`storybook_image.py build --push` built both images from `f9977d135`, the
last commit that changed the Storybook source, and `verify --registry` passed:

| Image | Digest (local and registry) | Attestation manifests | SBOM packages |
| --- | --- | --- | --- |
| `hy-home/storybook` | `sha256:74ba9c7febb7ce1501f11b855825ad38d986b9ce74a8bb2f01893b50fdca6917` | 1 | 71 |
| `hy-home/storybook-mcp` | `sha256:2e4bae4a4e648cb6e94ef168610f1af05e9be30391d95e5092e96f00d283508f` | 1 | 166 |

Both serve `components.json` `ea453f81…` and `docs.json` `11d40fe0…`, record
lockfile `2b91d0ba…` and UI package 0.2.0, and carry the provenance build
argument with the commit; `registry:3` kept the attestations. Compose and the
tech-stack registry now pin both to the commit (commit `1554622b9`).

The Storybook rehearsal then ran 4 tests: anonymous and `bob` got 302 to the
HTTPS Keycloak or 401 on every path with no content or login page; `alice`
got the index, iframe, a script, a stylesheet, both manifests and
`revision.json` (commit `f9977d135`) with `no-store` and `frame-ancestors`,
and 404 for an unknown page; the MCP gave 401 anonymous, 200 with three tools
and `ui-button` for a scoped reader, 401 for a token without its audience,
403 `insufficient_scope` for `bob`, 200 metadata and 404 outside its route.
Its first run failed in the test client, which cut JSON bodies at 300
characters; `revision.json` is now returned whole. The SSO rehearsal passed 3
of 3 on the refactored stack. No rehearsal container or network remained.

The design export at `1554622b9` wrote the 10 allowlisted files and its
manifest; no story kept a `packages/ui` import.

### W7 Validation

Pending.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Build contract | 1 | W1 | Unit tests; Alpine SHA check; trial build and verify | `cdbf5768a` | PASS | W1 Build Contract | accepted |
| Ingress checks | 2 | W2 | Static tests; missing-image failure | `f1ae14eb0` | PASS | W2 Ingress Regression | accepted |
| Shared UI | 3 | W3 | Story tests RED and GREEN; parity test; tarball consumer | `73beaa382` | PASS | W3 Shared UI | accepted |
| Dependencies | 3 | W4 | Full checks on TypeScript 6.0.3; TypeScript 7 trials | `943108232` | PASS | W4 Dependencies | accepted |
| Remote MCP and export | 2, 4 | W5 | Node and unit tests; live local server | `f9977d135` | PASS | W5 Remote MCP, Design Export and Documents | accepted |
| Images and rehearsal | 1, 2 | W6 | Build, push, verify; Storybook and SSO rehearsals; export | `1554622b9` | PASS | W6 Images and Rehearsal | accepted |
| Validation | 5 | W7 | Changed gate | Pending | NOT_RUN | W7 Validation | pending |

## Review and Completion

Not complete. Open for the owner: create the Keycloak client scope and client
in GDE-0101, start `experience` on HOME, sign other workspaces' Codex and
Claude Code in, and run `/design-sync` from an exported bundle.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
