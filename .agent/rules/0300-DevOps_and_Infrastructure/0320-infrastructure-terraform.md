---
trigger: model_decision
glob: ["**/*.tf", "**/*.tfvars"]
description: "Terraform Standards: State management, Module structure, and Security."
---

# 0320-Infrastructure-Terraform

- **Role**: Cloud Architect
- **Purpose**: Standardize Infrastructure as Code (IaC) using Terraform.
- **Activates When**: Editing `.tf` files.

## 1. Standards

### 1.1 Principles

- **[REQ-TRF-GEN-01] Remote State**: State MUST be stored remotely (S3/GCS) with locking (DynamoDB).
- **[REQ-TRF-GEN-02] Modularity**: Resources MUST be grouped into reusable modules.
- **[REQ-TRF-GEN-03] Formatting**: Code MUST be formatted with `terraform fmt`.

### 1.2 Scope

- **In-Scope**: Terraform configurations, variables, outputs.
- **Out-of-Scope**: Cloud-specific resource details (see 04xx rules).

### 1.3 Must / Must Not

- **[BAN-TRF-SEC-01] No Plaintext Secrets**: Secrets MUST NOT be in `variables.tf` defaults. Use `ENV` vars or Secret Manager.
- **[REQ-TRF-VER-01] Pin Versions**: Provider and Module versions MUST be pinned.
- **[REQ-TRF-Tag-01] Tagging**: All resources MUST have standard tags (Env, Service, Owner).

## 2. Procedures

### 2.1 Directory Structure

```text
modules/
  networking/
  database/
environments/
  dev/
    main.tf
    variables.tf
  prod/
```

### 2.2 Workflow

1. **Init**: `terraform init`.
2. **Plan**: `terraform plan -out=tfplan`. Review changes.
3. **Apply**: `terraform apply tfplan`.

## 3. Examples

### 3.1 Provider Configuration

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/app.tfstate"
    region = "us-east-1"
  }
}
```

## 4. Validation Criteria

- [ ] **[VAL-TRF-FMT-01]** `terraform fmt --check` passes.
- [ ] **[VAL-TRF-SEC-01]** No secrets in `.tf` files.
- [ ] **[VAL-TRF-LCK-01]** State locking is enabled.

## 5. References

- None.
