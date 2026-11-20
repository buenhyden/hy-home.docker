---
title: "Segmented Per-Flow Networks"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0055"
parent_ids:
- "AD-0026"
created: "2026-11-06"
---

# ADR-0055: Segmented Per-Flow Networks

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

The root `docker-compose.yml` declares segmented networks (SPEC-0180 S05,
AD-0026), each with an explicit `/24` in `10.250.0.0/16`: for example
`edge_net` `10.250.1.0/24`, `mng_data_net` `10.250.2.0/24`, `object_net`
`10.250.3.0/24` and the internal `seaweed_internal` `10.250.4.0/24`. Each
network carries only the flows named in GDE-0077, and a service joins a
network only for a peer it uses. Fixed addresses remain only where a consumer
needs one: Traefik at `10.250.1.2` on `edge_net`, whose dynamic range starts at
`.128`, and a few service-local addresses (RedisInsight, Crawl4AI). No HOME
Compose file declares `infra_net`.

- A flat network lets any container reach any other; segmentation limits blast
  radius.
- Subnets must be explicit so Docker's automatic pool never takes one first.
- Static addresses are maintenance cost and should exist only where needed.

###### Sources
<!-- core-payload-level:4 -->

Evidence is the current repository configuration; no runtime state is
claimed.

- [REQ-0023 Network standardization](../../01.requirements/0023-standardize-infra-net.md)
- [AD-0026 Network architecture](../01.descriptions/0026-standardize-infra-net.md)
- [GDE-0077 IP address management](../../05.operations/01.guides/02.gateway-and-networking/0077-ip-address-management.md)

##### Decision Scope

This decision covers the networks of the root Compose. Project application
networks and database cluster interconnects stay out of scope. Some LAB
sources (for example `labs/couchdb`) still use `infra_net` host names; LABs are
outside this decision until promoted.

#### Options

##### Considered Options

- One flat `infra_net` with static addresses: rejected; every service can reach
  every other, and the address plan grows with each service.
- Docker automatic CIDR: rejected; ranges and addresses change with start
  order.
- External IPAM service: rejected; too much machinery for a single-host
  Compose platform.
- Explicit per-flow `/24` networks with fixed addresses only where required:
  selected.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| One flat `infra_net` with static addresses | The ADR records no benefit for this option. | Every service can reach every other, and the address plan grows with each service. | Rejected; every service can reach every other, and the address plan grows with each service. |
| Docker automatic CIDR | The ADR records no benefit for this option. | Ranges and addresses change with start order. | Rejected; ranges and addresses change with start order. |
| External IPAM service | The ADR records no benefit for this option. | Too much machinery for a single-host Compose platform. | Rejected; too much machinery for a single-host Compose platform. |
| Explicit per-flow `/24` networks with fixed addresses only where required | A compromised container reaches only the peers it is wired to, and explicit subnets avoid collisions with Docker's automatic pool. | A new peer relationship needs a network edit, not just a host name, and `10.250.0.0/16` can still collide with another local network. | Selected; segmentation limits blast radius, subnets must be explicit, and static addresses should exist only where needed. |

- Trade-off: a new peer relationship needs a network edit, not just a host
  name.
- Trade-off: `10.250.0.0/16` can still collide with another local network.

#### Decision

##### Chosen Option

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

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval
record is linked. Effective from 2026-11-06.

###### Supersession
<!-- core-payload-level:4 -->

This record replaces ADR-0026, deleted in the same change (ADR-0051); ADR-0026
is historical and non-authoritative. ADR-0026
put every infrastructure service on one `infra_net` fixed at
`${INFRA_SUBNET:-172.19.0.0/16}`, required every included file to declare it,
kept extra networks such as `k3d-hyhome` alongside it, and gave each service a
static `ipv4_address`. It rejected Docker's automatic CIDR (addresses change
with start order) and an external IPAM service (too heavy for local Compose).
Its rejection of automatic CIDR and of external IPAM carries forward, as does
keeping an existing extra network when joining one; the single flat network and
blanket static addresses are withdrawn.

#### Consequences

##### Impacts

- Positive: a compromised container reaches only the peers it is wired to.
- Positive: explicit subnets avoid collisions with Docker's automatic pool.

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

Requirement and description text that still names `infra_net` is reconciled by
its owners.

###### Compliance
<!-- core-payload-level:4 -->

`scripts/hardening/check-all-hardening.sh` checks service network membership
(for example `check_service_network` for RedisInsight on `mng_data_net`).

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
