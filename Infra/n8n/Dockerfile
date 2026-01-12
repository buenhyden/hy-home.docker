ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-alpine

ARG N8N_VERSION=2.3.0

# 1. Update everything and install needed dependencies
RUN apk add --update graphicsmagick tzdata git tini su-exec

# 2. Set a custom user to not have n8n run as root
USER root

# 3. Install n8n and the packages it needs to build it correctly.
RUN apk --update add --virtual build-dependencies python3 build-base ca-certificates && \
    npm config set python "$(which python3)" && \
    npm_config_user=root npm install -g full-icu n8n@${N8N_VERSION} && \
    apk del build-dependencies \
    && rm -rf /root /tmp/* /var/cache/apk/* && mkdir /root;

# 4. Install fonts
RUN apk --no-cache add --virtual fonts msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f && \
    apk del fonts && \
    find  /usr/share/fonts/truetype/msttcorefonts/ -type l -exec unlink {} \; \
    && rm -rf /root /tmp/* /var/cache/apk/* && mkdir /root

ENV NODE_ICU_DATA /usr/local/lib/node_modules/full-icu

WORKDIR /data

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]

EXPOSE 5678/tcp