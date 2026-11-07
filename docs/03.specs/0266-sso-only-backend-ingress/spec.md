---
title: "SSO-Only Backend Ingress Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-07"
layer: "specs"
artifact_id: "SPEC-0266"
parent_ids:
- "REQ-0023"
- "AD-0001"
- "AD-0026"
created: "2026-11-07"
---

# SSO-Only Backend Ingress Specification

## Overview

### Intent

A Traefik backend that relies only on the gateway `sso-auth` middleware is
reachable from Traefik and from the peers its declared flows need, not from
every container on `edge_net`.

### Background

The D02 re-run on 2026-11-07 (SPEC-0212 TSK-0041, "D02 re-verification after
the LAB moves") rendered every profile and found that every routed backend
except RedisInsight and Storybook shares `edge_net` (37 peers). Any of those
containers can call another backend by service DNS without passing Traefik, so
a backend protected only by SSO is open to all of them. ADR-0055 says a
compromised container reaches only its wired peers, but the shared ingress
network wires every backend to every other one. The Traefik v3.7 Docker
provider reference makes no isolation claim: its `network` option only chooses
the network Traefik uses. RedisInsight (listener bound to its Traefik-only
ingress address) and Storybook (alone with Traefik on an internal ingress
network) already show the remedy. The owner chose on 2026-11-07 to fix this in
its own package. ADR-0061 records the decision.

## Scope

### In Scope

- The routed backends whose only access control is `sso-auth`. The 2026-11-07
  render lists Alertmanager, Alloy, cAdvisor, ComfyUI, Flower, Kafka Connect,
  Kafka REST Proxy, Loki, Mailpit, MLflow, Ollama, Prometheus, Pushgateway,
  Pyroscope, Qdrant, Schema Registry and Tempo; W1 confirms or corrects this
  list from source.
- One internal ingress network per in-scope backend, shared only with Traefik,
  and the `traefik.docker.network` label that makes Traefik use it.
- Named flow networks for flows that today exist only through `edge_net`. The
  2026-11-07 render found three: Alloy and Prometheus to `seaweedfs-s3`, and
  Grafana to Ollama.
- The root network declarations, the leaf Compose files, the render tests, and
  GDE-0077, AD-0026 and the affected service READMEs.

### Out of Scope

- Backends with their own login, OIDC or API credential (for example Keycloak,
  Grafana, n8n, OpenBao, OpenSearch, Open WebUI, Dozzle, kafbat-ui, Terrakube and
  Airflow). They stay on `edge_net` behind their own authentication.
- Changing any authentication, route rule, middleware or credential.
- LAB sources and runtime.
- Host publications, which SPEC-0212 TSK-0041 already pins.

## Contracts

### Normal Behavior

- Traefik reaches each in-scope backend over that backend's ingress network,
  and the existing route still requires SSO.
- Each flow W1 records keeps a working path over a named network that carries
  only that flow's peers.
- A container keeps every network it needs for its other declared flows.

### Error Behavior

- A container that is neither Traefik nor a declared flow peer of an in-scope
  backend shares no network with it, so a direct connection fails at the
  network layer.
- A render in which an in-scope backend is on `edge_net`, or shares a network
  with a container outside its declared peers, fails the test.

### Boundary Behavior

- A backend that also needs `edge_net` for its own outbound calls keeps it only
  if its listener can bind to the ingress address alone (the RedisInsight
  pattern); otherwise the outbound flow moves to a named flow network.
- A backend whose own authentication W1 finds keeps its current networks and
  is recorded as out of scope with its source.

### Constraints

- Each new network is `internal: true` with an explicit `/24` inside
  `10.250.0.0/16` that no existing network uses, and its dynamic range stays
  clear of any fixed address (ADR-0055).
- GDE-0077 changes in the same change as a network (ADR-0055 rule 5).
- The root Compose and its network declarations have one writer (D02).
- Static render evidence and live reachability evidence are recorded
  separately; neither proves the other.

## Acceptance Criteria

1. W1 records, for every routed backend on `edge_net`, its own authentication
   (present, absent or unknown, with the source line), each inbound and outbound
   flow, and the network that flow uses; it confirms or corrects the in-scope
   list and the `edge_net`-only flows.
2. Each in-scope backend leaves `edge_net`, joins one internal ingress network
   shared only with Traefik, and sets `traefik.docker.network` to it.
3. Each flow from criterion 1 has a named network carrying only its peers, and
   no other network membership of any service changes.
4. A render test fails when an in-scope backend is on `edge_net` or shares any
   network with a service outside Traefik and its declared flow peers.
5. GDE-0077, AD-0026 and each affected service README describe the new
   networks, and ADR-0061 is accepted.
6. In HOME, under its own approval, the affected services are recreated; each
   route still requires SSO, a direct connection from an `edge_net` peer is
   refused, each declared flow works, and a rollback to the previous networks is
   rehearsed.

## Failure Conditions

### Observable Failures

- A route returns 502/504 after the move because Traefik is not on the
  backend's ingress network or uses the wrong one.
- A flow from criterion 1 breaks (for example Prometheus scrapes or Grafana
  data sources fail).
- A new subnet collides with an existing network or with the host LAN.

### Stop Boundaries

- Stop before moving a backend whose flows W1 cannot fully name.
- Stop before any HOME recreation without its own approval, a maintenance
  window and the recorded previous network membership for rollback.
- Do not weaken or remove `sso-auth` or any other middleware to make a route
  work.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-sso-only-backend-ingress.md)
- [ADR-0061](../../02.architecture/decisions/0061-dedicated-ingress-for-sso-only-backends.md)
- [ADR-0055](../../02.architecture/decisions/0055-segmented-per-flow-networks.md)
- [REQ-0023](../../01.requirements/0023-standardize-infra-net.md)
- [AD-0026](../../02.architecture/descriptions/0026-standardize-infra-net.md)
- [AD-0001](../../02.architecture/descriptions/0001-gateway-architecture.md)
- [GDE-0077](../../05.operations/guides/02-gateway-and-networking/0077-ip-address-management.md)
- [D02 finding in SPEC-0212 TSK-0041](../0212-request-baseline-and-reconciliation/tasks/tsk-0041-service-connection-contracts.md)
