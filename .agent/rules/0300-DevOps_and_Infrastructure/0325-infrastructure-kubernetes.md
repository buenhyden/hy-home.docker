---
trigger: model_decision
glob: ["k8s/**/*.yml", "helm/**"]
description: "Kubernetes Standards: Resource management, Liveness/Readiness probes, and Deployment strategies."
---

# 0325-Infrastructure-Kubernetes

- **Role**: Kubernetes Operator
- **Purpose**: Ensure reliable, scalable, and manageable Kubernetes workoads.
- **Activates When**: Writing K8s manifests (Deployment, Service, Ingress).

## 1. Standards

### 1.1 Principles

- **[REQ-K8S-OPS-01] Reliability**: Workloads MUST define Health Checks (Probes).
- **[REQ-K8S-OPS-02] Scalability**: Workloads MUST define Resource Requests and Limits.
- **[REQ-K8S-OPS-03] Discovery**: Services MUST use Labels and Selectors consistently.

### 1.2 Scope

- **In-Scope**: Deployments, StatefulSets, Services, Ingress, HPA.
- **Out-of-Scope**: Security Policies (see 0200-Security-Guardrails).

### 1.3 Must / Must Not

- **[REQ-K8S-RES-01] Requests/Limits**: CPU and Memory requests/limits MUST be set.
- **[REQ-K8S-PRB-01] Probes**: Liveness and Readiness probes MUST be configured.
- **[BAN-K8S-CFG-01] No Hardcoding**: Configuration MUST handle via ConfigMaps/Secrets.

## 2. Procedures

### 2.1 Deployment Checklist

1. **Replicas**: Set `replicas` > 1 for HA.
2. **Resources**: Set `requests` (guaranteed) and `limits` (burst).
3. **Probes**:
    - **Liveness**: Restart if dead.
    - **Readiness**: Remove from load balancer if busy/starting.

## 3. Examples

### 3.1 Production Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
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
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
```

## 4. Validation Criteria

- [ ] **[VAL-K8S-RES-01]** Resources are defined.
- [ ] **[VAL-K8S-PRB-01]** Probes are defined.
- [ ] **[VAL-K8S-LBL-01]** Labels follow standard `app.kubernetes.io/name`.

## 5. References

- Related: [0200-security-guardrails.md](../2200-Security/0200-security-guardrails.md)
