---
description: Workflow for Kubernetes resource creation and deployment
---

# Kubernetes Deployment Workflow

Based on `410-infrastructure-k8s.md`.

1. **Containerization**
    - Ensure `Dockerfile` is optimized (Multi-stage build).
    - Build and Push image.

2. **Manifest Creation**
    - **Deployment**: Define Replicas, Selector, Template.
      - **Resources**: Set `requests` and `limits`.
      - **Probes**: Liveness/Readiness.
    - **Service**: Define Ports, Selector.
    - **Ingress/ConfigMap**: As needed.

3. **Validation**
    - Lint YAML.
    - `kubectl apply --dry-run=client -f manifest.yaml`.

4. **Documentation**
    - Update MkDocs if architectural changes occurred.
    - Document new Environment Variables.
