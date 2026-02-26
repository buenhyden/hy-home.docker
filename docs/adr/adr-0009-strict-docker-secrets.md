# ADR-0009: Strict Docker Secrets Adoption

## Status

Proposed

## Context

Sensitive information (passwords, API tokens) is currently documented in a registry but partially scattered. We need a uniform method for handling secrets that integrates with Docker Compose and prevents environment variable leakage in `docker inspect`. Existing ADRs (0002) touch on secrets but we need a stricter enforcement for ALL tiers.

## Decision

- **Mandatory Use**: All sensitive data MUST be stored in `secrets/**/*.txt`.
- **Mounting**: Secrets SHALL be mounted to `/run/secrets/` in containers.
- **Verification**: `scripts/validate-secrets.sh` (to be created) will verify that no plaintext passwords exist in `docker-compose.yml` or `.env`.

## Consequences

- **Positive**: Enhanced security posture, zero-plaintext in terminal history/logs.
- **Negative**: Increased complexity in bootstrapping (requires manual file creation for some secrets).
