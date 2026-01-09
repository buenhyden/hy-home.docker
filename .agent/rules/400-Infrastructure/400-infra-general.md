---
trigger: always_on
glob: "**/*"
description: "Infrastructure Core: GitOps, Security Triad, and Reliability standards."
---
# Infrastructure General Standards

## 1. GitOps & IaC

- **Immutable Infrastructure**: Never SSH into a live server to make changes. Update the code and re-provision.
- **Modular IaC**: Break Terraform/CloudFormation into small, reusable modules.
- **State Management**: Always use remote state with locking to prevent corruption in team environments.

## 2. The Security Triad (CIA)

- **Confidentiality**: Encrypt data at rest and in transit.
- **Integrity**: Use signing and checksums for artifacts.
- **Availability**: Implement Auto-scaling, Multi-AZ deployments, and Load Balancing.

### Example: Multi-AZ

**Good**
> Deploying application nodes across `us-east-1a`, `us-east-1b`, and `us-east-1c`.

**Bad**
> Running 3 instances all in `us-east-1a`. (Single point of failure for the entire AZ).

## 3. Cloud Native Observability

- **Synthetics**: Run periodic health-check pings against your public endpoints.
- **Logging**: Centralize logs (ELK, CloudWatch, Splunk). Use structured JSON.
- **Tracing**: Implement Distributed Tracing (OpenTelemetry) for microservice architectures.

## 4. Continuity

- **RTO/RPO**: Define and test your Recovery Time and Recovery Point Objectives.
- **Chaos Engineering**: Periodically inject failures (kill pods, latency) to verify system resilience.
