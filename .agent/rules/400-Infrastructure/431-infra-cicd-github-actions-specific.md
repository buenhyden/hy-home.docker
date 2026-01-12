---
trigger: always_on
glob: ".github/workflows/**/*.yml"
description: "GitHub Actions CI/CD: Standards for robust pipeline configuration."
---
# DevOps: GitHub Actions CI/CD Standards

## 1. Workflow Structure

- **Triggers**: Define precise triggers (`push` to main, `pull_request`). Use `workflow_dispatch` for manual runs.
- **Concurrency**: Use `concurrency` groups to cancel outdated runs on PRs.
- **Permissions**: Use least-privilege `permissions` block (e.g., `contents: read`).
- **Timeouts**: Always set `timeout-minutes` for jobs to prevent stuck runners.

## 2. Jobs & Steps

- **Naming**: Use descriptive names for Steps.
- **Caching**: Use `setup-node` or `setup-python` with built-in caching (`cache: 'npm'`).

## 3. Security & Validation

- **Secrets**: NEVER hardcode secrets. Use `${{ secrets.MY_KEY }}`. Pass secrets via `env` or inputs. NEVER log secrets.
- **Pinning**: Pin actions to full SHA1 hash (e.g., `actions/checkout@8f4b7...`) for security. Pin actions to SHA or specific tags (`@v4`) for security stability.
- **Linting**:
  - **actionlint**: Validate workflow syntax and logic.
  - **zizmor**: Audit for security vulnerabilities in workflows.
  - **check-jsonschema**: Validate against GitHub Workflow schema.

## 4. Docker & Containers

- **Buildx**: Use `docker/setup-buildx-action`.
- **Metadata**: Use `docker/metadata-action` for tagging.
- **Scanning**: Integrate container scanning (e.g., Trivy or Snyk) if available.

## 4. Terraform & IaC

- **Format**: Run `terraform fmt -check` in CI.
- **Plan**: Run `terraform plan` on PRs and post result to PR comment.
- **Apply**: Only run `terraform apply` on `main` branch (after approval if sensitive).

## 5. Security Scanning

- **CodeQL**: Enable for static analysis.
- **Audit**: Run `npm audit` or `pip check` in pipeline.
