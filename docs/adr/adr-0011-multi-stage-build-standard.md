# ADR-0011: Mandatory Multi-Stage Docker Builds

## Status

Accepted

## Context

Custom Docker images for services like Keycloak, n8n, and OpenSearch were inconsistently using multi-stage builds. Mono-stage builds often include unnecessary build-time dependencies (compilers, headers, cache), leading to bloated images and a larger security attack surface.

## Decision

All custom Dockerfiles within the `infra/` directory MUST utilize multi-stage builds.

- **Stage 1 (Builder)**: Install all necessary build tools and compile/process assets.
- **Stage 2 (Runner)**: Copy only the final artifacts from the Builder stage into a clean, minimal base image (e.g., Alpine or Distroless).

Layer ordering MUST also prioritize caching, placing stable commands (like installing generic system packages) above volatile commands (copying application source code).

## Consequences

- **Positive**: Significant reduction in final image size (often >50%).
- **Positive**: Improved security posture by removing build-time tools from production containers.
- **Positive**: Faster build/pull times due to smaller image layers.
- **Negative**: Slightly more complex Dockerfile syntax.
