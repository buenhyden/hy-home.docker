-- 1. n8n
CREATE USER n8n WITH PASSWORD 'xMl63AmDBd5QQhPn';
CREATE DATABASE n8n OWNER n8n;
GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n;
\connect n8n
GRANT ALL ON SCHEMA public TO n8n;

-- 2. app_user
CREATE USER app_user WITH PASSWORD '1Osi6L5r4pZiWYl';
CREATE DATABASE app_db OWNER app_user;
GRANT ALL PRIVILEGES ON DATABASE app_db TO app_user;
\connect app_db
GRANT ALL ON SCHEMA public TO app_user;

-- 3. keycloak
CREATE USER keycloak WITH PASSWORD 'jwjaps9jWgcuj1Vp';
CREATE DATABASE keycloak OWNER keycloak;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
\connect keycloak
GRANT ALL ON SCHEMA public TO keycloak;
