# Reference Dockerfile for a containerized service.
# Demonstrates: multi-stage build, pinned base images, non-root runtime,
# minimal final layer, and an in-image HEALTHCHECK.

# ---- build stage: prepare static assets ----
FROM alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf AS build
WORKDIR /src
COPY site/ ./site/
# Asset build/transform steps belong here. This sample copies static content only.

# ---- runtime stage: unprivileged nginx (uid 101, listens on 8080) ----
FROM nginxinc/nginx-unprivileged:1.31.7-alpine3.24-slim@sha256:a8cb0f33d51fa107c96fd2bd3a71aaf564ec131e9d2bdf8700944f0ed8b170d7 AS runtime
COPY --chown=101:101 nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build --chown=101:101 /src/site/ /usr/share/nginx/html/
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["wget", "--quiet", "--tries=1", "--spider", "http://127.0.0.1:8080/"]
