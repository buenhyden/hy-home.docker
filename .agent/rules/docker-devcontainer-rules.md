# Dev Container Rules for Agents

## Purpose

- The agent uses Dev Containers (or similar workspace containers) to provide a reproducible development environment on top of Docker.
- All Dev Container configuration must remain independent of a hard-coded host path and must operate relative to the repository root.

## Configuration Principles

- Place Dev Container configuration in a `.devcontainer` folder at the workspace root unless the repository uses a different documented convention.
- Use relative paths in `devcontainer.json`, `docker-compose.yml`, and other related files.
- Avoid host-specific assumptions such as:
  - Specific usernames.
  - Host-specific Docker socket paths (beyond well-known defaults).
  - Non-portable volume mount paths.

## Tools Inside the Dev Container

- Prefer installing tools that the agent will use (for example, CLIs, linters, language servers) inside the Dev Container image instead of requiring host-level tools.
- When Docker-in-Docker or a mounted Docker socket is required, clearly document:
  - Why Docker access is needed from inside the container.
  - Any security implications or limitations.

## Networking and Ports

- When exposing services from Dev Containers, prefer:
  - `localhost` bindings to avoid unnecessary public exposure.
  - A minimal number of exposed ports, using well-known or user-specified ports.
- Avoid port conflicts by:
  - Allowing users to override port mappings via environment variables or settings where possible.

## User Experience

- The agent must provide simple Dev Container lifecycle commands, such as:
  - Bringing the container up.
  - Rebuilding it when configuration changes.
  - Attaching an editor or agent to it.
- Document any required environment variables or prerequisites in a `README` or `docs/devcontainer.md` file.
