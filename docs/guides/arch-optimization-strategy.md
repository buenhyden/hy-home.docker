# Infra Architecture & Topologies Analysis

## 1. Architecture & Optimization Analysis

Based on the review of the current `docker-compose.yml` topology and the files in the `infra/` directory, the following architectural insights and optimization opportunities have been identified:

### 1.1 Infrastructure Network & Static IPs

- **Current State**: The `infra_net` bridge network configures subnet `172.19.0.0/16`. Containers (e.g., `traefik` at `172.19.0.13`, `mng-valkey` at `172.19.0.70`, `mng-pg` at `172.19.0.72`) are explicitly assigned static `ipv4_address` values.
- **Analysis**: While static IPs provide a sense of predictability, they introduce fragility in containerized environments. They can lead to IP conflicts, hinder scalability (e.g., running multiple instances or creating ephemeral test environments), and are generally considered a Docker anti-pattern.
- **Optimization Strategy**:
  - **Remove Static IPs**: Remove the `ipv4_address` field from all service configurations.
  - **Rely on Docker DNS**: Leverage Docker's native internal DNS. Services should discover and communicate with each other using their `container_name` or `aliases` (e.g., connecting to `mng-valkey:6379` instead of `172.19.0.70:6379`).

### 1.2 Redundant Initialization Containers

- **Current State**: In the `mng-db` stack (`infra/04-data/mng-db/docker-compose.yml`), a dedicated initialization container `mng-pg-init` is used to execute the `init_users_dbs.sql` script by explicitly waiting for `mng-pg` to be ready and then running `psql`.
- **Analysis**: The primary database container (`mng-pg`) already mounts `./init-scripts/init_users_dbs.sql` into `/docker-entrypoint-initdb.d/init_users_dbs.sql`. The official `postgres` Docker image automatically executes any `.sql` or `.sh` scripts found in `/docker-entrypoint-initdb.d/` precisely once during the initial database creation.
- **Optimization Strategy**:
  - **Remove `mng-pg-init`**: The `mng-pg-init` service is redundant. Relying on the official image's built-in initialization mechanism reduces resource overhead, simplifies the `docker-compose.yml`, and lowers the risk of race conditions during startup.

### 1.3 Best Practices Observed

- **Resource Limits**: The `deploy.resources.limits` and `reservations` are properly configured across services, adhering to stability and resource stewardship principles.
- **Security Contexts**: Excellent use of `read_only: true` and `security_opt: ["no-new-privileges:true"]` where applicable (e.g., in exporters and Traefik).
- **Restart Policies & Health Checks**: Well-defined health checks and `restart: unless-stopped` policies ensure robustness. Service dependencies use `condition: service_healthy`, which is the correct pattern for orchestrating startup sequences.
- **Secret Management**: Proper usage of Docker Secrets to avoid exposing sensitive variables in composing files is consistently applied.
