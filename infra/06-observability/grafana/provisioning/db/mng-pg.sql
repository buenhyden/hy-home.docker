-- Grafana read-only reader on mng-pg (feature-owned, SPEC-0193).
--
-- Creates one login that can only SELECT the tables the provisioned SQL
-- dashboards query: n8n executions and workflows, and Airflow DAGs, DAG runs
-- and task instances. Every session is read-only, bounded in time and in
-- connections. It never grants superuser, ownership or write access.
-- Run only through run-feature-provision.sh. Every statement is idempotent.
\set ON_ERROR_STOP on
\getenv grafana_db_user GRAFANA_DB_READER_USER
\getenv n8n_db_name GRAFANA_N8N_DB_NAME
\getenv airflow_db_name GRAFANA_AIRFLOW_DB_NAME
\getenv grafana_db_password GRAFANA_DB_READER_PASSWORD

\if :{?grafana_db_user} \else \echo 'grafana provisioning: GRAFANA_DB_READER_USER is not set' \\ SELECT 'missing GRAFANA_DB_READER_USER'::int; \endif
\if :{?n8n_db_name} \else \echo 'grafana provisioning: GRAFANA_N8N_DB_NAME is not set' \\ SELECT 'missing GRAFANA_N8N_DB_NAME'::int; \endif
\if :{?airflow_db_name} \else \echo 'grafana provisioning: GRAFANA_AIRFLOW_DB_NAME is not set' \\ SELECT 'missing GRAFANA_AIRFLOW_DB_NAME'::int; \endif
\if :{?grafana_db_password} \else \echo 'grafana provisioning: GRAFANA_DB_READER_PASSWORD is not set' \\ SELECT 'missing GRAFANA_DB_READER_PASSWORD'::int; \endif

-- Keep the password-bearing statements out of the server log even if they fail.
SET log_statement = 'none';
SET log_min_error_statement = panic;

SELECT pg_advisory_lock(hashtext('hy-home:provision:grafana'));

-- Only a role this job created carries the ownership marker; another
-- service's login is never altered.
SELECT NOT EXISTS (
         SELECT 1 FROM pg_catalog.pg_roles r
         WHERE r.rolname = :'grafana_db_user'
           AND (r.rolsuper OR r.rolname = current_user
                OR pg_catalog.shobj_description(r.oid, 'pg_authid')
                   IS DISTINCT FROM 'hy-home:feature:grafana')
       ) AS role_ok,
       EXISTS (SELECT 1 FROM pg_catalog.pg_database WHERE datname = :'n8n_db_name') AS n8n_exists,
       EXISTS (SELECT 1 FROM pg_catalog.pg_database WHERE datname = :'airflow_db_name') AS airflow_exists
\gset
\if :role_ok \else \echo 'grafana provisioning: GRAFANA_DB_READER_USER names an administrator or a role this job did not create' \\ SELECT 'refusing administrator role'::int; \endif
\if :n8n_exists \else \echo 'grafana provisioning: the n8n database does not exist yet' \\ SELECT 'missing n8n database'::int; \endif
\if :airflow_exists \else \echo 'grafana provisioning: the airflow database does not exist yet' \\ SELECT 'missing airflow database'::int; \endif

BEGIN;
SELECT format('CREATE ROLE %I', :'grafana_db_user')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :'grafana_db_user')
\gexec
SELECT format('COMMENT ON ROLE %I IS %L', :'grafana_db_user', 'hy-home:feature:grafana')
\gexec
COMMIT;

SELECT format(
  'ALTER ROLE %I WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS CONNECTION LIMIT 4 PASSWORD %L',
  :'grafana_db_user',
  :'grafana_db_password'
)
\gexec
SELECT format('ALTER ROLE %I SET default_transaction_read_only = on', :'grafana_db_user')
\gexec
SELECT format('ALTER ROLE %I SET statement_timeout = %L', :'grafana_db_user', '30s')
\gexec
SELECT format('GRANT CONNECT ON DATABASE %I TO %I', :'n8n_db_name', :'grafana_db_user')
\gexec
SELECT format('GRANT CONNECT ON DATABASE %I TO %I', :'airflow_db_name', :'grafana_db_user')
\gexec

\connect -reuse-previous=on dbname=:n8n_db_name
SELECT format('GRANT USAGE ON SCHEMA public TO %I', :'grafana_db_user')
\gexec
SELECT format('GRANT SELECT ON public.%I TO %I', t, :'grafana_db_user')
FROM unnest(ARRAY['execution_entity', 'workflow_entity']) AS t
WHERE to_regclass('public.' || t) IS NOT NULL
\gexec

\connect -reuse-previous=on dbname=:airflow_db_name
SELECT format('GRANT USAGE ON SCHEMA public TO %I', :'grafana_db_user')
\gexec
SELECT format('GRANT SELECT ON public.%I TO %I', t, :'grafana_db_user')
FROM unnest(ARRAY['dag', 'dag_run', 'task_instance']) AS t
WHERE to_regclass('public.' || t) IS NOT NULL
\gexec
