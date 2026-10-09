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

`styles.css` holds the `--hy-*` tokens; `DESIGN.md` is left to separate
later work. Button 0.2.0 takes `variant`, `disabled` and
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

`DESIGN.md` then left this Spec for separate work (commit `9cd150bfc`), which
changed the Storybook source, so both images were rebuilt from `9cd150bfc` and
`verify --registry` passed again:

| Image | Digest (local and registry) | Attestation manifests | SBOM packages |
| --- | --- | --- | --- |
| `hy-home/storybook` | `sha256:46710e1934a22909ae6a20e6ee404a7a79184a2936cfbdbad35055904ae8f31c` | 1 | 71 |
| `hy-home/storybook-mcp` | `sha256:df54b9fd2ec3c7fbdbc3cc589291ebf307e35cf6db2524d15f49e8448d654897` | 1 | 166 |

Both serve `components.json` `a9cebb3d…` and `docs.json` `a8a5f84e…` with the
same lockfile and UI package 0.2.0. Compose and the tech-stack registry pin
`9cd150bfc` (commit `300b12a86`). The Storybook rehearsal passed 4 of 4 again
with `revision.json` naming `9cd150bfc`; no rehearsal container or network
remained. The export now holds the 9 allowlisted files.

### W7 Validation

The changed-profile local gate ran in a throwaway worktree with the candidate
staged on base `6011c9f4c`. Its first run failed
`test_current_repository_spec_packages_cover_spec_directories` because root
`DESIGN.md` existed. The owner then decided that root `DESIGN.md` is not the
design Storybook implements and is separate later work; commit `9cd150bfc`
removed it, its token parity test and its export entry, and restored the
guard. That changed the Storybook source, so W6 records the rebuild and
rehearsal at `9cd150bfc`.

CI `candidate-quality` failed twice before passing. One run was a Go toolchain
download error from `proxy.golang.org`, cleared by a rerun. The other was
`leaf.dependency-vulnerability-audit`: the GHSA-vfj7 acceptance named
`eslint-config-next` 16.3.8, and W4 moved it to 16.4.0. The owner approved
amending the chain to 16.4.0 on 2026-10-09 with the same advisory, the same
dev-only `braces` 3.0.3 path and the same expiry, `2026-10-10T15:00:00Z`
(commit `0fe1d933d`). The adapter run printed raw audit FAIL, production audit
PASS and `ACCEPTED_RISK`; CI matched.

Two later local gate runs exposed two test defects. The design export test
read `HEAD`, which the gate worktree points at the base; it now exports an
unreferenced commit of the index (commit `6169a8f1f`). The script manifest
test did not list `storybook_image.py` as runtime-mutating (commit
`412ec8298`). At `6169a8f1f` every other suite passed: 13, 15, 130, 645, 239,
304 (32 optional skips), 25, 59, 42, 36, 50 and 18 tests. CI passed at
`6169a8f1f`, and the owner merged PR #393 as `d9ed32b54`. The script manifest
fix and this record follow in a separate PR.

### W8 HOME Activation

On 2026-10-09 the owner named `experience` on HOME as the target, with the
Keycloak client it needs. In `hy-home.realm` the client scope `storybook-mcp`
(audience `https://storybook-mcp.hy.home.arpa/mcp`, `groups` with full path,
included in the token scope) and the public client `storybook-mcp-client`
(standard flow only; direct grants, implicit flow and service accounts off;
PKCE `S256`; the two loopback redirects; `storybook-mcp` optional) were made
with the admin CLI inside `keycloak`. No client secret exists, and the admin
password was read from its secret file without being printed. `storybook` and
`storybook-mcp` started with `--no-deps` from the images of `9cd150bfc`, the
last commit that changed Storybook source; `storybook_image.py verify
--registry` passed and the served `revision.json` names that commit. Traefik
already held `experience_ingress_net`, so it was not recreated.

Without a session, `/` and `/index.json` redirect to the Keycloak login, `/mcp`
answers 401 with `Bearer scope="storybook-mcp"` and the resource metadata URL,
the protected resource metadata answers 200 and other paths 404; TLS verifies.
The owner signed in as an `/admins` user and Storybook loaded. A login from
another workspace's Codex or Claude Code and a document tool call were not
run by the agent. The owner's first `codex mcp login` reached Keycloak and was
refused with `Invalid parameter: redirect_uri`: Codex sends
`http://127.0.0.1:33419/callback/<random>`, so the Codex redirect URI became
`http://127.0.0.1:33419/callback/*`. A later attempt from the owner's shell
failed before reaching the server (`error sending request`); from the HOME
shell five Codex logins and fifteen requests reached the server, so the cause
is in that client environment. After the redirect URI change the owner's
`codex mcp login hyhome_storybook` on the HOME server completed ("Successfully
logged in"); the browser ran on another device, so the callback reached the
server by forwarding the redirected URL. GDE-0101 now carries the consumer
check, the Codex callback, the cross-device callback, and Ubuntu and Windows
steps for the root CA, `NODE_EXTRA_CA_CERTS` and `CODEX_CA_CERTIFICATE`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Build contract | 1 | W1 | Unit tests; Alpine SHA check; trial build and verify | `cdbf5768a` | PASS | W1 Build Contract | accepted |
| Ingress checks | 2 | W2 | Static tests; missing-image failure | `f1ae14eb0` | PASS | W2 Ingress Regression | accepted |
| Shared UI | 3 | W3 | Story tests RED and GREEN; parity test (removed with `DESIGN.md`); tarball consumer | `73beaa382` | PASS | W3 Shared UI | accepted |
| Dependencies | 3 | W4 | Full checks on TypeScript 6.0.3; TypeScript 7 trials | `943108232` | PASS | W4 Dependencies | accepted |
| Remote MCP and export | 2, 4 | W5 | Node and unit tests; live local server | `f9977d135` | PASS | W5 Remote MCP, Design Export and Documents | accepted |
| Images and rehearsal | 1, 2 | W6 | Build, push, verify; Storybook and SSO rehearsals; export | `1554622b9`, `300b12a86` | PASS | W6 Images and Rehearsal | accepted |
| Validation | 5 | W7 | Changed gate; CI; npm risk amendment | `6169a8f1f`, `412ec8298` | PASS | W7 Validation | accepted |
| HOME activation | 2 | W8 | Keycloak client and scope read-back; image verify; no-session probes; owner admin login | `0df98f405` | PASS | W8 HOME Activation | accepted |
| Codex MCP login on HOME | 2 | W8 | Owner's `codex mcp login` after the redirect URI change | `0df98f405` | PASS | W8 HOME Activation | accepted |
| Remote-device MCP login and tool call | 2 | W8 | Login from another device; `docs-list` | — | NOT_RUN | W8 HOME Activation | pending |

## Review and Completion

Not complete. Open for the owner: sign in from another device after its DNS
and root CA are set, call the document tools (GDE-0101), and run `/design-sync` from an
exported bundle. SPEC-0222 extended the GHSA-vfj7 acceptance to
`2026-11-08T07:00:00Z` by the owner's approval. `DESIGN.md` is separate later
work.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
