---
title: "Dedicated Ingress for SSO-Only Backends"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-07"
layer: "architecture"
artifact_id: "ADR-0061"
parent_ids:
- "AD-0001"
- "AD-0026"
created: "2026-11-07"
---

# ADR-0061: Dedicated Ingress for SSO-Only Backends

## Context

ADR-0055 segments the root Compose into per-flow networks and states that a
compromised container reaches only the peers it is wired to. Traefik reaches
almost every routed backend over one shared network, `edge_net`, so every
backend is wired to every other. A backend whose only access control is the
gateway `sso-auth` middleware is therefore reachable without SSO by every
`edge_net` member through its service name. The 2026-11-07 render found
seventeen such backends among 38 `edge_net` members (SPEC-0266 W1). The Traefik v3.7 Docker
provider makes no isolation claim; its `network` option only picks the network
Traefik uses. Two backends already avoid the problem: Storybook shares an
internal ingress network only with Traefik, and RedisInsight binds its
listener to its Traefik-only ingress address.

## Decision Drivers

- SSO at the gateway must not be bypassable from a neighbouring backend.
- Keep ADR-0055's explicit, internal, per-flow networks.
- Change only what lacks its own authentication.
- Stay within Compose, without a service mesh or extra proxy.

## Options

### Alternatives

- Keep the shared `edge_net` and accept the risk: rejected; one compromised
  backend opens every SSO-only one.
- Add application credentials to each backend: rejected as the general fix;
  many of these services have no built-in authentication, and those that do
  differ in mechanism.
- Group backends on a few ingress networks: rejected; backends in a group can
  still reach one another.
- Bind each listener to a fixed ingress address (the RedisInsight pattern):
  kept only for a backend that also needs `edge_net` for outbound calls,
  because it needs a fixed address and an application bind setting.
- One internal ingress network per SSO-only backend, shared only with Traefik:
  selected.

## Decision

1. Each routed backend whose only access control is `sso-auth` is attached to
   one internal ingress network that only Traefik shares, and sets
   `traefik.docker.network` to that network.
2. Such a backend is not on `edge_net`. If it needs `edge_net` for its own
   outbound calls, it keeps `edge_net` only when its listener can bind to the
   ingress address alone.
3. A flow that today exists only through `edge_net` moves to a named network
   that carries only that flow's peers.
4. Backends with their own login, OIDC or API credential stay on `edge_net`.
5. ADR-0055's rules for subnets, `internal: true` and GDE-0077 updates apply to
   every new network.

## Consequences

- Positive: a compromised backend no longer reaches an SSO-only backend unless
  a declared flow connects them.
- Positive: the network graph states each backend's real peers.
- Trade-off: Traefik joins one more network per SSO-only backend, and each one
  consumes a `/24` in `10.250.0.0/16`.
- Trade-off: each moved backend needs a `traefik.docker.network` label, and a
  missing label shows up as a broken route.

### Compliance

A render test in `tests/validation/test_p02_service_contracts.py` fails when an
SSO-only backend is on `edge_net` or shares a network with anything other than
Traefik and its declared flow peers.

### Follow-up

SPEC-0266 confirms the backend list and flows, implements the networks, and
applies the change in HOME under its own approval. The owner accepted this
decision on 2026-11-07 together with the SPEC-0266 Spec and Plan.

## Related Documents

- [ADR-0055](0055-segmented-per-flow-networks.md)
- [AD-0026](../descriptions/0026-standardize-infra-net.md)
- [AD-0001](../descriptions/0001-gateway-architecture.md)
- [SPEC-0266](../../03.specs/0266-sso-only-backend-ingress/spec.md)
