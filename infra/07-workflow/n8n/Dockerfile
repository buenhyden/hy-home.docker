# -----------------------------------------------------------

ARG N8N_VERSION=2.3.0
# Stage 1: Font Builder (Alpine)
FROM alpine:3.21 AS font-builder

RUN apk add --no-cache \
    fontconfig \
    font-noto \
    font-noto-cjk \
    ttf-dejavu \
    ttf-liberation \
    font-noto-emoji && \
    fc-cache -f -v


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

# 1. 시스템 도구 및 Python 설치 (Execute Command 노드용)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    make \
    g++ \
    build-base && \
    npm install -g n8n-cli


# Create fontconfig cache directory and refresh
# Create fontconfig cache directory and refresh
# hadolint ignore=SC2015
RUN mkdir -p /var/cache/fontconfig && \
    (if command -v fc-cache >/dev/null 2>&1; then fc-cache -f; fi || true)

# Switch back to node user for security
USER node

# Environment defaults
ENV NODE_ENV=production
ENV GENERIC_TIMEZONE=Asia/Seoul

WORKDIR /home/node

# Create custom node directory and ensure permissions
RUN mkdir -p /home/node/.n8n/custom && \
    chown -R node:node /home/node/.n8n

# Copy custom nodes (if any) from local context
COPY --chown=node:node ./custom /home/node/.n8n/custom


# The official n8n image already has proper ENTRYPOINT configured
