# Docker General Rules

## Scope and Goals

- The agent must configure and use Docker in a way that is independent of any hard-coded project path.
- All Docker-related instructions must work from any valid repository root that follows standard conventions (for example, having a `Dockerfile` or `docker-compose.yml` in the tree).
- The agent must prefer relative paths and workspace-root–based discovery instead of absolute paths.
- The agent should keep host system modifications minimal and reversible.

## Path-Agnostic Behavior

- Never hard-code absolute file system paths such as `/home/user/project` or `C:\Users\name\repo`.
- Always assume the current workspace root is the primary context when resolving paths.
- When unsure about the correct location of Docker files, the agent must:
  - Search the repository tree for `Dockerfile`, `docker-compose.yml`, `.devcontainer`, or `compose.*.yml` files using project-aware tools or commands.
  - Ask the user which directory or file should be treated as the main Docker entrypoint if multiple candidates exist.
- When generating new Docker-related files, place them in:
  - The workspace root (for `Dockerfile` or `docker-compose.yml`) unless the user requests otherwise.
  - A dedicated `.devcontainer` or `infra/` folder if the repository already follows that convention.

## Safety and Resource Usage

- Do not execute destructive Docker commands on the host such as:
  - `docker system prune -a`, `docker volume rm` without explicit user consent.
- Avoid binding host-sensitive directories (for example, `/`, `/var`, or the entire user home) into containers.
- Prefer minimal and well-scoped volume mounts.
- Avoid exposing unnecessary ports publicly; prefer localhost bindings such as `127.0.0.1:PORT:PORT`.

## Image and Container Conventions

- Prefer official and well-maintained base images (for example, `python`, `node`, `ubuntu`, `debian`) with explicit tags.
- Avoid using `latest` tags unless the user explicitly requests it.
- Always document the chosen base image and the reason if multiple options exist.
- Ensure that Dockerfiles are deterministic and reproducible:
  - Pin package versions when practical.
  - Avoid interactive commands; use non-interactive flags (for example, `apt-get install -y`).

## Networking and Security

- Containers must not expose unnecessary outbound or inbound network access without explicit user intent.
- When configuring firewalls or network rules inside containers, default to denying external access unless needed.
- Do not store secrets directly inside Dockerfiles or compose files:
  - Use environment variables, secrets management mechanisms, or `.env` files that are excluded from version control where appropriate.
- When the user’s workflow requires internet access, clearly describe which domains or services the container must reach.

## Cross-Platform Considerations

- Ensure all Docker commands and file paths work on Linux, macOS, and Windows hosts where possible.
- Avoid relying on shell features available only in a specific shell (for example, `zsh`-only features) inside Dockerfiles; use POSIX-compatible shells where feasible.
- Document any platform-specific assumptions (for example, reliance on Docker Desktop vs native Docker).

## Documentation Expectations

- Whenever the agent introduces or modifies Docker configuration, it must:
  - Explain the purpose of the change in a short comment in the Dockerfile or compose file.
  - Provide a minimal set of commands for the user to build and run the container.
- The agent should keep Docker-related documentation in a `docs/` or `infra/` folder when that pattern already exists in the repository.
