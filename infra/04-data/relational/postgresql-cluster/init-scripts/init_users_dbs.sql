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
SELECT format('\\connect %I', :'service_postgres_db')
\gexec

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
