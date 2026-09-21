-- Debezium CDC source provisioning on mng-pg (feature-owned).
--
-- Creates a dedicated replication login that can snapshot and stream only the
-- published schema plus its own heartbeat table, and the publication the connector consumes with
-- publication.autocreate.mode=disabled. It never grants superuser, database
-- ownership or write access outside the heartbeat schema it owns. The replication slot is created by the connector
-- on first start; this job never creates or drops slots.
-- Run only through run-feature-provision.sh. ON_ERROR_STOP does not roll back
-- earlier statements; every statement is idempotent and re-runnable.
\set ON_ERROR_STOP on
\getenv debezium_db_user DEBEZIUM_DB_USER
\getenv debezium_db_name DEBEZIUM_DB_NAME
\getenv debezium_schema DEBEZIUM_SCHEMA
\getenv debezium_publication DEBEZIUM_PUBLICATION
\getenv debezium_heartbeat_schema DEBEZIUM_HEARTBEAT_SCHEMA
\getenv debezium_source_owner DEBEZIUM_SOURCE_OWNER
\getenv debezium_db_password DEBEZIUM_DB_PASSWORD

\if :{?debezium_db_user} \else \echo 'debezium provisioning: DEBEZIUM_DB_USER is not set' \\ SELECT 'missing DEBEZIUM_DB_USER'::int; \endif
\if :{?debezium_db_name} \else \echo 'debezium provisioning: DEBEZIUM_DB_NAME is not set' \\ SELECT 'missing DEBEZIUM_DB_NAME'::int; \endif
\if :{?debezium_schema} \else \echo 'debezium provisioning: DEBEZIUM_SCHEMA is not set' \\ SELECT 'missing DEBEZIUM_SCHEMA'::int; \endif
\if :{?debezium_heartbeat_schema} \else \echo 'debezium provisioning: DEBEZIUM_HEARTBEAT_SCHEMA is not set' \\ SELECT 'missing DEBEZIUM_HEARTBEAT_SCHEMA'::int; \endif
\if :{?debezium_publication} \else \echo 'debezium provisioning: DEBEZIUM_PUBLICATION is not set' \\ SELECT 'missing DEBEZIUM_PUBLICATION'::int; \endif
\if :{?debezium_source_owner} \else \echo 'debezium provisioning: DEBEZIUM_SOURCE_OWNER is not set' \\ SELECT 'missing DEBEZIUM_SOURCE_OWNER'::int; \endif
\if :{?debezium_db_password} \else \echo 'debezium provisioning: DEBEZIUM_DB_PASSWORD is not set' \\ SELECT 'missing DEBEZIUM_DB_PASSWORD'::int; \endif

-- Keep the password-bearing statements out of the server log even if they fail.
SET log_statement = 'none';
SET log_min_error_statement = panic;

SELECT pg_advisory_lock(hashtext('hy-home:provision:debezium'));

-- Only roles this job created carry the ownership marker; an existing role
-- without it (another service's login) is never altered.
SELECT NOT EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles r
         WHERE r.rolname = :'debezium_db_user'
           AND (r.rolsuper OR r.rolname = current_user
                OR pg_catalog.shobj_description(r.oid, 'pg_authid')
                   IS DISTINCT FROM 'hy-home:feature:debezium')
       ) AS role_ok,
       EXISTS (
         SELECT 1 FROM pg_catalog.pg_database WHERE datname = :'debezium_db_name'
       ) AS db_exists,
       EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :'debezium_source_owner'
       ) AS source_owner_exists,
       current_setting('wal_level') = 'logical' AS wal_logical
\gset
\if :role_ok \else \echo 'debezium provisioning: DEBEZIUM_DB_USER names an administrator or a role this job did not create' \\ SELECT 'refusing administrator role'::int; \endif
\if :db_exists \else \echo 'debezium provisioning: DEBEZIUM_DB_NAME does not exist; run the base mng-pg-init job first' \\ SELECT 'missing source database'::int; \endif
\if :source_owner_exists \else \echo 'debezium provisioning: DEBEZIUM_SOURCE_OWNER role does not exist' \\ SELECT 'missing source owner'::int; \endif
\if :wal_logical
\else
  -- Grants remain valid, but streaming needs mng-pg restarted with the
  -- declared wal_level=logical; report instead of silently succeeding.
  \echo 'debezium provisioning: WARNING wal_level is not logical; restart of mng-pg with the declared command is required before the connector can stream'
\endif

BEGIN;
SELECT format('CREATE ROLE %I', :'debezium_db_user')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :'debezium_db_user')
\gexec
SELECT format('COMMENT ON ROLE %I IS %L', :'debezium_db_user', 'hy-home:feature:debezium')
\gexec
COMMIT;

SELECT format(
  'ALTER ROLE %I WITH LOGIN REPLICATION NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS PASSWORD %L',
  :'debezium_db_user',
  :'debezium_db_password'
)
\gexec

SELECT format('GRANT CONNECT ON DATABASE %I TO %I', :'debezium_db_name', :'debezium_db_user')
\gexec

\connect -reuse-previous=on dbname=:debezium_db_name
SELECT pg_advisory_lock(hashtext('hy-home:provision:debezium'));

SELECT EXISTS (
         SELECT 1 FROM pg_catalog.pg_namespace WHERE nspname = :'debezium_schema'
       ) AS schema_exists,
       COALESCE((
         SELECT pg_catalog.pg_get_userbyid(nspowner) = :'debezium_db_user'
         FROM pg_catalog.pg_namespace WHERE nspname = :'debezium_heartbeat_schema'
       ), true) AS heartbeat_owner_ok,
       :'debezium_heartbeat_schema' <> :'debezium_schema' AS schemas_distinct,
       NOT EXISTS (
         SELECT 1 FROM pg_catalog.pg_publication p
         WHERE p.pubname = :'debezium_publication'
           AND (SELECT count(*) FROM pg_catalog.pg_publication_namespace pn
                JOIN pg_catalog.pg_namespace n ON n.oid = pn.pnnspid
                WHERE pn.pnpubid = p.oid
                  AND n.nspname IN (:'debezium_schema', :'debezium_heartbeat_schema')) <> 2
       ) AS publication_scope_ok
\gset
\if :schema_exists \else \echo 'debezium provisioning: DEBEZIUM_SCHEMA does not exist' \\ SELECT 'missing source schema'::int; \endif
\if :heartbeat_owner_ok \else \echo 'debezium provisioning: DEBEZIUM_HEARTBEAT_SCHEMA exists with a different owner' \\ SELECT 'refusing foreign heartbeat schema'::int; \endif
\if :schemas_distinct \else \echo 'debezium provisioning: DEBEZIUM_HEARTBEAT_SCHEMA must differ from DEBEZIUM_SCHEMA' \\ SELECT 'heartbeat equals source'::int; \endif
\if :publication_scope_ok \else \echo 'debezium provisioning: DEBEZIUM_PUBLICATION exists without exactly the source and heartbeat schemas; review it manually' \\ SELECT 'publication scope mismatch'::int; \endif

BEGIN;

SELECT format('GRANT USAGE ON SCHEMA %I TO %I', :'debezium_schema', :'debezium_db_user')
\gexec
-- Initial and incremental snapshots read the captured tables.
SELECT format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO %I', :'debezium_schema', :'debezium_db_user')
\gexec
SELECT format(
  'ALTER DEFAULT PRIVILEGES FOR ROLE %I IN SCHEMA %I GRANT SELECT ON TABLES TO %I',
  :'debezium_source_owner',
  :'debezium_schema',
  :'debezium_db_user'
)
\gexec
-- Heartbeat: mng-pg hosts several databases, so WAL from other databases can
-- grow while this one is quiet. The connector's heartbeat.action.query writes
-- one row here; the change travels through the slot and lets the connector
-- confirm a newer LSN. This is the only table the role can write.
SELECT format('CREATE SCHEMA IF NOT EXISTS %I AUTHORIZATION %I', :'debezium_heartbeat_schema', :'debezium_db_user')
\gexec
SELECT format(
  'CREATE TABLE IF NOT EXISTS %I.heartbeat (id integer PRIMARY KEY, beat_at timestamptz NOT NULL)',
  :'debezium_heartbeat_schema'
)
\gexec
SELECT format('ALTER TABLE %I.heartbeat OWNER TO %I', :'debezium_heartbeat_schema', :'debezium_db_user')
\gexec
-- A schema-scoped publication (PostgreSQL 15+) also covers tables created
-- later; it matches the connector's schema.include.list.
SELECT format(
  'CREATE PUBLICATION %I FOR TABLES IN SCHEMA %I, %I',
  :'debezium_publication', :'debezium_schema', :'debezium_heartbeat_schema'
)
WHERE NOT EXISTS (
  SELECT 1 FROM pg_catalog.pg_publication WHERE pubname = :'debezium_publication'
)
\gexec

COMMIT;
