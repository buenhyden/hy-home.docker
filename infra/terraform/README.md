# Terraform Infrastructure as Code

**Terraform** is an open-source infrastructure as code software tool that provides a consistent CLI workflow to manage hundreds of cloud services.

In the `hy-home.docker` environment, we run Terraform within a Docker container to ensure consistency across different development environments and to avoid polluting the host system.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.
- Access to `infra_net` network (created by the main infrastructure stack).

### Project Structure

```
/infra/terraform/
├── docker-compose.yml  # Defines the Terraform container
├── README.md           # This documentation
└── (your .tf files)    # Place your Terraform configuration files here
```

## Usage

Since Terraform is running inside a container, you use `docker compose run` to execute commands.

### 1. Initialization

Initialize the Terraform working directory. This downloads providers and modules.

```bash
docker compose run --rm terraform init
```

### 2. Planning

Generate an execution plan.

```bash
docker compose run --rm terraform plan
```

### 3. Applying

Apply the changes required to reach the desired state of the configuration.

```bash
docker compose run --rm terraform apply
```

### 4. Formatting

Rewrites config files to canonical format.

```bash
docker compose run --rm terraform fmt
```

## State Management

By default, the `terraform.tfstate` file is stored in the local directory (since we mount `./:/workspace`).
**For production-grade setups**, configure a remote backend (like S3, GCS, or Consul) in your `.tf` files to store the state securely and enable collaboration.

## Best Practices

- **Modules**: Use modules to organize configurations.
- **Variables**: Do not hardcode secrets. Use `terraform.tfvars` (ensure it's `.gitignore`d) or environment variables.
- **Version Control**: Commit your `.tf` and `.lock.hcl` files. **Do NOT** commit `.tfstate` or `.tfvars` containing secrets.
