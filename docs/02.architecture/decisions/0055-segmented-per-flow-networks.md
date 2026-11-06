---
title: "Segmented Per-Flow Networks"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "ADR-0055"
parent_ids:
- "AD-0026"
created: "2026-11-06"
---

# ADR-0055: Segmented Per-Flow Networks

## Context

The root `docker-compose.yml` declares segmented networks (SPEC-0180 S05,
AD-0026), each with an explicit `/24` in `10.250.0.0/16`: for example
`edge_net` `10.250.1.0/24`, `mng_data_net` `10.250.2.0/24`, `object_net`
`10.250.3.0/24` and the internal `seaweed_internal` `10.250.4.0/24`. Each
network carries only the flows named in GDE-0077, and a service joins a
network only for a peer it uses. Fixed addresses remain only where a consumer
needs one: Traefik at `10.250.1.2` on `edge_net`, whose dynamic range starts at
`.128`, and a few service-local addresses (RedisInsight, Crawl4AI). No HOME
Compose file declares `infra_net`.

### Traceability

This record replaces ADR-0026, deleted in the same change (ADR-0051). ADR-0026
put every infrastructure service on one `infra_net` fixed at
`${INFRA_SUBNET:-172.19.0.0/16}`, required every included file to declare it,
kept extra networks such as `k3d-hyhome` alongside it, and gave each service a
static `ipv4_address`. It rejected Docker's automatic CIDR (addresses change
with start order) and an external IPAM service (too heavy for local Compose).
Its rejection of automatic CIDR and of external IPAM carries forward, as does
keeping an existing extra network when joining one; the single flat network and
blanket static addresses are withdrawn. Some LAB sources (for example
`labs/couchdb`) still use `infra_net` host names; LABs are outside this
decision until promoted. Evidence is the current repository configuration; no
runtime state is claimed.

## Decision Drivers

- A flat network lets any container reach any other; segmentation limits blast
  radius.
- Subnets must be explicit so Docker's automatic pool never takes one first.
- Static addresses are maintenance cost and should exist only where needed.

## Options

### Alternatives

- One flat `infra_net` with static addresses: rejected; every service can reach
  every other, and the address plan grows with each service.
- Docker automatic CIDR: rejected; ranges and addresses change with start
  order.
- External IPAM service: rejected; too much machinery for a single-host
  Compose platform.
- Explicit per-flow `/24` networks with fixed addresses only where required:
  selected.

## Decision

1. The root Compose declares each network with an explicit `/24` subnet inside
   `10.250.0.0/16`. A network that needs no egress is `internal: true`.
2. A network carries only the flows GDE-0077 names for it. A service joins a
   network only for a peer it uses.
3. A fixed `ipv4_address` is used only where a consumer depends on it, such as
   Traefik at `10.250.1.2`; the network keeps its dynamic `ip_range` clear of
   fixed addresses.
4. A service already attached to a network outside this plan keeps that
   attachment when it joins a segmented network.
5. Adding or changing a network updates GDE-0077 in the same change.

## Consequences

- Positive: a compromised container reaches only the peers it is wired to.
- Positive: explicit subnets avoid collisions with Docker's automatic pool.
- Trade-off: a new peer relationship needs a network edit, not just a host
  name.
- Trade-off: `10.250.0.0/16` can still collide with another local network.

### Compliance

`scripts/hardening/check-all-hardening.sh` checks service network membership
(for example `check_service_network` for RedisInsight on `mng_data_net`).
Project application networks and database cluster interconnects stay out of
scope.

### Follow-up

Requirement and description text that still names `infra_net` is reconciled by
its owners.

## Related Documents

- [REQ-0023 Network standardization](../../01.requirements/0023-standardize-infra-net.md)
- [AD-0026 Network architecture](../descriptions/0026-standardize-infra-net.md)
- [GDE-0077 IP address management](../../05.operations/guides/02-gateway-and-networking/0077-ip-address-management.md)
