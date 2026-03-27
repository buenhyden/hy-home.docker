\set ON_ERROR_STOP on
-- PostgreSQL 초기화 스크립트
-- psql -v 로 전달된 변수를 사용한다.

---------------------------------------------------------
-- 1. app_user 설정
---------------------------------------------------------
SELECT 'CREATE ROLE app_user LOGIN PASSWORD ' || quote_literal(:'patroni_superuser_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'app_user')
\gexec

ALTER ROLE app_user WITH LOGIN PASSWORD :'patroni_superuser_password';

SELECT 'CREATE DATABASE app_db OWNER app_user'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'app_db')
\gexec

GRANT ALL PRIVILEGES ON DATABASE app_db TO app_user;

\connect app_db
GRANT ALL ON SCHEMA public TO app_user;
ALTER SCHEMA public OWNER TO app_user;
