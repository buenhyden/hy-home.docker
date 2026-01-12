---
trigger: always_on
glob: "docker-compose*.yml,Dockerfile"
description: "Docker: Multi-stage builds, Rootless security, and Caching."
---
# Docker Standards

## 1. Optimization

- **Base Image**: Use official, slim images (e.g., `python:3.13-slim-bookworm`, `node:23-alpine`).
- **Multi-Stage**: Strip build dependencies. Use build stages to reduce final image size.
- **Layering**: Copy Dependency definitions (`requirements.txt`, `package.json`) FIRST, install, THEN copy source code.

### Example: Caching

**Good**

```dockerfile
COPY package.json .
RUN npm install
COPY . .
```

**Bad**

```dockerfile
COPY . .
RUN npm install # Busts cache on every code change
```

## 2. Security (Rootless)

- **User**: Switch to non-root user.
- **Secrets**: Use BuildKit secrets, never `ARG` for credentials.

### Example: User

**Good**

```dockerfile
USER node
CMD ["npm", "start"]
```

**Bad**

```dockerfile
# Running as root (ID 0) by default
CMD ["npm", "start"]
```

## 3. Compose

- **Healthchecks**: Define explicitly in Compose or Dockerfile.
- **Limits**: Set `cpus` and `memory` constraints.

### Example: Limits

**Good**

```yaml
deploy:
  resources:
    limits:
      memory: 512M
```

**Bad**

```yaml
```yaml
# No limits: Memory leak kills host
```

## 4. Docker Compose

- **Services**: Define services clearly (`api`, `db`, `redis`).
- **Volumes**: Use named volumes for persistent data.
- **Networks**: Use custom networks to isolate service communication.
- **Env Vars**: Use `${VAR_NAME}` syntax and `.env` files. Don't hardcode secrets.

## 5. Language Specifics

### Python

- **Environment**: Set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`.
- **Caching**: Use BuildKit cache for pip.

  ```dockerfile
  RUN --mount=type=cache,target=/root/.cache/pip \
      pip install -r requirements.txt
  ```

- **User**: Create a non-root user explicitly.

  ```dockerfile
  RUN useradd -m appuser && chown -R appuser /app
  USER appuser
  ```
