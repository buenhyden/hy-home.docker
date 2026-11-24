# syntax=docker/dockerfile:1.7
# The management PostgreSQL server with pgBackRest installed in the same image,
# so archive_command runs the real binary, config and repository as the server's
# own postgres user (UID/GID 70). Keep the base identical to the plain image.
ARG PG_BASE=postgres:18.7-alpine@sha256:0115267ab5a509022df9319c77be365cef335adb71556c75f60f5360ee247e71

# Alpine 3.24 only packages pgBackRest 2.58, below the 2.59.3 fix for weak
# encryption subkeys, so 2.60.1 is built from its checksum-pinned release
# tarball on the same base.
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
RUN apk add --no-cache libpq lz4-libs zstd-libs libbz2 libxml2 yaml libssh2 \
    && install -d -o postgres -g postgres -m 0750 /var/lib/pgbackrest /var/spool/pgbackrest \
    && pgbackrest version

COPY --chmod=0644 pgbackrest.conf /etc/pgbackrest/pgbackrest.conf
COPY --chmod=0755 entrypoint.sh /usr/local/bin/hyhome-pg-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/hyhome-pg-entrypoint.sh"]
CMD ["postgres"]
