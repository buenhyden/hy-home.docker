# Community (TSL + Apache components), PostgreSQL 18.6, Alpine 3.23.6,
# linux/amd64 manifest observed 2026-10-02. Build/load/restore are NOT_RUN.
FROM timescale/timescaledb:2.30.2-pg18@sha256:cdf97a4b5be91038b5c1be0ad304c5d5746132992e54f7dd26ec467a6d005755

# Alpine v3.23 community package; build must prove package and PG18 ABI.
RUN apk add --no-cache pgbackrest=2.57.0-r0 python3 \
    && install -d -o postgres -g postgres -m 0750 /var/lib/pgbackrest /var/spool/pgbackrest

COPY --chmod=0644 backup/pgbackrest.conf /etc/pgbackrest/pgbackrest.conf
COPY --chmod=0755 backup/entrypoint.sh /usr/local/bin/hyhome-dev-pg-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/hyhome-dev-pg-entrypoint.sh"]
CMD ["postgres"]
