-- mng-pg metrics role for mng-pg-exporter (SPEC-0224).
--
-- A marked LOGIN role with only the statistics, settings and WAL-directory
-- reads the exporter's collectors need; no pg_monitor, no CONNECT grant, no
-- table privilege. Every session is read-only and bounded. Each run sets the
-- password from the secret, so a rotation is: rewrite the secret, rerun this
-- job, recreate the exporter. Run only through run-feature-provision.sh.
\set ON_ERROR_STOP on
\getenv monitor_secret MNG_PG_MONITOR_PASSWORD
\if :{?monitor_secret} \else \echo 'monitor provisioning: MNG_PG_MONITOR_PASSWORD is not set' \\ SELECT 'missing monitor secret'::int; \endif

-- Keep the password-bearing statements out of the server log even if they fail.
SET log_statement = 'none';
SET log_min_error_statement = panic;

-- postgres_exporter builds a key/value DSN from the password and logs it when
-- the DSN is malformed, so only a base64 alphabet is accepted.
SELECT :'monitor_secret' ~ '^[A-Za-z0-9+/=_-]{16,}$'
       AND length(:'monitor_secret') <= 512 AS secret_ok \gset
\if :secret_ok \else \echo 'monitor provisioning: the monitor secret must be 16-512 base64 characters' \\ SELECT 'invalid monitor secret'::int; \endif

SELECT pg_advisory_lock(hashtext('mng-pg:monitor'));

SELECT NOT EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'mng_pg_monitor'
       ) AS create_role
\gset
\if :create_role
BEGIN;
CREATE ROLE mng_pg_monitor NOLOGIN;
COMMENT ON ROLE mng_pg_monitor IS 'mng-pg:management:monitor';
COMMIT;
\endif

-- Only the role this job created carries the marker; another login is never
-- altered.
SELECT EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles r
         WHERE r.rolname = 'mng_pg_monitor'
           AND NOT (r.rolsuper OR r.rolcreatedb OR r.rolcreaterole
                    OR r.rolreplication OR r.rolbypassrls)
           AND pg_catalog.shobj_description(r.oid, 'pg_authid') = 'mng-pg:management:monitor'
       ) AS role_ok
\gset
\if :role_ok \else \echo 'monitor provisioning: mng_pg_monitor exists without this job''s marker' \\ SELECT 'role ownership mismatch'::int; \endif

SELECT format(
  'ALTER ROLE mng_pg_monitor WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS CONNECTION LIMIT 3 PASSWORD %L',
  :'monitor_secret'
)
\gexec
\unset monitor_secret
ALTER ROLE mng_pg_monitor SET statement_timeout = '10s';
ALTER ROLE mng_pg_monitor SET default_transaction_read_only = on;
GRANT pg_read_all_stats, pg_read_all_settings TO mng_pg_monitor;
GRANT EXECUTE ON FUNCTION pg_catalog.pg_ls_waldir() TO mng_pg_monitor;
SELECT 'REVOKE pg_monitor FROM mng_pg_monitor'
WHERE pg_catalog.pg_has_role('mng_pg_monitor', 'pg_monitor', 'MEMBER')
\gexec

-- Fail when another membership was added by hand, or pg_monitor is still
-- held through another role, instead of reporting a least-privilege role.
DO $verify$ BEGIN
  IF pg_has_role('mng_pg_monitor', 'pg_monitor', 'MEMBER') OR EXISTS (
       SELECT 1 FROM pg_auth_members m JOIN pg_roles g ON g.oid = m.roleid
       WHERE m.member = 'mng_pg_monitor'::regrole
         AND g.rolname NOT IN ('pg_read_all_stats', 'pg_read_all_settings')) THEN
    RAISE EXCEPTION 'monitor role holds memberships beyond its grants';
  END IF;
END $verify$;
