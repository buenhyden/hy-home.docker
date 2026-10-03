\set ON_ERROR_STOP on

DO $owner$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'perf_owner') THEN
    CREATE ROLE perf_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
      NOREPLICATION NOBYPASSRLS;
    COMMENT ON ROLE perf_owner IS 'dev-pg:development:perf_db:owner';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM pg_roles r
    WHERE r.rolname = 'perf_owner'
      AND NOT r.rolcanlogin
      AND NOT (r.rolsuper OR r.rolcreatedb OR r.rolcreaterole
        OR r.rolreplication OR r.rolbypassrls)
      AND NOT EXISTS (
        SELECT 1 FROM pg_auth_members m WHERE m.member = r.oid
      )
      AND shobj_description(r.oid, 'pg_authid') =
        'dev-pg:development:perf_db:owner'
  ) THEN
    RAISE EXCEPTION 'role ownership mismatch';
  END IF;
END $owner$;

DO $migrator$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'perf_migrator') THEN
    CREATE ROLE perf_migrator NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
      NOREPLICATION NOBYPASSRLS;
    COMMENT ON ROLE perf_migrator IS 'dev-pg:development:perf_db:migrator';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM pg_roles r
    WHERE r.rolname = 'perf_migrator'
      AND NOT r.rolcanlogin
      AND NOT (r.rolsuper OR r.rolcreatedb OR r.rolcreaterole
        OR r.rolreplication OR r.rolbypassrls)
      AND NOT EXISTS (
        SELECT 1
        FROM pg_auth_members m
        JOIN pg_roles parent ON parent.oid = m.roleid
        WHERE m.member = r.oid AND parent.rolname <> 'perf_owner'
      )
      AND shobj_description(r.oid, 'pg_authid') =
        'dev-pg:development:perf_db:migrator'
  ) THEN
    RAISE EXCEPTION 'role ownership mismatch';
  END IF;
END $migrator$;

GRANT perf_owner TO perf_migrator WITH INHERIT FALSE, SET TRUE;

SELECT CASE WHEN EXISTS (
  SELECT 1 FROM pg_database WHERE datname = 'perf_db'
) THEN 'false' ELSE 'true' END AS create_db \gset
\if :create_db
  CREATE DATABASE perf_db OWNER perf_owner TEMPLATE template0;
  COMMENT ON DATABASE perf_db IS 'dev-pg:development:perf_db';
\endif

DO $database$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_database d
    WHERE d.datname = 'perf_db'
      AND pg_get_userbyid(d.datdba) = 'perf_owner'
      AND shobj_description(d.oid, 'pg_database') =
        'dev-pg:development:perf_db'
  ) THEN
    RAISE EXCEPTION 'database ownership mismatch';
  END IF;
END $database$;

REVOKE ALL ON DATABASE perf_db FROM PUBLIC;
GRANT CONNECT ON DATABASE perf_db TO perf_migrator;

\connect perf_db
SET ROLE perf_owner;
\ir schema.sql
RESET ROLE;
