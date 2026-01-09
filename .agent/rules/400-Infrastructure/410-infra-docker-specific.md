---
trigger: always_on
glob: "docker-compose*.yml,Dockerfile"
description: "Docker: Multi-stage builds, Rootless security, and Caching."
---
# Docker Standards

## 1. Optimization

- **Multi-Stage**: Strip build dependencies.
- **Layering**: COPY `package.json` before source code.

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
# No limits: Memory leak kills host
```
