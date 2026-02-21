---
trigger: model_decision
glob:
  - "services/**"
  - "k8s/**/*.yml"
  - "k8s/**/*.yaml"
  - "manifests/**/*.yml"
  - "manifests/**/*.yaml"
  - "helm/**"
  - "configs/**"
  - "feature-flags/**"
description: "Config and feature flags: deterministic configuration ownership, secret separation, versioned config, safe defaults, and kill-switch governance."
---

# 2000-Config-And-Feature-Flags

- **Role**: Configuration Governance Owner
- **Purpose**: Enforce deterministic configuration and feature-flag standards so releases remain safe, reversible, and auditable without leaking secrets or drifting runtime behavior.
- **Activates When**: Adding/changing configuration, environment variables, ConfigMaps/Secrets, or feature-flag definitions and usage.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-CFG-PREREQ-01] Configuration Ownership**
  - Every service MUST declare:
    - owner team
    - config file location
    - runtime config injection method

- **[REQ-CFG-OUT-01] Out of Scope**
  - This Rule does NOT mandate a specific feature-flag vendor.
  - This Rule mandates safety, auditability, and determinism.

---

### 1.2 Config vs Secret Separation

- **[REQ-CFG-SEC-01] Secrets in Secret Stores Only**
  - Secrets MUST be stored in Kubernetes Secrets or external secret providers.
  - Non-secret config MUST be stored in ConfigMaps or equivalent.

- **[BAN-CFG-SEC-01] Plaintext Secrets**
  - Plaintext secrets MUST NOT be committed in:
    - manifests
    - Helm values
    - application config files
    - CI variables committed to repo

---

### 1.3 Deterministic Configuration Injection

- **[REQ-CFG-INJ-01] Explicit Injection Method**
  - Every runtime config value MUST be injected via:
    - env var OR
    - mounted config file OR
    - config service client (feature-flag/config provider)

- **[REQ-CFG-INJ-02] Environment Variable Naming**
  - Env vars MUST use:
    - `UPPER_SNAKE_CASE`
  - Service-specific vars MUST be prefixed with the service name.

- **[REQ-CFG-INJ-03] Versioned Config**
  - Config changes affecting behavior MUST be versioned or traced to a commit SHA.
  - Rollback MUST be possible by redeploying a prior config version.

---

### 1.4 Feature Flag Governance (Decision Rule)

- **[REQ-FF-STD-01] Flags Must Be Declared**
  - Feature flags MUST be declared in a canonical location:
    - `feature-flags/<service>.yaml` OR equivalent registry.

- **[REQ-FF-STD-02] Default State Required**
  - Every flag MUST define:
    - default state
    - owner
    - purpose
    - scope (env/user/tenant)
    - expiration date OR explicit “no-expiration” justification

- **[REQ-FF-STD-03] Kill Switch for High-Risk Features**
  - High-risk features MUST have a kill switch flag that disables the feature immediately.

- **[BAN-FF-STD-01] Permanent Flags Without Governance**
  - Flags MUST NOT remain indefinitely without ownership and expiration/no-expiration justification.

- **[REQ-FF-STD-04] Safe Rollout Modes**
  - Flags MUST support controlled rollout when applicable:
    - percentage rollout OR
    - allow-list rollout

---

### 1.5 Auditability and Change Control

- **[REQ-CFG-AUD-01] Audit Trail**
  - Config and flag changes MUST be auditable:
    - who changed
    - what changed
    - when changed
    - why changed

- **[REQ-CFG-AUD-02] Review Requirement**
  - Changes to production-like config or flags MUST be reviewed and approved via PR process.

---

### 1.6 Success & Failure Behavior

- **[REQ-CFG-SUCCESS-01] Success Criteria**
  - Configuration is valid ONLY if:
    - secrets are separated and not plaintext
    - injection method is explicit
    - behavior-impacting config is versioned/traceable
    - flags are declared with defaults, ownership, and governance

- **[REQ-CFG-FAIL-01] Failure Behavior**
  - Any `[BAN-*]` violation MUST reject the change.
  - Missing flag defaults/ownership MUST block deployment of flag usage.

---

### 1.7 Reference-First

- **[REQ-CFG-REF-01] Canonical Examples**
  - Use canonical examples:
    - `configs/_examples/configmap-baseline.yaml`
    - `configs/_examples/secret-reference-baseline.yaml`
    - `feature-flags/_examples/flag-schema.yaml`
    - `feature-flags/_examples/rollout-strategy.md`

---

## 2. Procedures (Phased Execution)

### Phase P1 — Classify Values

1) Classify each value as secret or non-secret.
2) Place secrets into Secret store and config into ConfigMap or config service.

- **Outcome**: Separation is enforced.

### Phase P2 — Implement Injection

1) Choose injection method (env, mount, config service).
2) Ensure naming conventions and traceability.

- **Outcome**: Runtime behavior is deterministic.

### Phase P3 — Govern Feature Flags

1) Declare flag in registry.
2) Set default, owner, purpose, scope, expiration/no-expiration justification.
3) Add kill switch for high-risk features.

- **Outcome**: Flags are safe and auditable.

### Phase P4 — Validate and Gate

1) Verify no plaintext secrets exist.
2) Verify versioning/traceability and audit trail.

- **Outcome**: Changes are safe to deploy.

---

## 3. Examples

### Good Example — Controlled Rollout Flag

**Input**

- New feature flag declared with default off, 10% rollout, owner, expiration date, and kill switch.

**Expected Output**

- Feature can be enabled gradually and disabled immediately.

### Bad Example — Secret in Config File

**Input**

- API token committed in application YAML config.

**Rejected Because**

- Violates `[BAN-CFG-SEC-01]`.

---

## 4. Validation Criteria (Final Checklist)

- [ ] Secrets are stored only in secret stores; no plaintext secrets. (`[REQ-CFG-SEC-01]`, `[BAN-CFG-SEC-01]`)
- [ ] Injection method is explicit and naming conventions applied. (`[REQ-CFG-INJ-*]`)
- [ ] Behavior-impacting config is versioned/traceable and rollbackable. (`[REQ-CFG-INJ-03]`)
- [ ] Flags are declared with defaults, owner, purpose, scope, and expiration governance. (`[REQ-FF-STD-*]`, `[BAN-FF-STD-01]`)
- [ ] Audit trail and PR review exist for production-like changes. (`[REQ-CFG-AUD-*]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- @0200-Security-Guardrails.md
- examples/configs/configmap-baseline.yaml
- examples/configs/secret-reference-baseline.yaml
- examples/feature-flags/flag-schema.yaml
- examples/feature-flags/rollout-strategy.md
