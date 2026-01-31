#!/bin/bash
# post_init.sh

# Patroni가 전달하는 인자들을 활용하거나, 기본 psql 연결 사용
# Spilo 환경에서는 postgres 사용자로 실행됩니다.

echo "실행 중: post_init.sh - 초기 사용자 등록을 시작합니다."

# -f 플래그를 사용하여 마운트된 SQL 파일을 실행합니다.
# -v ON_ERROR_STOP=1 설정을 통해 에러 발생 시 즉시 중단하도록 합니다.
psql -v ON_ERROR_STOP=1 --username "$PATRONI_SUPERUSER_USERNAME" --dbname "postgres" -f /home/postgres/init-scripts/init_users_dbs.sql

echo "완료: post_init.sh - 초기 사용자 등록이 완료되었습니다."