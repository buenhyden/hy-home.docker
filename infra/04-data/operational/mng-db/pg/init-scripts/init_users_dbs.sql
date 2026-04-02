\set ON_ERROR_STOP on
-- PostgreSQL 초기화 스크립트
-- psql -v 로 전달된 변수를 사용한다.

---------------------------------------------------------
-- 1. n8n 설정
---------------------------------------------------------
SELECT 'CREATE ROLE n8n LOGIN PASSWORD ' || quote_literal(:'n8n_db_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'n8n')
\gexec

ALTER ROLE n8n WITH LOGIN PASSWORD :'n8n_db_password';

SELECT 'CREATE DATABASE n8n OWNER n8n'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'n8n')
\gexec

GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n;

\connect n8n
GRANT ALL ON SCHEMA public TO n8n;
ALTER SCHEMA public OWNER TO n8n;

---------------------------------------------------------
-- 2. keycloak 설정
---------------------------------------------------------
\connect postgres

SELECT 'CREATE ROLE keycloak LOGIN PASSWORD ' || quote_literal(:'keycloak_db_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'keycloak')
\gexec

ALTER ROLE keycloak WITH LOGIN PASSWORD :'keycloak_db_password';

SELECT 'CREATE DATABASE keycloak OWNER keycloak'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'keycloak')
\gexec

GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;

\connect keycloak
GRANT ALL ON SCHEMA public TO keycloak;
ALTER SCHEMA public OWNER TO keycloak;

---------------------------------------------------------
-- 3. airflow 설정
---------------------------------------------------------
\connect postgres

SELECT 'CREATE ROLE airflow LOGIN PASSWORD ' || quote_literal(:'airflow_db_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'airflow')
\gexec

ALTER ROLE airflow WITH LOGIN PASSWORD :'airflow_db_password';

SELECT 'CREATE DATABASE airflow OWNER airflow'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'airflow')
\gexec

GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;

\connect airflow
GRANT ALL ON SCHEMA public TO airflow;
ALTER SCHEMA public OWNER TO airflow;

---------------------------------------------------------
-- 4. terrakube 설정
---------------------------------------------------------
\connect postgres

SELECT 'CREATE ROLE terrakube LOGIN PASSWORD ' || quote_literal(:'terrakube_db_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'terrakube')
\gexec

ALTER ROLE terrakube WITH LOGIN PASSWORD :'terrakube_db_password';

SELECT 'CREATE DATABASE terrakube OWNER terrakube'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'terrakube')
\gexec

GRANT ALL PRIVILEGES ON DATABASE terrakube TO terrakube;

\connect terrakube
GRANT ALL ON SCHEMA public TO terrakube;
ALTER SCHEMA public OWNER TO terrakube;

---------------------------------------------------------
-- 5. sonarqube 설정
---------------------------------------------------------
\connect postgres

SELECT 'CREATE ROLE sonarqube LOGIN PASSWORD ' || quote_literal(:'sonarqube_db_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'sonarqube')
\gexec

ALTER ROLE sonarqube WITH LOGIN PASSWORD :'sonarqube_db_password';

SELECT 'CREATE DATABASE sonarqube OWNER sonarqube'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'sonarqube')
\gexec

GRANT ALL PRIVILEGES ON DATABASE sonarqube TO sonarqube;

\connect sonarqube
GRANT ALL ON SCHEMA public TO sonarqube;
ALTER SCHEMA public OWNER TO sonarqube;

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
