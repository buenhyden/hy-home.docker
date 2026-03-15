---
layer: entry
---

# hy-home.docker

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](#license)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](CHANGELOG.md)

> Modular Docker Compose infrastructure for local development and homelab multi-service stacks.

## Overview

`hy-home.docker` is the root orchestration repository for a layered, self-hosted platform stack built on Docker Compose `include` files and profiles. It is designed for operators who want a reproducible local or homelab environment and for contributors who need a clear entrypoint into the repository’s infrastructure, validation, and documentation workflows.

The repository assembles gateway, identity, data, messaging, observability, workflow, AI, and tooling tiers into one Compose-driven system. It favors secrets-first configuration, explicit operational runbooks, and spec-driven change management over ad hoc bring-up.

## Key Features

- Modular service tiers under [`infra/`](infra/)
- Profile-based stack assembly through a single root [`docker-compose.yml`](docker-compose.yml)
- File-based Docker secrets bootstrapped under [`secrets/`](secrets/)
- Local TLS bootstrap with `mkcert`
- Centralized architecture, context, plans, and runbooks under [`docs/`](docs/)
- Static validation and runtime preflight scripts before `docker compose up`
- Optional observability, workflow, AI, and tooling stacks for broader platform builds

## Tech Stack

| Category | Technology |
| --- | --- |
| Orchestration | Docker Engine 24+, Docker Compose v2 |
| Gateway / Edge | Traefik, optional Nginx |
| Identity / Access | Keycloak, OAuth2 Proxy |
| Data / Storage | PostgreSQL cluster, Valkey cluster, MinIO, OpenSearch, Qdrant |
| Optional Data Services | MongoDB, Cassandra, CouchDB, Neo4j, SeaweedFS, Supabase, InfluxDB |
| Messaging | Kafka, optional ksqlDB, optional RabbitMQ |
| Observability | Prometheus, Grafana, Loki, Tempo, Alloy, Pushgateway, Alertmanager |
| Workflow | Airflow, optional n8n |
| AI | Ollama, Open WebUI |
| Tooling | SonarQube, optional Terrakube, Syncthing, Locust, Terraform helpers |
| Deployment Model | Self-hosted Docker Compose on Linux, WSL2, and homelab hosts |

## Prerequisites

Install and verify the following before bootstrapping the stack:

- Docker Engine `24.x` or newer
- Docker Compose v2 `20.x` or newer
- `bash`
- `git`
- `mkcert` for local certificate generation
- `python3` and `openssl` for the secrets bootstrap workflow
- Enough RAM for the enabled profiles
  - `core,data,obs` is the default baseline
  - add more headroom before enabling `workflow`, `ai`, or `tooling`

Platform notes:

- Linux is the primary target.
- On WSL2, keep the repository inside the Linux filesystem, not under `/mnt/c`, to avoid slow mounts and permission issues.
- Ensure the host mount root configured by `DEFAULT_MOUNT_VOLUME_PATH` exists and is writable.
- External networks `project_net` and `kind` are optional for core boot, but integrations that rely on them need those networks to exist.

## Quick Start

### 1. Clone the repository

Clone the repo into a Linux or WSL2 filesystem path where Docker can mount volumes reliably.

```bash
git clone https://github.com/buenhyden/hy-home.docker.git
cd hy-home.docker
```

### 2. Create your local environment file

Start from the tracked example file so the scripts and Compose interpolation have all required defaults.

```bash
cp .env.example .env
```

Review these values before the first boot:

| Variable | Why it matters | Typical local value |
| --- | --- | --- |
| `DEFAULT_URL` | Base domain used by Traefik routers and service URLs | `127.0.0.1.nip.io` |
| `COMPOSE_PROFILES` | Profiles enabled by default on `docker compose up` | `core,data,obs` |
| `DEFAULT_MOUNT_VOLUME_PATH` | Host path for persistent service data | `/home/<user>/volumes` |
| `HTTP_HOST_PORT` / `HTTPS_HOST_PORT` | Host ports exposed by the gateway | `80` / `443` |
| `INFRA_SUBNET` | Internal Docker subnet for `infra_net` | `172.19.0.0/16` |

### 3. Prepare host volume directories

The preflight script expects the mount roots declared in `.env` to exist.

```bash
mkdir -p \
  /home/hy/volumes/auth \
  /home/hy/volumes/data \
  /home/hy/volumes/message_broker \
  /home/hy/volumes/obs \
  /home/hy/volumes/workflow \
  /home/hy/volumes/ai \
  /home/hy/volumes/tooling
```

Adjust the paths if you changed `DEFAULT_MOUNT_VOLUME_PATH`.

### 4. Generate local TLS certificates

This step installs the local CA via `mkcert` and writes certificates to `secrets/certs/`.

```bash
bash scripts/generate-local-certs.sh
```

Generated files:

- `secrets/certs/cert.pem`
- `secrets/certs/key.pem`
- `secrets/certs/rootCA.pem`

### 5. Bootstrap Docker secrets

Generate the file-based secrets referenced by the root Compose file.

```bash
bash scripts/bootstrap-secrets.sh --env-file .env
```

Notes:

- Secret files are written under `secrets/**/*.txt`.
- Existing files are preserved unless you pass `--force`.
- Some values are intentionally placeholders, for example Slack and SMTP credentials. Replace every `CHANGE_ME_*` value before enabling the integrations that depend on them.
- To fail fast on unresolved placeholders, run:

```bash
bash scripts/bootstrap-secrets.sh --env-file .env --strict
```

### 6. Validate the composed configuration

Run static validation before touching the Docker daemon state.

```bash
bash scripts/validate-docker-compose.sh
```

This script creates temporary dummy secret files only when needed and runs `docker compose config`.

### 7. Run the runtime preflight

Check the `.env`, certs, required secret files, mount directories, and optional external networks.

```bash
bash scripts/preflight-compose.sh
```

Warnings for optional-stack secrets or networks do not block the default core boot.

### 8. Start the default stack

Bring up the profiles defined in `COMPOSE_PROFILES`, which default to `core,data,obs`.

```bash
docker compose up -d
```

### 9. Open the initial endpoints

After the default stack is healthy, use the configured `DEFAULT_URL` to reach the main dashboards.

- Traefik dashboard: `https://dashboard.<DEFAULT_URL>`
- Keycloak: `https://keycloak.<DEFAULT_URL>`
- Grafana: `https://grafana.<DEFAULT_URL>`

With the default `.env.example`, those become:

- `https://dashboard.127.0.0.1.nip.io`
- `https://keycloak.127.0.0.1.nip.io`
- `https://grafana.127.0.0.1.nip.io`

## Configuration

### Core environment variables

Use [`.env.example`](.env.example) as the full reference. The table below covers the settings most readers need to understand first.

| Variable | Default | Description |
| --- | --- | --- |
| `DEFAULT_URL` | `127.0.0.1.nip.io` | Base domain for service ingress and certificate generation |
| `DEFAULT_TIMEZONE` | `Asia/Seoul` | Default timezone injected into services that honor it |
| `COMPOSE_PROFILES` | `core,data,obs` | Profiles enabled by default when no `--profile` flags are supplied |
| `DEFAULT_MOUNT_VOLUME_PATH` | `/home/hy/volumes` | Root host path for bind-mounted persistent volumes |
| `INFRA_SUBNET` | `172.19.0.0/16` | Internal bridge subnet for `infra_net` |
| `INFRA_GATEWAY` | `172.19.0.1` | Gateway IP for `infra_net` |
| `HTTP_HOST_PORT` | `80` | Host port for Traefik HTTP traffic |
| `HTTPS_HOST_PORT` | `443` | Host port for Traefik HTTPS traffic |

### Port variable policy

This repository uses a consistent port convention across Compose files:

- `*_PORT` means the container-side or service-side port.
- `*_HOST_PORT` means the host-exposed port.
- Compose files use `${VAR:-default}` interpolation to keep the root `.env` authoritative.

Examples:

- `POSTGRES_PORT=5432`
- `POSTGRES_HOST_PORT=25432`
- `GRAFANA_PORT=3000`
- `GRAFANA_HOST_PORT=3000`

### Volume path conventions

Persistent data is rooted under `DEFAULT_MOUNT_VOLUME_PATH`, then split by tier.

| Variable | Purpose |
| --- | --- |
| `DEFAULT_AUTH_DIR` | Identity and auth service state |
| `DEFAULT_DATA_DIR` | Databases, object storage, search, and cache |
| `DEFAULT_MESSAGE_BROKER_DIR` | Kafka and related broker state |
| `DEFAULT_OBSERVABILITY_DIR` | Observability stack data |
| `DEFAULT_WORKFLOW_DIR` | Airflow and workflow assets |
| `DEFAULT_AI_MODEL_DIR` | Ollama models and AI artifacts |
| `DEFAULT_TOOLING_DIR` | Tooling services such as SonarQube |

### Compose profiles

Services are included from modular Compose files and activated through profiles.

| Profile | Purpose | Representative services |
| --- | --- | --- |
| `core` | Ingress and identity baseline | Traefik, Keycloak, OAuth2 Proxy |
| `data` | Shared persistence layer | PostgreSQL cluster, Valkey cluster, MinIO, OpenSearch |
| `obs` | Metrics, logs, traces, and dashboards | Prometheus, Grafana, Loki, Tempo, Alloy |
| `messaging` | Event streaming and queueing | Kafka, optional RabbitMQ, optional ksqlDB |
| `workflow` | Orchestration and automation | Airflow, optional n8n |
| `ai` | Local inference and AI UI | Ollama, Open WebUI, Qdrant |
| `tooling` | Engineering and QA tooling | SonarQube and related tools |

### Secrets model

The root [`docker-compose.yml`](docker-compose.yml) declares file-backed secrets and maps them into services through `/run/secrets/...`.

Key points:

- Do not put passwords or tokens directly in `.env`.
- Generate secret files with [`scripts/bootstrap-secrets.sh`](scripts/bootstrap-secrets.sh).
- Keep secret files under `secrets/` with restrictive permissions.
- Replace every generated placeholder before enabling dependent integrations.

## Project Structure

This tree shows the meaningful repository layout. Local-only artifacts such as `node_modules/` and `.env` are omitted.

```text
hy-home.docker/
├── .agent/               # Agent rules, personas, and workflow pillars
├── .claude/              # Shared Claude memory fragments and imported guidance
├── .github/              # CI, issue templates, security policy, and repo automation
├── archive/              # Archived or historical artifacts
├── docs/                 # PRDs, ARDs, ADRs, specs, plans, runbooks, context, guides
│   ├── adr/              # Architectural Decision Records
│   ├── ard/              # Architecture Requirements Documents
│   ├── context/          # System and service context
│   ├── guides/           # Procedural and lifecycle guides
│   ├── manuals/          # Team and collaboration manuals
│   ├── operations/       # Incidents and postmortems (Shared memory)
│   ├── plans/            # Implementation plans
│   ├── prd/              # Product Requirements Documents
│   ├── runbooks/         # Executable runbooks
│   └── specs/            # Technical specifications
├── examples/             # Example assets and supporting reference material
├── infra/                # Tiered service definitions grouped by platform domain
│   ├── 01-gateway/
│   ├── 02-auth/
│   ├── 03-security/
│   ├── 04-data/
│   ├── 05-messaging/
│   ├── 06-observability/
│   ├── 07-workflow/
│   ├── 08-ai/
│   ├── 09-tooling/
│   └── 10-communication/
├── projects/             # Example or companion application projects
├── scripts/              # Bootstrap, validation, and maintenance scripts
├── secrets/              # File-backed Docker secrets and generated certs
├── templates/            # Markdown templates for engineering and product docs
├── tests/                # Global testing policy and cross-cutting test assets
├── AGENTS.md             # Cross-agent working contract for this repository
├── ARCHITECTURE.md       # Global architecture rules and runtime topology
├── CLAUDE.md             # Claude-specific deltas
├── GEMINI.md             # Gemini-specific deltas
├── OPERATIONS.md         # Environment tiers and operational policy
├── docker-compose.yml    # Root Compose entrypoint using include-based assembly
├── .env.example          # Environment defaults and host port configuration
└── README.md             # Primary operator and contributor entrypoint
```

## Architecture Overview

### Root orchestration model

The root [`docker-compose.yml`](docker-compose.yml) is the single entrypoint for the stack. It declares shared networks and secrets, then uses Compose `include` directives to assemble service modules from `infra/<tier>/<service>/docker-compose.yml`.

This keeps the repository modular:

- global concerns live at the root
- tier-specific services stay isolated in `infra/`
- profile selection decides what actually boots

### Network model

The repository defines three top-level networks:

| Network | Type | Purpose |
| --- | --- | --- |
| `infra_net` | Internal bridge | Primary service-to-service backbone |
| `project_net` | External | Optional integration point for other Docker projects |
| `kind` | External | Optional integration point for KinD or Kubernetes testing |

### Tiered service map

The platform is organized into ten logical tiers:

| Tier | Role | Example services |
| --- | --- | --- |
| `01-gateway` | Edge routing and ingress | Traefik, Nginx |
| `02-auth` | Identity and access proxy | Keycloak, OAuth2 Proxy |
| `03-security` | Secret management | Vault |
| `04-data` | Databases, cache, object and search storage | PostgreSQL, Valkey, MinIO, OpenSearch, Qdrant |
| `05-messaging` | Streams and queues | Kafka, RabbitMQ, ksqlDB |
| `06-observability` | Metrics, logs, traces, dashboards | Prometheus, Grafana, Loki, Tempo |
| `07-workflow` | Workflow execution and scheduling | Airflow, n8n |
| `08-ai` | Local inference and AI interfaces | Ollama, Open WebUI |
| `09-tooling` | QA and platform tooling | SonarQube, Terrakube, Locust |
| `10-communication` | Mail and relay tooling | Stalwart and related services |

### Profile-driven composition

The root compose file includes more modules than the default boot starts. Actual runtime scope is controlled by profiles defined in the included service files.

Examples:

- `core,data,obs` is the default baseline from `.env.example`
- `messaging` activates Kafka-related services
- `workflow` activates Airflow
- `ai` activates Ollama, Open WebUI, and AI-supporting services
- `tooling` activates SonarQube and related tooling

### Secrets-first and security baseline

The architecture intentionally keeps sensitive values out of `.env`.

Repository-wide rules:

- credentials are stored in `secrets/**/*.txt`
- services consume them via Docker secrets under `/run/secrets/`
- root architecture policy lives in [`ARCHITECTURE.md`](ARCHITECTURE.md)
- operational policy lives in [`OPERATIONS.md`](OPERATIONS.md)

## Running The Stack

### Start the default profiles

Use the profiles declared by `COMPOSE_PROFILES` in `.env`.

```bash
docker compose up -d
```

### Start specific profiles

Add profile flags when you want more than the default baseline.

```bash
docker compose --profile core --profile data --profile obs up -d
docker compose --profile messaging up -d
docker compose --profile workflow up -d
docker compose --profile ai up -d
docker compose --profile tooling up -d
```

If a service is included in the root compose file but does not appear at runtime, check its profile in the corresponding `infra/**/docker-compose.yml`.

### Inspect the fully rendered configuration

Use Compose interpolation output when debugging merged configuration.

```bash
docker compose config
```

### Follow logs

Inspect service logs after startup or while debugging.

```bash
docker compose logs -f
docker compose logs -f traefik
docker compose logs -f keycloak
```

### Restart or stop the stack

Use standard Compose lifecycle commands at the repo root.

```bash
docker compose restart
docker compose down
```

### Access the main dashboards

With `DEFAULT_URL=127.0.0.1.nip.io`, the main endpoints are:

- Traefik dashboard: `https://dashboard.127.0.0.1.nip.io`
- Keycloak: `https://keycloak.127.0.0.1.nip.io`
- Grafana: `https://grafana.127.0.0.1.nip.io`

Additional profile-specific services expose their own `https://<service>.<DEFAULT_URL>` routes through Traefik labels.

## Available Scripts And Validation Workflow

Use repository scripts instead of ad hoc commands whenever possible.

| Script / Command | Purpose |
| --- | --- |
| `bash scripts/generate-local-certs.sh` | Install local CA with `mkcert` and generate TLS files under `secrets/certs/` |
| `bash scripts/bootstrap-secrets.sh --env-file .env` | Generate file-backed Docker secrets without overwriting existing files |
| `bash scripts/bootstrap-secrets.sh --env-file .env --strict` | Fail if generated placeholders remain unresolved |
| `bash scripts/validate-docker-compose.sh` | Run static Compose validation with temporary dummy prerequisites |
| `bash scripts/preflight-compose.sh` | Check runtime prerequisites before starting containers |
| `pre-commit run --all-files` | Run repo-wide lint, security, and config validation hooks |

Validation order:

1. update `.env`
2. generate certs
3. bootstrap secrets
4. validate compose
5. run preflight
6. start or update the stack

CI mirrors the same philosophy:

- `pre-commit` runs in [`.github/workflows/ci-quality.yml`](.github/workflows/ci-quality.yml)
- `zizmor` scans GitHub Actions configuration in the same workflow

## Testing And Quality Gates

This repository is infrastructure-heavy, so most validation happens through configuration checks, script verification, and policy enforcement rather than a single application test runner.

Contributor expectations:

- run `pre-commit run --all-files`
- run `bash scripts/validate-docker-compose.sh`
- run `bash scripts/preflight-compose.sh` when your change affects runtime behavior
- follow test coverage and testing-layer requirements for code changes, as documented in deeper testing policy

Quality tooling currently includes:

- YAML linting
- Markdown linting
- ShellCheck
- Hadolint
- actionlint
- gitleaks
- `zizmor`
- project-specific ESLint hooks for the storybook examples

For deeper policy, read:

- [`tests/README.md`](tests/README.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml)

## Deployment And Operations

### Supported environment tiers

[`OPERATIONS.md`](OPERATIONS.md) defines three operating tiers:

| Tier | Name | Purpose |
| --- | --- | --- |
| `L1` | Local Dev | Service iteration and specification validation on a developer machine |
| `L2` | Home-Lab | 24/7 internal services on dedicated self-hosted hardware |
| `L3` | Pro-Lab | Higher-capacity hosts for resilience testing and benchmarking |

### Recommended deployment flow

For local and homelab deployment, this repository is the deployment artifact.

Recommended flow:

1. prepare `.env`
2. create host mount directories
3. generate certificates
4. bootstrap secrets
5. validate compose
6. run preflight
7. start the required profiles
8. verify ingress, auth, and observability routes
9. consult runbooks before making manual recovery changes

### Production-style checklist

- [ ] `.env` reviewed for host ports, domain, profiles, and mount paths
- [ ] required secret files created under `secrets/`
- [ ] placeholder values replaced for enabled integrations
- [ ] local certificates generated
- [ ] `docker compose config` validation passes
- [ ] preflight passes for required directories and files
- [ ] observability endpoints are reachable after boot
- [ ] recovery and maintenance paths are known before the system is treated as persistent infrastructure

### Where to go deeper

Use these docs instead of expanding the root README into an operating manual:

- [`docs/runbooks/README.md`](docs/runbooks/README.md) for executable recovery procedures
- [`docs/context/README.md`](docs/context/README.md) for service-specific architecture and operations context
- [`docs/gateway.md`](docs/agentic/gateway.md) for the AI agent discovery hub

## Troubleshooting

For common issues regarding secrets, certificates, or network configuration, refer to the [Troubleshooting Guide](docs/guides/troubleshooting.md).

## Contributing

We welcome contributions! Please read our [Contributing Guide](docs/guides/contributing-guide.md) and [Collaboration Guide](docs/manuals/collaboration-guide.md) before getting started.

## Related Documentation

- [`AGENTS.md`](AGENTS.md): Global agent contract.
- [`ARCHITECTURE.md`](ARCHITECTURE.md): Architectural invariants.
- [`OPERATIONS.md`](OPERATIONS.md): Operational index.
- [`docs/README.md`](docs/README.md): Documentation taxonomy and index.

## License

This repository is distributed under the Apache License 2.0.
