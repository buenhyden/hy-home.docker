---
trigger: always_on
glob: "**/*.tf"
description: "Terraform/IaC: Configuration, state management, modularity, and security best practices."
---
# Terraform Infrastructure Standards

## 1. Project Structure & Organization

- **Standard Files**: `main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`.
- **Modules**: Encapsulate reusable logic in `modules/`. Use versioning for external modules.
- **Root Module**: Should primarily call child modules and set up backend/providers.
- **Environment Separation**: Use separate directories (`environments/dev`, `environments/prod`) or workspaces.

## 2. State Management

- **Remote Backend**: ALWAYS use a remote backend (S3, GCS, Azure Blob) with state locking (DynamoDB).
- **Encryption**: Enable server-side encryption for the state bucket.
- **Isolation**: Never share state files between environments.

## 3. Variable Management & Validation

- **Type Constraints**: Always define `type` for variables.
- **Validation**: Use `validation` blocks to enforce constraints.
- **Descriptions**: Provide meaningful descriptions.

### Example: Validation

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

## 4. Security

- **Secrets**: NEVER hardcode secrets. Use external secret managers (Vault, AWS Secrets Manager) or environment variables.
- **Encryption**: Enable encryption at rest for state files and managed resources (e.g., EBS, RDS, S3).
- **Least Privilege**: IAM roles should be scoped strictly to required permissions.

## 5. Coding Best Practices

- **ForEach over Count**: Use `for_each` with maps instead of `count` for resources to avoid index-shifting issues during destruction.
- **Tags**: Use a consistent tagging strategy (e.g., `merge(var.tags, local.common_tags)`).
- **Naming**: Use `snake_case` for resource names.
- **Formatting**: Run `terraform fmt` before commit.
- **Linting**: Use `tflint` and `checkov`.

## 6. Testing

- **Integration Tests**: Use `Terratest` (Go) for infrastructure testing.
- **Plan Review**: Always review `terraform plan` output before applying.

### Example: Provider & Backend

```hcl
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project   = "my-project"
      ManagedBy = "terraform"
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```
