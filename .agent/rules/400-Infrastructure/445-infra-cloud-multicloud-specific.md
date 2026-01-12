---
trigger: always_on
glob: "**/*.{tf,yml,yaml,json}"
description: "Cloud (Azure/GCP): Well-Architected Framework and Resource Management."
---
# Multicloud Standards (Azure & GCP)

## 1. General Principles

- **IaC Mandatory**: Use Terraform or Bicep for all resources.
- **Idempotency**: All services and functions must be idempotent.
- **Secrets**: Never hardcode keys; use Key Vault (Azure) or Secret Manager (GCP).

## 2. Microsoft Azure

- **Well-Architected**: Follow CAF (Cloud Adoption Framework).
- **Identity**: Use Managed Identities for secure resource access.
- **Organization**: Modularize IaC into logical components.

## 3. Google Cloud Platform (GCP)

- **Least Privilege**: Apply the principle to Service Accounts. Use Workload Identity.
- **Serverless**: Minimize cold start latency by reducing dependencies in global scope.
- **Firestore**: Avoid sequential document IDs (prevents hotspotting). Use UUIDs or auto-IDs.
- **Cleanup**: Delete temporary files in `/tmp` for Cloud Functions/Run.

## 4. Operational Excellence

- **Logging**: Centralized logging via Azure Monitor or Cloud Logging.
- **Monitoring**: Set up alerts for error rates and latency.
- **Staging**: Always deploy via staged environments (Canary/Blue-Green).
