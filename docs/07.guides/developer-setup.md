---
layer: docs
---

# Developer Environment Setup Guide

This guide defines the required local environment configuration and permissions for contributing to the `hy-home.docker` ecosystem.

## 1. Context & Objective

- **Purpose**: To standardize the local development environment across different machines.
- **Goal**: Ensure agents have sufficient but safe permissions to execute build and validation scripts.

## 2. Recommended Permissions (Claude Code)

To interact effectively with the infrastructure, your `.claude/settings.local.json` should include the following permission patterns:

### Infrastructure & Validation
- `Bash(scripts/validate-docker-compose.sh:*)`
- `Bash(docker:*)`
- `Bash(docker-compose:*)`

### Development Tools
- `Bash(npm run:*)`
- `Bash(npx tsc:*)`
- `Bash(python3:*)`

### File System Access
- `Read(docs/**)`
- `Read(infra/**)`

## 3. Tool Configuration

### Shell Environment
All scripts assume a bash-compatible shell. If you are on Windows, use WSL2.

### Local Settings Pruning
- Avoid absolute paths (e.g., `D:/blog-data/...`) in shared settings.
- Use `$CLAUDE_PROJECT_DIR` for relative referencing in hooks.

## 4. Operational Procedures

### Initial Setup
1. Clone the repository.
2. Ensure Docker and Docker Compose (v2.x) are installed.
3. Run `bash scripts/validate-docker-compose.sh` to verify your local setup.

## 5. Maintenance & Safety

- **Security**: Never add `allow: ["*"]` permissions. Always scope permissions to specific tools or directories.
- **Secrets**: Ensure your local `.env` is never committed; use `secrets/SENSITIVE_ENV_VARS.md.example` as a template.
