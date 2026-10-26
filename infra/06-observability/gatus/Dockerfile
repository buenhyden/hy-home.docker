FROM golang:1.26.4-alpine3.22 AS builder

WORKDIR /src

RUN apk add --no-cache \
    ca-certificates \
    patch \
    wget

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

RUN wget -q \
      -O /tmp/gatus-source.tar.gz \
      https://github.com/TwiN/gatus/archive/ae605f291928ed9b3bdbe60ae5528cc57631433b.tar.gz \
    && echo "79145709c1f5328fa01ff472d6c1d083cc8eb1bba90ea2dc6def628e88e3c406  /tmp/gatus-source.tar.gz" \
      | sha256sum -c - \
    && tar -xzf /tmp/gatus-source.tar.gz --strip-components=1 \
    && rm /tmp/gatus-source.tar.gz

COPY patches/oidc-hardening.patch /tmp/oidc-hardening.patch

RUN patch --batch --forward --fuzz=0 -p1 < /tmp/oidc-hardening.patch \
    && go mod tidy -diff \
    && go test ./api ./security

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /gatus .

FROM alpine:3.24

RUN apk add --no-cache \
    ca-certificates \
    wget

COPY --from=builder /gatus /usr/local/bin/gatus
COPY --chmod=0555 docker-entrypoint.sh /usr/local/bin/gatus-oidc-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/gatus-oidc-entrypoint.sh"]
CMD ["/usr/local/bin/gatus"]
