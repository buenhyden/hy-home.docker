-- Superset metadata database provisioning on mng-pg (feature-owned).
--
-- Run only through run-feature-provision.sh, which validates every input
-- before this file executes. Inputs arrive through the psql process
-- environment, never the command line. ON_ERROR_STOP stops at the first error
-- but does not roll back statements that already committed; every statement
-- is idempotent, so a corrected re-run is the recovery path.
\set ON_ERROR_STOP on
\getenv superset_db_user SUPERSET_DB_USER
\getenv superset_db_name SUPERSET_DB_NAME
\getenv superset_db_password SUPERSET_DB_PASSWORD

\if :{?superset_db_user}
\else
  \echo 'superset provisioning: SUPERSET_DB_USER is not set'
  SELECT 'missing SUPERSET_DB_USER'::int;
\endif
\if :{?superset_db_name}
\else
  \echo 'superset provisioning: SUPERSET_DB_NAME is not set'
  SELECT 'missing SUPERSET_DB_NAME'::int;
\endif
\if :{?superset_db_password}
\else
  \echo 'superset provisioning: SUPERSET_DB_PASSWORD is not set'
  SELECT 'missing SUPERSET_DB_PASSWORD'::int;
\endif

-- Keep the password-bearing statements out of the server log even if they fail.
SET log_statement = 'none';
SET log_min_error_statement = panic;

-- Serialize concurrent runs of this job for the duration of this session.
SELECT pg_advisory_lock(hashtext('hy-home:provision:superset'));

-- Refuse to alter an administrator or another service's role, or to take over
-- a database owned by another role; each needs a separately approved migration.
-- Only roles this job created carry the ownership marker; an existing role
-- without it (another service's login) is never altered.
SELECT NOT EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles r
         WHERE r.rolname = :'superset_db_user'
           AND (r.rolsuper OR r.rolname = current_user
                OR pg_catalog.shobj_description(r.oid, 'pg_authid')
                   IS DISTINCT FROM 'hy-home:feature:superset')
       ) AS role_ok,
       COALESCE((
         SELECT pg_catalog.pg_get_userbyid(datdba) = :'superset_db_user'
         FROM pg_catalog.pg_database WHERE datname = :'superset_db_name'
       ), true) AS db_owner_ok
\gset
\if :role_ok
\else
  \echo 'superset provisioning: SUPERSET_DB_USER names an administrator or a role this job did not create'
  SELECT 'refusing administrator role'::int;
\endif
\if :db_owner_ok
\else
  \echo 'superset provisioning: SUPERSET_DB_NAME exists with a different owner'
  SELECT 'refusing foreign database owner'::int;
\endif

BEGIN;
SELECT format('CREATE ROLE %I', :'superset_db_user')
WHERE NOT EXISTS (
  SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :'superset_db_user'
)
\gexec
SELECT format('COMMENT ON ROLE %I IS %L', :'superset_db_user', 'hy-home:feature:superset')
\gexec
COMMIT;

-- Only this feature's role is synchronized with its secret; other roles are
-- not touched by this job.
SELECT format(
  'ALTER ROLE %I WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD %L',
  :'superset_db_user',
  :'superset_db_password'
)
\gexec

SELECT format('CREATE DATABASE %I OWNER %I', :'superset_db_name', :'superset_db_user')
WHERE NOT EXISTS (
  SELECT 1 FROM pg_catalog.pg_database WHERE datname = :'superset_db_name'
)
\gexec

-- The owner reaches the public schema through pg_database_owner (PostgreSQL
-- 15+); other login roles lose the default PUBLIC connect privilege.
SELECT format('REVOKE CONNECT, TEMPORARY ON DATABASE %I FROM PUBLIC', :'superset_db_name')
\gexec
