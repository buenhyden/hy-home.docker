# Local Development Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Accelerate local startup speed, simplify service management, and reduce resource footprint for infrastructure services.

**Architecture:**

1. Introduce a new `dev` profile for "bare-minimum" infrastructure.
2. Optimize `common-optimizations.yml` by introducing `dev` specific templates with reduced healthcheck intervals and more aggressive resource constraints.
3. Simplify `.env` management to support the `dev` workflow.

**Tech Stack:** Docker Compose v3.8+, YAML, Shell scripts.

---

### Task 1: Initialize Dev Templates in common-optimizations.yml

**Files:**

- Modify: `infra/common-optimizations.yml`

**Step 1: Add dev-specific resource and healthcheck constants**

Add anchors for faster healthchecks and minimal resources.

```yaml
x-healthcheck-dev: &healthcheck-dev
  interval: 5s
  timeout: 5s
  retries: 3
  start_period: 5s

x-resource-dev-tiny: &resource-dev-tiny
  cpus: "0.10"
  mem_limit: 64m

x-resource-dev-small: &resource-dev-small
  cpus: "0.20"
  mem_limit: 128m
```

**Step 2: Add template-dev-infra service**

```yaml
  template-dev-tiny:
    <<: [*service-defaults, *resource-dev-tiny]
    healthcheck: *healthcheck-dev

  template-dev-small:
    <<: [*service-defaults, *resource-dev-small]
    healthcheck: *healthcheck-dev
```

**Step 3: Commit**

```bash
git add infra/common-optimizations.yml
git commit -m "infra: add dev optimization templates"
```

---

### Task 2: Apply Dev Profile to Core Services

**Files:**

- Modify: `infra/01-gateway/traefik/docker-compose.yml`
- Modify: `infra/04-data/mng-db/docker-compose.yml`

**Step 1: Update Traefik to include 'dev' profile**

Add `- dev` to profiles list.

**Step 2: Update Management DB to include 'dev' profile**

Add `- dev` to `mng-pg` and `mng-valkey`.

**Step 3: Commit**

```bash
git add infra/01-gateway/traefik/docker-compose.yml infra/04-data/mng-db/docker-compose.yml
git commit -m "infra: enable dev profile for core gateway and databases"
```

---

### Task 3: Optimize .env.example for Dev Workflow

**Files:**

- Modify: `.env.example`

**Step 1: Add documentation for COMPOSE_PROFILES="dev"**

Update the comment around line 8 to suggest using `dev` for faster startup.

---

### Task 4: Create 'dev-up' utility script

**Files:**

- Create: `scripts/dev-up.sh` [NEW]

**Step 1: Implement the script**

```bash
#!/bin/bash
# scripts/dev-up.sh
# Quickly start the minimal development infrastructure.

docker compose --profile dev up -d --remove-orphans
```

**Step 2: Make executable**
Run: `chmod +x scripts/dev-up.sh`

**Step 3: Commit**

```bash
## User Review Required

> [!IMPORTANT]
> This change introduces a new `dev` profile which will be the recommended way to start the stack for local development. It sets aggressive defaults for resource limits and healthchecks. Please verify if the proposed `mem_limit` (64m/128m) is sufficient for your local machine's base load.

---

## Verification Plan

### Automated Tests
- Run `scripts/validate-docker-compose.sh` to ensure the new YAML structure is valid.
- Run `docker compose --profile dev config` to verify the merged configuration.

### Manual Verification
1. Run `scripts/dev-up.sh` and verify:
   - Only `traefik`, `mng-pg`, and `mng-valkey` (and their init jobs) are started.
   - Observability services (Grafana, Prometheus, etc.) are NOT started.
2. Check `docker stats` to confirm `mem_limit` is applied as expected.
3. Verify that `traefik` dashboard is accessible at `dashboard.127.0.0.1.nip.io`.
