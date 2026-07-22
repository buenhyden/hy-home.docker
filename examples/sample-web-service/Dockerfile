# Reference Dockerfile for a containerized service.
# Demonstrates: multi-stage build, pinned base images, non-root runtime,
# minimal final layer, and an in-image HEALTHCHECK.

# ---- build stage: prepare static assets ----
FROM alpine:3.21@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d AS build
WORKDIR /src
COPY site/ ./site/
# Asset build/transform steps belong here. This sample copies static content only.

# ---- runtime stage: unprivileged nginx (uid 101, listens on 8080) ----
FROM nginxinc/nginx-unprivileged:1.27.3-alpine@sha256:9e7238f579a54582263a960d1b0094b4a3ecce641342eda3f8e2ff82b1703d2b AS runtime
COPY --chown=101:101 nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build --chown=101:101 /src/site/ /usr/share/nginx/html/
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1:8080/ || exit 1
