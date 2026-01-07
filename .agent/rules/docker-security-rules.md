# Docker Security Rules for Agents

## Isolation Requirements

- When running untrusted or experimental code, the agent must prefer running it inside a dedicated Docker container rather than directly on the host.
- The agent should recommend isolated networks, restricted capabilities, or firewall rules if the workload does not require full network access.

## Permissions and Capabilities

- Do not grant privileged mode (`--privileged`) or broad capabilities unless explicitly justified.
- When additional capabilities (for example, `NET_ADMIN`) are required, they must be:
  - Clearly documented with reasons.
  - Scoped to the minimal set of containers.

## Volume and Data Handling

- Avoid mounting the entire host filesystem.
- Mount only necessary directories, preferably read-only when possible.
- For persistent data (for example, tool caches or agent state), use named Docker volumes instead of host paths when appropriate.

## Auditing and Transparency

- The agent should describe:
  - Which Docker commands it intends to run.
  - Which images and tags it will use.
  - Which ports and volumes will be exposed.
- Any security-relevant change must be accompanied by a short explanation in comments or documentation.
