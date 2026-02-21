---
trigger: model_decision
glob: ["**/azure/**", "**/gcp/**"]
description: "Cloud Provider Standards (Azure/GCP): Enforces provider-specific security, naming, and resource management policies."
---

# Cloud Provider Standards (Azure & GCP)

- **Role**: Multi-Cloud Infrastructure Engineer
- **Purpose**: Define standards for building and managing resources within Microsoft Azure and Google Cloud Platform (GCP) following platform-specific best practices.
- **Activates When**: Provisioning Azure/GCP resources or configuring provider-specific security and networking assets.

**Trigger**: model_decision — Apply during the design and implementation of provider-centric cloud features.

## 1. Standards

### Principles

- **[REQ-PRO-01] Native Security Alignment**
  - Projects MUST utilize provider-native security tools (Azure Defender, Google Security Command Center) for threat detection and compliance.
- **[REQ-PRO-02] Region-Affinity Optimization**
  - Resources MUST be co-located within the same region or zone where possible to minimize cross-regional data costs and latency.
- **[REQ-PRO-03] Identity Federation**
  - Preference MUST be given to managed identities (Azure Managed Identity) or Service Account impersonation (GCP) over long-lived access keys.

### Provider Baseline

| Platform | Requirement ID | Authority / Standard |
| --- | --- | --- |
| Azure | [REQ-PRO-04] | Azure Resource Manager (ARM) / Bicep |
| GCP | [REQ-PRO-05] | Google Cloud Deployment Manager / Terraform |
| Identity | [REQ-PRO-06] | Entra ID (Azure) / Cloud IAM (GCP) |
| Networking| [REQ-PRO-07] | VNet (Azure) / Shared VPC (GCP) |

### Must

- **[REQ-PRO-08] Standardized Resource Naming**
  - Resource names MUST follow the provider-specific convention (e.g., `rg-app-prod-001` for Azure, `prj-app-prod-001` for GCP).
- **[REQ-PRO-09] Mandatory Key Rotation**
  - All manually managed credentials and service account keys MUST be rotated every 90 days.
- **[REQ-PRO-10] Encryption-by-Default**
  - Utilized managed disks and storage buckets MUST have platform-managed or customer-managed encryption enabled.

### Must Not

- **[BAN-PRO-01] Over-Provisioned Tiers**
  - Do NOT select "Premium" or "High-Performance" SKUs for development/testing environments unless strictly required for specific testing.
- **[BAN-PRO-02] Shared Resource Groups (Non-Atomic)**
  - Avoid sharing Resource Groups or Projects between unrelated applications; maintain atomic lifecycle boundaries.

### Failure Handling

- **Stop Condition**: Stop feature deployment if a resource plan identifies a lack of a "Delete Lock" on production-critical stateful resources (e.g., Azure SQL DB).

## 2. Procedures

- **[PROC-PRO-01] Provider Compliance Scan**
  - Weekly, run the provider's built-in "Security Scorecard" and resolve all "High" or "Critical" recommendations.
- **[PROC-PRO-02] Billing Audit**
  - Review monthly billing reports to identify unused "Zombie" resources or inefficient SKU selections.

## 3. Examples

### compliant Azure Bicep (Good)

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: 'stappprod001'
  location: resourceGroup().location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}
```

## 4. Validation Criteria

- **[VAL-PRO-01] Naming Consistency**
  - [ ] Automated audit confirms that > 95% of resources align with the specified naming convention.
- **[VAL-PRO-02] Security Baseline Pass**
  - [ ] CSPM tools (Cloud Security Posture Management) confirm zero misconfigurations in public visibility.
- **[VAL-PRO-03] Key Lifecycle Verification**
  - [ ] audit logs confirm that 100% of rotated keys were replaced within the mandated window.
