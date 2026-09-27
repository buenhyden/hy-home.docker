# Reference Dockerfile for a containerized service.
# Demonstrates: multi-stage build, pinned base images, non-root runtime,
# minimal final layer, and an in-image HEALTHCHECK.

# ---- build stage: prepare static assets ----
FROM alpine:3.24@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6 AS build
WORKDIR /src
COPY site/ ./site/
# Asset build/transform steps belong here. This sample copies static content only.

# ---- runtime stage: unprivileged nginx (uid 101, listens on 8080) ----
FROM nginxinc/nginx-unprivileged:1.31.6-alpine3.24-slim@sha256:123fb7283ffb4788e260d4e980005a978995fefedcdbb04d268077a19b84576d AS runtime
COPY --chown=101:101 nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build --chown=101:101 /src/site/ /usr/share/nginx/html/
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["wget", "--quiet", "--tries=1", "--spider", "http://127.0.0.1:8080/"]
