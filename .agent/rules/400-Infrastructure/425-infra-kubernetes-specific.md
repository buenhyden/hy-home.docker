---
trigger: always_on
glob: "**/*.{yaml,yml}"
description: "Kubernetes: Deployment manifests, resource limits, security contexts, and autoscaling."
---
# Kubernetes Manifest Standards

## 1. Manifest Standards (YAML)

- **Declarative**: Use declarative YAML over imperative commands.
- **Documentation**: Use MkDocs for K8s docs. Validate YAML snippets.
- **Labels**: consistent `app`, `version`, `env`. Use `app.kubernetes.io/name`.
- **Resources**: ALWAYS define `requests` and `limits` for CPU/Memory.
- **Probes**: Define `livenessProbe` and `readinessProbe` for all services.

## 2. Security

- **Security Context**:
  - `runAsNonRoot: true`
  - `readOnlyRootFilesystem: true` (if possible)
- **Secrets**: Use K8s Secrets or external secret stores. Never ConfigMaps for sensitive data.

## 3. Autoscaling

- **HPA**: Use Horizontal Pod Autoscaler based on CPU/Memory utilization.
- **PDB**: Define Pod Disruption Budgets for high availability during upgrades.

### Example: Deployment Spec

#### Good

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: app
        image: my-app:1.0.0
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
```

#### Bad

```yaml
# Missing resources, running as root (default)
containers:
- name: app
  image: my-app:latest
```
