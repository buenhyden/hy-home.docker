FROM golang:1.26.3-alpine3.22 AS builder

WORKDIR /src

RUN apk add --no-cache \
    ca-certificates \
    patch \
    wget

RUN wget -q \
      -O /tmp/gatus-source.tar.gz \
      https://github.com/TwiN/gatus/archive/ed1107b41a30e22047eecfb6dbc3be5e39829d5a.tar.gz \
    && echo "5638de42703fc6a936b9820920c3e07d1b1e017f1aabea94808155ed9953433a  /tmp/gatus-source.tar.gz" \
      | sha256sum -c - \
    && tar -xzf /tmp/gatus-source.tar.gz --strip-components=1 \
    && rm /tmp/gatus-source.tar.gz

COPY patches/oidc-hardening.patch /tmp/oidc-hardening.patch

RUN patch --batch --forward --fuzz=0 -p1 < /tmp/oidc-hardening.patch \
    && go mod tidy -diff \
    && go test ./api ./security

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /gatus .

FROM alpine:3.22

RUN apk add --no-cache \
    ca-certificates \
    wget

COPY --from=builder /gatus /usr/local/bin/gatus
COPY --chmod=0555 docker-entrypoint.sh /usr/local/bin/gatus-oidc-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/gatus-oidc-entrypoint.sh"]
CMD ["/usr/local/bin/gatus"]
