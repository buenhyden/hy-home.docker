# Terraform

This directory provides a containerized Terraform CLI runner for managing infrastructure as code. Intended for on-demand execution using `docker compose run`.

## Service

| Service     | Image                      | Role                   | Mode    |
| :---        | :---                       | :---                   | :---    |
| `terraform` | `hashicorp/terraform:1.14.4` | IaC CLI runner       | Job (no restart) |

## Networking

- Connected to `infra_net` for access to internal services (e.g., MinIO for remote state).
- No port exposure or Traefik routing (job mode only).

## Persistence

- **Workspace**: `./workspace` bind mount → `/workspace` inside container. All `.tf` files and state are stored here.
- **AWS Credentials**: `$HOME/.aws` → `/root/.aws:ro` (for S3/MinIO backend auth).
- **Azure Credentials**: `$HOME/.azure` → `/root/.azure:ro` (for Azure provider auth).

## Configuration

- **Working Dir**: `/workspace` inside container.
- **Backend**: Configured per-workspace (S3/MinIO compatible or local filesystem).
- **Provider**: Manages Docker, Kubernetes, or cloud resources depending on workspace.

## Usage

```bash
# Initialize workspace
docker compose run --rm terraform init

# Plan changes
docker compose run --rm terraform plan

# Apply changes
docker compose run --rm terraform apply

# Format files
docker compose run --rm terraform fmt

# Destroy resources
docker compose run --rm terraform destroy
```

## File Map

| Path                | Description                                       |
| ------------------- | ------------------------------------------------- |
| `docker-compose.yml`| Terraform CLI job service definition.             |
| `workspace/`        | Terraform configuration files (user-managed).     |
| `README.md`         | Usage notes and provider setup (this file).       |
