---
description: Workflow for setting up Docker environments
---

1. **Requirement Analysis**

    Identify necessary services and base images.

    - **Base**: Alpine/Slim tags preferred (e.g., `node:23-alpine`)
    - **Services**: App, DB (Postgres/Redis), Queue

2. **Create Dockerfile**

    Write multi-stage Dockerfile for optimization.

    ```dockerfile
    # Build Stage
    FROM node:23-alpine AS builder
    WORKDIR /app
    COPY package*.json ./
    RUN npm ci
    COPY . .
    RUN npm run build

    # Runtime Stage
    FROM node:23-alpine AS runner
    WORKDIR /app
    COPY --from=builder /app/dist ./dist
    COPY --from=builder /app/node_modules ./node_modules
    CMD ["node", "dist/main.js"]
    ```

3. **Setup Docker Compose**

    Define services in `docker-compose.yml`.

    ```yaml
    services:
      app:
        build: .
        ports:
          - "3000:3000"
        environment:
          - NODE_ENV=development
        depends_on:
          db:
            condition: service_healthy
      
      db:
        image: postgres:15-alpine
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U postgres"]
          interval: 5s
          timeout: 5s
          retries: 5
    ```

4. **Security Scan**

    Run Trivy to check for vulnerabilities.

    // turbo

    ```bash
    # Verify trivy installation first or run via docker
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image my-app:latest
    ```

5. **Build and Verify**

    Build containers and check logs.

    ```bash
    docker-compose up --build -d
    ```

    // turbo

    ```bash
    docker-compose ps
    ```

6. **Cleanup (Optional)**

    Remove unused artifacts.

    ```bash
    docker system prune -f
    ```
