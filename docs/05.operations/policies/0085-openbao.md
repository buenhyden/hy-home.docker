---
title: "OpenBao Policy"
version: "0.4.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0085"
parent_ids:
- "AD-0003"
created: "2026-09-19"
---

# OpenBao Policy

## Overview

HOME secret control plane; Vault remains a separate migration source.

## Policy Scope

`infra/03-security/openbao` and services `openbao openbao-agent` under profiles `core / security / secrets`.

## Controls

Keep unseal/recovery material offline. Never log token, role_id, secret_id or rendered files. Current status health accepts sealed state: container health alone does not prove secret delivery. Existing application Docker Secrets are not automatically replaced by Agent output.

Normal human administration must use a non-root OpenBao token issued through
OpenBao native OIDC backed by Keycloak. The accepted HOME binding is the
Keycloak group `/openbao-admins`, role `home-admin`, OpenBao OIDC client
`home-openbao`, and OpenBao operator policy `hy-home-operator`. The policy TTL
for human tokens must be finite. Gateway SSO in front of the OpenBao UI is only
HTTP access control and does not replace OpenBao native OIDC authorization.

### Prometheus Metrics Credential

Prometheus must authenticate to `sys/metrics` with a dedicated service token
whose only service policy is the tracked
`infra/03-security/openbao/config/policies/prometheus.hcl`. That policy grants
only `read` on `sys/metrics`. The token is manually issued into
`secrets/security/openbao_token.txt`, mounted only by Prometheus, and rotated
before its finite expiry. Do not enable unauthenticated metrics or reuse a root,
human operator, renderer AppRole or renderer sink token.

Applying the policy, issuing or revoking the token, writing its file and
recreating Prometheus are live credential/runtime changes that require a
separately approved maintenance record. Tracked policy, Compose and scrape
configuration prove only the source contract.

### hy-home.k8s Kubernetes Auth

The hy-home.k8s cluster authenticates through the `kubernetes` auth method.
Only the External Secrets service account (`external-secrets` in namespace
`external-secrets`, audience `vault`) may log in, through role
`eso-read-platform`, whose policy reads only the `secret/platform/argocd`,
`postgres-app` and `notifications` entries. A cluster bootstrap token comes only
from the `k8s-bootstrap` token role: orphan, two-hour TTL, policy
`k8s-bootstrap` (read `platform/argocd`). The OIDC operator may update
`auth/kubernetes/config` and issue that token on each cluster rebuild; enabling
the method, writing policies and roles, and writing the KV entries need an
approved root session. The OpenBao Traefik route stays without SSO or an IP
allowlist so the cluster can reach it.

Root tokens are bootstrap and break-glass material only. Do not revoke the last
usable root token until all of the following are verified in the same maintenance
record: a human OIDC login succeeds, the resulting OpenBao token has the
expected non-root policy, AppRole renderer access still reads only the two
declared KV paths, the root recovery method for the deployed OpenBao version is
documented, and root token revocation has been observed.

The upstream OpenBao release line documented in Traceability uses authenticated
`/sys/generate-root-token` endpoints for `operator generate-root`. When no privileged human or root token remains, an
Agent read-only token must not be promoted to call root-generation endpoints.
The deprecated unauthenticated `/sys/generate-root/*` endpoints are disabled by
default as of 2.5.3 <!-- runtime-version-exception: history — unauthenticated root generation was disabled upstream to close a recovery-path security exposure --> and may be re-enabled only as an explicitly approved
break-glass exception on a temporary loopback-only listener. The exception must
keep the same data volumes and seal configuration, must not restore a snapshot
by default, must be removed immediately after native OIDC administration is
verified, and must end with revocation of the recovered root token.

[Implementation](../../../infra/03-security/openbao/docker-compose.yml) and [version projection](../../../infra/tech-stack.versions.json) own runtime pins.

## Exceptions

Owner @buenhyden must record scope, risk, expiry and exit condition before any deviation. Static configuration is not evidence of live backup or recovery.

The only approved shape for temporary unauthenticated generate-root recovery is
a loopback-only listener with `disable_unauthed_generate_root_endpoints = false`
for the duration required to generate a replacement root token and establish the
normal OIDC administrator path. The setting is forbidden on public or gateway
listeners and cannot remain in the steady-state configuration.

## Verification

Compose/profile validation and the [runbook](../runbooks/0085-openbao.md) provide separate static and runtime evidence. Stop on unexpected service, mount, authentication or readiness state.

## Review Cadence

Review monthly and before image, persistence, authentication or exposure changes.

## Traceability

- Governing architecture: [AD-0003](../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](../guides/0085-openbao.md), [Policy](0085-openbao.md), [Runbook](../runbooks/0085-openbao.md)
- Official OpenBao TCP listener parameters: <https://openbao.org/docs/configuration/listener/tcp/>
- Official OpenBao authenticated root generation API: <https://openbao.org/docs/api/system/generate-root-token/>
- Official OpenBao deprecated legacy root generation API: <https://openbao.org/docs/api/system/generate-root/>
- Official OpenBao deprecation note for unauthenticated generate-root: <https://openbao.org/community/deprecation/unauthed-generate-root/>
- Official OpenBao release notes for authenticated root generation: <https://openbao.org/community/release-notes/2-6-0/>

## Related Documents

- [Operations index](../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
- [OpenBao unauthenticated generate-root deprecation](https://openbao.org/community/deprecation/unauthed-generate-root/)
