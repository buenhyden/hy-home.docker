#!/bin/sh
set -eu

# 시크릿 읽기
REDIS_PASSWORD=$(cat /run/secrets/redis_password)
NODE_NAME="${NODE_NAME:-$(hostname)}"

# [중요] 외부에서 주입받은 포트로 실행 (기본값 6379)
PORT="${PORT:-6379}"

echo "🚀 Starting $NODE_NAME on Port $PORT..."

# [핵심 설정]
# 1. --port: 내부 리스닝 포트를 변경
# 2. --cluster-announce-ip: IP 대신 '호스트명(redis-node-0)'을 알림
#    -> Docker 안에서는 내부 IP로 해석됨 (OK)
#    -> Windows 밖에서는 127.0.0.1로 해석됨 (Hosts 파일 덕분, OK)

exec redis-server /usr/local/etc/redis/redis.conf \
  --port "$PORT" \
  --requirepass "$REDIS_PASSWORD" \
  --masterauth "$REDIS_PASSWORD" \
  --cluster-announce-ip "$NODE_NAME" \
  --cluster-announce-port "$PORT" \
  --cluster-announce-bus-port $(($PORT + 10000)) \
  --appendonly yes
