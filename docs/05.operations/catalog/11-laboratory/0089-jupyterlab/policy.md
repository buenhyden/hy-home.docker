---
title: "JupyterLab Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "POL-0089"
parent_ids:
- "AD-0011"
created: "2026-09-21"
---

# JupyterLab Operations Policy

## Overview

JupyterLab executes arbitrary code. Anyone who can reach a kernel or terminal
controls the container and every credential it can read.

## Policy Scope

Activation, authentication, network exposure, work-directory data, image
dependencies, MLflow client access, backup and removal.

## Controls

- Select only through `data-science`; keep outside HOME.
- Never run with an empty token or disabled authentication. Keep gateway SSO on
  the route and do not publish a host port.
- Treat the server as single-user. Do not grant access to several people until a
  reviewed JupyterHub design provides per-user isolation.
- Do not mount secrets, the Docker socket or shared storage credentials into the
  container. Notebook MLflow access goes through the artifact proxy.
- Keep the work directory outside the repository with owner UID 1000; back it up
  as user data.
- Pin library versions; review dependency changes like any image change.

## Exceptions

The internal MLflow SDK path is unauthenticated (see `POL-0088`). Terminals stay
enabled for the single user; disabling them is allowed without further review.

## Verification

Static rendering, then live checks: gateway 401 without session, server 403
without token, kernel start and WebSocket through the route, and denial for a
realm user who was not given the token.

## Review Cadence

Review on image or library change, auth change, new user, or JupyterHub decision.

## Traceability

- [Guide](guide.md) (`GDE-0089`)
- [Runbook](runbook.md) (`RUN-0089`)
- [Laboratory architecture](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Image Dockerfile](../../../../../infra/11-laboratory/jupyterlab/Dockerfile) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [JupyterLab Compose source](../../../../../infra/11-laboratory/jupyterlab/docker-compose.yml)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
