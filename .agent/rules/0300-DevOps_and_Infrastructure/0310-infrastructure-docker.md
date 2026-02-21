---
trigger: model_decision
glob: ["**/Dockerfile*", "**/docker-compose*.{yml,yaml}", "**/.dockerignore"]
description: "Docker Standards: Security, Optimization, and Multi-stage builds."
---

# 0310-Infrastructure-Docker

- **Role**: DevOps Engineer
- **Purpose**: Ensure secure, optimized, and portable container builds.
- **Activates When**: Writing or editing Dockerfiles or Compose files.

## 1. Standards

### 1.1 Principles

- **[REQ-DOC-GEN-01] Immutability**: Containers MUST NOT change after build.
- **[REQ-DOC-GEN-02] Ephemerality**: Containers MUST be disposable.
- **[REQ-DOC-GEN-03] Minimal**: Images MUST use minimal base images (alpine/distroless).

### 1.2 Scope

- **In-Scope**: Dockerfile, .dockerignore, docker-compose.yml.
- **Out-of-Scope**: Kubernetes manifests (see 0325).

### 1.3 Must / Must Not

- **[REQ-DOC-SEC-01] Non-Root**: Containers MUST run as a non-root user.
- **[REQ-DOC-OPT-01] Multi-Stage**: Builds MUST use multi-stage strategy to minimize size.
- **[BAN-DOC-SEC-01] No Secrets**: Secrets MUST NOT be baked into the image.
- **[BAN-DOC-TAG-01] No Latest**: Base images MUST be pinned to specific versions (not `:latest`).

## 2. Procedures

### 2.1 Optimization Strategy

1. **Base**: `FROM node:18-alpine AS builder`.
2. **Deps**: `COPY package*.json ./`, `RUN npm ci`.
3. **Source**: `COPY . .`, `RUN npm build`.
4. **Final**: `FROM node:18-alpine`. Copy only `dist/`.

### 2.2 Security Hardening

1. **User**: `RUN adduser -D appuser && USER appuser`.
2. **Ignore**: Add `.dockerignore` to exclude `.git`, `node_modules`, `.env`.
3. **Scan**: Run `trivy image` in CI.

## 3. Examples

### 3.1 Secure Node.js Dockerfile

```dockerfile
# Build Stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime Stage
FROM node:18-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production
USER appuser
CMD ["node", "dist/main.js"]
```

## 4. Validation Criteria

- [ ] **[VAL-DOC-SEC-01]** User is switched to non-root.
- [ ] **[VAL-DOC-OPT-01]** Multi-stage build is used.
- [ ] **[VAL-DOC-NET-01]** Healthcheck is defined.

## 5. References

- Reference: [Hadolint](https://github.com/hadolint/hadolint)
- Related: [0325-infrastructure-kubernetes.md](./0325-infrastructure-kubernetes.md)
