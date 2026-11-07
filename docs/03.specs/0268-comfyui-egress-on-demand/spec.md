---
title: "ComfyUI Egress on Demand Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0268"
parent_ids:
- "REQ-0023"
- "AD-0026"
created: "2026-11-08"
---

# ComfyUI Egress on Demand Specification

## Overview

### Intent

ComfyUI has no outbound network access and no host port in its default
configuration. An operator attaches outbound access and the loopback port
through an opt-in overlay only for a maintenance window that installs models
or custom nodes, then removes it.

### Background

SPEC-0266 moved ComfyUI off `edge_net` and gave it `comfyui_egress_net`
(`10.250.42.0/24`), a non-internal network with ComfyUI as its only member,
so that its outbound calls kept working. That network reaches any external
address. ComfyUI-Manager 3.41 is installed in HOME with no `network_mode` set,
so it uses the public default, and its `security_level` is `weak`. The image
entrypoint (`/runner-scripts/entrypoint.sh`) downloads nothing at start.
Outbound access is needed for installing models and custom nodes, not for
running workflows. On 2026-11-08 the owner chose egress off by default with an
opt-in overlay, over a domain-allowlist proxy and over an accepted risk.

## Scope

### In Scope

- Removing `comfyui_egress_net` and the loopback host port
  `127.0.0.1:8188` from the default ComfyUI render. Docker publishes no port
  for a container on internal networks only, so the port moves with the
  network (owner decision, 2026-11-08). The overlay fixes the host port at
  `8188`, and `COMFYUI_HOST_PORT` leaves `.env.example`, because the public
  environment scan reads only the root Compose includes.
- An opt-in leaf-base overlay `infra/08-ai/comfyui/docker-compose.egress.yml`
  (POL-0078 typed overlay) that attaches ComfyUI to `comfyui_egress_net` and
  publishes the loopback port.
- The attach and detach steps and the in-container health check in RUN-0081,
  with the ComfyUI README pointing to it.
- Render tests for the default and overlay renders, GDE-0077 and the affected
  documents.

### Out of Scope

- A forward proxy or a domain allowlist.
- ComfyUI-Manager settings such as `security_level` and `network_mode`, which
  live in ComfyUI's private state under `/root/ComfyUI/user`.
- Ingress, SSO and the ComfyUI data volumes.

## Contracts

### Normal Behavior

- With the default render, ComfyUI starts, passes its health check, serves its
  SSO route and runs a workflow that uses only local models.
- With the overlay, ComfyUI reaches external hosts and ComfyUI-Manager can
  install a custom node or download a model.
- Removing the overlay and recreating ComfyUI removes outbound access again.

### Error Behavior

- With the default render, a connection from ComfyUI to an external address
  fails.
- A default render that attaches ComfyUI to any non-internal network fails the
  test.

### Boundary Behavior

- A ComfyUI feature found in W1 to need outbound access at start or at
  workflow run time is recorded, and the default render is not changed until
  the owner decides.

### Constraints

- `comfyui_egress_net` keeps its subnet and stays declared, so the overlay
  needs no new address range (ADR-0055).
- GDE-0077 records the network as overlay-only.
- No secret value is printed or committed.

## Acceptance Criteria

1. W1 records every outbound dependency of ComfyUI at start and at workflow run
   time, with its source, and confirms none is needed outside a maintenance
   window.
2. The default render attaches ComfyUI only to `comfyui_ingress_net`.
3. The overlay adds to ComfyUI only `comfyui_egress_net` and the loopback
   port, and changes no other service.
4. A render test fails when the default render gives ComfyUI a non-internal
   network or a host port, or when the overlay adds anything other than that
   network and port.
5. RUN-0081 states the attach and detach steps and an in-container health
   check, the ComfyUI README points to it, and GDE-0077 records the network as
   overlay-only.
6. In HOME, under its own approval, ComfyUI is recreated with the default
   render; its health check, SSO route and data hold, an external connection
   fails, and an attach and detach with the overlay is rehearsed.

## Failure Conditions

### Observable Failures

- ComfyUI fails its health check or a local-model workflow fails without
  outbound access.
- An external connection succeeds with the default render.

### Stop Boundaries

- Stop before any HOME recreation without its own approval.
- Stop and report if W1 finds an outbound dependency needed at start or at
  workflow run time.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-comfyui-egress-on-demand.md)
- [SPEC-0266](../0266-sso-only-backend-ingress/spec.md)
- [SPEC-0267](../0267-secondary-listener-hardening/spec.md)
- [ADR-0055](../../02.architecture/decisions/0055-segmented-per-flow-networks.md)
- [ADR-0061](../../02.architecture/decisions/0061-dedicated-ingress-for-sso-only-backends.md)
- [REQ-0023](../../01.requirements/0023-standardize-infra-net.md)
- [AD-0026](../../02.architecture/descriptions/0026-standardize-infra-net.md)
- [GDE-0077](../../05.operations/guides/02-gateway-and-networking/0077-ip-address-management.md)
