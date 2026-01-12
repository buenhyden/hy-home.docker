---
description: Workflow for provisioning infrastructure with Terraform
---

# Terraform Infrastructure Workflow

Based on `420-infra-terraform-specific.md`.

1. **Setup**
    - Configure backend state (S3, GCS, Terraform Cloud) with locking (DynamoDB).
    - Organize structure: `modules/`, `environments/` (dev, prod).

2. **Module Development**
    - Create reusable modules.
    - Define `variables.tf` (inputs) and `outputs.tf` (exports).
    - enforce version check (`required_version`, `required_providers`).

3. **Planning**
    - `terraform init`
    - `terraform fmt -recursive` (Formatting)
    - `terraform validate` (Syntax check)
    - `terraform plan -out=tfplan` (Review changes)

4. **Execution**
    - `terraform apply tfplan`
    - Monitor for errors.

5. **Security & Compliance**
    - Check for sensitive data in output.
    - Use `checkov` or `tfsec` to scan for misconfigurations.
    - Verify resources are tagged properly.
