---
title: "Secondary Listener Hardening Specification"
version: "0.2.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0267"
parent_ids:
- "REQ-0023"
- "AD-0026"
created: "2026-11-07"
---

# Secondary Listener Hardening Specification

## Overview

### Intent

A metrics, profiling, management or broker listener that has no
authentication of its own is reachable only from the containers that consume
it, not from every container on `edge_net`. Pyroscope and ComfyUI keep their
state on declared volumes.

### Background

SPEC-0266 moved the SSO-only backends off `edge_net` and recorded, out of its
scope, the secondary listeners of services that keep `edge_net` because their
main port has its own login. A 2026-11-07 source and documentation review found
six such listeners that bind all interfaces and have no authentication:
SeaweedFS S3 metrics `9327`, OAuth2 Proxy metrics `44180`, the Keycloak
management port `9000`, the n8n task broker `5679`, Grafana pprof `6060` and
the Traefik metrics and ping entrypoint `8082`. Each upstream offers a bind
address setting. Metrics served on a main port (Grafana `3000`, n8n `5678`,
Gatus `8080`) cannot be bound apart from the route Traefik uses; only Grafana
offers built-in metrics authentication. The same day Pyroscope was found in a
crash loop on a corrupted metastore database that lives in an anonymous volume
the Compose file does not declare. The owner chose on 2026-11-07 to bind the
six listeners, add Grafana metrics authentication, record the remaining
exposures as accepted risks, and declare the Pyroscope metastore volume. During
the SPEC-0266 apply ComfyUI was found to keep all its state in the image's
undeclared `/root` volume while its seven declared volumes stay empty, and the
owner added moving those mounts onto the paths the image uses.

## Scope

### In Scope

- Binding each of the six listeners to one fixed address on a network shared
  only with its declared consumers, and moving those consumers to that address.
- Grafana metrics basic authentication, with the Prometheus job reading the
  password from a file.
- A declared named volume for the Pyroscope metastore and raft state, with the
  existing data carried over.
- ComfyUI volume mounts on the paths the image uses (`/root/ComfyUI/...`), with
  the data in its anonymous `/root` volume carried over.
- Accepted-risk records for n8n `/metrics`, Gatus `/metrics` and the POL-0096
  LAN publications of Loki, Tempo and Alloy.
- Render tests, the affected service READMEs and GDE-0077.

### Out of Scope

- Main-port authentication, routes and middleware.
- Sender-side changes for the POL-0096 LAN listeners, which run in LAB.
- The one-time recovery of the corrupted Pyroscope metastore, which runs and is
  recorded under SPEC-0266 TSK-0001 W5.
- A Gatus patch for `/metrics` authentication.

## Contracts

### Normal Behavior

- Each declared consumer reaches its listener at the fixed address, and its
  scrape, probe, profile or broker connection keeps working.
- Each container health check that used the listener still passes.
- Prometheus scrapes Grafana with basic authentication.
- Pyroscope starts with its metastore on the named volume and keeps the
  existing index.
- ComfyUI starts with its models, custom nodes, inputs, outputs and user data on
  declared volumes and keeps the existing data.

### Error Behavior

- A container that is not a declared consumer gets no connection to a bound
  listener.
- An unauthenticated request to Grafana `/metrics` is refused.
- A render where a bound listener's network has a member outside its consumers,
  or where the bind setting and the fixed address disagree, fails the test.

### Boundary Behavior

- A listener whose consumer set cannot be fully named from source stays as it
  is and is recorded.
- A listener whose health check cannot reach the bound address is not changed
  until the health check is moved to that address.

### Constraints

- Each new network is `internal: true` with an explicit `/24` and an
  `ip_range` that keeps the fixed addresses outside the dynamic range
  (ADR-0055); existing networks are not given a new IPAM configuration.
- GDE-0077 changes with each network.
- No secret value is printed or committed.

## Acceptance Criteria

1. W1 records for each of the six listeners its bind setting, every consumer
   with its source line, the health checks that use it, and the network and
   fixed address it will use.
2. Each listener binds only to its fixed address, and each consumer and health
   check uses that address.
3. Grafana `/metrics` requires basic authentication and the Prometheus job
   authenticates with a password file.
4. Pyroscope's metastore and raft directories and ComfyUI's state directories
   are on declared named volumes, and the previous data is carried over.
5. A render test fails when a bound listener's network has a member outside
   its consumers, when the bind setting does not match the fixed address, or
   when the Pyroscope metastore path or a ComfyUI state path is not on a
   declared volume.
6. The accepted risks for n8n `/metrics`, Gatus `/metrics` and the POL-0096 LAN
   listeners are recorded with their reason and review trigger.
7. In HOME, under its own approval, the services are recreated; each consumer
   works, a non-consumer `edge_net` container is refused, unauthenticated
   Grafana `/metrics` is refused, and a rollback is rehearsed.

## Failure Conditions

### Observable Failures

- A Prometheus target, Gatus probe, Alloy profile scrape or n8n task runner
  fails after the change.
- A container health check fails because it still uses `127.0.0.1` or the
  service name.
- Pyroscope starts with an empty metastore, or ComfyUI without its models or
  user data.

### Stop Boundaries

- Stop before any HOME recreation without its own approval.
- Stop before moving Pyroscope or ComfyUI data without a verified backup.
- Do not weaken any existing authentication to keep a consumer working.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-secondary-listener-hardening.md)
- SPEC-0266 (retired; its body is in Git history)
- [ADR-0055](../../02.architecture/decisions/0055-segmented-per-flow-networks.md)
- [ADR-0061](../../02.architecture/decisions/0061-dedicated-ingress-for-sso-only-backends.md)
- [REQ-0023](../../01.requirements/0023-standardize-infra-net.md)
- [AD-0026](../../02.architecture/descriptions/0026-standardize-infra-net.md)
- [GDE-0077](../../05.operations/guides/02-gateway-and-networking/0077-ip-address-management.md)
