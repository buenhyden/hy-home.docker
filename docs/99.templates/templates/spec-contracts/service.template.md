---
status: draft
---

<!-- Target: docs/03.specs/<feature-id>/service.md -->

# [Service Name] Service Scaffold

> Use this template for `docs/03.specs/<feature-id>/service.md`.
>
> Rules:
>
> - This document is a child design document under the feature spec.
> - It defines the runtime contract of one containerized service: image, build,
>   security hardening, networking, volumes, secrets, healthcheck, and validation.
> - Keep product intent in PRD, system-wide constraints in ARD, and ordered
>   recovery steps in a Runbook.
> - A concrete, copyable instance lives under `examples/sample-web-service/`.
> - Write this document in English. Preserve code identifiers, command names,
>   service names, environment variables, and quoted upstream terms exactly.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.

---

## Overview

This document defines the container runtime contract for [service name]. It
specifies image/build behavior, security hardening, networks, volumes, secret
references, health checks, and verification procedures.

## Parent Documents

- **Spec**: [./spec.md](./spec.md)
- **ARD**: [ARD folder](../../02.architecture/requirements/)
- **Related ADRs**: [ADR folder](../../02.architecture/decisions/)

## Scope & Non-goals

- **Covers**:
- **Does Not Cover**:

## Image & Build

- **Base image (pinned)**: `{registry/image:tag}` — no floating tags (`latest`, `stable`); pin a tag or digest per `infra/image-tag-policy.exceptions.json`.
- **Build strategy**: multi-stage build; final stage carries runtime artifacts only.
- **Build args**: `{ARG=value}` — never bake secrets into build args or layers.

## Security & Hardening

- **User**: runs as non-root (`USER` set, numeric UID where possible).
- **Filesystem**: `read_only: true` with explicit `tmpfs` for writable paths when feasible.
- **Capabilities**: `cap_drop: [ALL]`, add back only the minimum required.
- **Privilege**: `no-new-privileges` enabled; no `privileged: true`.
- **Resource limits**: CPU and memory limits declared.

## Networking & Volumes

- **Networks**: `{network}` — least-exposure; publish ports only when required.
- **Ports**: `{host:container}` or internal-only.
- **Volumes**: `{named-volume:/path}` — named volumes over bind mounts for state.

## Secrets

- **Mechanism**: `env_file` / Docker secrets / Vault reference — never plaintext in compose.
- **Referenced keys**: `{KEY (ref only, no value)}`.

## Healthcheck & Operations

- **Healthcheck**: command, interval, timeout, retries, start period.
- **Restart policy**: `{unless-stopped | on-failure}`.
- **Logging**: driver and retention.

## Validation

- `{compose config / hardening / smoke command}`
- {expected result}

## Related Documents

- **Spec**: [./spec.md](./spec.md)
- **Tests**: [./tests.md](./tests.md)
- **Onboarding guide**: [../../05.operations/guides/00-workspace/new-service-onboarding.md](../../05.operations/guides/00-workspace/new-service-onboarding.md)
- **Runbook, domain operations target**: [../../05.operations/runbooks/<domain>/<topic>.md](../../05.operations/runbooks/<domain>/<topic>.md)
