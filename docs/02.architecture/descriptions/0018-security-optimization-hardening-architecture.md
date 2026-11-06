---
title: "Security Optimization and Hardening Architecture"
version: "1.1.4"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0018"
parent_ids:
- "REQ-0003"
created: "2026-03-28"
---
# Security Optimization and Hardening Architecture

## Overview

### Context and Stakeholders

This document describes the OpenBao and OpenBao Agent boundary implemented in
`infra/03-security/`. The maintainer, service owner, and operator must clearly
separate ownership of the source secret, the rendered output, health, and the
recovery procedure.

## Scope

### System Boundaries

- OpenBao owns KV-v2 secret storage and lookup.
- OpenBao Agent owns AppRole authentication, the token sink, and per-service
  template rendering.
- The gateway owns external TLS termination and routing, and does not own the
  internal OpenBao secret lifecycle.
- Per-application configuration parsing and external KMS/HSM operation are
  outside this architecture.

## Structure

### Architecture

The current HOME implementation consists of `openbao` and `openbao-agent` from
`infra/03-security/openbao/docker-compose.yml`, the policy, configuration, and
template files, and a persistent volume. Traefik provides the external
boundary, and OpenBao Agent provides only minimum-scope output to consuming
services.

## Runtime and Deployment

### Runtime View

The source secret is stored in OpenBao KV-v2. OpenBao Agent authenticates with
AppRole, keeps restricted token state at `/openbao/agent/token`, and then
renders template output under `/openbao/out/<service>/`, bind-mounted from
`${DEFAULT_SECURITY_DIR}/openbao/out`. The source secret
and the rendered output maintain separate access boundaries.

### Deployment View

The current HOME deployment is a single Docker Compose-based OpenBao and
OpenBao Agent structure. The registered hardening and Compose validators check the tracked
configuration. Raft 3-node, auto-unseal, and a remote audit sink
are not the current implementation, and are not treated as the current
topology without a separately approved Requirement and ADR.

## Quality and Risks

### Quality Attributes

- **Security**: rejects plaintext secrets and placeholder paths, and keeps
  least privilege.
- **Reliability**: keeps healthchecks, persistent data, and an explicit
  recovery procedure.
- **Observability**: health and rendering results must be checkable without
  exposing the secret value.
- **Operability**: configuration, the Operations procedure, and validation
  results must describe the same current topology.

## Related Documents

### Traceability

- [REQ-0003](../../01.requirements/0003-security.md)
- [ADR-0050](../decisions/0050-openbao-as-secrets-manager.md), which supersedes ADR-0018
- [AD-0003 Security architecture](0003-security-architecture.md)
- [OpenBao policy](../../05.operations/policies/04-security-and-secrets/0085-openbao.md)
- [OpenBao runbook](../../05.operations/runbooks/04-security-and-secrets/0085-openbao.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
