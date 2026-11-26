# syntax=docker/dockerfile:1.7
# Community (TSL + Apache components), PostgreSQL 18.7, Alpine 3.24.4,
# linux/amd64 manifest verified 2026-11-24 (18.7 fixes CVEs affecting 18.6).
# r2 (2026-10-08): retention, archive-push-queue-max and repository-root ownership.
ARG PG_BASE=timescale/timescaledb:2.32.1-pg18@sha256:70e6526ad8e31e3f4833f2c5863b50b92d7a6bee4d432ad1f660e2c6dd956d94

# Alpine 3.24 only packages pgBackRest 2.58, below the 2.59.3 fix for weak
# encryption subkeys, so 2.60.1 is built from its checksum-pinned release
# tarball on the same base (as mng-pg does).
FROM ${PG_BASE} AS pgbackrest-build
RUN apk add --no-cache build-base meson ninja postgresql18-dev openssl-dev \
        lz4-dev zstd-dev bzip2-dev libxml2-dev yaml-dev libssh2-dev zlib-dev curl-dev py3-yaml
ADD --checksum=sha256:9a8aaf770e5e57c18426d5c2fa34e749db1ecb2d56979bf064550d5493a2df55 \
    https://github.com/pgbackrest/pgbackrest/archive/refs/tags/release/2.60.1.tar.gz /tmp/pgbackrest.tar.gz
RUN tar -xzf /tmp/pgbackrest.tar.gz -C /tmp \
    && meson setup /tmp/build /tmp/pgbackrest-release-2.60.1 --buildtype=release -Dlibsystemd=disabled \
    && ninja -C /tmp/build \
    && strip /tmp/build/src/pgbackrest

FROM ${PG_BASE}
COPY --from=pgbackrest-build /tmp/build/src/pgbackrest /usr/bin/pgbackrest
RUN apk add --no-cache libpq lz4-libs zstd-libs libbz2 libxml2 yaml libssh2 python3 \
    && install -d -o postgres -g postgres -m 0750 /var/lib/pgbackrest /var/spool/pgbackrest \
    && install -d -m 0755 /etc/pgbackrest \
    && pgbackrest version

COPY --chmod=0644 backup/pgbackrest.conf /etc/pgbackrest/pgbackrest.conf
COPY --chmod=0755 backup/entrypoint.sh /usr/local/bin/hyhome-dev-pg-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/hyhome-dev-pg-entrypoint.sh"]
CMD ["postgres"]
