---
trigger: model_decision
glob: ["k8s/**/*.yml", "k8s/**/*.yaml", "helm/**", "manifests/**/*.yaml"]
description: "Security Guardrails: Enforces Kubernetes workload security, including non-root execution, immutable images, and network isolation."
---

# Security Guardrails Standard

- **Role**: Cloud Security Architect / Platform Owner
- **Purpose**: Define mandatory security guardrails for containerized workloads to ensure isolation, immutability, and least-privilege operations.
- **Activates When**: Creating or updating Kubernetes manifests, Helm charts, or infrastructure-as-code deployment configurations.

**Trigger**: model_decision — Apply during the design and deployment of cloud-native workloads.

## 1. Standards

### Principles

- **[REQ-GRD-01] Least-Privilege Execution**
  - Containers MUST run with the minimum required OS capabilities. The use of `privileged: true` or `hostNetwork` is STRICTLY PROHIBITED.
- **[REQ-GRD-02] Configuration Immutability**
  - Workload images MUST be pinned using immutable SHA-256 digests. The use of the `:latest` tag is PROHIBITED in production environments.
- **[REQ-GRD-03] Default-Deny Network Isolation**
  - All namespaces MUST implement a `default-deny` NetworkPolicy, with only explicit whitelisting for required ingress and egress traffic.

### Workload Hardening Matrix

| Guardrail | Requirement ID | Mandatory Value |
| --- | --- | --- |
| Non-Root | [REQ-GRD-04] | `runAsNonRoot: true` |
| Read-Only Root | [REQ-GRD-05] | `readOnlyRootFilesystem: true` |
| Privilege Escalation| [REQ-GRD-06] | `allowPrivilegeEscalation: false` |
| Capabilities | [REQ-GRD-07] | `drop: ["ALL"]` |

### Must

- **[REQ-GRD-08] Dedicated Service Accounts**
  - Every unique workload MUST utilize a dedicated Kubernetes ServiceAccount with scoped permissions instead of the `default` account.
- **[REQ-GRD-09] Explicit Resource Limits**
  - All container definitions MUST specify `requests` and `limits` for CPU and Memory to prevent resource exhaustion and DoS.
- **[REQ-GRD-10] Secure Secret Injection**
  - Sensitive data MUST be injected via Kubernetes Secrets or an external Vault provider. Plaintext secrets in YAML manifests are STRICTLY PROHIBITED.

### Must Not

- **[BAN-GRD-01] Host Path Access**
  - Workloads MUST NOT use `hostPath` volumes unless justified for system-level monitoring agents.
- **[BAN-GRD-02] Unfiltered Capabilities**
  - Do NOT add Linux capabilities (e.g., `CAP_SYS_ADMIN`) unless they are vital for the application's core function.

### Failure Handling

- **Stop Condition**: Stop deployment if a workload manifest is identified as running as the `root` user or using an unpinned container image tag.

## 2. Procedures

- **[PROC-GRD-01] Manifest Security Scan**
  - IF modifying K8s manifests THEN MUST run a static analysis tool (e.g., Kube-score, Checkov) to verify compliance with guardrail standards.
- **[PROC-GRD-02] Network Verification**
  - Perform weekly connectivity audits to ensure that NetworkPolicies correctly isolate cross-namespace traffic.

## 3. Examples

### Secure Pod Security Context (Good)

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
containers:
  - name: app
    securityContext:
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
```

## 4. Validation Criteria

- **[VAL-GRD-01] Static Audit Pass**
  - [ ] Automated security scanners confirm 100% compliance with non-root and immutable image requirements.
- **[VAL-GRD-02] Policy Enforcement**
  - [ ] Integration tests verify that an unauthorized pod cannot communicate with the secured workload.
- **[VAL-GRD-03] Secret integrity**
  - [ ] Binary audit of YAML manifests confirms zero instances of plaintext API keys or certificates.
