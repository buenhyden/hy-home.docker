---
trigger: model_decision
glob: ["**/*"]
description: "Cloud Governance Standards: Enforces FinOps (Cost Optimization), Security-first IAM, and Compliance-as-Code."
---

# Cloud Governance Standards

- **Role**: Cloud Governance Architect
- **Purpose**: Define standards for managing multi-cloud infrastructure focusing on cost optimization (FinOps), security architecture, and regulatory compliance.
- **Activates When**: Provisioning cloud resources, configuring IAM permissions, or performing cloud cost audits.

**Trigger**: model_decision — Apply during all cloud infrastructure management and design phases.

## 1. Standards

### Principles

- **[REQ-CLD-01] Financial Accountability (FinOps)**
  - Every cloud resource MUST be meticulously tagged with ownership, environment, and cost-center metadata to ensure 100% cost transparency.
- **[REQ-CLD-02] Least-Privilege Identity (IAM)**
  - Identities MUST follow the principle of least-privilege. Deny-by-default MUST be the baseline for all IAM policy configurations.
- **[REQ-CLD-03] Policy-as-Code Compliance**
  - Infrastructure compliance MUST be enforced through automated policies (e.g., AWS Config, Azure Policy) to prevent configuration drift.

### Governance Matrix

| Domain | Requirement ID | Critical Control |
| --- | --- | --- |
| Cost | [REQ-CLD-04] | Spot Instances for fault-tolerant tasks |
| Identity | [REQ-CLD-05] | MFA enforced for all IAM principals |
| Network | [REQ-CLD-06] | Zero-Trust architecture with TLS 1.2+ |
| Persistence| [REQ-CLD-07] | Automated lifecycle / Intelligent Tiering |

### Must

- **[REQ-CLD-08] Mandatory Resource Tagging**
  - Resources without mandatory tags (`Owner`, `Environment`) MUST be automatically identified and flagged for remediation/deletion.
- **[REQ-CLD-09] Short-Lived Identity Tokens**
  - Avoid using long-lived IAM access keys; utilize temporary, token-based authentication (OIDC/SSO) for all automated services.
- **[REQ-CLD-10] Encrypted-at-Rest Default**
  - All storage volumes (EBS, S3, Azure Disks) MUST utilize KMS/KeyVault encryption by default at the platform level.

### Must Not

- **[BAN-CLD-01] Publicly Accessible Storage/DB**
  - Cloud storage buckets and databases MUST NOT be accessible from the public internet without explicit, documented architectural approval.
- **[BAN-CLD-02] Shared Root Credentials**
  - The use of the platform "Root" or "Global Admin" account for daily operational tasks is STRICTLY PROHIBITED.

### Failure Handling

- **Stop Condition**: Stop resource provisioning if the Terraform/Cloud-init plan fails the security policy scan for unencrypted storage.

## 2. Procedures

- **[PROC-CLD-01] Cost Anomaly Audit**
  - IF cloud spending exceeds the monthly budget by > 10% THEN MUST conduct a formal FinOps review within 48 hours.
- **[PROC-CLD-02] Identity Perimeter Review**
  - Perform a quarterly audit of all IAM principals and roles to prune unused permissions and credentials.

## 3. Examples

### compliant S3 Policy (Good)

```yaml
Resources:
  SecureBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
```

## 4. Validation Criteria

- **[VAL-CLD-01] Tagging Coverage**
  - [ ] Cloud cost explorer confirms that > 98% of resources possess valid mandatory tags.
- **[VAL-CLD-02] Security Scorecard**
  - [ ] Platform-native security audit (e.g., Security Hub) confirms > 90% compliance with industry benchmarks (CIS/NIST).
- **[VAL-CLD-03] MFA Enforcement**
  - [ ] Audit confirms that 100% of human users utilize MFA for console and CLI access.
