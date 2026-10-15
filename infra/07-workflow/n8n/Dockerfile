ARG N8N_VERSION=2.43.6

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

# Latest stable Current builder; exact-image compatibility is separately verified.
FROM node:26.11.1-alpine3.24@sha256:143494b1da2945f061539253adc65e4f1569ddf07da2d384c022c791a9d90a4a AS opsflow-builder
WORKDIR /build/opsflow
COPY ./workloads/manifest-outbox-notifier/nodes/OpsflowSmtp/package.json ./workloads/manifest-outbox-notifier/nodes/OpsflowSmtp/package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund --bin-links=false
COPY ./workloads/manifest-outbox-notifier/nodes/OpsflowSmtp/*.ts ./workloads/manifest-outbox-notifier/nodes/OpsflowSmtp/tsconfig.json ./
RUN node node_modules/typescript/bin/tsc -p tsconfig.json && \
  npm prune --omit=dev --ignore-scripts --no-audit --no-fund --bin-links=false && \
  mkdir -p /artifact/opsflow && \
  cp package.json /artifact/opsflow/ && \
  cp -R dist node_modules /artifact/opsflow/ && \
  chmod -R a+rX,go-w /artifact/opsflow
WORKDIR /artifact/opsflow
RUN find package.json dist node_modules -type f -exec sha256sum '{}' ';' > /tmp/opsflow-hashes && \
  sort -k2 /tmp/opsflow-hashes > SHA256SUMS

FROM n8nio/n8n:${N8N_VERSION}@sha256:dd580fe1ab6e99e85bc66f2acf8bc8c5e9409fbe61b2e2803c5024403ef52833
ARG N8N_VERSION=2.43.6

USER 0

COPY --from=opsflow-builder /artifact/opsflow /opt/hyhome/n8n-custom/opsflow

COPY --from=font-builder /usr/share/fonts /usr/share/fonts
COPY --from=font-builder /var/cache/fontconfig /var/cache/fontconfig
COPY --from=font-builder /etc/fonts /etc/fonts
COPY --from=font-builder /font-builder-packages.txt /usr/share/hy-home-font-builder-packages.txt

RUN mkdir -p /var/cache/fontconfig && \
  (if command -v fc-cache >/dev/null 2>&1; then fc-cache -f; fi || true)

RUN test "$(id -u node)" = "1000" && \
  test "$(id -g node)" = "1000"

USER 1000

ENV NODE_ENV=production
ENV GENERIC_TIMEZONE=Asia/Seoul

WORKDIR /home/node

RUN test "$(n8n --version)" = "${N8N_VERSION}"

RUN mkdir -p /home/node/.n8n/custom && \
  chown -R node:node /home/node/.n8n

COPY --chown=node:node ./custom /home/node/.n8n/custom
COPY --chown=node:node ./docker-entrypoint.sh /home/node/docker-entrypoint.sh
RUN chmod 0755 /home/node/docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
