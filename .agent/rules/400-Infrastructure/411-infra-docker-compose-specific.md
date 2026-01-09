---
trigger: always_on
glob: "docker-compose*.yml,docker-compose*.yaml,compose*.yml,compose*.yaml"
description: "Docker Compose: Service Definition, Networking, Volumes, and Best Practices."
---
# Docker Compose Standards

## 1. Service Definition

- **Version**: Use Compose Specification (no `version` key) for modern Compose.
- **Image vs Build**: Prefer `image` for production, `build` for development.
- **Naming**: Use descriptive service names (`api`, `db`, `redis`).

### Example: Services

**Good**

```yaml
services:
  api:
    image: myapp/api:${TAG:-latest}
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
```

**Bad**

```yaml
version: "3.8"  # Deprecated version key
services:
  app1:
    build: .
    ports:
      - "8080"  # Random host port, hard to access
```

## 2. Health Checks

- **Always Define**: Add healthcheck to services with dependencies.
- **depends_on.condition**: Use `service_healthy` for startup order.

### Example: Healthcheck

**Good**

```yaml
services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## 3. Networking

- **Named Networks**: Create explicit networks for isolation.
- **Internal**: Use `internal: true` for backend-only networks.

## 4. Environment & Secrets

- **env_file**: Use `.env` files for configuration.
- **Secrets**: Use Docker secrets for sensitive data (not env vars).

### Example: Env

**Good**

```yaml
services:
  api:
    env_file:
      - .env
    environment:
      - NODE_ENV=production
```

**Bad**

```yaml
services:
  api:
    environment:
      - DB_PASSWORD=my_secret_password  # Hardcoded secret!
```
