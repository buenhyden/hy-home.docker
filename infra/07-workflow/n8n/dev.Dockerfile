ARG N8N_VERSION=2.15.0

FROM alpine:3.21 AS font-builder
RUN apk add --no-cache \
  fontconfig \
  font-noto \
  font-noto-cjk \
  ttf-dejavu \
  ttf-liberation \
  font-noto-emoji && \
  fc-cache -f -v

FROM n8nio/n8n:${N8N_VERSION}

USER root

COPY --from=font-builder /usr/share/fonts /usr/share/fonts
COPY --from=font-builder /var/cache/fontconfig /var/cache/fontconfig
COPY --from=font-builder /etc/fonts /etc/fonts

RUN mkdir -p /var/cache/fontconfig && \
  (if command -v fc-cache >/dev/null 2>&1; then fc-cache -f; fi || true)

USER node

ENV NODE_ENV=production
ENV GENERIC_TIMEZONE=Asia/Seoul

WORKDIR /home/node

RUN mkdir -p /home/node/.n8n/custom && \
  chown -R node:node /home/node/.n8n

COPY --chown=node:node ./custom /home/node/.n8n/custom
COPY --chown=node:node ./docker-entrypoint.dev.sh /home/node/docker-entrypoint.sh
RUN chmod 0755 /home/node/docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
