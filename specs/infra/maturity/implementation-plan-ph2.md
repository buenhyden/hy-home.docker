# Implementation Plan: Phase 2 Automation & Scaling

## Proposed Changes

### 1. Initialization Automation

- [ ] Implement `init-sidecar` for OpenSearch index templates.
- [ ] Implement `init-sidecar` for Kafka topic creation.

### 2. Monitoring Standardization

- [ ] Convert manual Grafana dashboards in `infra/` to provisioned files in `grafana/dashboards/`.
- [ ] Update `alloy` configuration to aggregate logs from the `project_net` external network.

### 3. Safety & Preflight

- [ ] Update `scripts/preflight-compose.sh` to check for `project_net` existence if non-external.
- [ ] Standardize `mem_reservation` across the `04-data` tier.

---

## Verification Plan

- **Verification-1**: Run `preflight-compose.sh` and ensure it fails gracefully if `project_net` is missing.
- **Verification-2**: Delete a MinIO bucket and ensure the `init` sidecar recreates it on next `up`.
