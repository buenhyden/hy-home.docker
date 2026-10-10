ARG N8N_VERSION=2.42.6

FROM alpine:3.24.2@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6 AS font-builder
RUN apk add --no-cache \
  fontconfig=2.17.1-r1 \
  font-noto=2026.06.01-r0 \
  font-noto-cjk=0_git20220127-r1 \
  font-dejavu=2.37-r6 \
  font-liberation=2.1.5-r2 \
  font-liberation-sans-narrow=1.07.6-r2 \
  font-noto-emoji=2.051-r0 && \
  apk --no-network info -v > /font-builder-packages.txt && \
  fc-cache -f -v

FROM n8nio/n8n:${N8N_VERSION}@sha256:526daa38b68e923cc00c5280d18b4da5d489f115a73bdbf3b8e452b184197a9a
ARG N8N_VERSION=2.42.6

USER root

COPY --from=font-builder /usr/share/fonts /usr/share/fonts
COPY --from=font-builder /var/cache/fontconfig /var/cache/fontconfig
COPY --from=font-builder /etc/fonts /etc/fonts
COPY --from=font-builder /font-builder-packages.txt /usr/share/hy-home-font-builder-packages.txt

RUN mkdir -p /var/cache/fontconfig && \
  (if command -v fc-cache >/dev/null 2>&1; then fc-cache -f; fi || true)

USER node

ENV NODE_ENV=production
ENV GENERIC_TIMEZONE=Asia/Seoul

WORKDIR /home/node

RUN test "$(n8n --version)" = "${N8N_VERSION}"

RUN mkdir -p /home/node/.n8n/custom && \
  chown -R node:node /home/node/.n8n

COPY --chown=node:node ./custom /home/node/.n8n/custom
COPY --chown=node:node ./docker-entrypoint.dev.sh /home/node/docker-entrypoint.sh
RUN chmod 0755 /home/node/docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
