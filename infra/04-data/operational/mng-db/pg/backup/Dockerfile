# The management PostgreSQL server with pgBackRest installed in the same image,
# so archive_command runs the real binary, config and repository as the server's
# own postgres user (UID/GID 70). Keep the base identical to the plain image.
FROM postgres:18.6-alpine

# Alpine packages pgBackRest; the package release is pinned for reproducibility.
RUN apk add --no-cache pgbackrest=2.58.0-r0 \
    && install -d -o postgres -g postgres -m 0750 /var/lib/pgbackrest /var/spool/pgbackrest

COPY --chmod=0644 pgbackrest.conf /etc/pgbackrest/pgbackrest.conf
COPY --chmod=0755 entrypoint.sh /usr/local/bin/hyhome-pg-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/hyhome-pg-entrypoint.sh"]
CMD ["postgres"]
