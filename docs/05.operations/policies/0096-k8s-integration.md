---
title: "hy-home.k8s Integration Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0096"
parent_ids:
- "AD-0026"
created: "2026-09-23"
---

# hy-home.k8s Integration Operations Policy

## Overview

The hy-home.k8s cluster uses a fixed set of endpoints on the host address and
two OpenBao auth paths. This policy fixes that set, its authentication, and
the handling of the credentials exchanged between the two repositories.

## Policy Scope

Endpoints the cluster may call, OpenBao Kubernetes auth and the bootstrap
token, the Prometheus HTTP API credential, and hand-off of values across the
repository boundary.

## Controls

- The cluster reaches this stack only through `192.168.0.13`. No Compose
  service joins a k3d network again, and no fixed address is reserved for the
  cluster.
- OpenBao is reached through the Traefik route without SSO or an IP allowlist
  (ESO logs in from the cluster). OpenBao authorization is the control: the ESO
  role binds only `external-secrets/external-secrets` with audience `vault`
  and reads only `secret/platform/*`.
- The bootstrap token comes only from the `k8s-bootstrap` token role: orphan,
  policy `k8s-bootstrap`, lifetime at most two hours, requested explicitly on
  each issue. A longer-lived token is revoked on sight.
- The OIDC operator may update `auth/kubernetes/config`, issue bootstrap
  tokens, and update `secret/platform/prometheus-api` for a credential
  rotation, `secret/platform/grafana-api` for a token reissue and
  `secret/platform/notifications` for a Slack token replacement. Enabling
  the method, writing policies and roles, and writing `secret/platform/*`
  need an approved temporary-root session that ends with revocation.
- Prometheus is reachable from the cluster only through `/api/v1/` with Basic
  Auth (`INFRA-007`). The cluster gets the credential only through OpenBao
  `secret/platform/prometheus-api`, which changes in the same rotation as
  `OBS-013` and `INFRA-007`; no Prometheus host port is published and the UI keeps
  SSO. Grafana gets no host port and no anonymous access; Kiali reads it with
  the token of the Viewer service account `k8s-kiali` (90 days) from
  `secret/platform/grafana-api`.
- Loki `3100`, Tempo `3200` and `mng-valkey` `26379` stay published on all
  host interfaces without gateway authentication (Valkey keeps its password).
  This is an accepted LAN exposure for the cluster; narrowing it needs the
  same review as adding an endpoint.
- Values cross the repository boundary only through files or a protected
  channel: never chat, issue text, command arguments or logs. Evidence records
  names, booleans and non-secret fields only.

## Exceptions

None. A new endpoint, a different authentication or a longer token lifetime
needs a reviewed change to this policy and the guide's contract table.

## Verification

- Hardening pins the Prometheus API route, its middleware and `usersFile`, and
  keeps the two k8s OpenBao policies read-only and wildcard-free.
- The runbook's checks: 401 without and 200 with the Prometheus credential,
  role and config reads, the bootstrap token's policies, orphan flag and TTL,
  and allow/deny reads.

## Review Cadence

On every hy-home.k8s change that adds a consumer, on an OpenBao or Traefik
upgrade, and when a credential is rotated.

## Traceability

- [Guide](../guides/0096-k8s-integration.md) (`GDE-0096`)
- [Runbook](../runbooks/0096-k8s-integration.md) (`RUN-0096`)
- [OpenBao policy](0085-openbao.md)

## Related Documents

- [OpenBao ESO read policy](../../../infra/03-security/openbao/config/policies/eso-read-platform.hcl)
- [OpenBao operator policy](../../../infra/03-security/openbao/config/policies/operator.hcl)
- [Prometheus policy](0045-prometheus.md)
