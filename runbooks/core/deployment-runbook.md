# Deployment Runbook

## 1. Document Purpose

Deterministic procedure for deploying a service change to a target environment.

## 2. Prerequisites

- Access Requirements: Deployment permissions for target environment
- Tools: GitHub Actions access, deployment CLI/tooling used by project
- Inputs: Approved PR, passing CI, rollback target version

## 3. Execution Steps

1. Verify readiness gates.

   ```bash
   # Confirm all checks passed in CI before deployment.
   ```

2. Start deployment through approved pipeline.
   - For services subject to `.agent/rules/0341-progressive-delivery.md`, explicitly trigger the Canary or Blue/Green configuration rather than a "Big Bang" release.

   ```bash
   # Trigger deployment workflow/release command for target environment.
   ```

3. Monitor rollout and verify progressive delivery health checks.

   ```bash
   # Inspect deployment status and service health endpoints.
   ```

## 4. Validation

- New version is running in target environment.
- Health checks pass.
- Error rate and latency remain within expected thresholds.

## 5. Rollback / Reversal Procedure

1. Identify last known stable version.
2. Trigger rollback to stable version.
   - For Progressive Delivery, trigger the automated rollback/abort signal to safely shift traffic back.
3. Re-validate health and metrics.

## 6. Escalation Contacts

- Primary Contact: DevOps / On-call engineer
- Secondary Contact: Service owner team
