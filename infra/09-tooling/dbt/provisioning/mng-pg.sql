-- dbt transformation role provisioning on mng-pg (feature-owned).
--
-- dbt reads the application source schema and writes only its own target
-- schema in the application database created by the base mng-pg-init job.
-- Run only through run-feature-provision.sh. ON_ERROR_STOP does not roll back
-- earlier statements; every statement is idempotent and re-runnable.
\set ON_ERROR_STOP on
\getenv dbt_db_user DBT_DB_USER
\getenv dbt_db_name DBT_DB_NAME
\getenv dbt_schema DBT_SCHEMA
\getenv dbt_source_schema DBT_SOURCE_SCHEMA
\getenv dbt_source_owner DBT_SOURCE_OWNER
\getenv dbt_db_password DBT_DB_PASSWORD

\if :{?dbt_db_user} \else \echo 'dbt provisioning: DBT_DB_USER is not set' \\ SELECT 'missing DBT_DB_USER'::int; \endif
\if :{?dbt_db_name} \else \echo 'dbt provisioning: DBT_DB_NAME is not set' \\ SELECT 'missing DBT_DB_NAME'::int; \endif
\if :{?dbt_schema} \else \echo 'dbt provisioning: DBT_SCHEMA is not set' \\ SELECT 'missing DBT_SCHEMA'::int; \endif
\if :{?dbt_source_schema} \else \echo 'dbt provisioning: DBT_SOURCE_SCHEMA is not set' \\ SELECT 'missing DBT_SOURCE_SCHEMA'::int; \endif
\if :{?dbt_source_owner} \else \echo 'dbt provisioning: DBT_SOURCE_OWNER is not set' \\ SELECT 'missing DBT_SOURCE_OWNER'::int; \endif
\if :{?dbt_db_password} \else \echo 'dbt provisioning: DBT_DB_PASSWORD is not set' \\ SELECT 'missing DBT_DB_PASSWORD'::int; \endif

-- Keep the password-bearing statements out of the server log even if they fail.
SET log_statement = 'none';
SET log_min_error_statement = panic;

SELECT pg_advisory_lock(hashtext('hy-home:provision:dbt'));

-- Only roles this job created carry the ownership marker; an existing role
-- without it (another service's login) is never altered.
SELECT NOT EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles r
         WHERE r.rolname = :'dbt_db_user'
           AND (r.rolsuper OR r.rolname = current_user
                OR pg_catalog.shobj_description(r.oid, 'pg_authid')
                   IS DISTINCT FROM 'hy-home:feature:dbt')
       ) AS role_ok,
       EXISTS (
         SELECT 1 FROM pg_catalog.pg_database WHERE datname = :'dbt_db_name'
       ) AS db_exists,
       EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :'dbt_source_owner'
       ) AS source_owner_exists,
       :'dbt_schema' <> :'dbt_source_schema' AS schemas_distinct
\gset
\if :role_ok \else \echo 'dbt provisioning: DBT_DB_USER names an administrator or a role this job did not create' \\ SELECT 'refusing administrator role'::int; \endif
\if :db_exists \else \echo 'dbt provisioning: DBT_DB_NAME does not exist; run the base mng-pg-init job first' \\ SELECT 'missing target database'::int; \endif
\if :source_owner_exists \else \echo 'dbt provisioning: DBT_SOURCE_OWNER role does not exist' \\ SELECT 'missing source owner'::int; \endif
\if :schemas_distinct \else \echo 'dbt provisioning: DBT_SCHEMA must differ from DBT_SOURCE_SCHEMA' \\ SELECT 'target equals source'::int; \endif

BEGIN;
SELECT format('CREATE ROLE %I', :'dbt_db_user')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :'dbt_db_user')
\gexec
SELECT format('COMMENT ON ROLE %I IS %L', :'dbt_db_user', 'hy-home:feature:dbt')
\gexec
COMMIT;

SELECT format(
  'ALTER ROLE %I WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD %L',
  :'dbt_db_user',
  :'dbt_db_password'
)
\gexec

SELECT format('GRANT CONNECT ON DATABASE %I TO %I', :'dbt_db_name', :'dbt_db_user')
\gexec

\connect -reuse-previous=on dbname=:dbt_db_name
SELECT pg_advisory_lock(hashtext('hy-home:provision:dbt'));

SELECT COALESCE((
         SELECT pg_catalog.pg_get_userbyid(nspowner) = :'dbt_db_user'
         FROM pg_catalog.pg_namespace WHERE nspname = :'dbt_schema'
       ), true) AS target_owner_ok,
       EXISTS (
         SELECT 1 FROM pg_catalog.pg_namespace WHERE nspname = :'dbt_source_schema'
       ) AS source_exists
\gset
\if :target_owner_ok \else \echo 'dbt provisioning: DBT_SCHEMA exists with a different owner' \\ SELECT 'refusing foreign schema owner'::int; \endif
\if :source_exists \else \echo 'dbt provisioning: DBT_SOURCE_SCHEMA does not exist' \\ SELECT 'missing source schema'::int; \endif

BEGIN;

SELECT format('GRANT USAGE ON SCHEMA %I TO %I', :'dbt_source_schema', :'dbt_db_user')
\gexec
SELECT format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO %I', :'dbt_source_schema', :'dbt_db_user')
\gexec
-- Tables the application owner creates later become readable without re-running.
SELECT format(
  'ALTER DEFAULT PRIVILEGES FOR ROLE %I IN SCHEMA %I GRANT SELECT ON TABLES TO %I',
  :'dbt_source_owner',
  :'dbt_source_schema',
  :'dbt_db_user'
)
\gexec
SELECT format('CREATE SCHEMA IF NOT EXISTS %I AUTHORIZATION %I', :'dbt_schema', :'dbt_db_user')
\gexec

COMMIT;
