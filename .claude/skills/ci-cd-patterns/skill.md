---
name: ci-cd-patterns
description: >
  CI/CD pipeline patterns for hy-home.docker: Docker Compose deployment strategies (Rolling,
  Blue-Green, Canary via Traefik), pipeline security gate design (SAST/SCA/Secret/Container
  scanning), GitHub Actions workflow patterns, health check design, DORA metrics, and
  rollback procedures. Use for 'deployment strategy', 'blue-green', 'canary', 'rolling update',
  'pipeline security', 'SAST', 'Gitleaks', 'Trivy', 'DORA metrics', 'rollback'.
  Enhances infra-implementer, security-auditor, and code-reviewer for GitHub Actions work.
  Note: actual deployment execution is outside scope.
---

# CI/CD Patterns — Deployment and Pipeline Reference for hy-home.docker

Adapted deployment strategies and pipeline security patterns for a Docker Compose + Traefik + GitHub Actions stack.

## Deployment Strategy Comparison

| Strategy | Downtime | Risk | Extra Resources | Rollback Speed | Suitable For |
|----------|----------|------|----------------|---------------|-------------|
| **Recreate** | Yes | High | None | Slow | Dev / non-critical |
| **Rolling** | None | Medium | Minimal | Medium | Standard service updates |
| **Blue-Green** | None | Low | 2x service instances | Instant (Traefik switch) | Mission-critical services |
| **Canary** | None | Very Low | Minimal (weighted routing) | Instant (weight to 0%) | Gradual feature rollout |

---

## Docker Compose Deployment Patterns

### Rolling Update (Default Docker Compose Approach)

Replace service instances one at a time. Suitable for stateless services.

```bash
# Pull new image
docker pull myservice:v2.0.0

# Update service without taking down dependents
docker compose up -d --no-deps --pull=never myservice

# Verify health before declaring success
docker compose ps myservice
```

Requirements:
- Service must have a health-check defined (`healthcheck.test`, `interval`, `retries`)
- Upstream service (Traefik) must have retry logic or connection draining
- Image must be backward-compatible with running data schemas

Rollback:
```bash
# Pin image back to previous tag in compose file, then:
docker compose up -d --no-deps myservice
```

---

### Blue-Green Deployment (Traefik Router Switch)

Run two service versions simultaneously; switch Traefik routing atomically.

**Compose setup** — use profile-based service variants:

```yaml
services:
  myservice-blue:
    image: myservice:v1.0.0
    profiles: [blue]
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.myservice-blue.rule=Host(`svc.example.com`) && Headers(`X-Deploy-Slot`, `blue`)"
    networks:
      - infra_net

  myservice-green:
    image: myservice:v2.0.0
    profiles: [green]
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.myservice-green.rule=Host(`svc.example.com`)"
    networks:
      - infra_net
```

**Switch procedure**:
1. Deploy green with `docker compose --profile green up -d myservice-green`.
2. Run smoke tests against green (internal access or header-based routing).
3. Swap Traefik router rules: make green the primary host route; make blue header-gated.
4. Monitor for 15 minutes; if stable, stop blue with `docker compose --profile blue stop`.

**Rollback**: Re-enable blue router rule; disable green → instant.

---

### Canary Deployment (Traefik Weighted Routing)

Route a small percentage of production traffic to the new version.

```yaml
# Traefik dynamic configuration for weighted canary
http:
  services:
    myservice-canary:
      weighted:
        services:
          - name: myservice-stable
            weight: 95
          - name: myservice-canary
            weight: 5
```

**Stage progression**:

| Stage | Canary Weight | Wait | Validation |
|-------|--------------|------|-----------|
| 1 | 5% | 15 min | HTTP error rate, p99 latency |
| 2 | 20% | 30 min | + container health, memory |
| 3 | 50% | 60 min | + business metrics (if available) |
| 4 | 100% | — | Remove stable; canary becomes primary |

**Automatic rollback conditions**:
- HTTP 5xx rate > 2% sustained for 5 minutes
- p99 latency > 2× baseline sustained for 5 minutes
- Container restart count > 2 within 10 minutes

**Rollback**: Set canary weight to 0%; stable handles 100% traffic instantly.

---

## Health Check Design

### Three-Level Health Checks

| Type | Purpose | Compose Key | Typical Endpoint |
|------|---------|-------------|-----------------|
| **Liveness** | Is the process alive? | `healthcheck.test` | `/healthz` or `pg_isready` |
| **Readiness** | Ready to serve traffic? | `healthcheck.start_period` | `/readyz` or app-level check |
| **Startup** | Has initialisation completed? | `healthcheck.start_period` with long timeout | Same as liveness |

**Compose health-check pattern**:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/healthz"]
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 30s     # Allow startup before counting failures
```

**Traefik health-check integration**:

```yaml
labels:
  - "traefik.http.services.myservice.loadbalancer.healthcheck.path=/healthz"
  - "traefik.http.services.myservice.loadbalancer.healthcheck.interval=10s"
```

### Rollback Triggers

| Metric | Threshold | Duration | Action |
|--------|-----------|---------|--------|
| HTTP 5xx rate | > 5% | 2 min | Trigger rollback alert |
| p99 latency | > 3× SLO baseline | 5 min | Trigger rollback |
| Container restarts | > 3 | Within 10 min | Trigger rollback |
| Memory usage | > 90% mem_limit | 5 min | Trigger OOM alert |

---

## Pipeline Security Gates

### Gate Placement — GitHub Actions

```
[Pre-Commit Hook]
  ├── Secret detection (Gitleaks or detect-secrets)
  └── YAML lint / docker-compose validate

[Pull Request Check]
  ├── SAST: Semgrep (OWASP rule packs)
  ├── SCA: Dependabot alerts / Trivy fs scan
  ├── Secret scan: Gitleaks full history
  └── Compose lint: validate-docker-compose.sh

[Build]
  ├── Container image scan: Trivy image
  ├── SBOM generation: Syft or Trivy SBOM
  └── Image pinned digest verification

[Staging deploy]
  └── Smoke test + integration health check

[Production deploy]
  └── Manual approval gate (GitHub Environment protection rule)
```

### Gate Block/Warn Policy

| Scan Type | Critical | High | Medium | Low |
|-----------|----------|------|--------|-----|
| SAST | Block | Block | Warn | Ignore |
| SCA (CVE) | Block | Block | Warn | Ignore |
| Secret detection | Block | Block | Block | Warn |
| Container image | Block | Warn | Ignore | Ignore |
| IaC (compose) | Block | Warn | Ignore | Ignore |

### Recommended Tool Selection (hy-home.docker)

| Gate | Tool | Why |
|------|------|-----|
| Secret detection | Gitleaks | Full Git history scan; fast; pre-commit hook support |
| SAST | Semgrep | OWASP rule packs; Docker-specific rules available; open source |
| SCA | Trivy | Covers OS packages + app dependencies + container image in one tool |
| Container scan | Trivy | Unified with SCA; generates SBOM |
| SBOM | Syft or Trivy | CycloneDX format; attestable |

### GitHub Actions Snippet Templates

```yaml
# Secret detection
- uses: gitleaks/gitleaks-action@v2
  with:
    config-path: .gitleaks.toml

# Trivy container + SCA
- uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'image'
    image-ref: '${{ env.IMAGE }}'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'
    format: 'sarif'
    output: 'trivy-results.sarif'

# Compose validation gate
- name: Validate docker-compose
  run: bash scripts/validate-docker-compose.sh
```

### Vulnerability SLA (CVSS v3.1)

| Rating | CVSS | Fix Deadline | Pipeline Action |
|--------|------|-------------|-----------------|
| Critical | 9.0–10.0 | Within 24 hours | Block merge |
| High | 7.0–8.9 | Within 7 days | Block merge |
| Medium | 4.0–6.9 | Within 30 days | Warn; allow merge |
| Low | 0.1–3.9 | Within 90 days | Informational |

---

## DORA Metrics

Four key metrics for pipeline maturity assessment:

| Metric | Calculation | Elite | High | Target for hy-home.docker |
|--------|-------------|-------|------|--------------------------|
| Deployment frequency | Production deploys / period | Multiple/day | Daily-weekly | Weekly (home lab cadence) |
| Lead time | Commit timestamp → deploy timestamp | < 1 hour | < 1 day | < 4 hours |
| Change failure rate | Rollbacks / total deploys × 100 | < 5% | < 15% | < 10% |
| Recovery time | Incident detected → service restored | < 1 hour | < 1 day | < 30 min (MTTR SLO) |

---

## Branch Strategy and Deployment Mapping

```
feature/*  -> PR -> main     (auto: compose validate + SAST + secret scan)
main       -> push           (auto: staging deploy + integration test)
main + tag -> push           (manual approval gate -> production deploy)
hotfix/*   -> PR -> main     (expedited: security review only + emergency approval)
```

---

## Related Governance

- `docs/00.agent-governance/rules/github-governance.md` §4 — GitHub Actions security baseline (unpinned actions, secret exposure, OIDC)
- `.pre-commit-config.yaml` — Pre-commit hooks (linting, secret detection)
- `scripts/validate-docker-compose.sh` — Compose validation gate
