# The upstream release the source commit below is tagged as; the Compose tag
# names it (scripts/lib/supply_chain/local_image_tags.py).
ARG GATUS_VERSION=5.38.0

FROM golang:1.26.4-alpine3.22@sha256:727cfc3c40be55cd1bc9a4a059406b28a059857e3be752aa9d09531e12c20c56 AS builder

WORKDIR /src

RUN apk add --no-cache \
    ca-certificates \
    patch \
    wget

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

RUN wget -q \
      -O /tmp/gatus-source.tar.gz \
      https://github.com/TwiN/gatus/archive/d255d0cd4d69ce818574cfdb3a7e82407e6559d7.tar.gz \
    && echo "b0a5cd58784cf582410310269c8afe5695fbe33102aea8e7c9222a0ec9c3c692  /tmp/gatus-source.tar.gz" \
      | sha256sum -c - \
    && tar -xzf /tmp/gatus-source.tar.gz --strip-components=1 \
    && rm /tmp/gatus-source.tar.gz

COPY patches/oidc-hardening.patch /tmp/oidc-hardening.patch

RUN patch --batch --forward --fuzz=0 -p1 < /tmp/oidc-hardening.patch \
    && go mod tidy -diff \
    && go test ./api ./security

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /gatus .

FROM alpine:3.24

ARG GATUS_VERSION
LABEL org.opencontainers.image.version="${GATUS_VERSION}"

RUN apk add --no-cache \
    ca-certificates \
    wget

COPY --from=builder /gatus /usr/local/bin/gatus
COPY --chmod=0555 docker-entrypoint.sh /usr/local/bin/gatus-oidc-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/gatus-oidc-entrypoint.sh"]
CMD ["/usr/local/bin/gatus"]
