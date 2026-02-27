# ADR-0012: Standardized Init Process for Infrastructure Containers

- **Status**: Accepted
- **Date**: 2026-02-27
- **Author**: Antigravity (AI Coder)

## 1. Context

Many containers in the Hy-Home infrastructure run as PID 1, which often leads to issues with signal handling (e.g., containers not stopping immediately upon SIGTERM) and zombie process reaping. This can impact observability accuracy and resource cleanup performance during scale-down or redeployment events.

## 2. Decision

We will mandate the use of `init: true` in the `base-security` template within `infra/common-optimizations.yml`.

- **Requirement**: Every infrastructure service inheriting from the security baseline SHALL utilize the Docker-integrated `tini` init process.
- **Enforcement**: Applied globally via the inheritance model in `infra/common-optimizations.yml`.

## 3. Options Considered

### Option A: Manual Entrypoint Modification

Modify every `Dockerfile` to include `tini`.

- **Pros**: Container-level guarantee.
- **Cons**: High maintenance overhead across 20+ service directories.

### Option B: Docker Compose `init: true` (Selected)

Utilize the built-in Compose feature.

- **Pros**: Zero modification to images, centralized enforcement, works across all standard Docker runtimes.
- **Cons**: Requires standardizing on Compose for all deployments.

## 4. Consequences

- **Signal Handling**: Services will respond correctly to `docker stop` and `docker restart`, improving build and deployment loop speed.
- **Zombie Reaping**: Prevents resource leakage from orphaned child processes, improving long-term stability.
- **Observability**: Process metrics correctly reflect the lifecycle of the actual application process rather than the shell wrapper.

## 5. REQ Compliance

- `[REQ-ADR-04]`: Standardized init behavior for observability and stability.
