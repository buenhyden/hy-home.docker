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
| Open WebUI | Running `ghcr.io/open-webui/open-webui:v0.11.3-cuda`; trusted-header auth from OAuth2 Proxy headers | Candidate | Requires dedicated Keycloak confidential client, secret file, account-preservation check, then remove only the Open WebUI ForwardAuth chain after login/deny evidence | Running container source exposes `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `OPENID_PROVIDER_URL`, `ENABLE_OAUTH_SIGNUP` in `/app/backend/open_webui/config.py`; official docs: <https://docs.openwebui.com/features/sso/> |
| Gatus | Running `hy/gatus:local`; route uses `sso-errors@file,sso-auth@file` | Candidate after cookie hardening/acceptance | Requires dedicated Keycloak confidential client, `security.oidc` config, secret file and status-route login/deny evidence | Gatus OIDC source: <https://raw.githubusercontent.com/TwiN/gatus/master/security/oidc.go> |
| Terrakube | Not running; Compose declares Keycloak issuer but reuses OAuth2 Proxy client id | Candidate after runtime window | Use a dedicated `home-terrakube` client id and verify API/UI/executor auth before removing ForwardAuth | Current Compose: `infra/09-tooling/terrakube/docker-compose.yml`; Terrakube docs: <https://docs.terrakube.io/> |
| Prometheus, Alertmanager, Pushgateway | Running; routes use ForwardAuth | Keep ForwardAuth | These projects support web TLS/basic auth config, not native Keycloak browser OIDC login | Prometheus web config: <https://prometheus.io/docs/prometheus/latest/configuration/https/> |
| Loki, Tempo, Alloy, Pyroscope | Running; accessed mainly through Grafana or APIs | Keep ForwardAuth | Native browser OIDC login is not the auth model for these service endpoints in this stack | Grafana Loki auth docs: <https://grafana.com/docs/loki/latest/operations/authentication/> |
| Flower | Running Airflow image command `celery flower` | Keep ForwardAuth | Flower does not provide a first-party Keycloak/OIDC browser login contract in the installed path | Flower docs: <https://flower.readthedocs.io/> |
| n8n | Running community self-hosted image | Keep ForwardAuth | SSO is edition/plan gated; no unapproved paid feature migration | n8n SSO docs: <https://docs.n8n.io/user-management/saml/> |
| SonarQube | Compose route uses ForwardAuth | Keep ForwardAuth | Direct OIDC is not available as a free installed-edition assumption; do not replace with paid/unsupported SSO | SonarQube auth docs: <https://docs.sonarsource.com/> |
| Mailpit | Running `axllent/mailpit:v1.31.1` | Keep ForwardAuth | Mailpit has built-in/basic auth style controls, not native Keycloak OIDC UI login | Mailpit docs: <https://mailpit.axllent.org/docs/> |
| Stalwart admin UI | Route uses ForwardAuth | Keep ForwardAuth | OIDC backend support does not prove the admin UI can replace gateway SSO for this deployment | Stalwart OIDC backend docs: <https://stalw.art/docs/auth/backend/oidc/> |
| Ollama, ComfyUI, cAdvisor, Open Notebook, RedisInsight | Routes use ForwardAuth | Keep ForwardAuth unless a separate native auth contract is proven | No accepted native Keycloak OIDC browser login contract for the current tracked deployment | Tracked Compose files under `infra/08-ai`, `infra/06-observability` and `infra/11-laboratory` |

## Verification Evidence

Read-only verification completed on 2026-09-20: current Docker containers,
tracked Traefik labels, Open WebUI runtime source and Gatus upstream source were
inspected without printing secret values. No service restart, Keycloak client
mutation, secret creation or gateway middleware removal was performed in this
step.

Pending implementation verification for any approved candidate: Keycloak client
readback without secret output, config render, targeted service restart, successful
allowed-user login, denied-user rejection, logout/session behavior and rollback
proof.

## Review Evidence

Automatic approval review rejected the combined Open WebUI/Gatus implementation
patch as too broad before exact service-level security acceptance. The safer
outcome is this documented candidate matrix and explicit approval boundary.

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

Concrete targets and acceptance steps are being established. Existing OpenBao
recovery custody and isolated restore limitations remain in Task 0002.
