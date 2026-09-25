---
title: "hy-home.k8s Integration Usage Guide"
version: "1.3.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "operations"
artifact_id: "GDE-0096"
parent_ids:
- "POL-0096"
created: "2026-09-23"
---

# hy-home.k8s Integration Usage Guide

## Usage

### Purpose

The hy-home.k8s repository runs a k3d cluster (`hyhome`) on the same host.
Since the k3d removal no Compose service shares a Docker network with it: the
cluster reaches this stack only through the host address `192.168.0.13`, and
OpenBao reaches the cluster API the same way. This guide describes that
contract; the [runbook](../runbooks/0096-k8s-integration.md) is the end-to-end procedure that sets it up
and repeats it after each cluster rebuild.

### Contract

| Consumer in the cluster | Endpoint | Authentication | Owner here |
| --- | --- | --- | --- |
| External Secrets Operator | `https://openbao.hy.home.arpa` (Traefik `192.168.0.13:443`) | OpenBao Kubernetes auth, role `eso-read-platform` | [OpenBao](0085-openbao.md) |
| Cluster bootstrap (before ESO) | same | `k8s-bootstrap` token, two hours | OpenBao |
| Alloy metrics (remote write), Argo Rollouts analysis | `https://prometheus.hy.home.arpa/api/v1/write`, `/api/v1/query*` | Basic Auth from OpenBao `secret/platform/prometheus-api` (source `PROMETHEUS_API_USERNAME`, `OBS-013`) | [Prometheus](0045-prometheus.md) |
| Kiali queries | `https://prometheus.hy.home.arpa` (only `/api/v1/` passes) | same | Prometheus |
| Kiali Grafana links | `https://grafana.hy.home.arpa` | bearer token of the Viewer service account `k8s-kiali`, from OpenBao `secret/platform/grafana-api` | [Grafana](0041-grafana.md) |
| Alloy logs | `http://192.168.0.13:3100` (Loki push) | none | Loki |
| Traces | `http://192.168.0.13:3200` (Tempo) | none | Tempo |
| Argo CD cache | `192.168.0.13:26379` (`mng-valkey`) | Valkey password (`CACHE-007`, delivered through OpenBao `platform/argocd`) | [Management database](0028-management-database.md) |
| Apps needing PostgreSQL (optional) | `192.168.0.13:15432` write, `15433` read | database credentials through OpenBao `platform/postgres-app` | `postgres-ha` profile |
| OpenBao to the cluster | `https://192.168.0.13:6550` (k3d API) | the cluster CA in `auth/kubernetes/config` | OpenBao |

Not provided: Grafana on a host port or with anonymous access (an owner
decision; Kiali uses the Viewer token instead), and Alloy OTLP on `4317/4318` (the
HOME Alloy configuration has no OTLP receiver). Traefik has no
`*.k8s.hy.home.arpa` route: the unauthenticated catch-all to the native k3s
NodePort was removed on 2026-09-24 (no request in the prior seven days).

### What hy-home.k8s needs from this side

| Item | Where it lives | How it is handed over |
| --- | --- | --- |
| Gateway CA | `secrets/certs/rootCA.pem` (mkcert root, public) | copy |
| Prometheus API credential | OpenBao `secret/platform/prometheus-api` (`username`, `password`), from `.env` `PROMETHEUS_API_USERNAME` and `secrets/observability/prometheus_api_password.txt` | ESO sync; no manual copy |
| Kiali Grafana token | OpenBao `secret/platform/grafana-api` (`token`), issued by the runbook for 90 days | ESO sync; no manual copy |
| Bootstrap token | `/tmp/bao-k8s/k8s-bootstrap.token` (created by the runbook) | protected channel, used within two hours |
| Name resolution | `openbao.hy.home.arpa`, `prometheus.hy.home.arpa`, `grafana.hy.home.arpa` → `192.168.0.13` | cluster DNS entry |

The cluster side also owns a `system:auth-delegator` ClusterRoleBinding for
the ESO service account, egress to `192.168.0.13` ports 443, 3100, 3200 and
26379, and the `cluster` external label on remote-written series.

### Common Pitfalls

- A single-file Docker secret keeps the inode it had when the container was
  created: after a secret file is regenerated, recreate its consumer (Traefik
  for `INFRA-007`).
- `curl` from the host returns `000` when the name does not resolve; the host
  `/etc/hosts` has only a few `hy.home.arpa` names, so use `--resolve`.
- In zsh, a variable holding several `curl` options is not split; write the
  options out.
- A new Prometheus API password must also reach OpenBao
  `secret/platform/prometheus-api`; otherwise the cluster's remote write gets
  `401`. The runbook's rotation section does all three places together.

## Common Checks

- `bash scripts/operations/gen-secrets.sh --sync-metadata-check` (exit 0)
- `bash scripts/hardening/check-all-hardening.sh` (route, policy and middleware pins)
- `docker network inspect k3d-hyhome --format '{{range .Containers}}{{.Name}} {{end}}'` lists only `k3d-hyhome-*` containers

## Runbook Handoff

Follow the [runbook](../runbooks/0096-k8s-integration.md) for first setup, every cluster rebuild and
credential rotation.

## Traceability

- [Policy](../policies/0096-k8s-integration.md) (`POL-0096`)
- [Runbook](../runbooks/0096-k8s-integration.md) (`RUN-0096`)
- [Compose network segmentation architecture](../../02.architecture/descriptions/0026-standardize-infra-net.md)

## Related Documents

- [OpenBao runbook](../runbooks/0085-openbao.md)
- [Prometheus policy](../policies/0045-prometheus.md)
- [Traefik guide](0013-traefik.md)
