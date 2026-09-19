FROM twinproduction/gatus:v5.36.0 AS gatus

FROM alpine:3.22

RUN apk add --no-cache \
    ca-certificates \
    wget

COPY --from=gatus /gatus /usr/local/bin/gatus

ENTRYPOINT ["/usr/local/bin/gatus"]