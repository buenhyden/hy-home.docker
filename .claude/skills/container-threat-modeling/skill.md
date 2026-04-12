---
name: container-threat-modeling
description: >
  STRIDE/DREAD threat modeling methodology adapted for Docker container environments.
  Container trust boundary analysis, attack tree construction, and NIST CSF mapping.
  Use for 'threat model', 'STRIDE analysis', 'container security', 'attack surface',
  'trust boundary', 'DREAD scoring', 'attack tree', 'security review before deployment'.
  Enhances security-auditor and workflow-supervisor. Note: active penetration testing
  and live exploit execution are outside scope.
---

# Container Threat Modeling — STRIDE/DREAD for Docker Stacks

Systematic threat identification and risk scoring for Docker Compose service stacks.

## STRIDE Threat Classification

| Category | Threat | Security Property | Typical Container Pattern |
|----------|--------|-------------------|--------------------------|
| **S**poofing | Impersonating a service identity | Authentication | Weak or absent mTLS between services |
| **T**ampering | Modifying data in transit or at rest | Integrity | Writable container root filesystem |
| **R**epudiation | Denying an action occurred | Non-repudiation | Missing structured audit logging |
| **I**nformation Disclosure | Exposing sensitive data | Confidentiality | Plaintext env vars, container inspect leakage |
| **D**enial of Service | Disrupting service availability | Availability | No resource limits (`mem_limit`/`cpus` absent) |
| **E**levation of Privilege | Gaining unintended permissions | Authorization | Running as root, missing `no-new-privileges` |

## Trust Boundary Mapping — hy-home.docker Stack

```
Internet
    │ HTTPS/443
    ▼ [Trust Boundary: External → Gateway]
┌─────────┐
│ Traefik │  ← Only container exposing external ports
└────┬────┘
     │ HTTP (infra_net)
     ▼ [Trust Boundary: Gateway → Application Services]
┌──────────┐    ┌──────────┐    ┌───────────┐
│ Keycloak │    │ Services │    │ Open-WebUI│
└────┬─────┘    └────┬─────┘    └─────┬─────┘
     │               │                │
     │ [Trust Boundary: Services → Data Stores]
     ▼               ▼                ▼
┌──────────┐   ┌───────────┐   ┌───────────┐
│PostgreSQL│   │  Kafka    │   │  Ollama   │
└──────────┘   └───────────┘   └───────────┘
                                     │
                               ┌─────▼────┐   ┌──────────┐
                               │OpenSearch│   │  MinIO   │
                               └──────────┘   └──────────┘

[Trust Boundary: All Services → Secrets]
→ /run/secrets/* mounts only (Docker Secrets)
→ No env-var plaintext
```

## Per-boundary STRIDE Analysis Template

```markdown
### Boundary: [Source] → [Destination]

| Threat | Risk | Likelihood | Impact | Mitigation |
|--------|------|-----------|--------|------------|
| S: Token replay | HIGH | Medium | High | Short-lived JWTs, token revocation |
| T: Header injection | MED | Low | Medium | Input validation at gateway |
| R: Request non-attribution | MED | Medium | Low | Structured request logging with correlation ID |
| I: Credential in logs | CRIT | High | Critical | Log sanitisation, no credential echo |
| D: Resource exhaustion | HIGH | Medium | High | Rate limiting, `mem_limit` enforcement |
| E: Container escape | CRIT | Low | Critical | `no-new-privileges`, non-root user |
```

## DREAD Risk Scoring

Score each identified threat 1–10 per dimension:

```
Damage          — Impact if successfully exploited
Reproducibility — How reliably can the attack be repeated?
Exploitability  — Skill and resources needed to execute
Affected Users  — Proportion of users/services impacted
Discoverability — How easy is it to find this vulnerability?

Risk Score = (D + R + E + A + D) / 5

8–10: Critical — Immediate remediation required
5–7:  High     — Fix within current sprint
3–4:  Medium   — Schedule in backlog
1–2:  Low      — Document and monitor
```

### Example: Unauthenticated Internal Service Access

```
Threat: Service B on infra_net directly calls Service A without auth token
├── Damage:          8 (service A state manipulable)
├── Reproducibility: 9 (trivially repeatable within network)
├── Exploitability:  6 (requires infra_net access — container compromise first)
├── Affected Users:  7 (all users of Service A)
├── Discoverability: 5 (requires network sniffing or source access)
└── Risk Score:     (8+9+6+7+5)/5 = 7.0 → High
```

## Attack Tree — Common Container Attack Paths

```
Goal: Obtain database credentials

OR ─┬── Plaintext in compose env section
    │     check: grep -r "POSTGRES_PASSWORD=" docker-compose*.yml
    │
    ├── Container env leak via docker inspect
    │     check: docker inspect <svc> | jq '.[].Config.Env'
    │
    ├── Secret mount world-readable
    │     check: ls -la /run/secrets/
    │
    └── AND ─┬── Compromise Traefik container
             └── Lateral move to postgres via infra_net
```

## Audit Checklist — Pre-deployment Threat Review

### Authentication & Identity (Spoofing)
- [ ] Service-to-service calls use token validation or mTLS
- [ ] Keycloak realm and client settings reviewed
- [ ] Default passwords changed or managed via Docker Secrets
- [ ] Admin endpoints not exposed externally

### Data Integrity (Tampering)
- [ ] Writable volumes restricted to necessary paths
- [ ] Database migrations use checksums or version control
- [ ] Network traffic between sensitive services uses TLS

### Audit Trail (Repudiation)
- [ ] Structured JSON logging enabled on all services
- [ ] Log driver configured (json-file with rotation, or remote)
- [ ] Auth events logged by Keycloak

### Data Exposure (Information Disclosure)
- [ ] No credentials in compose env sections — only `_FILE` references to secrets
- [ ] Container inspect output clean of credentials
- [ ] Debug endpoints disabled in production images

### Availability (Denial of Service)
- [ ] `mem_limit` and `cpus` set on all containers
- [ ] Traefik rate limiting enabled
- [ ] Health-check `retries` and `start_period` configured
- [ ] Stateful services have restart policies

### Privilege (Elevation of Privilege)
- [ ] `no-new-privileges: true` on all containers
- [ ] Services run as non-root user
- [ ] `privileged: false` (not overridden)
- [ ] Specific `cap_drop: ALL` with minimal `cap_add` where needed

## NIST CSF Gap Assessment Template

| Function | Sub-category | Current Implementation | Gap | Priority |
|----------|-------------|----------------------|-----|----------|
| **Identify** | Asset inventory | Docker Compose service list | Missing image SBOMs | HIGH |
| **Protect** | Access control | infra_net isolation, Docker Secrets | No mTLS between services | MED |
| **Detect** | Anomaly detection | Docker healthchecks | No SIEM/log aggregation | HIGH |
| **Respond** | Response plan | incident-responder agent | No automated alerting | MED |
| **Recover** | Recovery plan | Volume backup labels | No tested restore procedure | HIGH |

## Output Format

Produce `_workspace/threat_model_<YYYY-MM-DD>.md`:

```
# Container Threat Model — YYYY-MM-DD

## Scope
- Services analysed: [list]
- Trigger: [new service / routine / incident]

## Trust Boundary Analysis
[Per-boundary STRIDE table]

## DREAD Risk Register
| Threat ID | Description | D | R | E | A | D | Score | Priority |
|-----------|-------------|---|---|---|---|---|-------|----------|

## Attack Trees
[Critical path attack trees]

## Findings Summary
| ID | Severity | Finding | STRIDE Category | Mitigation |

## NIST CSF Gap Table
[Gap assessment]

## Remediation Roadmap
### Immediate (0–48h)
### Short-term (1–4 weeks)
### Long-term (1–3 months)
```
