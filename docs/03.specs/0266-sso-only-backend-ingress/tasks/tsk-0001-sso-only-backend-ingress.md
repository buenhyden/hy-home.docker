---
title: "SSO-Only Backend Ingress Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-07"
layer: "specs"
artifact_id: "SPEC-0266-TSK-0001"
parent_ids:
- "SPEC-0266-PLAN-0001"
created: "2026-11-07"
---

# SSO-Only Backend Ingress Task

## Overview

### Objective

Execute W1–W5 of the Plan: confirm the SSO-only backends and their flows, move
them to dedicated ingress networks, test the isolation, update the documents
and, under separate approval, apply the change in HOME.

## Inputs and Authorization

The owner asked on 2026-11-07 to start this Spec after the D02 finding in
SPEC-0212 TSK-0041. The Spec and Plan are `draft`; no implementation starts
until both are approved. The 2026-11-07 render inputs are `main`
`56104a49ec2ee6b3756408d73520363080c9b55a` with the public `.env.example`.
HOME recreation (W5) needs its own approval.

## Work Log

### Draft inputs (2026-11-07)

A value-free render of every profile from `.env.example` listed 38 `edge_net`
members. Traefik holds `10.250.1.2` and the aliases `keycloak.hy.home.arpa`
and `auth.hy.home.arpa` on `edge_net`, so OIDC clients on it reach Keycloak
through Traefik; the SSO-only backends are not OIDC clients and do not need
those aliases. A text match of each member's environment, command and mounted
configuration against the other members' names, filtered to pairs that share
no network but `edge_net`, found three `edge_net`-only flows: Alloy and
Prometheus to `seaweedfs-s3`, and Grafana to Ollama. The match is approximate
(it also counts public host names and unused references), so W1 replaces it
with a source-read inventory before any change.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft reachability and flow scan | `56104a49e`, public render | NOT_RUN | Approximate draft input only; the source-read inventory is W1 | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Awaiting W1 | @buenhyden |
| 2 | pending | - | Awaiting W2 | @buenhyden |
| 3 | pending | - | Awaiting W2 | @buenhyden |
| 4 | pending | - | Awaiting W3 | @buenhyden |
| 5 | pending | - | Awaiting W4 | @buenhyden |
| 6 | pending | - | Awaiting W5 and its approval | @buenhyden |

## Review and Completion

Not started. The Spec and Plan are drafts.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0061](../../../02.architecture/decisions/0061-dedicated-ingress-for-sso-only-backends.md)
