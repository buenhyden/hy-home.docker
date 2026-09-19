---
title: "Native OIDC Service Migration"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0004"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
created: "2026-09-20"
---

# Native OIDC Service Migration

## Objective

Following the completed auth research documents, migrate services currently
behind OAuth2 Proxy to direct Keycloak OIDC where the installed product and
edition support it. The owner explicitly requested implementation and updated
operational documentation. Preserve existing users, data and effective access.

## Inputs

- [Spec](../spec.md), [Plan](../plan.md), and [research task](tsk-0003-keycloak-oidc-operations-research.md).
- Current tracked router, image and application-auth configuration.
- Primary upstream capability/configuration documentation and bounded runtime
  metadata; no secret-value output.

## Work Log

The bullets below are chronological history. The capability matrix and final
runtime evidence describe the current state; intermediate pending states are not
current blockers.

- Auth research completed in reviewed commit `3a4912678`, pushed to Draft PR #168.
- Read-only inventory found ForwardAuth routes for Open WebUI, Gatus, Terrakube
  API/UI/executor, Prometheus, Loki, Tempo, Alloy, cAdvisor, Pyroscope,
  Alertmanager, Pushgateway, Flower, n8n, SonarQube, Mailpit, Stalwart admin UI,
  ComfyUI, Ollama, Open Notebook and RedisInsight. Airflow, Kafbat UI, Grafana
  and OpenBao already have native/gateway-only declarations and are outside this
  migration set.
- Open WebUI is the strongest running candidate. The running image source exposes
  native OAuth/OIDC settings (`OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`,
  `OPENID_PROVIDER_URL`) and currently consumes trusted identity headers from
  OAuth2 Proxy. Existing user preservation matters: the local database has an
  existing administrator and no chat data; the staged migration must preserve the
  user identity/role and disable any temporary email-merge setting after human
  acceptance.
- Gatus supports `security.oidc` with issuer, redirect URL, client id, client
  secret, scopes and `/authorization-code/callback`. Its current upstream source
  sets the session cookie without explicit `Secure` or `HttpOnly`; do not remove
  the gateway boundary until that risk is patched or accepted with concrete
  evidence.
- Terrakube already declares a direct Keycloak issuer through its DEX/OIDC fields,
  but no Terrakube containers are running in the current snapshot and the tracked
  Compose still reuses `OAUTH2_PROXY_CLIENT_ID`. Correct it to a dedicated
  `home-terrakube` client only during a separate runtime acceptance window; keep
  existing ForwardAuth until API/UI/executor behavior is proven.
- A concrete Open WebUI/Gatus Compose/client-secret patch was prepared, but the
  automatic approval review rejected applying it because it would remove the
  current gateway ForwardAuth boundary, introduce new client secrets and enable
  application account auto-provisioning before service-specific login and
  negative-access evidence. The rejected action was not retried through another
  path.
- Unsupported services keep OAuth2 Proxy ForwardAuth. The main reasons are no
  application login surface, reverse-proxy-auth design, auth handled through
  Grafana/API paths, paid or edition-gated SSO, or a product contract that does
  not provide native Keycloak OIDC browser login in the installed deployment.

Capability matrix:

| Service | Current evidence | Native OIDC ruling | Action | Primary source |
| --- | --- | --- | --- | --- |
| Open WebUI | Running the declared Open WebUI image; native OIDC, gateway-standard only | Migrated | Dedicated client and native-only route; existing administrator identity preserved, signup/merge/password auth disabled | Running container source exposes `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `OPENID_PROVIDER_URL`, `ENABLE_OAUTH_SIGNUP` in `/app/backend/open_webui/config.py`; official docs: <https://docs.openwebui.com/features/sso/> |
| Gatus | Running reviewed `hy/gatus:local`; native OIDC, gateway-standard only | Migrated with reviewed patch | Dedicated client, exact subject, cookie/PKCE/data-route hardening, native-only route and internal-only metrics | Gatus OIDC source: <https://raw.githubusercontent.com/TwiN/gatus/master/security/oidc.go> |
| Terrakube | Not running; Compose declares Keycloak issuer but reuses OAuth2 Proxy client id | Candidate after runtime window | Use a dedicated `home-terrakube` client id and verify API/UI/executor auth before removing ForwardAuth | Current Compose: `infra/09-tooling/terrakube/docker-compose.yml`; Terrakube docs: <https://docs.terrakube.io/> |
| Prometheus, Alertmanager, Pushgateway | Running; routes use ForwardAuth | Keep ForwardAuth | These projects support web TLS/basic auth config, not native Keycloak browser OIDC login | Prometheus web config: <https://prometheus.io/docs/prometheus/latest/configuration/https/> |
| Loki, Tempo, Alloy, Pyroscope | Running; accessed mainly through Grafana or APIs | Keep ForwardAuth | Native browser OIDC login is not the auth model for these service endpoints in this stack | Grafana Loki auth docs: <https://grafana.com/docs/loki/latest/operations/authentication/> |
| Flower | Running Airflow image command `celery flower` | Keep ForwardAuth | Flower does not provide a first-party Keycloak/OIDC browser login contract in the installed path | Flower docs: <https://flower.readthedocs.io/> |
| n8n | Running community self-hosted image | Keep ForwardAuth | SSO is edition/plan gated; no unapproved paid feature migration | n8n SSO docs: <https://docs.n8n.io/user-management/saml/> |
| SonarQube | Compose route uses ForwardAuth | Keep ForwardAuth | Direct OIDC is not available as a free installed-edition assumption; do not replace with paid/unsupported SSO | SonarQube auth docs: <https://docs.sonarsource.com/> |
| Mailpit | Running `axllent/mailpit:v1.31.1` | Keep ForwardAuth | Mailpit has built-in/basic auth style controls, not native Keycloak OIDC UI login | Mailpit docs: <https://mailpit.axllent.org/docs/> |
| Stalwart admin UI | Route uses ForwardAuth | Keep ForwardAuth | OIDC backend support does not prove the admin UI can replace gateway SSO for this deployment | Stalwart OIDC backend docs: <https://stalw.art/docs/auth/backend/oidc/> |
| Ollama, ComfyUI, cAdvisor, Open Notebook, RedisInsight | Routes use ForwardAuth | Keep ForwardAuth unless a separate native auth contract is proven | No accepted native Keycloak OIDC browser login contract for the current tracked deployment | Tracked Compose files under `infra/08-ai`, `infra/06-observability` and `infra/11-laboratory` |

### Staged Execution

- A read-only delegated researcher exceeded its scope and restored/deleted other
  workers' in-progress files, then committed/pushed candidate documentation as
  `64d8200bd`. That agent was stopped. Owned implementation files were recovered
  from worker backups/source and reviewed again; history is corrected forward.
- Open WebUI SQLite online backup passed integrity verification. The sole existing
  administrator matches the sole enabled, email-verified Keycloak identity.
  Initial signup is disabled and the existing gateway remains in place.
- Dedicated `home-openwebui` confidential client was created with exact HTTPS
  callback/origin, S256 required, and implicit/direct/service-account flows off.
  Verified-TLS readback passed before writing its ignored client-secret file.
- Target-only recreation preserved the image and named data volume. Initial
  startup failed closed because UID 0 with all capabilities dropped cannot read
  UID 1000-owned mode-0600 bind files. Only the newly created client secret was
  transferred to root:root 0600 using a transient CHOWN-only container. The public
  root CA certificate was validated as certificate-only and made mode 0644. No
  secret values, data ownership, or long-running capabilities were changed.
- Earlier Keycloak admin-secret mode 0664 was narrowed to 0600, preserving its
  existing owner and contents. These permission changes are separate from the
  completed Task 0002 value-preserving metadata-prune evidence.
- Private/public metadata synchronization added the Gatus subject key and two
  client-secret registry IDs; prior private values were preserved. Protected
  pre-sync copies are under the dated OIDC migration custody directory.
- New Open WebUI and Gatus regression modules are registered in the existing
  Compose baseline gate. Gatus client/runtime rollout remains pending.

- Open WebUI recovered healthy after the permission correction. Runtime config
  confirms Keycloak provider, login form enabled and signup disabled; secret is
  root-owned 0600 and process effective capabilities remain zero. Anonymous
  `/api/v1/auths/` returns 401; OIDC initiation redirects to the expected Keycloak
  host with exact client/callback and S256. Human acceptance remains pending.
- Gatus implementation initially edited the live bind-mounted `config.yaml`,
  causing approximately ten minutes of crash-loop/unhealthy state (18 restarts).
  The original bytes were restored; Gatus recovered healthy without a manual
  restart at 2026-09-19T15:33:48Z. OIDC configuration was moved to a separate
  `config.oidc.yaml` for the later reviewed recreation. This was a runtime impact
  despite the absence of an explicit rollout command; no image/volume replacement
  or data restoration occurred.

- Owner confirmed Open WebUI Keycloak login and administrator menu. Blind DB
  comparison confirmed the same user ID/admin role, zero chats and exact Keycloak
  `oidc.sub`. A second online backup preserved the linked state. The installed
  per-key `Config.upsert` changed only `ui.enable_login_form` to false; all other
  config rows including timestamps and user/chat identities were unchanged.
- Initial operator-model invocation stopped before writes because its separate
  process lacked the existing startup secret environment. Initializing from the
  same existing key file enabled the reviewed one-key write without token forgery.
- Open WebUI merge is disabled and its route now retains only the standard gateway
  chain. A first password probe returned 400, which proved only invalid credentials.
  Installed source showed a separate `ENABLE_PASSWORD_AUTH` switch; false was added
  and a targeted restart performed to require explicit 403 password denial.
- Owner explicitly approved the concrete Gatus transition after automatic review
  required it. Dedicated client creation/readback passed. A brief Gatus-only stop
  produced a protected full data-directory archive; copied SQLite integrity passed.
  The old image was retained and original container restarted pending final patch.
- Final Gatus route review identified native auth gaps in metrics/badges/history.
  Broader data-route coverage is being patched before removing ForwardAuth; public
  bootstrap/health and independently bearer-authenticated ingestion are assessed
  separately. No claim of cross-application logout is made.

## Verification Evidence

Read-only verification completed on 2026-09-20: current Docker containers,
tracked Traefik labels, Open WebUI runtime source and Gatus upstream source were
inspected without printing secret values. This initial inventory preceded the staged execution above; it does not
represent the latest runtime state. No gateway middleware has yet been removed.

Final runtime evidence on 2026-09-20:

- Owner confirmed Gatus native login/status list and Open WebUI fresh Keycloak
  re-login/admin menu. Both final routers use only the standard gateway chain.
- Open WebUI: healthy; public anonymous auth API 401, real password signin 403,
  OIDC redirect 302 with correct client/callback/S256; signup/merge/password auth
  off. Identity/role/chat ownership preserved as recorded above.
- Gatus: healthy on reviewed image `sha256:c52ad9511a84a5738eda73155807acd5a2fe3842bd6a33f223fc570d308bba91`,
  same volume and UID 1000. Public status/badge/uptime/history requests return 401;
  bootstrap and health 200; malformed callback 400; OIDC login 302 with exact
  client/callback/S256 and Secure/HttpOnly/Lax state/nonce/verifier cookies.
  Public metrics, trailing-slash and query variants return 404; internal metrics
  returns 200 and Prometheus target `up` was 1.
- Gatus backup integrity and live DB integrity passed. Endpoint definitions and
  each of seven endpoints' last pre-migration result were preserved. This is
  preservation evidence, not an isolated full restore rehearsal.
- Exact other-subject denial is covered by patched Go regression tests; no second
  real Keycloak user was created for live rejection. Invalid/absent live sessions
  are rejected. Gatus has no proven RP logout; the owner explicitly accepted the
  maximum one-hour local-session lifetime in the exact rollout approval.
- Private/public environment keys match at 247, registry IDs at 93; metadata prune
  check reports zero drift. Existing private values remain preserved.
- Open WebUI seven Python regressions, Gatus eleven Python regressions, patched
  Go API/security tests and image build passed. Earlier Compose/metadata regressions
  passed 39 tests. Workflow contract, public AI/availability render, version
  projection, tier-06/08 hardening, Ruff and configured ShellCheck passed.
  A pre-existing informational SC2016 warning appears only without the repository's
  configured warning severity. Final documentation gates are recorded below.

## Review Evidence

Automatic approval review rejected the combined Open WebUI/Gatus implementation
patch as too broad before exact service-level security acceptance. The materially safer implementation proceeds one service at a time with the
existing gateway retained until native-login acceptance. Automatic signup is
disabled. The owner already authorized scoped native migration; this candidate
matrix is an intermediate inventory, not completion evidence.

Final independent closure review passed specification, quality and security with
no blocking finding or public secret value. The final combined focused suite
passed 57 tests; document metadata selected eight changed documents with zero
violations, Markdown lint passed, and link checking passed 919 documents/7713
links. The staged secret scan passed. Python validation dependency resolution was
audited with no known vulnerabilities; the temporary resolution changed no
repository requirement or installed package.

The preceding remote CI run on `64d8200bd` failed on a pre-existing Storybook
TypeScript/ESLint compatibility issue, not native OIDC checks. Its minimal
compatibility correction pins the Storybook example's TypeScript to exact
`5.9.3`, the intersection of typescript-eslint's `<6.1` and tsconfck's `^5`
peer contracts, in its manifest and lock only. ESLint and other dependency
versions are unchanged. Clean npm install, lint, typecheck, dependency-tree check
and npm audit all passed; no known npm vulnerability was reported. Independent
review approved the two-file correction. Existing Storybook addon/Vitest peer
range debt was not expanded or hidden: lock-only regeneration needed force for
that pre-existing resolution, but subsequent clean `npm ci` passed without it.
Fresh hosted CI is pending the final push.

The OIDC implementation is committed as `e3fd3c7`. The normal pre-commit hook
initially mistook a quoted environment placeholder for a credential. Equivalent
YAML block-scalar syntax resolved that false positive without disabling hooks;
parsed YAML equality and eleven Gatus tests passed. Exact-path Git whitespace
attributes preserve mandatory unified-diff context markers without changing the
patch or suppressing other paths' checks. Final narrow review passed both changes.

## Commit Ledger

Use separate reviewed commits on `codex/openbao-bootstrap-access` and PR #168.
No protected-branch push, force push, merge or protection change is authorized.

## Rulings

The owner's migration instruction authorizes the necessary scoped configuration,
Keycloak integration and service rollout for confirmed targets. It does not
approve paid licensing, new auth plugins, new identity providers, unrelated
service changes, data deletion or blanket administrator access. Unsupported
services retain their existing protection and receive an explicit explanation.

## Deferred Items

Open WebUI and Gatus are migrated. Terrakube remains behind ForwardAuth because
it is not running and its API audience validation is not established; no optional
IaC stack was started for this auth change. Unsupported/edition-gated services
retain the documented proxy boundary. OpenBao recovery custody and isolated
restore limitations remain in Task 0002.
