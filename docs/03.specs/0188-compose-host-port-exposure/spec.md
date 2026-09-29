---
title: "Compose Host Port Exposure Specification"
version: "0.3.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0188"
parent_ids:
- "REQ-0003"
- "REQ-0027"
- "AD-0031"
created: "2026-09-29"
---

# Compose Host Port Exposure Specification

## Overview

The Conftest `compose` policy reports 35 host port publications as bound to
all interfaces. Most of this repository already publishes diagnostic ports on
`127.0.0.1`, and [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
prefers loopback diagnostic ports. The 35 findings are the exceptions. This
package binds each one to the narrowest interface its consumers need, fixes
the rule's false positive, and then turns the rule into a `deny` so a new
wildcard publication fails the job.

A port Docker publishes on `0.0.0.0` bypasses host firewall rules such as UFW,
so a wildcard binding exposes the port to every network the host joins, not
only to the LAN the documents assume.

## Boundaries and Inputs

Findings, measured with `check-conftest-policy.sh` on `main` at `d6b68128e`:

| Group | Services and host ports | Count | Consumers found | Target binding |
| --- | --- | --- | --- | --- |
| A. Rule false positive | `traefik` 80, 443 (already `${TRAEFIK_BIND_IP:-192.168.0.13}:`) | 2 | LAN and the k3d cluster | Unchanged; the rule stops flagging an explicit host IP |
| B. Intended LAN reach | `loki` 3100, `tempo` 3200, `mng-valkey` 26379, `alloy` 4317 and 4318, `pg-router` 15432 and 15433, `nginx` 80 and 443 | 9 | The k3d cluster at `192.168.0.13` (POL-0096, GDE-0096, GDE-0040); `nginx` is the alternative gateway | The host LAN address variable, not all interfaces |
| C. Host-local only | `mng-pg` 25432; `pyroscope` 4040; `locust-master` 18089; `supabase` Kong 8000 and 8443, analytics 4000, Supavisor 5432 and 6543; `opensearch-node1` 9600; `kafka-1..3` external, JMX, and JMX exporter (9); `valkey-node-0..5` (6) | 24 | None beyond the host operator; Kafka advertises `localhost`, Valkey cluster nodes announce container names, and Prometheus scrapes over the Docker network | `127.0.0.1` |

In scope:

- The listed `ports` entries in nine Compose leaves under `infra/`.
- `infra/09-tooling/conftest/policy/compose.rego` and its tests.
- The root `.env.example` key for the host LAN address.
- Stage 05 documents that state these bindings: POL-0096 and GDE-0096 (the
  allowed LAN exposure list and the OTLP statement that contradicts
  `config.home.alloy`), POL-0095, GDE-0095, the Conftest README, and the
  service guides and policies whose text names a published port's reach.

Out of scope:

- Starting, recreating, or stopping any service. Bindings change only when an
  operator recreates a service; that runtime step needs its own approval.
- Adding authentication, TLS, or Traefik routes.
- The `VALKEY_MNG_HOST_POST` key spelling, and the Tempo and Pyroscope
  `OPTIONAL` versus HOME wording. Both are recorded as follow-ups.

## Behavior Contract

1. Group C ports publish as `127.0.0.1:${X_HOST_PORT:-N}:N`, the form the
   repository already uses.
2. Group B ports publish on one host LAN address taken from a single `.env`
   key, with the current address as its default, so the k3d cluster keeps
   reaching them at `192.168.0.13`.
3. The Conftest rule treats a publication as scoped when it names a host
   address: a literal IP, a `${VAR:-address}` interpolation, bracketed IPv6,
   or long syntax `host_ip`. It flags a publication with no host address, or
   with `0.0.0.0` or `::`.
4. Once the source passes, the rule becomes a `deny` with its message and
   tests, as POL-0095 requires for a new `deny`.
5. The Stage 05 documents name each exposed port's binding and consumer, and
   POL-0096's allowed LAN list matches Group B.

## Technical Approach

1. Change the rule and its tests first: add pass and fail cases for an
   explicit IP, an interpolated address, IPv6 loopback, long syntax, and the
   wildcard forms. Traefik's two findings disappear; the other 33 remain.
2. Rebind Group C per file and check each file with
   `validate-docker-compose.sh` and the Conftest job.
3. Add the LAN address key to `.env.example` and rebind Group B to it.
4. Promote the rule to `deny` when the Conftest job reports zero findings.
5. Update the Stage 05 documents in the same change as the bindings they
   describe.

## Interfaces and Data

- One new `.env` key for the host LAN address (name decided at approval; see
  Open Questions). Existing host-port keys keep their names and defaults.
- No service, image, network, or volume changes. Container listeners stay as
  they are; only the host side of each publication changes.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| A host-local consumer used a Group B port through `localhost` | The investigation found none; the Task lists each port's consumer, and the rebinding keeps the LAN address the k3d cluster uses |
| An operator reached a Group C port from another LAN machine | The documents gain the binding, and the loopback form is the repository's documented default for unauthenticated diagnostic ports |
| The LAN address changes | It comes from one `.env` key, with the Traefik key as the precedent |
| The rule change hides a real wildcard | Behavior rule 3 keeps `0.0.0.0` and `::` flagged, with tests |
| Recreating services interrupts running work | No runtime step is in scope; bindings apply on the operator's next recreate |

## Acceptance Contract

1. The rule's tests cover scoped and wildcard forms, and fail against the
   current rule.
2. Every Group C publication binds `127.0.0.1`.
3. Every Group B publication binds the LAN address key, and `.env.example`
   declares that key.
4. The Conftest job reports zero host publication findings, and the rule is a
   `deny`.
5. POL-0096, GDE-0096, POL-0095, GDE-0095, the Conftest README, and the
   affected service documents state the new bindings, and GDE-0096 no longer
   contradicts the Alloy OTLP receiver.
6. `validate-docker-compose.sh`, the changed-profile gate members including
   `check-conftest-policy.sh`, `tests/lib`, and `tests/validation` pass.

## Traceability

- REQ-0003: security requirements for the stack.
- REQ-0027 and AD-0031: the HOME development host and its preference for
  gateway ingress and loopback diagnostic ports.
- POL-0095: Conftest rule lifecycle, `warn` first and `deny` once the source
  passes.
- POL-0096: the current allowed LAN exposure for the k3d cluster.

## Open Questions

1. The LAN address key: a new host-wide key (for example `HOST_LAN_BIND_IP`)
   that Traefik also reads, or reuse `TRAEFIK_BIND_IP` for every Group B port.
2. Whether `pg-router` 15432 and 15433 stay reachable from the k3d cluster
   (GDE-0096 lists them as optional) or move to Group C.

## Operational Impact

None until an operator recreates the affected services. After recreation,
Group C ports answer only on the host itself, and Group B ports answer only on
the host LAN address.
