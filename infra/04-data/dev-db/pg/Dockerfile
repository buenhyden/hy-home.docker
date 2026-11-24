# Community (TSL + Apache components), PostgreSQL 18.7, Alpine 3.24.4,
# linux/amd64 manifest verified 2026-11-24 (18.7 fixes CVEs affecting 18.6).
# r2 (2026-10-08): retention, archive-push-queue-max and repository-root ownership.
FROM timescale/timescaledb:2.30.3-pg18@sha256:b98cd6bed74fb090de6158c9367ea31545390e7140a43fa6aad3334181fce4e2

# Alpine v3.24 community package; build must prove package and PG18 ABI.
RUN apk add --no-cache pgbackrest=2.58.0-r0 python3 \
    && install -d -o postgres -g postgres -m 0750 /var/lib/pgbackrest /var/spool/pgbackrest

COPY --chmod=0644 backup/pgbackrest.conf /etc/pgbackrest/pgbackrest.conf
COPY --chmod=0755 backup/entrypoint.sh /usr/local/bin/hyhome-dev-pg-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/hyhome-dev-pg-entrypoint.sh"]
CMD ["postgres"]
