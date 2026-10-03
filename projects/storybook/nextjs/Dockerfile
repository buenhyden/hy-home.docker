# Build only the tracked Storybook workspace. The caller supplies its source commit.
ARG NODE_IMAGE=node:24.21.0-alpine3.24@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1
ARG STORYBOOK_SOURCE_REVISION=uncommitted
ARG NGINX_IMAGE=nginxinc/nginx-unprivileged:1.31.6-alpine3.24@sha256:26b0bf6fbf07297983cb341998d79c831508787de26627dd2a112321b9c3a4af
FROM ${NODE_IMAGE} AS build
WORKDIR /work
COPY package.json package-lock.json ./
COPY packages/ui/package.json packages/ui/package.json
RUN npm ci --ignore-scripts
COPY . .
ARG STORYBOOK_SOURCE_REVISION
ENV STORYBOOK_SOURCE_REVISION=${STORYBOOK_SOURCE_REVISION}
RUN npm run build-storybook

FROM ${NGINX_IMAGE}
ARG STORYBOOK_SOURCE_REVISION
LABEL org.opencontainers.image.revision=${STORYBOOK_SOURCE_REVISION}
COPY --from=build /work/storybook-static/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1
