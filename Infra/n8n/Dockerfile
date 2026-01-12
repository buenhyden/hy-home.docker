# syntax=docker/dockerfile:1
# -----------------------------------------------------------
# Custom n8n Dockerfile - Multi-stage Build
# -----------------------------------------------------------
# The official n8n image is distroless (no package manager).
# This multi-stage build installs fonts in Alpine stage,
# then copies them to the final n8n image.
# -----------------------------------------------------------

ARG N8N_VERSION=2.3.0

# ===========================================
# Stage 1: Font Builder (Alpine)
# ===========================================
FROM alpine:3.21 AS font-builder

# Install fonts
RUN apk add --no-cache \
    fontconfig \
    font-noto \
    font-noto-cjk \
    ttf-dejavu \
    ttf-liberation \
    font-noto-emoji

# Build font cache
RUN fc-cache -f -v

# ===========================================
# Stage 2: Final n8n Image
# ===========================================
FROM n8nio/n8n:${N8N_VERSION}

# Switch to root to copy files
USER root

# Copy fonts from builder stage
COPY --from=font-builder /usr/share/fonts /usr/share/fonts
COPY --from=font-builder /var/cache/fontconfig /var/cache/fontconfig
COPY --from=font-builder /etc/fonts /etc/fonts

# Create fontconfig cache directory and refresh
RUN mkdir -p /var/cache/fontconfig && \
    if command -v fc-cache >/dev/null 2>&1; then fc-cache -f; fi || true

# Switch back to node user for security
USER node

# Environment defaults
ENV NODE_ENV=production
ENV GENERIC_TIMEZONE=Asia/Seoul

WORKDIR /home/node

# The official n8n image already has proper ENTRYPOINT configured