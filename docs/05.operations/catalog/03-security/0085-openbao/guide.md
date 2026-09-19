---
title: "OpenBao Guide"
version: "0.2.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0085"
parent_ids:
- "POL-0085"
created: "2026-09-19"
---

# OpenBao Guide

## Usage

HOME secret control plane; Vault remains a separate migration source.

Profiles: `core / security / secrets`. Services: `openbao openbao-agent`. Root Compose owns inclusion.

Raft data, AppRole bootstrap material and rendered output use separate bind volumes. Agent config must be mounted at the command path; rendered files must stay under /openbao/out. VAULT_ADDR overrides the HCL server address.

[Implementation](../../../../../infra/03-security/openbao/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

**Administrator access.** Human administrator access is Keycloak-backed OpenBao native OIDC, not the
gateway SSO session in front of the UI. Keycloak or OAuth2 Proxy can protect the
HTTP route, but OpenBao still needs its own `jwt/oidc` auth method before a
browser user receives an OpenBao token with OpenBao policies. The OpenBao OIDC
documentation requires OpenBao and the OIDC provider redirect URIs to match; the
UI callback shape is `/ui/vault/auth/{path}/oidc/callback`. Verification date:
2026-09-19. Source: <https://openbao.org/docs/auth/jwt/>.

The configured HOME identity mapping is:

| Field | Value | Purpose |
| --- | --- | --- |
| Realm | `hy-home.realm` | Keycloak realm that owns the human identity. |
| Client | `home-openbao` | Keycloak OIDC client for OpenBao native OIDC. |
| Group | `/openbao-admins` | Human operator group allowed to request admin policy. |
| OpenBao OIDC role | `home-admin` | OpenBao role bound to the exact Keycloak group claim. |
| OpenBao policy | `hy-home-operator` | Least-privilege non-root operator policy. |
| Current user | `hyunyoun` | Existing user assigned to the dedicated operator group. |

Open the OpenBao UI at `https://openbao.hy.home.arpa/ui/`, choose **OIDC**,
enter role `home-admin` if prompted, and sign in with the existing Keycloak
account. The initial root token and the temporary recovery root token have both
been revoked; neither is a login credential. The human password belongs to
Keycloak, not to a new local OpenBao account. No password or token is recorded in
this guide. The owner confirmed a successful OIDC login; server-side metadata
confirmed only `default` and `hy-home-operator` policies on that session.

For CLI access on a host that can resolve the HOME domain and trusts its CA:

```bash
export BAO_ADDR=https://openbao.hy.home.arpa
bao login -method=oidc -path=oidc role=home-admin
```

The CLI stores an OpenBao token through its token helper; protect that local
file. Gateway browser SSO may prevent non-browser API access on the public route;
use an approved API transport rather than bypassing gateway authentication or
TLS verification. The configured callbacks are the exact UI path
`https://openbao.hy.home.arpa/ui/vault/auth/oidc/oidc/callback` and CLI callback
`http://localhost:8250/oidc/callback`. The client requires S256 PKCE.

The [operator policy](../../../../../infra/03-security/openbao/config/policies/operator.hcl)
permits reading/updating only the Keycloak and Grafana KV values, issuing renderer
SecretIDs, reading Raft snapshots and initiating/cancelling authenticated quorum
root recovery. It does not grant root, secret deletion, arbitrary secret access,
policy changes or auth configuration changes. OIDC token TTL is one hour, with
four-hour maximum lifetime. Because broad list permissions are absent, navigate
to the known secret paths instead of expecting all secrets to appear in a list.

Never place a root token, unseal key, OIDC client secret, AppRole `role_id`,
AppRole `secret_id`, wrapping token or rendered secret on a command line, in a
guide, or in shell history.

**Credential boundaries.** Unseal keys, root tokens, OIDC human users, AppRole credentials and OIDC client
secrets are different controls:

| Material | Holder | Use | Normal lifetime |
| --- | --- | --- | --- |
| Unseal key share | Quorum holders | Unseal OpenBao after restart and approve quorum operations. | Offline, long-lived, never used for UI login. |
| Root token | Break-glass operators | Initial bootstrap or emergency repair only. | Short-lived; revoke after verified human admin and recovery path. |
| OIDC user session | Human operator | Normal OpenBao UI/CLI administration through `hy-home-operator`. | Finite human TTL from OpenBao role. |
| AppRole `role_id` and `secret_id` | Renderer or automation | Machine access for declared paths only. | Separate TTL/use-limit policy; never human admin. |
| Keycloak client secret | OpenBao OIDC backend | Trust OpenBao as a Keycloak OIDC client. | Stored as secret material; rotate on exposure. |

The server uses three Shamir shares with threshold two. Human OIDC acceptance,
renderer checks and the corrected recovery procedure are recorded in the
[current follow-up Task](../../../../03.specs/0180-home-dev-convergence/tasks/tsk-0002-openbao-access-and-env-convergence.md).
Snapshot creation and server restart/unseal were verified; isolated restore and
offline transfer of the shares remain separate operator responsibilities.

## Common Checks

Check selected services, declared mounts, published interfaces and container state before use. Readiness and data recovery remain unverified until the runbook evidence is collected.

## Runbook Handoff

[Runbook](runbook.md) owns commands, expected results and recovery. [Policy](policy.md) owns controls.

## Traceability

- Governing architecture: [AD-0003](../../../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)
- Official OpenBao OIDC auth method: <https://openbao.org/docs/auth/jwt/>
- Official OpenBao token model: <https://openbao.org/docs/concepts/tokens/>
- Official OpenBao seal/unseal model: <https://openbao.org/docs/concepts/seal/>
- Official OpenBao AppRole auth method: <https://openbao.org/docs/auth/approle/>
- Official Keycloak reverse proxy guidance: <https://www.keycloak.org/server/reverseproxy>

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
