---
trigger: always_on
glob: "**/*.tf"
description: "Terraform/IaC: Configuration, state management, modularity, and security best practices."
---
# Terraform Infrastructure Standards

## 1. Structure & Modularity

- **Standard Files**: `main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`.
- **Modules**: Encapsulate reusable logic in `modules/`. Use versioning for external modules.
- **Root Module**: Should primarily call child modules and set up backend/providers.

## 2. State Management

- **Remote Backend**: ALWAYS use a remote backend (S3, GCS, Azure Blob) with state locking (DynamoDB).
- **Isolation**: Use `terraform workspaces` or separate directories for environments (dev/prod).

## 3. Security

- **Secrets**: NEVER hardcode secrets. Use external secret managers (Vault, AWS Secrets Manager) or environment variables.
- **Encryption**: Enable encryption at rest for state files and managed resources.

## 4. Coding & Loops

- **ForEach**: Proper `for_each` with map keys over `count` (count index shifts destroy resources).
- **Versioning**: Pin module versions (`version = "5.0.0"`).
- **Validation**: Run `terraform validate` and `terraform fmt`.

## 5. Coding Style

- **Formatting**: Run `terraform fmt` before commit.
- **Validation**: Run `terraform validate`.
- **Naming**: Use `snake_case` for resource names.

### Example: Secure Provider Setup

#### Good

```hcl
provider "aws" {
  region = var.aws_region
  # Credentials via env vars (AWS_ACCESS_KEY_ID)
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

#### Bad

```hcl
provider "aws" {
  access_key = "AKIA..." # HARDCODED SECRET!
}
```
