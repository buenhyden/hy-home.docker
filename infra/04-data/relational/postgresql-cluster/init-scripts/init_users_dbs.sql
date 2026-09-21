\set ON_ERROR_STOP on

-- Required psql variables:
--   patroni_exporter_username
--   patroni_exporter_password
--   service_postgres_username
--   service_postgres_password
--   service_postgres_db

-----------------------------------------------------------------------
-- 1. exporter role 생성 / 비밀번호 동기화
-----------------------------------------------------------------------
SELECT format(
  'CREATE ROLE %I WITH LOGIN PASSWORD %L',
  :'patroni_exporter_username',
  :'patroni_exporter_password'
)
WHERE NOT EXISTS (
  SELECT 1
  FROM pg_catalog.pg_roles
  WHERE rolname = :'patroni_exporter_username'
)
\gexec

SELECT format(
  'ALTER ROLE %I WITH LOGIN PASSWORD %L',
  :'patroni_exporter_username',
  :'patroni_exporter_password'
)
\gexec

SELECT format(
  'GRANT pg_monitor TO %I',
  :'patroni_exporter_username'
)
\gexec

SELECT format(
  'GRANT CONNECT ON DATABASE postgres TO %I',
  :'patroni_exporter_username'
)
\gexec

-----------------------------------------------------------------------
-- 2. app/service role 생성 / 비밀번호 동기화
-----------------------------------------------------------------------
SELECT format(
  'CREATE ROLE %I WITH LOGIN PASSWORD %L',
  :'service_postgres_username',
  :'service_postgres_password'
)
WHERE NOT EXISTS (
  SELECT 1
  FROM pg_catalog.pg_roles
  WHERE rolname = :'service_postgres_username'
)
\gexec

SELECT format(
  'ALTER ROLE %I WITH LOGIN PASSWORD %L',
  :'service_postgres_username',
  :'service_postgres_password'
)
\gexec

-----------------------------------------------------------------------
-- 3. app/service database 생성
-----------------------------------------------------------------------
SELECT format(
  'CREATE DATABASE %I OWNER %I',
  :'service_postgres_db',
  :'service_postgres_username'
)
WHERE NOT EXISTS (
  SELECT 1
  FROM pg_database
  WHERE datname = :'service_postgres_db'
)
\gexec

SELECT format(
  'ALTER DATABASE %I OWNER TO %I',
  :'service_postgres_db',
  :'service_postgres_username'
)
\gexec

SELECT format(
  'GRANT ALL PRIVILEGES ON DATABASE %I TO %I',
  :'service_postgres_db',
  :'service_postgres_username'
)
\gexec

-----------------------------------------------------------------------
-- 4. app/service database 내부 schema 권한 정리
-----------------------------------------------------------------------
-- gexec sends SQL to the server; connect must be executed by psql itself.
-- Quote a libpq dbname value, including literal quotes/backslashes, so names
-- containing '=' or URI prefixes cannot override the existing connection.
SELECT 'dbname=''' || replace(
  replace(:'service_postgres_db', chr(92), chr(92) || chr(92)),
  '''', chr(92) || ''''
) || '''' AS service_postgres_conninfo
\gset
\connect -reuse-previous=on :service_postgres_conninfo

SELECT format(
  'ALTER SCHEMA public OWNER TO %I',
  :'service_postgres_username'
)
\gexec

SELECT format(
  'GRANT ALL ON SCHEMA public TO %I',
  :'service_postgres_username'
)
\gexec

-----------------------------------------------------------------------
-- 5. MLFLOW
-----------------------------------------------------------------------
\connect postgres

SELECT
  'CREATE ROLE mlflow LOGIN PASSWORD '
  || quote_literal(:'mlflow_db_password')
WHERE NOT EXISTS (
  SELECT 1
  FROM pg_catalog.pg_roles
  WHERE rolname = 'mlflow'
)
\gexec

SELECT format(
  'ALTER ROLE mlflow WITH LOGIN PASSWORD %L',
  :'mlflow_db_password'
)
\gexec

SELECT 'CREATE DATABASE mlflow OWNER mlflow'
WHERE NOT EXISTS (
  SELECT 1
  FROM pg_database
  WHERE datname = 'mlflow'
)
\gexec

\connect mlflow

ALTER SCHEMA public OWNER TO mlflow;
GRANT ALL ON SCHEMA public TO mlflow;

-----------------------------------------------------------------------
-- 6. dbt
-----------------------------------------------------------------------
\connect postgres

SELECT
  'CREATE ROLE dbt LOGIN PASSWORD '
  || quote_literal(:'dbt_db_password')
WHERE NOT EXISTS (
  SELECT 1
  FROM pg_catalog.pg_roles
  WHERE rolname = 'dbt'
)
\gexec

SELECT format(
  'ALTER ROLE dbt WITH LOGIN PASSWORD %L',
  :'dbt_db_password'
)
\gexec

\connect app_db

GRANT CONNECT ON DATABASE app_db TO dbt;

GRANT USAGE
ON SCHEMA public
TO dbt;

GRANT SELECT
ON ALL TABLES IN SCHEMA public
TO dbt;

CREATE SCHEMA IF NOT EXISTS analytics
AUTHORIZATION dbt;

-----------------------------------------------------------------------
-- 7. debezium
-----------------------------------------------------------------------
SELECT
  'CREATE PUBLICATION hyhome_app_publication FOR TABLES IN SCHEMA public'
WHERE NOT EXISTS (
  SELECT 1
  FROM pg_publication
  WHERE pubname = 'hyhome_app_publication'
)
\gexec