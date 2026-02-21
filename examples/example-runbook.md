# Example: Runbook / Standard Operating Procedure

This is a concrete example of a runbook following the `templates/operations/runbook-template.md` structure.

---

## Runbook / Standard Operating Procedure

## 1. Service Overview & Ownership

- **Description**: This runbook describes the procedure for deploying a new version of the API service to the production Kubernetes cluster with zero downtime, as well as handling common alerts.
- **Owner Team**: Platform Engineering
- **Primary Contact**: `#platform-oncall`

## 2. Dependencies

- **Upstream Dependencies:**
  - Database (PostgreSQL) must be online and reachable.
  - Redis cache must be available.
- **Access Requirements:**
  - Kubernetes cluster admin access
  - Docker Hub write access (for image pushes)
  - GitHub repository write access

- **Tools:**
  - `kubectl` (v1.28+)
  - `docker` (v24+)
  - `helm` (v3.12+)

## 3. Dashboards, Alerts, & SLOs

- **Primary Dashboard:** [Grafana API Dashboard](https://grafana.example.com/api)
- **Log Aggregation:** [Datadog API Logs](https://app.datadoghq.com/logs/api)
- **SLOs/SLIs:**
  - 99.9% API Uptime (measured per month).
  - p95 Latency < 200ms.
- **Alert Routing:** `#api-alerts` Slack channel / PagerDuty API Service.

## 4. Alerts & Common Failures

### Scenario A: High Latency Alert

- **Symptoms**: Paged for `p95 Latency > 200ms` alert.
- **Investigation Steps**:
  1. Check Grafana API Dashboard.
  2. Verify if DB connections are maxed out via Datadog.
- **Remediation Action**:
  - [ ] Action 1: Look for specific long-running queries causing the delay.
  - [ ] Action 2: Scale up the deployment if CPU bound: `kubectl scale deployment api-deployment --replicas=5 -n production`

### Scenario B: Deployment Pipeline Execution

1. **Verify CI pipeline has passed**

   ```bash
   gh run list --limit 1 --json conclusion --jq '.[0].conclusion'
   # Expected output: "success"
   ```

2. **Pull the latest container image tag**

   ```bash
   export IMAGE_TAG=$(gh run list --limit 1 --json headBranch --jq '.[0].headBranch')
   echo "Deploying image tag: $IMAGE_TAG"
   ```

3. **Update Helm values with new image tag**

   ```bash
   helm upgrade api-release ./helm/api \
     --namespace production \
     --set image.tag=$IMAGE_TAG \
     --values ./helm/api/values-prod.yaml
   ```

4. **Verify rollout status**

   ```bash
   kubectl rollout status deployment/api-deployment -n production --timeout=300s
   # Expected output: "deployment "api-deployment" successfully rolled out"
   ```

## 5. Validation

- **Health Check:**

  ```bash
  curl -s https://api.example.com/health | jq '.status'
  # Expected output: "healthy"
  ```

- **Smoke Test:**

  ```bash
  curl -s https://api.example.com/api/v1/status | jq '.version'
  # Expected output: matches $IMAGE_TAG
  ```

## 5. Safe Rollback Procedure

If deployment fails or health checks return errors:

1. **Immediate rollback to previous version:**

   ```bash
   helm rollback api-release -n production
   ```

2. **Verify rollback:**

   ```bash
   kubectl rollout status deployment/api-deployment -n production --timeout=120s
   curl -s https://api.example.com/health | jq '.status'
   ```

3. **Notify team:**

   ```bash
   # Post to Slack incident channel
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"⚠️ API deployment rolled back to previous version"}' \
     $SLACK_WEBHOOK_URL
   ```

## 6. Data Safety Notes

- **Warning:** Migrations run automatically on start. If rolling back, verify that the previous API version is compatible with the newly migrated database schema. If not, refer to `runbooks/database-rollback-runbook.md` BEFORE scaling back up.

## 7. Escalation Path

- **Primary Contact:** Platform Team Slack: `#platform-oncall`
- **Secondary Contact:** PagerDuty: `platform-escalation@company.pagerduty.com`

## 8. Verification Steps (Post-Fix)

- [ ] Health Check (`curl -s https://api.example.com/health | jq '.status'`) returns `healthy`.
- [ ] Error rate on Grafana dashboard drops below 1%.
