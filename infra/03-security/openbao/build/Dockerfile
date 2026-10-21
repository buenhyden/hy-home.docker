# Consumed by build-owned-image.py inside its bounded public runtime container.
FROM docker.io/library/alpine@sha256:d56c381f961d307a21b3ca004cf1e3910f106644aefb1f43e654c8a56c4fd395
COPY --chmod=555 bao /usr/bin/bao
COPY --chmod=755 docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY --chmod=644 LICENSE /licenses/mozilla.txt
RUN --mount=type=bind,source=apks,target=/public/apks,readonly apk --no-logfile --keys-dir /public/keys verify /public/apks/*.apk && apk --no-logfile --keys-dir /public/keys add --no-cache --no-network /public/apks/*.apk && addgroup -g 1000 openbao && adduser -S -u 100 -G openbao openbao && awk -F: -v OFS=: -v epoch="$SOURCE_DATE_EPOCH" 'BEGIN {if(epoch !~ /^[0-9]+$/) exit 1; day=int(epoch/86400)} $1=="openbao" {if(NF!=9 || $2 !~ /^[!*]/) exit 1; $3=day; count++} {print} END {if(count!=1) exit 1}' /etc/shadow > /etc/shadow.hyhome && cat /etc/shadow.hyhome > /etc/shadow && rm /etc/shadow.hyhome && ln -s /usr/bin/bao /usr/bin/vault && mkdir -p /openbao/logs /openbao/file /openbao/config && chown -R 100:1000 /openbao
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
EXPOSE 8200
USER openbao
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["server", "-dev", "-dev-no-store-token"]
LABEL org.opencontainers.image.source="https://github.com/openbao/openbao"
LABEL org.opencontainers.image.revision="a5db72cef75c24b920ade02065b18dd8eb666bac"
LABEL org.opencontainers.image.version="2.7.1+hyhome.go1.27.3.net0.60.0.r1"
LABEL com.hyhome.openbao.upstream_signed="false"
